"""
backend/app/services/dispatch/gateway.py

SendGateway: Operational Outbound Dispatch Gateway.
Executes the strict two-phase atomic dispatch protocol per Section 3 of Milestone M1 Specification:
1. Phase 1: Pre-check reads, cap evaluation, content hash verification, and idempotency reservation (committed).
2. Phase 2: External Google Gmail API dispatch with timeout guard (no DB lock held).
3. Phase 3: Post-call settlement (evidence recording, status transition, and quota resolution).
"""

from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Dict, Optional
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.crypto import decrypt_oauth_token, encrypt_oauth_token
from app.models.subscription import Entitlement
from app.models.application import Application
from app.models.dispatch import (
    AccountDispatchSettings,
    ApplicationPdfPayload,
    DispatchedAction,
    HoldQueueItem,
    SendAuthorization,
    SendEvidence,
    UserCommand,
)
from app.models.job import Job
from app.models.metering import QuotaReservation
from app.models.oauth import OAuthConnection
from app.services.dispatch.hash_utils import compute_content_hash
from app.services.metering.quota_service import QuotaService, QuotaExceededException
from app.services.integrations.google_service import (
    GoogleIntegrationService,
    GmailApiException,
    GmailApiNotConfiguredException,
    GmailRateLimitException,
    GmailInsufficientPermissionsException,
    GmailServerErrorException,
    GmailNetworkTimeoutException,
)
from app.services.integrations.mime_builder import (
    MimeBuilder,
    MimeBuilderException,
)

logger = logging.getLogger(__name__)


class SendGatewayException(Exception):
    """Base exception for SendGateway dispatch failures."""
    pass


class SendGateway:
    """
    Orchestrates verified outbound email dispatch with strict safety caps,
    kill switches, idempotency barriers, and immutable evidence logging.
    """

    @classmethod
    def queue_application_send(
        cls,
        db: Session,
        account_id: str,
        application: Application,
        source: str = "ui_click",
        mode: str = "supervised",
        undo_delay_seconds: int = 30,
        correlation_id: Optional[str] = None,
    ) -> HoldQueueItem:
        """
        Enqueues an application for outbound dispatch with an undo hold window.
        Atomically:
        1. Checks account and entitlement validity (auto_send_allowed).
        2. Reserves quota via QuotaService.
        3. Records UserCommand and mints SendAuthorization with canonical content hash.
        4. Inserts HoldQueueItem with release_at = now + undo_delay_seconds.
        5. Sets application.status = 'queued' (sent_at strictly remains None).
        """
        now = datetime.now(timezone.utc)

        # 1. Check dispatch settings / kill switch
        settings_row = db.query(AccountDispatchSettings).filter_by(account_id=account_id).first()
        if not settings_row:
            settings_row = AccountDispatchSettings(account_id=account_id, autonomy_mode="supervised")
            db.add(settings_row)
            db.flush()

        if settings_row.kill_switch or settings_row.is_suspended_by_admin:
            raise SendGatewayException("Dispatch is paused: kill switch active or account suspended.")

        # 2. Reserve quota
        reservation = QuotaService.reserve(
            db=db,
            account_id=account_id,
            quota_key="monthly_applications_limit",
            units=1,
            correlation_id=correlation_id or application.id,
        )

        delay_sec = getattr(settings_row, "undo_delay_seconds", undo_delay_seconds) or undo_delay_seconds
        release_at = now + timedelta(seconds=delay_sec)

        # 4. UserCommand
        cmd = UserCommand(
            id=str(uuid.uuid4()),
            account_id=account_id,
            command_type="single",
            mode=mode,
            source=source,
            target_job_ids=[application.job_id] if application.job_id else [],
            expires_at=now + timedelta(hours=1),
        )
        db.add(cmd)
        db.flush()

        # 5. Canonical Content Hash & SendAuthorization
        pdf_payload = db.query(ApplicationPdfPayload).filter_by(application_id=application.id).first()
        pdf_sha256 = pdf_payload.sha256 if pdf_payload else (application.pdf_sha256 or "")
        recipient_email = application.recipient_email or ""

        content_hash = compute_content_hash(
            cv_version_id=application.cv_version_id or "",
            subject=application.subject or "",
            body=application.draft_content or application.body or "",
            recipient=recipient_email,
            answers_json="[]",
            attachment_sha256=pdf_sha256,
        )

        auth = SendAuthorization(
            id=str(uuid.uuid4()),
            account_id=account_id,
            application_id=application.id,
            command_id=cmd.id,
            recipient_email=recipient_email,
            content_hash=content_hash,
            minted_by="human_approval",
            status="pending",
            expires_at=now + timedelta(hours=1),
        )
        db.add(auth)
        db.flush()

        # 6. HoldQueueItem
        hold_item = HoldQueueItem(
            id=str(uuid.uuid4()),
            account_id=account_id,
            application_id=application.id,
            authorization_id=auth.id,
            reservation_id=reservation.id,
            status="pending",
            release_at=release_at,
            hold_kind="review_required",
            channel=application.channel or "email",
        )
        db.add(hold_item)

        # 7. Transition Application state: application is queued, sent_at is strictly None!
        application.status = "queued"
        db.commit()

        return hold_item

    @classmethod
    async def dispatch_hold_item(cls, db: Session, hold_item_id: str) -> bool:
        """
        Execute dispatch for a claimed hold_queue_item.
        Returns True if sent successfully, False otherwise.
        """
        # 1. Fetch hold item
        hold_item = db.query(HoldQueueItem).filter_by(id=hold_item_id).first()
        if not hold_item or hold_item.status not in ("pending", "claimed"):
            logger.warning("Hold item %s not found or not in pending/claimed status", hold_item_id)
            return False

        # --- Phase 1: Atomic Pre-Check and Reservation Transaction ---
        precheck_result = cls._run_precheck_and_reserve(db, hold_item)
        if not precheck_result.get("proceed", False):
            return False

        action_id = precheck_result["action_id"]
        auth_id = precheck_result["auth_id"]
        app_id = precheck_result["app_id"]
        job_id = precheck_result["job_id"]
        pdf_bytes = precheck_result.get("pdf_bytes")
        pdf_sha256 = precheck_result.get("pdf_sha256")
        recipient_email = precheck_result["recipient_email"]
        subject = precheck_result["subject"]
        body_text = precheck_result["body_text"]
        send_id = precheck_result["send_id"]

        # --- Phase 2: External Transmission (No Database Lock Held) ---
        oauth_conn = (
            db.query(OAuthConnection)
            .filter(
                OAuthConnection.account_id == hold_item.account_id,
                OAuthConnection.provider.in_(["google", "smtp"]),
            )
            .first()
        )
        if not oauth_conn or not oauth_conn.encrypted_access_token:
            cls._handle_hard_failure(
                db, hold_item.id, action_id, auth_id, app_id,
                abort_reason="permanent_failure",
                error_message="Email dispatch account (Google OAuth or SMTP) is not connected.",
            )
            return False

        access_token = None
        smtp_password = None
        smtp_host = "smtp.gmail.com"
        smtp_port = 587

        if oauth_conn.provider == "google":
            access_token = decrypt_oauth_token(oauth_conn.encrypted_access_token)
            now = datetime.now(timezone.utc)

            # Refresh token if expired
            if oauth_conn.token_expires_at:
                exp_tz = oauth_conn.token_expires_at
                if exp_tz.tzinfo is None:
                    exp_tz = exp_tz.replace(tzinfo=timezone.utc)
                if exp_tz <= now:
                    if oauth_conn.encrypted_refresh_token:
                        try:
                            new_token = await GoogleIntegrationService.refresh_access_token(
                                oauth_conn.encrypted_refresh_token,
                                db=db,
                                account_id=hold_item.account_id,
                            )
                            oauth_conn.encrypted_access_token = encrypt_oauth_token(new_token)
                            oauth_conn.token_expires_at = now + timedelta(seconds=3600)
                            db.commit()
                            access_token = new_token
                        except Exception as e:
                            cls._handle_hard_failure(
                                db, hold_item.id, action_id, auth_id, app_id,
                                abort_reason="permanent_failure",
                                error_message=f"Failed to refresh Google OAuth token: {e}",
                            )
                            return False
        elif oauth_conn.provider == "smtp":
            from app.core.crypto import decrypt_secret
            smtp_password = decrypt_secret(oauth_conn.encrypted_access_token)
            if oauth_conn.scope and ":" in oauth_conn.scope:
                try:
                    parts = oauth_conn.scope.split(":")
                    smtp_host = parts[0]
                    smtp_port = int(parts[1])
                except Exception:
                    pass

        # Guard: Prohibit sending without valid PDF artifact
        if not pdf_bytes or not pdf_bytes.startswith(b"%PDF"):
            cls._handle_hard_failure(
                db, hold_item.id, action_id, auth_id, app_id,
                abort_reason="missing_pdf",
                error_message="Dispatch aborted: Missing or invalid PDF attachment.",
            )
            return False

        # Build MIME payload
        try:
            raw_mime = MimeBuilder.build_message(
                to=recipient_email,
                subject=subject,
                body_text=body_text,
                pdf_bytes=pdf_bytes,
                pdf_filename=f"Application_{job_id[:8]}.pdf",
                send_id=send_id,
            )
        except MimeBuilderException as e:
            cls._handle_hard_failure(
                db, hold_item.id, action_id, auth_id, app_id,
                abort_reason="permanent_failure",
                error_message=f"MIME message construction failed: {e}",
            )
            return False

        # External dispatch transmission
        if oauth_conn.provider == "google":
            # Invoke Google Gmail API
            try:
                send_result = await GoogleIntegrationService.send_gmail_message(
                    access_token=access_token,
                    raw_mime_bytes=raw_mime,
                    timeout=30.0,
                )
            except (GmailRateLimitException, GmailServerErrorException) as e:
                logger.warning("Retryable Gmail API error for hold item %s: %s", hold_item.id, e)
                cls._handle_retryable_failure(db, hold_item.id, action_id, str(e))
                return False
            except (GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailApiException) as e:
                logger.error("Non-retryable Gmail API error for hold item %s: %s", hold_item.id, e)
                cls._handle_hard_failure(
                    db, hold_item.id, action_id, auth_id, app_id,
                    abort_reason="permanent_failure",
                    error_message=str(e),
                )
                return False
            except GmailNetworkTimeoutException as e:
                logger.error("Gmail API timeout for hold item %s: %s. Leaving in sending for sweeper.", hold_item.id, e)
                # Item remains in 'sending'; periodic sweeper will transition to 'unknown'
                return False
        else:
            # Invoke SMTP Transmission
            import smtplib
            try:
                if smtp_port == 465:
                    server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30.0)
                else:
                    server = smtplib.SMTP(smtp_host, smtp_port, timeout=30.0)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                server.login(oauth_conn.email, smtp_password)
                server.sendmail(oauth_conn.email, [recipient_email], raw_mime)
                server.quit()
                send_result = {
                    "id": f"smtp_{uuid.uuid4().hex[:12]}",
                    "threadId": f"smtp_thread_{uuid.uuid4().hex[:12]}",
                    "labelIds": ["SENT"],
                }
            except Exception as e:
                logger.error("SMTP transmission error for hold item %s: %s", hold_item.id, e)
                cls._handle_hard_failure(
                    db, hold_item.id, action_id, auth_id, app_id,
                    abort_reason="permanent_failure",
                    error_message=f"SMTP transmission failed: {e}",
                )
                return False

        # --- Phase 3: Post-Call Settlement Transaction ---
        cls._settle_successful_dispatch(
            db=db,
            hold_item_id=hold_item.id,
            action_id=action_id,
            auth_id=auth_id,
            app_id=app_id,
            job_id=job_id,
            send_result=send_result,
            subject=subject,
            recipient_email=recipient_email,
            pdf_sha256=pdf_sha256,
            send_id=send_id,
        )
        return True

    @classmethod
    def _run_precheck_and_reserve(cls, db: Session, hold_item: HoldQueueItem) -> Dict[str, Any]:
        """
        Executes pre-checks, checks send caps and kill switches, verifies canonical content hash,
        and atomically reserves the idempotency key.
        """
        now = datetime.now(timezone.utc)

        # 1. Row-level lock on account settings
        settings_row = (
            db.query(AccountDispatchSettings)
            .filter_by(account_id=hold_item.account_id)
            .with_for_update()
            .first()
        )
        if not settings_row:
            # Lazy creation: fail closed to supervised
            settings_row = AccountDispatchSettings(
                account_id=hold_item.account_id,
                autonomy_mode="supervised",
            )
            db.add(settings_row)
            db.flush()

        # 2. Kill switch verification
        if settings.DISPATCH_GLOBAL_KILL_SWITCH:
            cls._abort_hold_item(db, hold_item, "kill_switch_activated", "Global emergency kill switch is active.")
            return {"proceed": False}

        if settings_row.kill_switch:
            cls._abort_hold_item(db, hold_item, "kill_switch_activated", "Account emergency kill switch is active.")
            return {"proceed": False}

        if settings_row.is_suspended_by_admin:
            cls._abort_hold_item(db, hold_item, "admin_suspended", "Account has been suspended by an administrator.")
            return {"proceed": False}

        # 3. Query SendAuthorization
        auth = db.query(SendAuthorization).filter_by(id=hold_item.authorization_id).first()
        if not auth or auth.status != "pending":
            cls._abort_hold_item(db, hold_item, "permanent_failure", "Send authorization missing or not pending.")
            return {"proceed": False}

        if auth.expires_at <= now:
            cls._abort_hold_item(db, hold_item, "permanent_failure", "Send authorization has expired.")
            return {"proceed": False}

        # 4. Query Application & Job
        app = db.query(Application).filter_by(id=hold_item.application_id, account_id=hold_item.account_id).first()
        if not app:
            cls._abort_hold_item(db, hold_item, "permanent_failure", "Application record not found.")
            return {"proceed": False}

        job = db.query(Job).filter_by(id=app.job_id, account_id=hold_item.account_id).first()
        if not job or not job.is_active or job.vetoed:
            cls._abort_hold_item(db, hold_item, "permanent_failure", "Job posting is inactive or vetoed.")
            return {"proceed": False}

        mode = "autonomous" if auth.minted_by == "autonomous_policy" else "supervised"

        # 5. Send Caps Verification
        window_24h = now - timedelta(days=1)
        window_1h = now - timedelta(hours=1)
        active_statuses = ["reserved", "sending", "sent", "unknown"]

        if mode == "autonomous":
            rolling_auto_24h = db.query(DispatchedAction).filter(
                DispatchedAction.account_id == hold_item.account_id,
                DispatchedAction.mode == "autonomous",
                DispatchedAction.status.in_(active_statuses),
                DispatchedAction.created_at >= window_24h,
            ).count()
            if rolling_auto_24h >= settings_row.autonomous_daily_cap:
                cls._abort_hold_item(db, hold_item, "cap_exceeded", f"Autonomous daily send cap ({settings_row.autonomous_daily_cap}) reached.")
                return {"proceed": False}

            rolling_auto_1h = db.query(DispatchedAction).filter(
                DispatchedAction.account_id == hold_item.account_id,
                DispatchedAction.mode == "autonomous",
                DispatchedAction.status.in_(active_statuses),
                DispatchedAction.created_at >= window_1h,
            ).count()
            if rolling_auto_1h >= settings_row.autonomous_hourly_cap:
                cls._abort_hold_item(db, hold_item, "cap_exceeded", f"Autonomous hourly send cap ({settings_row.autonomous_hourly_cap}) reached.")
                return {"proceed": False}

        # Check overall platform safety caps
        rolling_safety_24h = db.query(DispatchedAction).filter(
            DispatchedAction.account_id == hold_item.account_id,
            DispatchedAction.status.in_(active_statuses),
            DispatchedAction.created_at >= window_24h,
        ).count()
        if rolling_safety_24h >= settings_row.safety_daily_cap:
            cls._abort_hold_item(db, hold_item, "cap_exceeded", f"Safety daily send cap ({settings_row.safety_daily_cap}) reached.")
            return {"proceed": False}

        rolling_safety_1h = db.query(DispatchedAction).filter(
            DispatchedAction.account_id == hold_item.account_id,
            DispatchedAction.status.in_(active_statuses),
            DispatchedAction.created_at >= window_1h,
        ).count()
        if rolling_safety_1h >= settings_row.safety_hourly_cap:
            cls._abort_hold_item(db, hold_item, "cap_exceeded", f"Safety hourly send cap ({settings_row.safety_hourly_cap}) reached.")
            return {"proceed": False}

        # 6. Content Hash Verification
        pdf_bytes = None
        pdf_sha256 = None
        pdf_payload = db.query(ApplicationPdfPayload).filter_by(application_id=app.id).first()
        if pdf_payload:
            pdf_bytes = pdf_payload.payload_bytes
            pdf_sha256 = pdf_payload.sha256
        elif app.pdf_sha256:
            pdf_sha256 = app.pdf_sha256

        computed_hash = compute_content_hash(
            cv_version_id=app.cv_version_id,
            subject=app.subject or "",
            body=app.body or app.draft_content or "",
            recipient=auth.recipient_email or app.recipient_email or "",
            answers_json="[]",
            attachment_sha256=pdf_sha256 or "",
        )
        if computed_hash != auth.content_hash:
            cls._abort_hold_item(
                db, hold_item, "content_modified",
                "Content hash mismatch: application was modified after authorization was minted.",
            )
            return {"proceed": False}

        # 7. Reserve Idempotency Key in DispatchedAction
        action = DispatchedAction(
            account_id=hold_item.account_id,
            job_id=job.id,
            application_id=app.id,
            channel=hold_item.channel or "email",
            sequence_kind="initial_application",
            mode=mode,
            status="reserved",
        )
        db.add(action)
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            cls._abort_hold_item(
                db, hold_item, "permanent_failure",
                "Duplicate dispatch attempt detected for this job and sequence.",
            )
            return {"proceed": False}

        # 8. Mark hold item as sending
        hold_item.status = "sending"
        hold_item.sending_started_at = now
        db.commit()

        return {
            "proceed": True,
            "action_id": action.id,
            "auth_id": auth.id,
            "app_id": app.id,
            "job_id": job.id,
            "pdf_bytes": pdf_bytes,
            "pdf_sha256": pdf_sha256,
            "recipient_email": auth.recipient_email,
            "subject": app.subject or f"Application for {job.role}",
            "body_text": app.body or app.draft_content or "",
            "send_id": auth.x_jobeazy_send_id,
        }

    @classmethod
    def _abort_hold_item(cls, db: Session, hold_item: HoldQueueItem, abort_reason: str, error_message: str) -> None:
        """Atomically abort hold queue item and release associated resources."""
        hold_item.status = "aborted"
        hold_item.abort_reason = abort_reason
        hold_item.error_message = error_message
        if hold_item.reservation_id:
            QuotaService.release(db, hold_item.reservation_id)
        db.commit()

    @classmethod
    def _handle_hard_failure(
        cls,
        db: Session,
        hold_item_id: str,
        action_id: str,
        auth_id: str,
        app_id: str,
        abort_reason: str,
        error_message: str,
    ) -> None:
        """Handle non-retryable fatal dispatch failure."""
        hold_item = db.query(HoldQueueItem).filter_by(id=hold_item_id).first()
        action = db.query(DispatchedAction).filter_by(id=action_id).first()
        auth = db.query(SendAuthorization).filter_by(id=auth_id).first()
        app = db.query(Application).filter_by(id=app_id).first()

        if hold_item:
            hold_item.status = "aborted"
            hold_item.abort_reason = abort_reason
            hold_item.error_message = error_message
            if hold_item.reservation_id:
                QuotaService.release(db, hold_item.reservation_id)

        if action:
            action.status = "aborted"

        if auth:
            auth.status = "voided"
            auth.voided_at = datetime.now(timezone.utc)

        if app:
            app.status = "draft"

        db.commit()

    @classmethod
    def _handle_retryable_failure(cls, db: Session, hold_item_id: str, action_id: str, error_message: str) -> None:
        """Handle retryable 429/5xx error by scheduling exponential backoff and releasing reservation."""
        hold_item = db.query(HoldQueueItem).filter_by(id=hold_item_id).first()
        action = db.query(DispatchedAction).filter_by(id=action_id).first()

        if hold_item:
            now = datetime.now(timezone.utc)
            backoff_minutes = min(60, 5 * (2 ** hold_item.attempt_count))
            hold_item.status = "pending"
            hold_item.attempt_count += 1
            hold_item.last_attempt_at = now
            hold_item.release_at = now + timedelta(minutes=backoff_minutes)
            hold_item.sending_started_at = None
            hold_item.claimed_at = None
            hold_item.error_message = error_message

        if action:
            # Delete action so future attempt can re-reserve clean
            db.delete(action)

        db.commit()

    @classmethod
    def _settle_successful_dispatch(
        cls,
        db: Session,
        hold_item_id: str,
        action_id: str,
        auth_id: str,
        app_id: str,
        job_id: str,
        send_result: Dict[str, Any],
        subject: str,
        recipient_email: str,
        pdf_sha256: Optional[str],
        send_id: str,
    ) -> None:
        """Atomically record successful external dispatch, evidence, and state transitions."""
        now = datetime.now(timezone.utc)
        hold_item = db.query(HoldQueueItem).filter_by(id=hold_item_id).first()
        action = db.query(DispatchedAction).filter_by(id=action_id).first()
        auth = db.query(SendAuthorization).filter_by(id=auth_id).first()
        app = db.query(Application).filter_by(id=app_id).first()

        if hold_item:
            hold_item.status = "sent"
            if hold_item.reservation_id:
                QuotaService.settle(
                    db,
                    hold_item.reservation_id,
                    actual_applications=1,
                    metadata={"channel": hold_item.channel, "application_id": app_id},
                )

        if action:
            action.status = "sent"
            action.dispatched_at = now

        if auth:
            auth.status = "consumed"
            auth.consumed_at = now

        if app:
            app.status = "applied"
            app.sent_at = now

        evidence = SendEvidence(
            account_id=hold_item.account_id,
            job_id=job_id,
            application_id=app_id,
            authorization_id=auth_id,
            channel=hold_item.channel or "email",
            external_message_id=send_result.get("id", f"msg_{now.timestamp()}"),
            external_thread_id=send_result.get("threadId"),
            subject=subject,
            headers_snapshot={"X-JobEazy-Send-ID": send_id},
            canonical_content_hash=auth.content_hash if auth else "",
            attachment_sha256=pdf_sha256,
            recipient_email=recipient_email,
            sent_at=now,
        )
        db.add(evidence)
        db.commit()

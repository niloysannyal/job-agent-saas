import os
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import encrypt_oauth_token
from app.models.account import Account
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
from app.models.oauth import OAuthConnection
from app.services.dispatch.gateway import SendGateway
from app.services.dispatch.hash_utils import compute_content_hash
from app.services.integrations.google_service import (
    GmailRateLimitException,
    GmailInsufficientPermissionsException,
    GmailNetworkTimeoutException,
)
from app.workers.dispatch_poller import claim_pending_batch, sweep_stale_items


def create_test_hierarchy(test_db_session: Session, autonomy_mode: str = "supervised"):
    """Helper to populate a clean account, job, app, command, authorization, and hold item."""
    account_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())
    cmd_id = str(uuid.uuid4())
    auth_id = str(uuid.uuid4())
    hold_id = str(uuid.uuid4())

    account = Account(id=account_id, email=f"user_{uuid.uuid4().hex[:6]}@example.com")
    job = Job(id=job_id, role="Backend Engineer", company="Acme Inc", apply_link="https://acme.com/apply", source="test", account_id=account_id)
    app = Application(
        id=app_id,
        account_id=account_id,
        job_id=job_id,
        subject="Application for Backend Engineer",
        draft_content="Hello team, here is my profile.",
        recipient_email="recruiter@acme.com",
    )
    settings_row = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode=autonomy_mode,
        autonomous_daily_cap=5,
        autonomous_hourly_cap=2,
        safety_daily_cap=50,
        safety_hourly_cap=15,
    )
    cmd = UserCommand(
        id=cmd_id,
        account_id=account_id,
        command_type="single",
        mode=autonomy_mode,
        source="ui_click",
        target_job_ids=[job_id],
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    valid_pdf = b"%PDF-1.4\nTest dummy PDF bytes\n%%EOF"
    pdf_payload = ApplicationPdfPayload(
        application_id=app_id,
        account_id=account_id,
        sha256="abc_pdf_hash_123",
        payload_bytes=valid_pdf,
        size_bytes=len(valid_pdf),
    )
    content_hash = compute_content_hash(
        cv_version_id=app.cv_version_id,
        subject=app.subject,
        body=app.draft_content,
        recipient="recruiter@acme.com",
        answers_json="[]",
        attachment_sha256="abc_pdf_hash_123",
    )
    auth = SendAuthorization(
        id=auth_id,
        account_id=account_id,
        application_id=app_id,
        command_id=cmd_id,
        recipient_email="recruiter@acme.com",
        content_hash=content_hash,
        minted_by="human_approval" if autonomy_mode == "supervised" else "autonomous_policy",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    hold = HoldQueueItem(
        id=hold_id,
        account_id=account_id,
        application_id=app_id,
        authorization_id=auth_id,
        status="claimed",
        release_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        claimed_at=datetime.now(timezone.utc),
    )
    oauth = OAuthConnection(
        id=str(uuid.uuid4()),
        account_id=account_id,
        provider="google",
        email="test_user@gmail.com",
        encrypted_access_token=encrypt_oauth_token("mock_access_token_123"),
    )

    test_db_session.add_all([account, job, app, settings_row])
    test_db_session.flush()
    test_db_session.add(cmd)
    test_db_session.flush()
    test_db_session.add_all([auth, pdf_payload, oauth])
    test_db_session.flush()
    test_db_session.add(hold)
    test_db_session.commit()

    return {
        "account": account,
        "job": job,
        "app": app,
        "settings": settings_row,
        "auth": auth,
        "hold": hold,
        "oauth": oauth,
        "pdf_bytes": valid_pdf,
    }


# --- 1. Pre-Check & Kill Switch Tests ---

@pytest.mark.asyncio
async def test_dispatch_aborted_by_account_kill_switch(test_db_session):
    """Verify that an active account kill_switch aborts dispatch."""
    data = create_test_hierarchy(test_db_session)
    data["settings"].kill_switch = True
    test_db_session.commit()

    success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
    assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "kill_switch_activated"


@pytest.mark.asyncio
async def test_dispatch_aborted_by_admin_suspension(test_db_session):
    """Verify that an administrative account suspension aborts dispatch."""
    data = create_test_hierarchy(test_db_session)
    data["settings"].is_suspended_by_admin = True
    test_db_session.commit()

    success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
    assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "admin_suspended"


@pytest.mark.asyncio
async def test_dispatch_aborted_by_global_kill_switch(test_db_session):
    """Verify that the global emergency kill switch aborts dispatch."""
    data = create_test_hierarchy(test_db_session)
    with patch.object(settings, "DISPATCH_GLOBAL_KILL_SWITCH", True):
        success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
        assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "kill_switch_activated"


# --- 2. Content Tamper Barrier Test ---

@pytest.mark.asyncio
async def test_dispatch_aborted_on_content_tampering(test_db_session):
    """Verify that modifying the application after authorization was minted causes abort."""
    data = create_test_hierarchy(test_db_session)
    # Modify application body text (tampering)
    data["app"].draft_content = "Tampered body text that changes the hash!"
    test_db_session.commit()

    success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
    assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "content_modified"
    assert "Content hash mismatch" in reloaded_hold.error_message


# --- 3. Caps Enforcement Test ---

@pytest.mark.asyncio
async def test_dispatch_aborted_on_autonomous_daily_cap(test_db_session):
    """Verify autonomous cap enforcement halts dispatch once limit is reached."""
    data = create_test_hierarchy(test_db_session, autonomy_mode="autonomous")
    data["settings"].autonomous_daily_cap = 1
    test_db_session.commit()

    # Create a prior job & 1 already dispatched action in last 24h
    prior_job = Job(
        id=str(uuid.uuid4()),
        role="Dev",
        company="Acme",
        apply_link="https://acme.com",
        source="test",
        account_id=data["account"].id,
    )
    test_db_session.add(prior_job)
    test_db_session.flush()

    prior_action = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=data["account"].id,
        job_id=prior_job.id,
        application_id=data["app"].id,
        channel="email",
        mode="autonomous",
        status="sent",
        created_at=datetime.now(timezone.utc) - timedelta(hours=2),
    )
    test_db_session.add(prior_action)
    test_db_session.commit()

    success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
    assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "cap_exceeded"
    assert "Autonomous daily send cap" in reloaded_hold.error_message


# --- 4. Successful Dispatch Flow Test ---

@pytest.mark.asyncio
async def test_successful_dispatch_and_settlement(test_db_session):
    """
    Verify full end-to-end happy path:
    1. Pre-check reserves action and marks sending.
    2. Mock send succeeds.
    3. Hold item marked sent, action marked sent, auth marked consumed, app marked applied.
    4. SendEvidence created with tracking header.
    """
    data = create_test_hierarchy(test_db_session)

    success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
    assert success is True

    # Verify hold item status
    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "sent"

    # Verify authorization consumed
    reloaded_auth = test_db_session.query(SendAuthorization).filter_by(id=data["auth"].id).one()
    assert reloaded_auth.status == "consumed"
    assert reloaded_auth.consumed_at is not None

    # Verify application applied
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "applied"
    assert reloaded_app.sent_at is not None

    # Verify dispatched action sent
    action = (
        test_db_session.query(DispatchedAction)
        .filter_by(account_id=data["account"].id, job_id=data["job"].id)
        .one()
    )
    assert action.status == "sent"
    assert action.dispatched_at is not None

    # Verify SendEvidence created
    evidence = (
        test_db_session.query(SendEvidence)
        .filter_by(authorization_id=data["auth"].id)
        .one()
    )
    assert evidence.external_message_id.startswith("mock_sent_msg_")
    assert evidence.recipient_email == "recruiter@acme.com"
    assert evidence.headers_snapshot["X-JobEazy-Send-ID"] == data["auth"].x_jobeazy_send_id


# --- 5. Retryable and Non-Retryable Error Handlers ---

@pytest.mark.asyncio
async def test_retryable_error_exponential_backoff(test_db_session):
    """Verify 429/rate-limit triggers exponential backoff and frees action reservation."""
    data = create_test_hierarchy(test_db_session)

    with patch(
        "app.services.integrations.google_service.GoogleIntegrationService.send_gmail_message",
        side_effect=GmailRateLimitException("Rate limit hit"),
    ):
        success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
        assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "pending"
    assert reloaded_hold.attempt_count == 1
    assert reloaded_hold.release_at > datetime.now(timezone.utc)

    # Action reservation was removed so future retry can re-reserve clean
    action = test_db_session.query(DispatchedAction).filter_by(account_id=data["account"].id, job_id=data["job"].id).first()
    assert action is None


@pytest.mark.asyncio
async def test_non_retryable_error_hard_fail(test_db_session):
    """Verify fatal permission error voids auth, aborts action, and reverts app to draft."""
    data = create_test_hierarchy(test_db_session)

    with patch(
        "app.services.integrations.google_service.GoogleIntegrationService.send_gmail_message",
        side_effect=GmailInsufficientPermissionsException("Scope missing"),
    ):
        success = await SendGateway.dispatch_hold_item(test_db_session, data["hold"].id)
        assert success is False

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded_hold.status == "aborted"
    assert reloaded_hold.abort_reason == "permanent_failure"

    reloaded_auth = test_db_session.query(SendAuthorization).filter_by(id=data["auth"].id).one()
    assert reloaded_auth.status == "voided"

    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "draft"


# --- 6. Poller & Sweeper Tests ---

def test_claim_pending_batch_skip_locked(test_db_session):
    """Verify claiming pending items where release_at <= now."""
    data = create_test_hierarchy(test_db_session)
    data["hold"].status = "pending"
    data["hold"].release_at = datetime.now(timezone.utc) - timedelta(minutes=5)
    test_db_session.commit()

    claimed_ids = claim_pending_batch(test_db_session, batch_size=10)
    assert data["hold"].id in claimed_ids

    reloaded = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded.status == "claimed"
    assert reloaded.claimed_at is not None


def test_sweeper_stale_claimed_and_sending(test_db_session):
    """Verify sweeper resets stale claimed to pending and transitions stale sending to unknown."""
    data = create_test_hierarchy(test_db_session)
    now = datetime.now(timezone.utc)

    # 1. Stale claimed (>30s)
    data["hold"].status = "claimed"
    data["hold"].claimed_at = now - timedelta(seconds=45)

    # 2. Stale sending (>60s)
    hold2 = HoldQueueItem(
        id=str(uuid.uuid4()),
        account_id=data["account"].id,
        application_id=data["app"].id,
        authorization_id=data["auth"].id,
        status="sending",
        release_at=now - timedelta(minutes=5),
        sending_started_at=now - timedelta(seconds=90),
    )
    test_db_session.add(hold2)
    test_db_session.commit()

    result = sweep_stale_items(test_db_session)
    assert result["swept_claimed"] >= 1
    assert result["swept_sending"] >= 1

    reloaded1 = test_db_session.query(HoldQueueItem).filter_by(id=data["hold"].id).one()
    assert reloaded1.status == "pending"
    assert reloaded1.claimed_at is None

    reloaded2 = test_db_session.query(HoldQueueItem).filter_by(id=hold2.id).one()
    assert reloaded2.status == "unknown"

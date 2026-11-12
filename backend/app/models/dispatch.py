import uuid
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey,
    ForeignKeyConstraint, Index, Integer, JSON, LargeBinary, String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AccountDispatchSettings(Base):
    """
    Tenant-scoped dispatch settings, safety caps, and kill switches.
    Users can self-serve toggle autonomy_mode and set caps within safety limits.
    is_suspended_by_admin and safety caps are superadmin-only.
    """
    __tablename__ = "account_dispatch_settings"

    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        primary_key=True,
    )
    autonomy_mode: Mapped[str] = mapped_column(
        String(20),
        default="supervised",
        nullable=False,
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    acknowledgment_text_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )
    kill_switch: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_suspended_by_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    autonomous_daily_cap: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )
    autonomous_hourly_cap: Mapped[int] = mapped_column(
        Integer,
        default=2,
        nullable=False,
    )
    safety_daily_cap: Mapped[int] = mapped_column(
        Integer,
        default=50,
        nullable=False,
    )
    safety_hourly_cap: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "autonomy_mode IN ('supervised', 'autonomous')",
            name="ck_dispatch_autonomy_mode",
        ),
        CheckConstraint(
            "autonomous_daily_cap > 0 AND autonomous_daily_cap <= 10",
            name="ck_dispatch_auto_daily_cap",
        ),
        CheckConstraint(
            "autonomous_hourly_cap > 0 AND autonomous_hourly_cap <= 5",
            name="ck_dispatch_auto_hourly_cap",
        ),
        CheckConstraint(
            "safety_daily_cap > 0 AND safety_daily_cap <= 100",
            name="ck_dispatch_safety_daily_cap",
        ),
        CheckConstraint(
            "safety_hourly_cap > 0 AND safety_hourly_cap <= 20",
            name="ck_dispatch_safety_hourly_cap",
        ),
        CheckConstraint(
            "autonomous_daily_cap <= safety_daily_cap",
            name="ck_dispatch_caps_hierarchy_daily",
        ),
        CheckConstraint(
            "autonomous_hourly_cap <= safety_hourly_cap",
            name="ck_dispatch_caps_hierarchy_hourly",
        ),
    )


class UserCommand(Base):
    """
    Immutable authority-to-attempt minted by UI clicks, verified chat intent, or voice commands.
    Freezes target_job_ids so SendGateway can verify authorization matches command scope.
    """
    __tablename__ = "user_commands"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    command_type: Mapped[str] = mapped_column(String(20), nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    source_message_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    target_job_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("command_type IN ('single', 'batch')", name="ck_user_command_type"),
        CheckConstraint("mode IN ('supervised', 'autonomous')", name="ck_user_command_mode"),
        CheckConstraint("source IN ('ui_click', 'chat_text', 'voice')", name="ck_user_command_source"),
        CheckConstraint("status IN ('active', 'completed', 'cancelled', 'expired')", name="ck_user_command_status"),
        UniqueConstraint("account_id", "source_message_id", name="uq_user_cmd_msg"),
    )


class SendAuthorization(Base):
    """
    Content-pinned authorization. Binds exact recipient, content hash, tracking id,
    and attachment hash. Voided if content is edited during hold.
    """
    __tablename__ = "send_authorizations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    command_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("user_commands.id", ondelete="SET NULL"),
        nullable=True,
    )
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    attachment_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    x_jobeazy_send_id: Mapped[str] = mapped_column(
        String(64),
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    minted_by: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    voided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("minted_by IN ('human_approval', 'autonomous_policy')", name="ck_send_auth_minted_by"),
        CheckConstraint("status IN ('pending', 'consumed', 'voided', 'expired')", name="ck_send_auth_status"),
    )


class ApplicationPdfPayload(Base):
    """
    Stores compiled PDF byte payloads outside applications table to prevent bloat.
    """
    __tablename__ = "application_pdf_payloads"

    application_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applications.id", ondelete="CASCADE"),
        primary_key=True,
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_bytes: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class HoldQueueItem(Base):
    """
    Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP LOCKED.
    Tracks worker claiming and sending timestamps for stale sweepers.
    """
    __tablename__ = "hold_queue_items"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    authorization_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("send_authorizations.id", ondelete="RESTRICT"),
        nullable=False,
    )
    reservation_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("quota_reservations.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    hold_kind: Mapped[str] = mapped_column(String(50), default="review_required", nullable=False)
    abort_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    channel: Mapped[str] = mapped_column(String(20), default="email", nullable=False)
    release_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sending_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'claimed', 'sending', 'sent', 'cancelled', 'aborted', 'unknown')",
            name="ck_hold_queue_status",
        ),
        CheckConstraint(
            "hold_kind IN ('review_required', 'autonomous_delay', 'tofu_unknown')",
            name="ck_hold_queue_hold_kind",
        ),
        CheckConstraint(
            "abort_reason IS NULL OR abort_reason IN ('user_cancelled', 'kill_switch_activated', 'admin_suspended', 'content_modified', 'recipient_untrusted', 'cap_exceeded', 'permanent_failure')",
            name="ck_hold_queue_abort_reason",
        ),
        Index("ix_hold_queue_pending", "status", "release_at", postgresql_where=(status == "pending")),
    )


class SendEvidence(Base):
    """
    Immutable audit evidence of external transmission.
    Uses NO ACTION DEFERRABLE INITIALLY DEFERRED to allow clean account deletion.
    """
    __tablename__ = "send_evidence"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    authorization_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("send_authorizations.id", ondelete="RESTRICT"),
        nullable=False,
    )
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    external_message_id: Mapped[str] = mapped_column(String(255), nullable=False)
    external_thread_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    headers_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    canonical_content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    attachment_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            ondelete="NO ACTION",
            deferrable=True,
            initially="DEFERRED",
            name="fk_send_evidence_app_deferrable",
        ),
        UniqueConstraint("channel", "external_message_id", name="uq_evidence_ext_msg"),
        Index("ix_evidence_account_sent", "account_id", "sent_at"),
    )


class DispatchedAction(Base):
    """
    Sequenced idempotency barrier.
    Partial unique index excludes aborted/failed so user can retry failed attempts.
    """
    __tablename__ = "dispatched_actions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(20), default="email", nullable=False)
    sequence_kind: Mapped[str] = mapped_column(String(30), default="initial_application", nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            ondelete="NO ACTION",
            deferrable=True,
            initially="DEFERRED",
            name="fk_dispatched_app_deferrable",
        ),
        CheckConstraint("mode IN ('supervised', 'autonomous')", name="ck_dispatched_mode"),
        CheckConstraint(
            "status IN ('reserved', 'sending', 'sent', 'failed', 'aborted', 'unknown')",
            name="ck_dispatched_status",
        ),
        Index(
            "uq_dispatch_idempotency_active",
            "account_id",
            "job_id",
            "channel",
            "sequence_kind",
            unique=True,
            postgresql_where=(status.notin_(["aborted", "failed"])),
        ),
        Index("ix_dispatched_account_time", "account_id", "dispatched_at"),
    )


class TrustedRecipient(Base):
    """
    TOFU Exact-Address allowlist.
    Email uniqueness is enforced case-insensitively via lower(email).
    """
    __tablename__ = "trusted_recipients"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    confirmed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index("uq_trusted_recipient_lower", "account_id", sa.text("lower(email)"), unique=True),
        CheckConstraint("source IN ('manual_approval', 'human_review')", name="ck_trusted_recipient_source"),
    )


class JobFeedback(Base):
    """
    Ground-truth precision tracking with integer rating (+1 or -1).
    Unique constraint guarantees exactly one rating per job per account.
    """
    __tablename__ = "job_feedback"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    score_at_rating: Mapped[Optional[float]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("rating IN (-1, 1)", name="ck_feedback_rating"),
        UniqueConstraint("account_id", "job_id", name="uq_account_job_feedback"),
    )


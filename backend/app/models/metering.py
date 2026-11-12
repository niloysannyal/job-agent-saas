import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, JSON, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AccountSubscription(Base):
    """
    Tracks tenant subscription plan association and billing cycles.
    One active subscription per account enforced by partial unique index.
    """
    __tablename__ = "account_subscriptions"

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
    plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("subscription_plans.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    source: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("current_period_end > current_period_start", name="ck_sub_period_valid"),
        CheckConstraint(
            "status IN ('active', 'past_due', 'cancelled', 'expired')",
            name="ck_sub_status",
        ),
        Index("uq_account_active_sub", "account_id", unique=True, postgresql_where=(status == "active")),
    )


class AccountUsageCounter(Base):
    """
    Live aggregated balances per billing period. Updated transactionally with SELECT ... FOR UPDATE.
    Tokens and costs are integer micro-USD stored as BigInteger.
    """
    __tablename__ = "account_usage_counters"

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
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    applications_sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    applications_reserved_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    llm_tokens_used: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    llm_tokens_reserved: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_cost_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_cost_reserved_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    voice_seconds_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    voice_seconds_reserved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("period_end > period_start", name="ck_counter_period_valid"),
        UniqueConstraint("account_id", "period_start", name="uq_account_usage_period"),
    )


class QuotaReservation(Base):
    """
    Multi-dimensional atomic reservation lifecycle (reserved -> settled | released | expired).
    Sweeper uses index on (status, expires_at) to expire stale uncommitted holds.
    """
    __tablename__ = "quota_reservations"

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
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    quota_key: Mapped[str] = mapped_column(String(50), nullable=False)
    units: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    est_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    est_cost_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    voice_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="reserved", nullable=False)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("status IN ('reserved', 'settled', 'released', 'expired')", name="ck_quota_res_status"),
        Index("ix_quota_res_status_expires", "status", "expires_at"),
        Index("ix_res_account_key_active", "account_id", "quota_key", postgresql_where=(status == "reserved")),
    )


class UsageEvent(Base):
    """
    Append-only usage ledger. scope separates tenant usage from platform background tasks.
    account_id is SET NULL on account deletion, preserving platform revenue/cost ledger.
    """
    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    scope: Mapped[str] = mapped_column(String(20), default="tenant", nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), default="dispatch", nullable=False)
    provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pricing_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_estimated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    quota_key: Mapped[str] = mapped_column(String(50), nullable=False)
    units: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    cost_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="succeeded", nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    metadata_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("scope IN ('tenant', 'platform')", name="ck_usage_event_scope"),
        CheckConstraint("status IN ('succeeded', 'failed')", name="ck_usage_event_status"),
    )


class AccountQuotaOverride(Base):
    """
    Administrative overrides for quota limits. Precedence: Override > Plan > Entitlement.
    """
    __tablename__ = "account_quota_overrides"

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
    quota_key: Mapped[str] = mapped_column(String(50), nullable=False)
    override_limit: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("account_id", "quota_key", name="uq_account_quota_key"),
    )


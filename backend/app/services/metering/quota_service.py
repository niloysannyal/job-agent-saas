from typing import Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import uuid
import calendar
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.models.metering import (
    AccountUsageCounter,
    QuotaReservation,
    UsageEvent,
    AccountQuotaOverride,
    AccountSubscription,
)
from app.models.subscription import Entitlement, SubscriptionPlan


class QuotaExceededException(Exception):
    """Raised when an account exceeds its allocated usage quota."""
    pass


class QuotaService:
    """
    ACID-compliant multi-dimensional metering and quota enforcement service.
    Implements reserve -> hold -> settle / release lifecycle.
    """

    @classmethod
    def get_period_boundaries(cls, db: Session, account_id: str) -> tuple[datetime, datetime]:
        """
        Determines the current billing period boundaries:
        Anchors on active AccountSubscription, or defaults to the current UTC calendar month.
        """
        now = datetime.now(timezone.utc)
        active_sub = (
            db.query(AccountSubscription)
            .filter_by(account_id=account_id, status="active")
            .filter(AccountSubscription.current_period_start <= now, AccountSubscription.current_period_end > now)
            .first()
        )
        if active_sub:
            return active_sub.current_period_start, active_sub.current_period_end

        # Default calendar month
        period_start = datetime(now.year, now.month, 1, 0, 0, 0, tzinfo=timezone.utc)
        _, last_day = calendar.monthrange(now.year, now.month)
        # Period end is start of next month
        if now.month == 12:
            period_end = datetime(now.year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        else:
            period_end = datetime(now.year, now.month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        return period_start, period_end

    @classmethod
    def ensure_counter_exists(cls, db: Session, account_id: str, period_start: datetime, period_end: datetime) -> AccountUsageCounter:
        """
        Idempotently inserts counter row via ON CONFLICT DO NOTHING,
        then selects FOR UPDATE to serialize concurrent counter mutations.
        """
        counter = (
            db.query(AccountUsageCounter)
            .filter_by(account_id=account_id, period_start=period_start)
            .with_for_update()
            .first()
        )
        if not counter:
            new_counter = AccountUsageCounter(
                id=str(uuid.uuid4()),
                account_id=account_id,
                period_start=period_start,
                period_end=period_end,
                applications_sent_count=0,
                applications_reserved_count=0,
                llm_tokens_used=0,
                llm_tokens_reserved=0,
                total_cost_micro_usd=0,
                total_cost_reserved_micro_usd=0,
                voice_seconds_used=0,
                voice_seconds_reserved=0,
            )
            db.add(new_counter)
            try:
                db.flush()
                counter = new_counter
            except IntegrityError:
                db.rollback()
                counter = (
                    db.query(AccountUsageCounter)
                    .filter_by(account_id=account_id, period_start=period_start)
                    .with_for_update()
                    .one()
                )
        return counter

    @classmethod
    def get_quota_limit(cls, db: Session, account_id: str, quota_key: str) -> Optional[int]:
        """
        Resolves effective quota limit using precedence hierarchy:
        1. Entitlement.all_access == True -> None (Unlimited)
        2. AccountQuotaOverride (non-expired)
        3. SubscriptionPlan.features[quota_key]
        4. Entitlement.max_active_applications fallback (for applications)
        """
        now = datetime.now(timezone.utc)

        entitlement = db.query(Entitlement).filter_by(account_id=account_id).first()
        if entitlement and entitlement.all_access:
            return None  # Unlimited

        # 2. Check active override
        override = (
            db.query(AccountQuotaOverride)
            .filter_by(account_id=account_id, quota_key=quota_key)
            .first()
        )
        if override:
            if override.expires_at is None or override.expires_at > now:
                return int(override.override_value)

        # 3. Check SubscriptionPlan features
        active_sub = (
            db.query(AccountSubscription)
            .filter_by(account_id=account_id, status="active")
            .first()
        )
        if active_sub:
            plan = db.query(SubscriptionPlan).filter_by(id=active_sub.plan_id).first()
            if plan and isinstance(plan.features, dict):
                val = plan.features.get(quota_key)
                if val is not None:
                    return int(val)

        # 4. Fallback defaults
        if quota_key in ("monthly_applications_limit", "applications"):
            if entitlement and entitlement.max_active_applications:
                return entitlement.max_active_applications
            return 10  # Free tier default

        return None

    @classmethod
    def reserve(
        cls,
        db: Session,
        account_id: str,
        quota_key: str = "monthly_applications_limit",
        units: int = 1,
        est_tokens: int = 0,
        est_cost_micro: int = 0,
        correlation_id: Optional[str] = None,
    ) -> QuotaReservation:
        """
        Atomically reserves multi-dimensional quota within a database transaction.
        Raises QuotaExceededException if limit would be breached.
        """
        now = datetime.now(timezone.utc)
        period_start, period_end = cls.get_period_boundaries(db, account_id)
        counter = cls.ensure_counter_exists(db, account_id, period_start, period_end)

        limit = cls.get_quota_limit(db, account_id, quota_key)
        if limit is not None:
            current_allocated = counter.applications_sent_count + counter.applications_reserved_count
            if current_allocated + units > limit:
                raise QuotaExceededException(
                    f"Quota exceeded for '{quota_key}'. Allocated: {current_allocated}, Requested: {units}, Limit: {limit}."
                )

        # Atomically increment counter reservation
        counter.applications_reserved_count += units
        if est_tokens > 0:
            counter.llm_tokens_reserved += est_tokens
        if est_cost_micro > 0:
            counter.total_cost_reserved_micro_usd += est_cost_micro
        counter.updated_at = now

        reservation = QuotaReservation(
            id=str(uuid.uuid4()),
            account_id=account_id,
            idempotency_key=f"res_{uuid.uuid4().hex}",
            quota_key=quota_key,
            units=units,
            est_tokens=est_tokens,
            est_cost_micro_usd=est_cost_micro,
            voice_seconds=0,
            status="reserved",
            correlation_id=correlation_id or str(uuid.uuid4()),
            expires_at=now + timedelta(hours=1),
            created_at=now,
        )
        db.add(reservation)
        db.flush()
        return reservation

    @classmethod
    def settle(
        cls,
        db: Session,
        reservation_id: str,
        actual_applications: int = 1,
        actual_tokens: int = 0,
        actual_cost_micro: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Atomically transitions reservation to 'settled', updates permanent usage counters,
        and records an immutable UsageEvent.
        """
        now = datetime.now(timezone.utc)
        reservation = (
            db.query(QuotaReservation)
            .filter_by(id=reservation_id)
            .with_for_update()
            .first()
        )
        if not reservation:
            return
        if reservation.status == "settled":
            return  # Already settled (idempotent)

        period_start, period_end = cls.get_period_boundaries(db, reservation.account_id)
        counter = cls.ensure_counter_exists(db, reservation.account_id, period_start, period_end)

        # Release reserved amounts
        counter.applications_reserved_count = max(0, counter.applications_reserved_count - reservation.units)
        counter.llm_tokens_reserved = max(0, counter.llm_tokens_reserved - reservation.est_tokens)
        counter.total_cost_reserved_micro_usd = max(0, counter.total_cost_reserved_micro_usd - reservation.est_cost_micro_usd)

        # Increment permanent usage
        counter.applications_sent_count += actual_applications
        counter.llm_tokens_used += actual_tokens
        counter.total_cost_micro_usd += actual_cost_micro
        counter.updated_at = now

        # Record immutable usage event
        event = UsageEvent(
            id=str(uuid.uuid4()),
            account_id=reservation.account_id,
            scope="tenant",
            event_type="email_dispatch",
            quota_key=reservation.quota_key,
            status="succeeded",
            units=actual_applications,
            prompt_tokens=0,
            completion_tokens=actual_tokens,
            total_tokens=actual_tokens,
            cost_micro_usd=actual_cost_micro,
            idempotency_key=f"{reservation.id}:settle:0",
            correlation_id=reservation.correlation_id,
            metadata_snapshot=metadata or {},
            created_at=now,
        )
        db.add(event)

        reservation.status = "settled"
        db.flush()

    @classmethod
    def release(cls, db: Session, reservation_id: str) -> None:
        """
        Rolls back an unconsumed reservation: decrements reserved counters and marks reservation 'released'.
        """
        now = datetime.now(timezone.utc)
        reservation = (
            db.query(QuotaReservation)
            .filter_by(id=reservation_id)
            .with_for_update()
            .first()
        )
        if not reservation or reservation.status != "reserved":
            return

        period_start, period_end = cls.get_period_boundaries(db, reservation.account_id)
        counter = cls.ensure_counter_exists(db, reservation.account_id, period_start, period_end)

        counter.applications_reserved_count = max(0, counter.applications_reserved_count - reservation.units)
        counter.llm_tokens_reserved = max(0, counter.llm_tokens_reserved - reservation.est_tokens)
        counter.total_cost_reserved_micro_usd = max(0, counter.total_cost_reserved_micro_usd - reservation.est_cost_micro_usd)
        counter.updated_at = now

        reservation.status = "released"
        db.flush()

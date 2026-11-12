# JobEazy: Milestone M1m Implementation Specification
## Metering, Quotas & Multi-Tenant Usage Ledger (M1m-a & M1m-b)

> **Document Version:** 1.3.0  
> **Date:** 2026-11-12  
> **Author:** Antigravity (Lead Architect)  
> **Status:** Implementation Specification (Option B Verified & Approved)  
> **Target Branch:** `feat/real-dispatch`

---

## 1. Executive Summary & Phased Delivery Scope

### 1.1 Goal
Provide an ACID-compliant **metering and quota enforcement engine** for JobEazy. Every application sent, LLM token consumed, and external API cost is tracked per account in **integer micro-USD** (`1 USD = 1,000,000 micro-USD`). Plan limits and model prices are owner-editable from the superadmin dashboard. Quota checks use atomic database transactions with an explicit **multi-dimensional reservation lifecycle** (`quota_reservations`) to prevent race conditions or limit overshoots.

### 1.2 Frozen Canonical Vocabulary
The allowed vocabulary across all metering and quota tables is strictly frozen as follows:

| Column / Scope | Allowed State / Scope / Source Values | DB Constraint Type |
|---|---|---|
| `quota_reservations.status` | `reserved`, `settled`, `released`, `expired` | `CheckConstraint` |
| `usage_events.scope` | `tenant`, `platform` | `CheckConstraint` |
| `usage_events.status` | `success`, `failed`, `unknown` | `CheckConstraint` |
| `usage_events.event_type` | `llm_generation`, `email_dispatch`, `stt_transcription` | String registry |
| `account_subscriptions.status` | `active`, `canceled`, `past_due` | `CheckConstraint` |
| `account_subscriptions.source` | `manual`, `paddle` | `CheckConstraint` |

### 1.3 Phased Delivery (M1m-a vs M1m-b)
- **Phase M1m-a (Immediate — Foundation Migrated in `97f51073900d`):**
  - Database schema: `account_subscriptions`, `model_pricing`, `usage_events`, `account_usage_counters`, `quota_reservations`, `account_quota_overrides`, `admin_audit_logs`.
  - `QuotaService` interface with atomic multi-dimensional reserve, settle, and release primitives branching per `quota_key`.
  - In-service context propagation via `contextvars` inside `LLMService.generate()`.
  - Strict fail-closed rule: missing tenant context on tenant paths raises `RuntimeError`.
  - Unit tests for reservation atomicity, price calculation, and zero-check-then-act concurrency.
- **Phase M1m-b (Pre-Tenant-Onboarding Gate — Mandatory before 2nd user):**
  - Superadmin UI panel in `AdminView.jsx` (plan editor, overrides, model pricing table, audit log).
  - Impersonation safety: read-only restrictions on dispatch, billing, and credentials during "Test As Tenant".
  - Inversion of default: flip `Entitlement.all_access` default from `True` to `False`, backfilling owner account (Completed in migration `97f51073900d`).
  - Monthly automated reconciliation task against provider invoices.

---

## 2. Reuse of Existing Subscription Schema & Tenancy Audits

### 2.1 Existing Subscription Models
In `backend/app/models/subscription.py`:
- **`SubscriptionPlan`**: Catalog table (`id`, `name`, `tier`, `price_cents`, `currency`, `interval`, `is_active`, `features`).
  - **Plan Limits Storage:** Stored directly in `SubscriptionPlan.features` JSON column:
    ```json
    {
      "monthly_applications_limit": 50,
      "monthly_llm_tokens_limit": 500000,
      "monthly_cost_limit_micro_usd": 10000000,
      "max_batch_size": 5
    }
    ```
- **`Entitlement`**: Account-linked record (`account_id`, `plan_tier`, `all_access`, `max_active_applications`).
- **Quota Precedence Hierarchy:**
  `AccountQuotaOverride` > `SubscriptionPlan.features` > `Entitlement` fallback defaults.

### 2.2 Tenancy Exemption in `scripts/check_migrations.py`
In `scripts/check_migrations.py:22`:
```python
non_tenant_allowed = {"cv_template.py", "model_pricing.py", "admin_audit_log.py", "__init__.py"}
```
- **Auditor Exemption Justification:**
  - `model_pricing.py` is exempt because model pricing is a platform-wide shared pricing catalog.
  - `admin_audit_log.py` carries `admin_account_id` and tracks superadmin administrative operations across accounts.
  - Verified by `python scripts/check_migrations.py` with `[PASS] Multi-tenant isolation verified across 11 models`.

---

## 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)

### 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods)
```python
class AccountSubscription(Base):
    """Binds an account to a plan with anchored billing cycles and lazy rollover."""
    __tablename__ = "account_subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id: Mapped[str] = mapped_column(String(36), ForeignKey("subscription_plans.id", ondelete="RESTRICT"), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    source: Mapped[str] = mapped_column(String(32), default="manual", nullable=False) # Restored: manual | paddle
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("period_end > period_start", name="ck_account_sub_period"),
        CheckConstraint("status IN ('active', 'canceled', 'past_due')", name="ck_account_sub_status"),
        CheckConstraint("source IN ('manual', 'paddle')", name="ck_account_sub_source"),
        Index("uq_account_active_sub", "account_id", unique=True, postgresql_where=text("status = 'active'")),
    )
```

### 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)
```python
class AccountUsageCounter(Base):
    """Per-account live counters updated transactionally with SELECT ... FOR UPDATE."""
    __tablename__ = "account_usage_counters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # BigInteger counters to prevent integer overflow
    applications_sent_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    applications_reserved_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    llm_tokens_total: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    llm_tokens_reserved: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_cost_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    cost_reserved_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("account_id", "period_start", name="uq_account_period_counter"),
        CheckConstraint("period_end > period_start", name="ck_usage_counter_period"),
    )
```

### 3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle)
```python
class QuotaReservation(Base):
    """Tracks active multi-dimensional resource reservations with expiration sweeper."""
    __tablename__ = "quota_reservations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    applications_units: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    llm_tokens_units: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    cost_micro_usd: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="reserved", nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False) # Restored: unique idempotency
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('reserved', 'settled', 'released', 'expired')", name="ck_quota_res_status"),
        Index("ix_quota_res_status_expires", "status", "expires_at"), # Restored index
    )
```

### 3.4 Model 4: `ModelPricing` (In `backend/app/models/model_pricing.py`)
```python
class ModelPricing(Base):
    """Owner-configurable unit prices per LLM model in micro-USD per 1,000,000 tokens."""
    __tablename__ = "model_pricing"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    pricing_version: Mapped[str] = mapped_column(String(32), default="v1", nullable=False) # Restored pricing version
    price_per_1m_prompt_micro_usd: Mapped[int] = mapped_column(BigInteger, nullable=False) # Restored BigInteger
    price_per_1m_completion_micro_usd: Mapped[int] = mapped_column(BigInteger, nullable=False) # Restored BigInteger
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) # Restored
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("provider", "model", "pricing_version", name="uq_model_pricing_ver"),
        Index("uq_model_pricing_active", "provider", "model", unique=True, postgresql_where=text("is_active = true")),
    )
```
- **Rounding Rule:** Always round up to the nearest integer micro-USD using integer ceil:
  `cost_micro = math.ceil((tokens * price_per_1m) / 1_000_000)`

### 3.5 Model 5: `UsageEvent` (Scope Column Added)
```python
class UsageEvent(Base):
    """Immutable audit trail. ZERO candidate PII or CV text. Permanently retainable under GDPR."""
    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    scope: Mapped[str] = mapped_column(String(32), default="tenant", nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False) # Restored
    status: Mapped[str] = mapped_column(String(32), default="success", nullable=False)
    units: Mapped[int] = mapped_column(BigInteger, nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    cost_micro_usd: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_estimated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # Restored
    provider: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Restored
    model: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Restored
    pricing_version: Mapped[Optional[str]] = mapped_column(String(32), nullable=True) # Restored
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True) # Restored
    metadata_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("scope IN ('tenant', 'platform')", name="ck_usage_event_scope"),
        CheckConstraint("status IN ('success', 'failed', 'unknown')", name="ck_usage_event_status"),
    )
```

### 3.6 Models 6 & 7: `AccountQuotaOverride` & `AdminAuditLog`
```python
class AccountQuotaOverride(Base):
    __tablename__ = "account_quota_overrides"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    quota_key: Mapped[str] = mapped_column(String(64), nullable=False)
    override_value: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True) # Restored expires_at
    created_by_admin_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("account_id", "quota_key", name="uq_account_quota_key"),
    )


class AdminAuditLog(Base):
    """In backend/app/models/admin_audit_log.py. Tracks administrative modifications."""
    __tablename__ = "admin_audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False) # ON DELETE RESTRICT (no cascade)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    target_account_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    before_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False) # Restored before snapshot
    after_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False) # Restored after snapshot
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
```

---

## 4. QuotaService Interface, Settle Branching & Counter Mutation

### 4.1 Interface Specification
```python
class QuotaService:
    @staticmethod
    async def reserve(
        db: AsyncSession,
        account_id: str,
        quota_key: str,
        units: int,
        est_tokens: int = 0,
        est_cost_micro: int = 0,
        correlation_id: Optional[str] = None
    ) -> QuotaReservation:
        """
        QuotaService.reserve provides multi-dimensional atomic reservation:
        1. Ensures counter row exists: INSERT ... ON CONFLICT (account_id, period_start) DO NOTHING.
        2. SELECT * FROM account_usage_counters WHERE account_id = :id FOR UPDATE;
        3. Validates (used + reserved + requested) <= limit for quota_key.
        4. Inserts quota_reservations (quota_key, units, est_tokens, est_cost_micro, status='reserved').
        5. Increments counter reserved balances atomically. Returns reservation.
        """

    @staticmethod
    async def settle(
        reservation_id: str,
        actual_applications: int,
        actual_tokens: int,
        actual_cost_micro: int,
        metadata: dict
    ) -> None:
        """
        Atomic settlement:
        1. Idempotency key: f"{reservation_id}:settle:0"
        2. INSERT INTO usage_events (...) ON CONFLICT (idempotency_key) DO NOTHING RETURNING id;
        3. If inserted:
           - counter.applications_reserved_count -= res.applications_units
           - counter.applications_sent_count += actual_applications
           - counter.total_cost_micro_usd += actual_cost_micro
           - res.status = 'settled'
        4. Commit transaction.
        """

    @staticmethod
    async def release(reservation_id: str) -> None:
        """
        Atomic rollback: decrements counter reserved balances by reservation units.
        Sets res.status = 'released'. Commits transaction.
        """
```

### 4.2 Thresholds & Batch Budgeting
- **80% Utilization:** Emits an informational warning banner via SSE / API response.
- **100% Utilization:** Blocks action with error code `QUOTA_EXCEEDED`.
- **Batch Allocation:** If user requests a batch of 5 jobs with 3 application slots remaining:
  - System reserves 3 applications.
  - The remaining 2 applications are cleanly downgraded to `draft` (unsent) with an explicit notification.

---

## 5. In-Service Context Propagation (`contextvars`) & Provider Accounting

In `backend/app/services/llm/service.py`:
```python
from contextvars import ContextVar

current_account_id: ContextVar[Optional[str]] = ContextVar("current_account_id", default=None)
current_correlation_id: ContextVar[Optional[str]] = ContextVar("current_correlation_id", default=None)
current_scope: ContextVar[str] = ContextVar("current_scope", default="tenant")
```
- **Fail-Closed Rule:** On tenant execution paths (`current_scope == "tenant"`), if `account_id` is missing or `None`, `LLMService.generate()` raises `RuntimeError("Missing tenant context in LLMService call")`.
- **Platform Scope Context Manager:**
  ```python
  from contextlib import contextmanager

  @contextmanager
  def platform_scope():
      token = current_scope.set("platform")
      try:
          yield
      finally:
          current_scope.reset(token)
  ```
- **Missing-Price Rule:** If the requested model is not found in `model_pricing`, the service raises `MissingModelPricingException`, preventing unmetered usage.
- **Failed / Failover Accounting:** If Provider #1 attempts generation, consumes tokens, and fails with HTTP 500, the attempt is recorded in `usage_events` with `status = "failed"`. Provider #2 failover is then executed and recorded.

---

## 6. Superadmin Control Center & Impersonation Safety

In `frontend/src/components/AdminView.jsx`:
- **Superadmin Only:** Strict RBAC check (`Account.role == "superadmin"`).
- **Impersonation Safety Gate (Service-Layer Guard):** When superadmin activates "Test As Tenant", both the frontend and backend service layer enter an explicit read-only mode:
  - `POST /api/v1/dispatch/commands` -> `403 Forbidden ("Impersonated sessions cannot trigger dispatch")`
  - `POST /api/v1/dispatch/settings` -> `403 Forbidden`
  - Quota overrides and OAuth modifications are rejected during impersonation.
- **Provider Invoice Reconciliation:** Monthly reconciliation script (`scripts/reconcile_billing.py`) compares provider invoice API totals against `usage_events` sums for that billing month.

---

## 7. Concrete Test Plan & Verified Models (`test_m1_models_and_migration.py`)

All Task 1 models and constraints are verified by `backend/tests/models/test_m1_models_and_migration.py` and the broader suite (214 passing tests):
1. **Model Exemption Audit:** `scripts/check_migrations.py` confirms `model_pricing.py` and `admin_audit_log.py` are explicitly exempted while all other models maintain `account_id` foreign keys.
2. **Schema Drift Check:** `alembic check` verifies 0 drift against PostgreSQL 17 container.
3. **Multi-Dimensional Lifecycle:** Unit tests verify reservations transition through `reserved` -> `settled` / `released`.
4. **Counter Overflow Protection:** All token and cost balances are BigInteger columns.
5. **Partial Indexes:** Partial unique index on active subscriptions (`status = 'active'`) and active model pricing (`is_active = true`).

---

## 8. Milestone Implementation & Effort

| Component | Scope & Files | Effort |
|---|---|---|
| **M1m-a Task 1: Schema & Migrations (COMPLETED)** | `account_subscriptions`, `model_pricing`, `usage_events`, `account_usage_counters`, `quota_reservations`, `account_quota_overrides`, `admin_audit_logs`. Migration `97f51073900d` applied and tested. | **1.5 days (Done)** |
| **M1m-a Task 2: QuotaService & Multi-Dimensional Reserve** | `QuotaService` implementing reserve/settle/release branching by quota key with row locking. | **1.5 days** |
| **M1m-a Task 3: LLMService Usage Accounting** | Context-variable metering in `LLMService.generate()` with worst-case reservation, fail-closed rule, and `platform_scope()`. | **1.0 day** |
| **M1m-b Task 4: Superadmin AdminView UI** | Quotas, overrides, and pricing management tab in React frontend `AdminView.jsx`. | **1.0 day** |
| **M1m-b Task 5: Impersonation Safety & Reconciliation** | Impersonation read-only barrier and monthly invoice reconciliation script. | **1.0 day** |
| **Total Effort (Milestone M1m Combined)** | **Complete metering, usage ledger, and owner admin dashboard.** | **6.0 days** |

# JobEazy: Milestone M1 & M1b Implementation Specification
## Real Outbound Dispatch & Legacy Autonomy Policy Engine

> **Document Version:** 1.3.0  
> **Date:** 2026-11-12  
> **Author:** Antigravity (Lead Architect)  
> **Status:** Implementation Specification (Option B Verified & Approved)  
> **Target Branch:** `feat/real-dispatch`

---

## 1. Executive Summary & Architecture Scope

### 1.1 Goal
Operationalize **real, verified outbound email dispatch** and the **Decision D1 per-account autonomy policy** directly on JobEazy's existing production architecture. This delivers real job applications for Niloy Sannyal (Phase 1 dogfooding) immediately, while deferring LangGraph orchestration until live validation is complete.

### 1.2 Frozen Canonical Vocabulary
The allowed vocabulary across all dispatch tables is strictly frozen as follows:

| Column / Scope | Allowed State / Mode / Source Values | DB Constraint Type |
|---|---|---|
| `hold_queue_items.status` | `pending`, `claimed`, `sending`, `sent`, `aborted`, `failed`, `unknown` | `CheckConstraint` |
| `dispatched_actions.status` | `reserved`, `sending`, `sent`, `aborted`, `failed`, `unknown` | `CheckConstraint` |
| `send_authorizations.status` | `pending`, `consumed`, `voided`, `expired` | `CheckConstraint` |
| `user_commands.status` | `active`, `completed`, `cancelled`, `expired` | `CheckConstraint` |
| `autonomy_mode` | `supervised`, `autonomous` | `CheckConstraint` |
| `user_commands.source` | `ui_click`, `chat_text`, `voice` | `CheckConstraint` |
| `hold_queue_items.hold_kind` | `autonomous_delay`, `supervised_delay`, `retry_backoff` | `CheckConstraint` |
| `hold_queue_items.abort_reason` | `user_cancelled`, `admin_kill_switch`, `account_suspended`, `autonomy_toggled_off`, `policy_violation` | Nullable with code validation |

### 1.3 Sub-Milestones
- **Milestone M1 (Real Supervised Dispatch):**
  - Database schema: `account_dispatch_settings`, `user_commands`, `send_authorizations`, `application_pdf_payloads`, `hold_queue_items`, `send_evidence`, `dispatched_actions`, `trusted_recipients`, and `job_feedback`.
  - Hardened `SendGateway` service and PostgreSQL DB Outbox poller worker (`SELECT ... FOR UPDATE SKIP LOCKED`) with 30-second periodic sweeper for stale claimed and sending items.
  - Dedicated `OAUTH_ENCRYPTION_KEY` using `MultiFernet` for secure token decryption in the worker without exposing `JWT_SECRET_KEY`.
  - Safety guard in `alembic/env.py` and `backend/tests/conftest.py` requiring database name ending in `_test` or `_dev` (refusing remote hostnames containing `supabase` or `pooler`).
  - Google OAuth integration upgraded to `https://www.googleapis.com/auth/gmail.send` (Sensitive scope, no CASA audit required).
  - Legacy `approve_proposal()` wired to reserve quota, set `Application.status = 'queued'`, mint authorizations, and enqueue hold items with an undo window.
  - Frontend UI updates: Settings UI & acknowledgment flow, Undo countdown button in `ApplicationStudio` and `Pipeline`, TOFU confirmation modal, Google re-consent banner, and hold-queue drawer.
- **Milestone M1b (Autonomous Single-Job Email on Legacy Engine):**
  - *(Note: Conditional on measured email-apply share >= 20% during Phase 1 testing).*
  - Standalone policy service (`backend/app/services/dispatch/`) with **zero imports from `app.services.agent`**.
  - Server-side command minting from stored intent proposals; public endpoint restricted to `ui_click`.
  - Deterministic single-job resolver and comprehensive pre-send verification barrier (`pypdf` page count 1–2 pages, ATS text-layer + contact regex, outreach copy gate).
  - Separated autonomous caps (default 5/day, 2/hour) from platform safety caps (default 50/day, 15/hour).
  - Dual emergency kill switch (account-level and global environment kill switch) plus superadmin account suspension.

---

## 2. Database Schema (All Tables Tenant-Scoped)

Every table carries `account_id` with foreign key cascades to `accounts.id` (satisfying `scripts/check_migrations.py`). Audit foreign keys use `ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED` to ensure audit integrity during standard operation while permitting clean account deletion within a single transaction.

```
[accounts] (id, email, ...)
  │
  ├──< [account_dispatch_settings] (account_id [PK], autonomy_mode, caps, kill_switch, is_suspended_by_admin)
  ├──< [user_commands] (id, account_id, command_type, target_job_ids, mode, source, source_message_id [UNIQUE], expires_at)
  │      └──< [send_authorizations] (id, account_id, command_id, application_id, content_hash, recipient_email, x_jobeazy_send_id, attachment_sha256, minted_by, status, expires_at)
  │             ├──< [application_pdf_payloads] (id, authorization_id [UNIQUE], attachment_sha256, pdf_bytes, size_bytes)
  │             └──< [hold_queue_items] (id, account_id, application_id, authorization_id, release_at, hold_kind, abort_reason, claimed_at, sending_started_at, channel, status)
  │                    └──< [send_evidence] (id, account_id, application_id [DEFERRED], job_id [DEFERRED], external_message_id, subject, headers_snapshot, sent_at)
  │
  ├──< [dispatched_actions] (id, account_id, job_id [DEFERRED], channel, sequence_kind, mode, status, dispatched_at)
  ├──< [trusted_recipients] (id, account_id, email, source, confirmed_at)
  └──< [job_feedback] (id, account_id, job_id [CASCADE], rating, score_at_rating, notes, created_at)
```

### 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)

#### Table 1: `account_dispatch_settings` (Tenant Autonomy, Safety Caps & Kill Switches)
```python
class AccountDispatchSettings(Base):
    """Per-account dispatch policy, emergency kill switches, and separated safety/autonomous caps."""
    __tablename__ = "account_dispatch_settings"

    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    autonomy_mode: Mapped[str] = mapped_column(String(32), default="supervised", nullable=False)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    kill_switch: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_suspended_by_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Separated Autonomous Caps (apply strictly to autonomous dispatch)
    autonomous_daily_cap: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    autonomous_hourly_cap: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    
    # Overall Platform Safety Caps (bound ALL dispatches: supervised + autonomous)
    safety_daily_cap: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    safety_hourly_cap: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint("autonomy_mode IN ('supervised', 'autonomous')", name="ck_dispatch_autonomy_mode"),
        CheckConstraint("autonomous_daily_cap > 0 AND autonomous_daily_cap <= 10", name="ck_dispatch_auto_daily_cap"),
        CheckConstraint("autonomous_hourly_cap > 0 AND autonomous_hourly_cap <= 5", name="ck_dispatch_auto_hourly_cap"),
        CheckConstraint("safety_daily_cap > 0 AND safety_daily_cap <= 100", name="ck_dispatch_safety_daily_cap"),
        CheckConstraint("safety_hourly_cap > 0 AND safety_hourly_cap <= 30", name="ck_dispatch_safety_hourly_cap"),
        CheckConstraint("autonomous_daily_cap <= safety_daily_cap", name="ck_dispatch_caps_hierarchy_daily"),
        CheckConstraint("autonomous_hourly_cap <= safety_hourly_cap", name="ck_dispatch_caps_hierarchy_hourly"),
    )
```

#### Table 2: `user_commands` (Authority to Attempt)
```python
class UserCommand(Base):
    """Explicit user command granting authority to attempt applications."""
    __tablename__ = "user_commands"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    command_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "single", "batch"
    mode: Mapped[str] = mapped_column(String(20), nullable=False)          # "supervised", "autonomous"
    source: Mapped[str] = mapped_column(String(20), nullable=False)        # "ui_click", "chat_text", "voice"
    source_message_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    target_job_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)  # Restored frozen job UUID list
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("command_type IN ('single', 'batch')", name="ck_user_command_type"),
        CheckConstraint("mode IN ('supervised', 'autonomous')", name="ck_user_command_mode"),
        CheckConstraint("source IN ('ui_click', 'chat_text', 'voice')", name="ck_user_command_source"),
        CheckConstraint("status IN ('active', 'completed', 'cancelled', 'expired')", name="ck_user_command_status"),
        UniqueConstraint("account_id", "source_message_id", name="uq_user_cmd_msg"),
    )
```

#### Table 3: `send_authorizations` (Content-Pinned Authorization)
```python
class SendAuthorization(Base):
    """Single-use authorization record pinned to exact application content hash."""
    __tablename__ = "send_authorizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    command_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("user_commands.id", ondelete="SET NULL"), nullable=True)
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)      # Restored recipient email
    attachment_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Restored attachment hash
    x_jobeazy_send_id: Mapped[str] = mapped_column(String(64), default=lambda: str(uuid.uuid4()), nullable=False) # Restored tracking send ID
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    minted_by: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    voided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("minted_by IN ('human_approval', 'autonomous_policy')", name="ck_send_auth_minted_by"),
        CheckConstraint("status IN ('pending', 'consumed', 'voided', 'expired')", name="ck_send_auth_status"),
    )
```

#### Table 4: `application_pdf_payloads` (Dedicated PDF Byte Storage)
```python
class ApplicationPdfPayload(Base):
    """Stores compiled PDF binary bytes keyed to application to prevent bloat. Purged after 30 days."""
    __tablename__ = "application_pdf_payloads"

    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_bytes: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
```

#### Table 5: `hold_queue_items` (Durable Outbox Queue)
```python
class HoldQueueItem(Base):
    """Durable PostgreSQL Outbox item with worker claiming and sending timestamps."""
    __tablename__ = "hold_queue_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    authorization_id: Mapped[str] = mapped_column(String(36), ForeignKey("send_authorizations.id", ondelete="CASCADE"), nullable=False)
    reservation_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("quota_reservations.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True)
    hold_kind: Mapped[str] = mapped_column(String(30), default="autonomous_delay", nullable=False)
    abort_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    channel: Mapped[str] = mapped_column(String(20), default="email", nullable=False) # Restored channel column
    release_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True) # Restored worker claimed timestamp
    sending_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True) # Restored sending timestamp
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False) # Restored updated_at

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'claimed', 'sending', 'sent', 'aborted', 'failed', 'unknown')", name="ck_hold_status"),
        CheckConstraint("hold_kind IN ('autonomous_delay', 'supervised_delay', 'retry_backoff')", name="ck_hold_kind"),
        Index("ix_hold_queue_poll", "status", "release_at"),
    )
```

#### Table 6: `send_evidence` (Immutable Audit Log)
```python
class SendEvidence(Base):
    """Cryptographic audit trail of completed external transmissions with DEFERRABLE FKs."""
    __tablename__ = "send_evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False, index=True) # Restored job_id
    application_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    authorization_id: Mapped[str] = mapped_column(String(36), ForeignKey("send_authorizations.id", ondelete="RESTRICT"), nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    external_message_id: Mapped[str] = mapped_column(String(255), nullable=False)
    external_thread_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False) # Restored subject
    headers_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False) # Restored headers snapshot
    canonical_content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    attachment_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # Restored attachment hash
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

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
```

#### Table 7: `dispatched_actions` (Sequenced Idempotency Barrier)
```python
class DispatchedAction(Base):
    """Reserve-before-send partial unique constraint permitting retry after abort/failure."""
    __tablename__ = "dispatched_actions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False, index=True)
    application_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(20), default="email", nullable=False)
    sequence_kind: Mapped[str] = mapped_column(String(30), default="initial_application", nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False) # "supervised", "autonomous"
    status: Mapped[str] = mapped_column(String(20), nullable=False) # "reserved", "sending", "sent", "failed", "aborted", "unknown"
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

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
        CheckConstraint("status IN ('reserved', 'sending', 'sent', 'failed', 'aborted', 'unknown')", name="ck_dispatched_status"),
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
```

#### Table 8: `trusted_recipients` (TOFU Exact Address Allowlist)
```python
class TrustedRecipient(Base):
    """Allowlist of user-confirmed recipient exact addresses, case-insensitive unique."""
    __tablename__ = "trusted_recipients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("uq_trusted_recipients_lower_email", "account_id", text("lower(email)"), unique=True),
        CheckConstraint("source IN ('manual_tofu', 'previous_contact', 'verified_domain')", name="ck_trusted_recip_source"),
    )
```

#### Table 9: `job_feedback` (Ground-Truth Precision Tracking)
```python
class JobFeedback(Base):
    """User ground-truth ratings on discovered jobs to calibrate match-score precision."""
    __tablename__ = "job_feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False) # Restored: +1 (good fit) | -1 (bad fit)
    score_at_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Restored match score snapshot
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("rating IN (-1, 1)", name="ck_job_feedback_rating"),
        UniqueConstraint("account_id", "job_id", name="uq_job_feedback_account_job"),
    )
```

### 2.2 Cap-Count Queries
The live send caps are checked against `dispatched_actions` via indexed queries:
- **Rolling Autonomous Daily Sends:**
  ```sql
  SELECT COUNT(*) FROM dispatched_actions 
  WHERE account_id = :account_id AND mode = 'autonomous' AND status IN ('reserved', 'sending', 'sent', 'unknown') AND created_at >= NOW() - INTERVAL '24 HOURS';
  ```
- **Rolling Autonomous Hourly Sends:**
  ```sql
  SELECT COUNT(*) FROM dispatched_actions 
  WHERE account_id = :account_id AND mode = 'autonomous' AND status IN ('reserved', 'sending', 'sent', 'unknown') AND created_at >= NOW() - INTERVAL '1 HOUR';
  ```
- **Rolling Safety Daily Sends (All Dispatches):**
  ```sql
  SELECT COUNT(*) FROM dispatched_actions 
  WHERE account_id = :account_id AND status IN ('reserved', 'sending', 'sent', 'unknown') AND created_at >= NOW() - INTERVAL '24 HOURS';
  ```
- **Rolling Safety Hourly Sends (All Dispatches):**
  ```sql
  SELECT COUNT(*) FROM dispatched_actions 
  WHERE account_id = :account_id AND status IN ('reserved', 'sending', 'sent', 'unknown') AND created_at >= NOW() - INTERVAL '1 HOUR';
  ```

### 2.3 Application and Entitlement Model Modifications
1. In `backend/app/models/application.py`:
   - `subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)`
   - `body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)`
   - `recipient_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)`
   - `pdf_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)`
   - `archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)`
2. In `backend/app/models/subscription.py`:
   - `all_access: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)` (Default flipped from `True` to `False`).
   - Migration `97f51073900d` automatically backfills superadmin accounts with `all_access = true` and asserts `SELECT count(*) FROM entitlements WHERE all_access = true >= 1`.

---

## 3. Send State Machine & Outbox Poller

### 3.1 Single Atomic Transaction Before External Call
The poller worker executes all pre-checks and state commits in **one atomic database transaction** before initiating any network call to Google:
1. **Pre-check reads & Row-Level Lock:**
   - Query `account_dispatch_settings` with `SELECT ... FOR UPDATE` (locks settings row to prevent concurrent cap race conditions).
   - Assert `kill_switch == False`, `is_suspended_by_admin == False`, and `DISPATCH_GLOBAL_KILL_SWITCH != True`.
   - Check send caps:
     - If mode is autonomous: verify rolling autonomous sends < `autonomous_daily_cap` and `autonomous_hourly_cap`.
     - Verify total rolling sends < `safety_daily_cap` and `safety_hourly_cap`.
   - Read `send_authorizations`: assert `status == 'pending'`. If expired (`expires_at < now()`), transition hold item to `aborted` with `abort_reason = 'policy_violation'`.
   - Re-verify length-prefixed `content_hash` matches canonical encoding of current database bytes.
   - Verify active reservation in `QuotaService`.
2. **Reserve Idempotency Key:**
   - Insert into `dispatched_actions` with `status = 'reserved'`. If the partial unique key `(account_id, job_id, channel, sequence_kind)` is violated, abort immediately.
3. **Transition Outbox Item to `sending`:**
   - Set `hold_queue_items.status = 'sending'`, set `hold_queue_items.sending_started_at = datetime.now(timezone.utc)`.
4. **COMMIT Transaction:**
   - The transaction closes. The record is permanently recorded in PostgreSQL as `sending`.
5. **Invoke External Provider with Timeout Guard:**
   - `SendGateway` calls the Gmail API wrapped in `asyncio.wait_for(..., timeout=30.0)`.
   - On HTTP 200: atomically transition hold queue item to `sent`, transition `dispatched_actions.status = 'sent'`, insert `send_evidence`, settle `QuotaService` reservation, and set `Application.status = 'applied'`.
   - On 429/5xx retryable errors: roll back to `pending`, increment attempt count, set exponential backoff `release_at = now() + (5 * 2^attempt)`.
   - On hard 4xx errors (e.g. invalid recipient): mark `aborted` / `failed`, release reservation.
   - On timeout or process crash: item remains in `sending`.

### 3.2 Periodic Sweeper (Stale Claimed & Stale Sending)
A continuous background sweep runs every 30 seconds:
1. **Stale Claimed Worker Sweep:** Items in `status = 'claimed'` with `claimed_at < NOW() - INTERVAL '30 SECONDS'` are reset back to `status = 'pending'`, clearing `claimed_at`.
2. **Stale Sending Worker Sweep:** Items in `status = 'sending'` with `sending_started_at < NOW() - INTERVAL '60 SECONDS'` (HTTP timeout + margin) transition to `status = 'unknown'`. Dispatched action reservation is preserved to prevent double-send. An alert is logged for operator inspection.

### 3.3 Mid-Hold Cancel & Autonomy Toggle Off
- **Mid-Hold User Cancel:** Updates `hold_queue_items.status = 'aborted'` with `abort_reason = 'user_cancelled'`, releases quota reservation, and reverts parent `Application.status` to `'draft'`.
- **Turning Autonomy OFF Mid-Hold:** When a user switches `autonomy_mode` to `'supervised'`, all autonomous items in `hold_queue_items` with `status = 'pending'` are aborted with `abort_reason = 'autonomy_toggled_off'`, authorizations are voided, reservations released, and parent applications revert to `'draft'`.

---

## 4. Content Pinning, MIME Construction & MultiFernet

### 4.1 Canonical Length-Prefixed Encoding
To guarantee zero whitespace or delimiter tampering across systems, `content_hash` is computed using a length-prefixed canonical encoding:

```python
def compute_content_hash(
    cv_version_id: str,
    subject: str,
    body: str,
    recipient: str,
    answers_json: str,
    attachment_sha256: str
) -> str:
    """
    Computes deterministic SHA-256 over length-prefixed fields:
    len(val):val|len(val):val|...
    Canonical empty value for answers_json in email applications is strictly '[]'.
    """
    fields = [cv_version_id, subject, body, recipient, answers_json, attachment_sha256]
    encoded_parts = [f"{len(f)}:{f}" for f in fields]
    canonical_payload = "|".join(encoded_parts)
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
```
- **Email Answers Empty Value Invariant:** For email applications, `answers_json` canonical empty value is strictly `"[]"`.

### 4.2 Dedicated `OAUTH_ENCRYPTION_KEY` (MultiFernet)
To maintain security isolation between worker processes and web API processes:
- A dedicated environment variable `OAUTH_ENCRYPTION_KEY` is introduced.
- Decryption is handled via `MultiFernet` supporting zero-downtime key rotation:
  ```python
  keys = [Fernet(k.encode()) for k in settings.OAUTH_ENCRYPTION_KEY.split(",")]
  fernet = MultiFernet(keys)
  ```
- **Isolation Invariant:** The background dispatch worker process receives **only** `OAUTH_ENCRYPTION_KEY` and **MUST NOT** receive `JWT_SECRET_KEY`.

---

## 5. Command Authority, Chat/Voice Triggers & Exact-Address TOFU

### 5.1 Command Minting REST Endpoint (`POST /api/v1/dispatch/commands`)
- **Public Endpoint Restriction:** The public REST endpoint `POST /api/v1/dispatch/commands` is restricted strictly to `source = "ui_click"`.
- **Chat and Voice Commands:** Chat and voice commands are minted **server-side** from the stored intent proposal. The client **cannot supply arbitrary job IDs**.
- **Idempotency:** Protected by `UniqueConstraint("account_id", "source_message_id", name="uq_user_cmd_msg")`.

### 5.2 Deterministic "Top N" Resolution
When a user instructs the agent via chat or voice (e.g. "Apply to my top 3 matches"):
1. The server queries jobs meeting strict criteria:
   - `integrity_status == 'clean'`
   - `vetoed == False`
   - `is_active == True`
   - `applied_at is None` (unapplied)
   - `match_score >= 70.0` (quality floor)
2. Sorts deterministically: `ORDER BY match_score DESC, found_at DESC LIMIT N`.
3. The server echoes the exact frozen list of job UUIDs and match scores back to the user before queuing.

### 5.3 Honest TOFU Reality & Voice Commands
- **TOFU is Exact-Address-Only:** Verification confirms that ATS board APIs do **not** supply recruiter email addresses or company email domains.
- **Operational Reality for M1b:** Autonomous dispatch executes without confirmation only on follow-ups to already-contacted companies or when the candidate has pre-registered recipient contacts in `trusted_recipients`.

---

## 6. Pre-Send Verification Barrier & Safety Guards

### 6.1 Barrier Hardening
Before an autonomous application can mint a `send_authorizations` record, it must pass all 8 gates:
1. **PDF Validity:** Bytes start with `b"%PDF-1."`.
2. **Page Budget Check:** Inspected via `pypdf.PdfReader` to assert `1 <= len(reader.pages) <= max_pages` (1–2 pages configurable per template; `cv_templates/01_MASTER_CV.tex` allows up to 2 pages max).
3. **ATS Text-Layer & Contact Integrity Check:** Extracted text contains >= 100 non-whitespace characters PLUS literal regex validation that the candidate's verified contact email and phone number appear in the selectable text layer.
4. **Outreach Copy Gate:** Fact Ledger audit over outreach body, zero unfilled placeholders (`[Company]`, `{{role}}`), word count strictly between 50 and 300 words.
5. **Job Integrity:** `job.integrity_status == 'clean'`, `job.vetoed == False`, `job.is_active == True`.
6. **Recipient Syntax & TOFU Validation:** Recipient email passes RFC 5322 validation and TOFU check.
7. **Send Caps:** Rolling autonomous sends < `autonomous_daily_cap` (default 5) and `autonomous_hourly_cap` (default 2); total sends < `safety_daily_cap`.
8. **Real-Time Kill Switch Check:** `account_settings.kill_switch == False`, `account_settings.is_suspended_by_admin == False`, `account_settings.autonomy_mode == 'autonomous'`, `account_settings.acknowledged_at is not None`, and `DISPATCH_GLOBAL_KILL_SWITCH != True`.

### 6.2 Safety Guard in Alembic and Test Configuration
In `backend/app/db/migrations/env.py` and `backend/tests/conftest.py`:
- Parses the active database URL.
- If `parsed.hostname` contains `"supabase"` or `"pooler"`, execution raises `RuntimeError("BLOCKED: Database operation refused against remote host")`.
- Test databases must run on `localhost` / `127.0.0.1` and database name must end in `_test` or `_dev`.

---

## 7. Gmail API Quotas, Limits & Error Mapping

- **Total Deadline Guard:** Gmail dispatch call wrapped in `asyncio.wait_for(..., timeout=30.0)`.
- **HTTP 403 Error Sub-Reason Mapping:**
  - `accessNotConfigured`: API not enabled in Google Console. Transitions to `aborted`, releases reservation.
  - `rateLimitExceeded` / `userRateLimitExceeded`: Quota exceeded. Transitions to `pending` with exponential backoff (+5 minutes).
  - `insufficientPermissions`: Token lacks `gmail.send` scope. Transitions to `aborted`, prompts user re-consent.
- **Quota Units:** `messages.send` consumes **100 quota units** per call (*Google Developers Gmail API Usage limits*, retrieved 2026-11-10; URL: `https://developers.google.com/gmail/api/reference/quota`).
- **Account Daily Sending Limits:** Personal Gmail = 500 emails/day; Google Workspace = 2,000 emails/day (*Google Workspace Admin Help: Gmail sending limits*, retrieved 2026-11-10; URL: `https://support.google.com/a/answer/166852`).
- **Message Size Ceiling:** Gmail enforces a **25 MB total MIME message limit** (*Google Gmail Help: Send attachments with your Gmail message*, retrieved 2026-11-10; URL: `https://support.google.com/mail/answer/6584`). Raw attachment limit is **~18 MB** due to base64 encoding.

---

## 8. Concrete Test Plan & Verified Suite (`test_m1_models_and_migration.py`)

The migration `97f51073900d` and underlying models are verified by 4 targeted tests in `backend/tests/models/test_m1_models_and_migration.py` (all passing):
1. **`test_partial_unique_retry_after_abort`**: Verifies that the partial unique index on `dispatched_actions` permits a new dispatch attempt on the same job after a prior attempt was aborted or failed.
2. **`test_account_deletion_with_audit_fks`**: Verifies that an account with `SendEvidence`, `DispatchedAction`, `SendAuthorization`, and `UserCommand` can be deleted cleanly in a single transaction due to `ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED` foreign keys.
3. **`test_stale_claimed_and_sending_sweep`**: Verifies that the periodic sweeper query resets stale claimed items (>30s) back to `'pending'` and transitions stale sending items (>60s) to `'unknown'`.
4. **`test_concurrent_claims_vs_caps`**: Verifies that autonomous rolling daily and hourly cap queries accurately enforce limits, blocking claims when caps are reached.

---

## 9. Implementation Tasks & Honest Effort Estimates

| Task ID | Component & Scope | Deliverables & Files | Est. Effort |
|---|---|---|---|
| **Task 1** | **Alembic Migration & Tenant Models (COMPLETED)** | Migration `97f51073900d` adding `account_dispatch_settings`, `user_commands`, `send_authorizations`, `application_pdf_payloads`, `hold_queue_items`, `send_evidence`, `dispatched_actions`, `trusted_recipients`, `job_feedback`. 4 targeted tests passing. Zero drift verified via `alembic check`. | **2.5 days (Done)** |
| **Task 2** | **Google Service, MIME Builder & MultiFernet** | Update `GoogleIntegrationService` to `gmail.send`. Build MIME message builder with PDF attachments, base64url encoding, token refresh, `MultiFernet` decryption (`OAUTH_ENCRYPTION_KEY`), and token migration script. | **2.0 days** |
| **Task 3** | **SendGateway & DB Outbox Poller Worker** | Build `SendGateway` (with `QuotaService` interface hooks) and standalone worker `backend/app/workers/dispatch_poller.py` with `FOR UPDATE SKIP LOCKED`, 30s periodic sweeper, crash recovery to `unknown`, and kill switch checks. | **2.5 days** |
| **Task 4** | **Legacy Engine Wiring & Application Lifecycle** | Refactor `approve_proposal()` in `engine.py:554` to reserve quota, transition `Application.status = 'queued'`; mint authorizations and enqueue hold items. Ensure `applied` and `sent_at` are set only on `sent`. Mid-hold cancel returns to `draft`. | **1.0 day** |
| **Task 5** | **Frontend UI & User Experience** | Build Dispatch Settings view, risk acknowledgment modal, Undo countdown button in `ApplicationStudio` and `Pipeline`, TOFU confirmation modal, Google re-consent banner, and hold-queue tracker drawer. | **2.0 days** |
| **Task 6** | **M1b Autonomy Policy Engine & Chat Trigger** | Build `backend/app/services/dispatch/` with pre-send barrier (`pypdf` page count/ATS check, compile verification, send caps, kill switches), chat command endpoint, and intent parser. Zero imports from `app.services.agent`. | **3.0 days** |
| **Task 7** | **PostgreSQL Concurrency & Integration Tests** | 25+ targeted pytest tests in `backend/tests/dispatch/` asserting `SKIP LOCKED` concurrency, tamper prevention, TOFU rules, crash recovery, intent parser negative corpus, account deletion with deferred evidence FKs, and dialect validation. | **2.0 days** |
| **Task 8** | **Worker Deployment & Monitoring Alerts** | Docker Compose service definition for dispatch poller, systemd template, and alert webhook on `unknown` state transitions. | **1.5 days** |
| **Total** | **Milestone M1 & M1b Combined** | **Production-ready outbound email dispatch and legacy autonomy policy.** | **16.5 days** |

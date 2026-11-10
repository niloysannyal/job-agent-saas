# JobEazy: Milestone M1 & M1b Implementation Specification
## Real Outbound Dispatch & Legacy Autonomy Policy Engine

> **Document Version:** 1.1.0  
> **Date:** 2026-11-10  
> **Author:** Antigravity (Lead Architect)  
> **Status:** Active Implementation Specification (Option B selected)  
> **Target Branch:** `feat/real-dispatch`

---

## 1. Executive Summary & Architecture Scope

### 1.1 Goal
Operationalize **real, verified outbound email dispatch** and the **Decision D1 per-account autonomy policy** directly on JobEazy's existing production architecture. This delivers real personal job applications for Niloy Sannyal (Phase 1 dogfooding) immediately, while deferring LangGraph orchestration until live validation is complete.

### 1.2 Sub-Milestones
- **Milestone M1 (Real Supervised Dispatch):**
  - Database schema: `account_dispatch_settings`, `user_commands`, `send_authorizations`, `hold_queue_items`, `send_evidence`, `dispatched_actions`, `trusted_recipients`, and `job_feedback`.
  - Hardened `SendGateway` service and PostgreSQL DB Outbox poller worker (`SELECT ... FOR UPDATE SKIP LOCKED`) with 30-second periodic sweeper.
  - Google OAuth integration upgraded to `https://www.googleapis.com/auth/gmail.send` (Sensitive scope, no CASA audit required).
  - Legacy `approve_proposal()` ([`backend/app/services/agent/engine.py:554-607`](file:///c:/Users/NiloySannyal/Projects/job-agent-saas/backend/app/services/agent/engine.py#L554-L607)) wired to set `Application.status = 'queued'`, mint authorizations, and enqueue hold items with an undo window.
  - Frontend UI updates: Settings UI & acknowledgment flow, Undo button with countdown timer, TOFU domain confirmation modal, Google re-consent banner, and hold-queue drawer.
- **Milestone M1b (Autonomous Single-Job Email on Legacy Engine):**
  - Standalone policy service (`backend/app/services/dispatch/`) with **zero imports from `app.services.agent`**.
  - `user_commands` table for explicit, authenticated user intents created only via dedicated endpoint.
  - Deterministic single-job resolver and comprehensive pre-send verification barrier (including `pypdf` page count, ATS text-layer extraction, and PDF compile checks).
  - Dual emergency kill switch (account-level and global environment kill switch).
  - Multi-job batches and web forms remain disabled until their respective gates (M5b precision, M5c ToS).

---

## 2. Database Schema (All Tables Tenant-Scoped)

Every table carries `account_id` with foreign key cascades to `accounts.id` (satisfying `scripts/check_migrations.py`), while foreign keys to `applications` and `jobs` use `ON DELETE RESTRICT` or `ON DELETE SET NULL` on audit tables to prevent accidental deletion of compliance records.

```
[accounts] (id, email, ...)
  │
  ├──< [account_dispatch_settings] (account_id [PK], autonomy_mode, acknowledged_at, kill_switch, daily_cap, hourly_cap)
  ├──< [user_commands] (id, account_id, command_type, target_job_ids, mode, status, expires_at)
  │      └──< [send_authorizations] (id, account_id, command_id, application_id, content_hash, recipient_email, attachment_sha256, minted_by, status, expires_at, consumed_at)
  │             └──< [hold_queue_items] (id, account_id, application_id, authorization_id, release_at, status, sending_started_at)
  │                    └──< [send_evidence] (id, account_id, application_id [RESTRICT], job_id [RESTRICT], provider_message_id, headers_snapshot, attachment_hash, sent_at)
  │
  ├──< [dispatched_actions] (id, account_id, job_id [RESTRICT], channel, sequence_kind [UNIQUE composite], status, dispatched_at)
  ├──< [trusted_recipients] (id, account_id, domain_or_address, entry_type, company_reference, confirmed_at)
  └──< [job_feedback] (id, account_id, job_id [CASCADE], user_rating, match_score_at_rating, feedback_notes, created_at)
```

### 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)

#### Table 1: `account_dispatch_settings` (Tenant Autonomy & Cap Settings)
```python
class AccountDispatchSettings(Base):
    """Per-account dispatch policy, emergency kill switch, and hourly/daily caps."""
    __tablename__ = "account_dispatch_settings"

    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    autonomy_mode: Mapped[str] = mapped_column(String(32), default="supervised", nullable=False)  # "supervised" | "autonomous"
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    kill_switch: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    daily_cap: Mapped[int] = mapped_column(Integer, default=5, nullable=False)    # Max dispatches per rolling 24 hours (default 5, max 10)
    hourly_cap: Mapped[int] = mapped_column(Integer, default=2, nullable=False)   # Max dispatches per rolling 60 minutes
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
```
- **Dual Kill Switch Architecture:**
  - **Account Kill Switch (`kill_switch`):** Set by tenant owner via UI toggle or API (`POST /api/v1/dispatch/settings/kill-switch`). Immediately pauses outbox processing for that tenant.
  - **Global Kill Switch (`DISPATCH_GLOBAL_KILL_SWITCH`):** Set via environment variable or platform superadmin configuration. Immediately halts all outbound processing across all tenants in `SendGateway` and the poller worker.
- **Authority:** Only the authenticated account owner may modify their account dispatch settings. Platform superadmins control the global kill switch.

#### Table 2: `user_commands` (Authority to Attempt)
```python
class UserCommand(Base):
    """Explicit, authenticated user command granting authority to attempt applications."""
    __tablename__ = "user_commands"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    command_type: Mapped[str] = mapped_column(String(32), nullable=False)  # "single" | "batch"
    target_job_ids: Mapped[List[str]] = mapped_column(JSON, nullable=False)  # Frozen list of job UUIDs
    mode: Mapped[str] = mapped_column(String(32), nullable=False)          # "supervised" | "autonomous"
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # "active" | "completed" | "canceled" | "revoked" | "expired"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
```
- **Command Authority Invariant:** `user_commands` are created **only** via the dedicated authenticated REST endpoint `POST /api/v1/dispatch/commands` following explicit human interaction in the UI. No LLM tool call or agent prompt can mint a `user_command`.

#### Table 3: `send_authorizations` (Content-Pinned Authorization)
```python
class SendAuthorization(Base):
    """Single-use authorization record pinned to exact application content hash."""
    __tablename__ = "send_authorizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    command_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("user_commands.id", ondelete="SET NULL"), nullable=True, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA-256 of canonical length-prefixed payload
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    attachment_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    pdf_payload: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)  # Final compiled PDF bytes (or content-addressed storage key)
    minted_by: Mapped[str] = mapped_column(String(32), nullable=False)     # "human_approval" | "autonomous_policy"
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # "active" | "consumed" | "revoked" | "expired"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_send_auth_lookup", "account_id", "application_id", "status"),
    )
```

#### Table 4: `hold_queue_items` (Durable Outbox Queue)
```python
class HoldQueueItem(Base):
    """Durable PostgreSQL Outbox item waiting for hold delay expiration."""
    __tablename__ = "hold_queue_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    authorization_id: Mapped[str] = mapped_column(String(36), ForeignKey("send_authorizations.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), default="email")
    release_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)  # "pending" | "claimed" | "sending" | "sent" | "unknown" | "canceled" | "aborted"
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sending_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_hold_queue_poller", "status", "release_at"),
    )
```

#### Table 5: `send_evidence` (Immutable Audit Log)
```python
class SendEvidence(Base):
    """Cryptographic audit trail of completed external transmissions."""
    __tablename__ = "send_evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id", ondelete="RESTRICT"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(32), default="email")
    provider_message_id: Mapped[str] = mapped_column(String(128), nullable=False)  # Gmail message id
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    headers_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # From, To, Date, Message-ID
    attachment_hash: Mapped[str] = mapped_column(String(64), nullable=False)      # SHA-256 of attached PDF bytes
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```
- **FK Cascades:** Foreign keys to `applications` and `jobs` are set to `ondelete="RESTRICT"` so audit logs can never be orphaned or silently wiped if a user deletes a job or application. Account deletion cascades for GDPR compliance.

#### Table 6: `dispatched_actions` (Sequenced Idempotency Barrier)
```python
class DispatchedAction(Base):
    """Reserve-before-send unique constraint preventing duplicate applications or follow-ups."""
    __tablename__ = "dispatched_actions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    sequence_kind: Mapped[str] = mapped_column(String(32), nullable=False)  # "initial_application" | "follow_up_1" | "follow_up_2"
    status: Mapped[str] = mapped_column(String(32), nullable=False)         # "reserved" | "dispatched"
    dispatched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("account_id", "job_id", "channel", "sequence_kind", name="uq_dispatched_action_seq"),
    )
```
- **Re-ingested Duplicate Postings:** If a job posting is re-ingested with a new `job_id` from a secondary source, the pre-send barrier performs a secondary lookup for existing `dispatched_actions` across all jobs with the same normalized company and role for that account within 90 days. If found, autonomous dispatch is blocked and requires human review.

#### Table 7: `trusted_recipients` (TOFU Allowlist)
```python
class TrustedRecipient(Base):
    """Allowlist of user-confirmed recipient domains or specific addresses."""
    __tablename__ = "trusted_recipients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    domain_or_address: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g. "anthropic.com" or "recruiter@company.com"
    entry_type: Mapped[str] = mapped_column(String(32), nullable=False)           # "corporate_domain" | "exact_address"
    company_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("account_id", "domain_or_address", name="uq_account_recipient"),
    )
```

#### Table 8: `job_feedback` (Ground-Truth Precision Tracking)
```python
class JobFeedback(Base):
    """User ground-truth ratings on discovered job postings to calibrate match-score precision."""
    __tablename__ = "job_feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    user_rating: Mapped[int] = mapped_column(Integer, nullable=False)  # +1 (Good fit) | -1 (Bad fit)
    match_score_at_rating: Mapped[float] = mapped_column(Float, nullable=False)
    feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```

### 2.2 Existing Model Citations & Schema Additions
In the existing codebase:
- [`backend/app/models/application.py:25-88`](file:///c:/Users/NiloySannyal/Projects/job-agent-saas/backend/app/models/application.py#L25-L88): `id` (L25), `account_id` (L31), `job_id` (L37), `cv_version_id` (L43), `channel` (L50), `draft_content` (L55), `sent_at` (L60), `status` (L65), `follow_up_due` (L70), `follow_up_count` (L74), `notes` (L79).
- [`backend/app/models/job.py:30-160`](file:///c:/Users/NiloySannyal/Projects/job-agent-saas/backend/app/models/job.py#L30-L160): `id` (L30), `account_id` (L36), `company` (L42), `role` (L47), `vetoed` (L109), `integrity_status` (L125), `is_active` (L130), `apply_link` (L150).
- **Migration Additions to `Application`:** Task 1 adds `recipient_email` (`String(255)`, nullable=True) and `pdf_sha256` (`String(64)`, nullable=True) to `applications`.

---

## 3. Send State Machine & Outbox Poller

### 3.1 State Machine Lifecycle & Order of Operations

```
[pending] ──(Poller claims via SKIP LOCKED)──> [claimed]
   │
   ├──(Pre-checks fail: hash / caps / kill switch / TOFU)──> [aborted] (Release reservation)
   │
   └──(Pre-checks clean)──> Commit [sending] & reserve idempotency in DB
                                 │
                                 ├──(Commit complete)──> Invoke Gmail API
                                 │                           │
                                 │                           ├──(200 OK)──> [sent] (Dispatched status)
                                 │                           ├──(401 refresh fail / 400)──> [aborted] (Release reservation)
                                 │                           ├──(429 Rate Limit)──> [pending] + backoff (Release reservation)
                                 │                           └──(Timeout / 5xx / Network crash)──> [unknown] (KEEP reservation)
                                 │
                                 └──(Periodic Sweeper: sending > 60s)──> [unknown] (KEEP reservation)
```

### 3.2 Single Atomic Transaction Before External Call
The poller worker executes all pre-checks and state commits in **one atomic database transaction** before initiating any network call to Google:
1. **Pre-check reads:**
   - Read `account_dispatch_settings` (assert `autonomy_mode` allows dispatch, `kill_switch == False`, and `DISPATCH_GLOBAL_KILL_SWITCH != True`).
   - Check send caps: rolling 24-hour sends < `daily_cap`; rolling 60-minute sends < `hourly_cap`.
   - Read `send_authorizations` (assert `status == 'active'`, not expired, and `content_hash` matches canonical encoding of current application state).
2. **Reserve Idempotency Key:**
   - Insert into `dispatched_actions` with `status = 'reserved'`. If the composite unique key `(account_id, job_id, channel, sequence_kind)` is violated, abort immediately.
3. **Transition Outbox Item to `sending`:**
   - Set `hold_queue_items.status = 'sending'`, set `hold_queue_items.sending_started_at = datetime.now(timezone.utc)`.
4. **COMMIT Transaction:**
   - The transaction closes. The record is permanently recorded in PostgreSQL as `sending`.
5. **Invoke External Provider:**
   - `SendGateway` calls the Gmail API via HTTP POST with 30-second socket timeout.

### 3.3 Recovery Sweeper & Periodic Sweep
A dedicated async periodic sweeper runs every 30 seconds inside the worker process (and runs immediately upon worker startup):
- **Stale Claims:** Rows in `claimed` older than 60 seconds (worker process died between claiming and pre-commit) are reset to `pending` with `claimed_at = None`.
- **Stale In-Flight Sends:** Rows in `sending` older than `HTTP_TIMEOUT (30s) + MARGIN (30s)` = 60 seconds are transitioned to `unknown`.
- **Worker Alerting:** Any transition to `unknown` triggers a high-severity structured log and an in-app administrative notification: *"Transmission status uncertain for Application {id}. Manual audit required before re-sending."*

### 3.4 Error Mapping & Reservation Handling
| Provider Outcome | State Transition | Reservation Action | Application Status | Reason / Remedy |
|---|---|---|---|---|
| **HTTP 200 OK** | `sent` | Marked `dispatched` | `applied` (`sent_at = now()`) | Transmission confirmed. Record `send_evidence`. |
| **Provable Pre-Send Error** (Token refresh fail, invalid recipient syntax, cap reached, hash mismatch) | `aborted` | **RELEASED** (Deleted from `dispatched_actions`) | `draft` | Message was provably never submitted to Google. User can fix and re-queue. |
| **HTTP 400 Bad Request** | `aborted` | **RELEASED** | `draft` | Google rejected MIME structure prior to processing. Payload invalid. |
| **HTTP 401 Unauthorized** (Mid-flight after failed refresh) | `unknown` | **KEPT** | `unknown` | Ambiguous; request reached endpoint. |
| **HTTP 403 Forbidden** (`rateLimitExceeded` / `quotaExceeded`) | `pending` (Backoff + 5m) | **RELEASED** | `queued` | Google rejected request due to quota. Reschedule for later release. |
| **HTTP 429 Too Many Requests** | `pending` (Backoff + 5m) | **RELEASED** | `queued` | Rate limit hit. Reschedule with exponential backoff. |
| **HTTP 5xx Server Error** | `unknown` | **KEPT** | `unknown` | Google server error during processing; email may have been delivered. |
| **Socket Timeout / Network Drop** | `unknown` | **KEPT** | `unknown` | Bytes were written to socket but response was lost. Never auto-retry. |

---

## 4. Content Pinning & MIME Construction

### 4.1 Canonical Length-Prefixed Content Hash
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
    """
    fields = [cv_version_id, subject, body, recipient, answers_json, attachment_sha256]
    encoded_parts = [f"{len(f)}:{f}" for f in fields]
    canonical_payload = "|".join(encoded_parts)
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
```

### 4.2 SendGateway MIME Assembly from Pinned Bytes
`SendGateway` builds the RFC 2822 MIME message strictly from the verified, pinned database bytes:
1. Pinned subject, body, and recipient are loaded from `send_authorizations`.
2. The final PDF bytes are retrieved from `send_authorizations.pdf_payload` (or content-addressed storage).
3. The worker verifies: `hashlib.sha256(pdf_bytes).hexdigest() == authorization.attachment_sha256`. If mismatched, aborts immediately.
4. An `EmailMessage` object is constructed, the PDF attached with application filename, base64url-encoded, and transmitted. Zero prompt re-evaluations or text modifications are allowed.

### 4.3 OAuth Token Decryption
The poller worker retrieves `OAuthConnection` rows and decrypts access/refresh tokens using the backend environment variable `APP_SECRET_KEY` (or dedicated `OAUTH_ENCRYPTION_KEY`), executing AES-256-GCM decryption via [`app.core.security.decrypt_token`](file:///c:/Users/NiloySannyal/Projects/job-agent-saas/backend/app/core/security.py).

---

## 5. Command Authority & Agent Boundary

### 5.1 Command Minting Restrictions
- `user_commands` records are created **exclusively** by the authenticated FastAPI endpoint `POST /api/v1/dispatch/commands`.
- Creation requires an active JWT token and explicit payload confirmation (`{job_id, mode: "single", channel: "email"}`).
- **Agent Boundary:** The Career Copilot / LLM agent can only create `AgentActionProposal` objects in chat; it has **no tool** registered in `ToolRegistry` that can create a `user_command` or mint a `send_authorization`.
- **Test Enforcement:** Unit tests will verify that prompting the agent to "Apply immediately" only yields an approval proposal and does not insert rows into `user_commands` or `send_authorizations`.

---

## 6. M1b Autonomy Policy Engine

### 6.1 Package Production Without `app.services.agent`
`backend/app/services/dispatch/` contains zero imports from `app.services.agent`. When evaluating an autonomous dispatch command:
- **Direct Service Invocation:** It invokes `app.services.cv_tailor.tailor_service.tailor_for_job()` (deterministic LaTeX compilation) and `app.services.llm.LLMService.generate()` directly for outreach copy, OR
- **Staged Package Requirement:** It reads an existing staged `Application` package that has already been compiled and stored.

### 6.2 Pre-Send Verification Barrier
Before an autonomous application can mint a `send_authorization`, it must pass all 8 gates of the verification barrier:
1. **PDF Validity:** Bytes start with `b"%PDF-1."`.
2. **Page Budget Check:** Inspected via `pypdf.PdfReader` to assert `len(reader.pages) == 1` (strict single-page rule).
3. **ATS Text-Layer Check:** Extracted text via `pypdf` contains >= 100 non-whitespace characters (verifies text is selectable, not an unparsed scan).
4. **Fact Ledger Audit:** Passed with 0 unverified claims ([`backend/app/services/cv_tailor/fact_ledger.py`](file:///c:/Users/NiloySannyal/Projects/job-agent-saas/backend/app/services/cv_tailor/fact_ledger.py)).
5. **Job Integrity:** `job.integrity_status == 'clean'`, `job.vetoed == False`, `job.is_active == True`.
6. **Recipient Syntax & TOFU:** Recipient email passes RFC 5322 validation and TOFU domain checks.
7. **Send Caps:** Rolling 24-hour sends < `daily_cap` (default 5, max 10); rolling 60-minute sends < `hourly_cap` (default 2).
8. **Real-Time Kill Switch Check:** `account_settings.kill_switch == False`, `account_settings.autonomy_mode == 'autonomous'`, `account_settings.acknowledged_at is not None`, and `DISPATCH_GLOBAL_KILL_SWITCH != True`.

If any gate fails, the system logs the reason, cancels autonomous dispatch, and downgrades the application to `supervised` mode for human review.

### 6.3 TOFU Domain Rules
- **Independent Domain Sources:** Allowed corporate domains must originate from verified ATS platforms (`greenhouse.io/<company>`, `lever.co/<company>`, `ashbyhq.com/<company>`, `workable.com/<company>`) or a verified `TargetCompany.website` record.
- **Untrusted Sources:** Recipient domains extracted solely from aggregators (RemoteOK, Remotive descriptions) or LinkedIn text are strictly untrusted.
- **Exact Address Reusability:** Once an exact recruiter email (`recruiter@company.com`) is confirmed by the user in the TOFU modal, it is stored in `trusted_recipients` with `entry_type = 'exact_address'` and is reusable for subsequent applications to that specific company.
- **Autonomous Cold Postings:** Because cold job postings rarely disclose direct recruiter emails on job boards, autonomous email will rarely trigger without an initial TOFU confirmation.

---

## 7. Gmail API Quotas, Limits & Scopes

### 7.1 Official Quotas & Limits
- **Quota Units:** `messages.send` consumes **100 quota units** per call (*Google Developers Gmail API Usage limits*, retrieved 2026-11-10; URL: `https://developers.google.com/gmail/api/reference/quota`).
- **Account Daily Sending Limits:**
  - Personal Gmail (`@gmail.com`): **500 emails/day** (*Google Workspace Admin Help: Gmail sending limits*, retrieved 2026-11-10; URL: `https://support.google.com/a/answer/166852`).
  - Google Workspace accounts: **2,000 emails/day** (*Google Workspace Admin Help: Gmail sending limits*, retrieved 2026-11-10; URL: `https://support.google.com/a/answer/166852`).
- **Message Size Ceiling:** Gmail enforces a **25 MB total MIME message limit** (*Google Gmail Help: Send attachments with your Gmail message*, retrieved 2026-11-10; URL: `https://support.google.com/mail/answer/6584`). Because base64 encoding adds ~33% overhead, the maximum raw attachment size is **~18 MB**. JobEazy single-page PDF CVs average 50–150 KB, well within this ceiling.

### 7.2 OAuth Scope Classification
- **Scope Used:** `https://www.googleapis.com/auth/gmail.send`.
- **Classification:** **Sensitive Scope** (*Google Cloud OAuth API verification FAQ*, retrieved 2026-11-10; URL: `https://support.google.com/cloud/answer/9110914`).
- **Verification Requirements:**
  - **Phase 1 Owner Use:** Deployed in Google Cloud Console in "Production (Unverified)" mode. The owner authorizes directly via the standard Google unverified-app warning screen.
  - **Public Launch:** Requires Google OAuth Brand Verification (privacy policy, Terms of Service, YouTube video walkthrough). **Does NOT require CASA Tier-2 security assessment** (CASA is mandatory only for Restricted scopes like `gmail.compose` or `gmail.readonly`).

---

## 8. Implementation Tasks & Honest Effort Estimates

| Task ID | Component & Scope | Deliverables & Files | Est. Effort |
|---|---|---|---|
| **Task 1** | **Alembic Migration & Tenant Models** | Create migration adding `account_dispatch_settings`, `user_commands`, `send_authorizations`, `hold_queue_items`, `send_evidence`, `dispatched_actions`, `trusted_recipients`, `job_feedback`, plus `recipient_email` and `pdf_sha256` on `applications`. Enforce `account_id` tenancy and `ON DELETE RESTRICT` on audit FKs. | **2.0 days** |
| **Task 2** | **Google Service & RFC 2822 MIME Builder** | Update `GoogleIntegrationService` to `gmail.send`. Build MIME message builder with PDF attachments, base64url encoding, token refresh, and 401/403/429/5xx error handling. | **2.0 days** |
| **Task 3** | **SendGateway & DB Outbox Poller Worker** | Build `SendGateway` and standalone background worker `backend/app/workers/dispatch_poller.py` with `FOR UPDATE SKIP LOCKED`, 30s periodic sweeper, crash recovery to `unknown`, and kill switch checks. | **2.5 days** |
| **Task 4** | **Legacy Engine Wiring & Application Lifecycle** | Refactor `approve_proposal()` in `engine.py:554` to transition `Application.status = 'queued'`; mint authorizations and enqueue hold items. Ensure `applied` and `sent_at` are set only on `sent`. | **1.0 day** |
| **Task 5** | **Frontend UI & User Experience** | Build Dispatch Settings view, risk acknowledgment modal, Undo countdown button in `ApplicationStudio` and `Pipeline`, TOFU domain confirmation modal, Google re-consent banner, and hold-queue tracker drawer. | **2.0 days** |
| **Task 6** | **M1b Autonomy Policy Engine** | Build `backend/app/services/dispatch/` with pre-send barrier (`pypdf` page count/ATS check, compile verification, send caps, kill switches) and command endpoint `POST /api/v1/dispatch/commands`. Zero imports from `app.services.agent`. | **2.5 days** |
| **Task 7** | **PostgreSQL Concurrency & Integration Tests** | 25+ targeted pytest tests in `backend/tests/dispatch/` asserting `SKIP LOCKED` concurrency, tamper prevention, TOFU rules, crash recovery, and dialect validation. | **2.0 days** |
| **Task 8** | **Worker Deployment & Monitoring Alerts** | Docker Compose service definition for dispatch poller, systemd template, and alert webhook on `unknown` state transitions. | **1.5 days** |
| **Total** | **Milestone M1 & M1b Combined** | **Production-ready outbound email dispatch and legacy autonomy policy engine.** | **15.5 days** |

---

## 9. Test Plan & PostgreSQL Dialect Requirements

### 9.1 PostgreSQL Prerequisite
Because `SELECT ... FOR UPDATE SKIP LOCKED` and row-level locking are core database requirements, all tests under `backend/tests/dispatch/` require a real PostgreSQL instance (via Docker or local PostgreSQL).
- In `backend/tests/dispatch/conftest.py`, the database fixture verifies:
  ```python
  if db.bind.dialect.name == "sqlite":
      pytest.fail("Dispatch queue tests require PostgreSQL with SKIP LOCKED support. Run docker-compose or local PostgreSQL.")
  ```

### 9.2 Targeted Test Suite (25+ Scenarios)
1. **Outbox Poller Concurrency:** Spawn 3 concurrent async pollers; verify no dual-claims on 10 queued items (`SKIP LOCKED` verification).
2. **Crash Recovery to `unknown`:** Inject crash during send; verify 30-second periodic sweeper transitions item to `unknown` and preserves idempotency reservation.
3. **Tamper Prevention:** Modify tailored text or PDF during hold window; verify `SendGateway` detects content hash mismatch and aborts.
4. **Idempotency Sequencing:** Assert unique constraint prevents duplicate initial applications or follow-ups for same `(account_id, job_id, channel, sequence_kind)`.
5. **Agent Boundary Isolation:** Assert prompt to Career Copilot cannot create `user_commands` or `send_authorizations`.
6. **Pre-Send Barrier Hardening:** Assert multi-page PDFs, PDFs with < 100 ATS characters, or invalid PDF headers fail barrier and downgrade to `supervised`.
7. **Rate Caps & Kill Switches:** Assert daily cap (5), hourly cap (2), account kill switch, and global kill switch immediately halt dispatch.
8. **TOFU Security:** Assert public email domains (`gmail.com`) always require per-address confirmation, while corporate domains require ATS or company reference validation.

---

## 10. Document Changelog

| Version | Date | Author | Description of Changes |
|---|---|---|---|
| **1.0.0** | 2026-11-10 | Antigravity | Initial implementation spec for M1/M1b. |
| **1.1.0** | 2026-11-10 | Antigravity | **Advisor Review 3 Overhaul:**<br>• Added `account_dispatch_settings` (autonomy_mode, acknowledged_at, kill_switch, daily_cap, hourly_cap) and dual kill switch architecture.<br>• Refined state machine: single transaction pre-commit of `sending` and reservation before Gmail call; 30s periodic sweeper for `unknown` and stale claims; explicit reservation release rules on provable aborts.<br>• Replaced hashed PK with composite UNIQUE constraint `(account_id, job_id, channel, sequence_kind)` on `dispatched_actions`.<br>• Added canonical length-prefixed `content_hash` specification and pinned MIME construction.<br>• Mandated PDF bytes storage and AES-256-GCM OAuth key decryption.<br>• Enforced command authority: `user_commands` created only via authenticated REST endpoint, agent restricted to proposals.<br>• Defined M1b package production without importing `app.services.agent`.<br>• Protected audit trail: `send_evidence` and `dispatched_actions` use `ON DELETE RESTRICT` on jobs/applications.<br>• Hardened test infra: required PostgreSQL dialect, fail if SQLite.<br>• Application status updates: approval sets `queued`; `applied`/`sent_at` set only on `sent`; follow-ups key off real send time.<br>• Hardened barrier: added `pypdf` page count, ATS text-layer check, compile verification, and file:line citations.<br>• Defined TOFU independent domain sources (ATS only) and exact address reusability.<br>• Added verified Gmail quotas (100 units/send), daily limits (500/2,000), 25 MB MIME ceiling (~18 MB raw), and Sensitive scope verification.<br>• Added Tasks for Settings UI, worker deployment, monitoring alert on `unknown`, and in-app notifications. Re-estimated total effort to 15.5 days. |

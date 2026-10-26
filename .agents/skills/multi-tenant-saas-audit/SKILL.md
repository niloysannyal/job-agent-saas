---
name: multi-tenant-saas-audit
description: >-
  Audit database models, Alembic migrations, FastAPI routers, and service queries
  against multi-tenant SaaS isolation, security boundaries, and human-in-the-loop rules.
---

# Multi-Tenant SaaS Auditor

Use this skill when introducing new models, creating database migrations, adding API endpoints, or reviewing code for multi-tenant isolation and security compliance.

## Multi-Tenant Invariants (Non-Negotiable)

1. **`account_id` on Every Table**:
   - Every database model must include `account_id: Mapped[str] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)`.
   - Never remove or make `account_id` optional on tenant data tables (`jobs`, `applications`, `cv_templates`, `account_cv_versions`).

2. **Tenant Isolation in Queries**:
   - Every query reading or writing tenant records must filter explicitly by `account_id`.
   - Test isolation explicitly: seed records for two accounts (`Alice` and `Bob`) and assert that querying one account never leaks the other's records, even with `show_all=True`.

3. **Authentication Blocker Audit**:
   - In Phase 0/1 (solo use), endpoints accept `account_id: str = Query(...)` as an unverified test parameter.
   - **Flag immediately** whenever a new endpoint is added with an unverified `account_id` query param, marking it as a blocker before multi-user launch (Phase 3) that must be replaced by `current_account = Depends(get_current_account)`.

4. **Human-in-the-Loop Send Gate**:
   - All application flows must terminate at `Draft -> Human Review -> Send`.
   - Never implement an unattended auto-send or automated submit loop.

5. **No Password Storage**:
   - Never store third-party credentials (usernames/passwords) for job portals.
   - Use only official APIs or OAuth tokens encrypted at rest.

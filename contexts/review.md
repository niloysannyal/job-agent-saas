# Code Review Context — Job Application Agent SaaS

Mode: PR & Code Review Quality Gate
Focus: Enterprise security, multi-tenant isolation, async correctness, and anti-template UI design.

## Review Workflow
1. Inspect git diff and modified files first.
2. Verify all tests pass without warnings or regressions.
3. Check against the Review Checklist below.
4. Categorize findings by severity: Critical > High > Medium > Low.

## SaaS Review Checklist

### 1. Multi-Tenant Data Isolation (Critical)
- [ ] Every SQLAlchemy model carries `account_id` (foreign key to `accounts.id`).
- [ ] Every router query filters explicitly by `account_id` from the authenticated session context.
- [ ] No data leaks across tenant boundaries.

### 2. Security & Credentials (Critical)
- [ ] No hardcoded API keys, tokens, or plaintext secrets.
- [ ] External LLM provider API keys encrypted at rest using AES-256 (`app.core.security`).
- [ ] Password hashes never exposed in Pydantic response models.
- [ ] Ingested job postings screened by `PostingIntegrityGate` for prompt injection.

### 3. Async & Performance (High)
- [ ] Route handlers using `async def` only call non-blocking async clients.
- [ ] No synchronous blocking operations (e.g. `requests`, sync DB sessions) inside async routes.
- [ ] Database sessions injected via FastAPI `Depends(get_db)`.

### 4. Human-in-the-Loop & Business Rules (Critical)
- [ ] Application pipeline ends strictly at Draft; human reviews and confirms Send.
- [ ] No LinkedIn/Facebook scraping or credential storage.
- [ ] CV tailoring strictly reorders/trims from `cv_templates/01_MASTER_CV.tex` without inventing facts.

### 5. Frontend & UI/UX Standards (High)
- [ ] Conforms to Obsidian & Cyber Emerald dual theme (`[data-theme="dark"]` and Light mode).
- [ ] Frosted glassmorphism modal backdrops (`--modal-backdrop-bg`, blur filter) with intact sidebar.
- [ ] No generic template look; intentional hierarchy, crisp contrast, accessible interactive states.


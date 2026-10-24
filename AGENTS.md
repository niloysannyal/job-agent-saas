# Agent Behavior Rules — Job Application Agent SaaS

These are *how-to-code* rules. For *what we're building*, see `GEMINI.md` and
`docs/ARCHITECTURE.md`.

## Folder structure — put new code in the right place
```
backend/app/
  api/              # FastAPI routers only — no business logic here
  core/             # config, security, startup wiring
  models/           # SQLAlchemy models + Pydantic schemas, matching ARCHITECTURE.md §7
  services/
    job_sources/    # one file per source, each implementing JobSource.fetch()
    llm/            # provider-abstraction interface + one file per provider
    cv_tailor/      # CV tailoring pipeline, reads cv_templates/
    matching/       # Qdrant embedding + similarity scoring
  db/               # session, migrations (Alembic)
  workers/          # async/background tasks (Celery or Arq) — not needed yet,
                     # but new background jobs go here when they're added
backend/tests/      # mirror the app/ structure; one test file per module
cv_templates/       # admin-curated LaTeX templates, never user-uploaded code
docs/               # reference docs — read, don't edit as a side effect of a task
```

## Interfaces to honor, not bypass
- **`JobSource`**: every job-data integration (Adzuna, Remotive, RemoteOK,
  Greenhouse/Lever, and later JSearch) implements the same
  `fetch(query) -> list[JobPosting]` interface. New source = new file in
  `services/job_sources/`, not a special case in the API layer.
- **LLM provider interface**: every model call goes through one
  `generate(prompt, context) -> text` interface in `services/llm/`. Provider
  selection (OpenAI now, Claude fallback later, admin-added providers) is
  **data** (a `llm_providers` config table: provider name, encrypted API key,
  active flag, priority), not an `if/else` on a hardcoded provider name.

## Database & migrations
- Every new table includes `account_id` (even where only one account exists).
- Every schema change is a migration (Alembic) — never a manual `ALTER TABLE`
  or an edit to an already-applied migration file.
- Secrets (API keys, OAuth tokens) are encrypted at rest. Never log them, never
  put them in a commit, never put them in a Knowledge Item or GEMINI.md.

## What NOT to build without being asked
- Any LinkedIn/Facebook login automation or credential storage — out of scope
  permanently for this SaaS (`ARCHITECTURE.md` §4). If a task seems to need it,
  stop and flag it instead of implementing a workaround.
- Any auto-send path that skips human review — same: stop and flag, don't build.
- Billing/Paddle integration, OAuth email sending, rate limiting — these are
  Phase 2/3 per `ROADMAP.md`. Don't scope-creep them into a Phase 0 task.

## Code conventions
- Python: type-hinted, PEP 8, FastAPI dependency-injection style (no global
  mutable state for DB/Redis/Qdrant clients — inject them).
- Every new endpoint or service function gets a corresponding test in
  `backend/tests/`, mirroring the path under `app/`.
- Commit messages: one logical change per commit, imperative mood
  ("add Adzuna job source", not "added" or "adding").
- When a task is ambiguous between two designs already described in
  `docs/ARCHITECTURE.md`, follow what's written there. When it isn't covered
  there at all, implement the simplest version that fits the existing
  interfaces, and leave a comment flagging the assumption rather than silently
  deciding a business rule.

## When to stop and ask instead of proceeding
- Any change that would touch the human-in-the-loop Send gate.
- Any change that adds a new third-party data source outside the layered list
  in `docs/ARCHITECTURE.md` §4.
- Any change to the multi-tenant schema's shape (not its content) — e.g.
  removing `account_id` from a table, merging tables across tenants.

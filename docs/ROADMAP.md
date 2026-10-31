# Roadmap — Job Application Agent SaaS

**Current phase: Phase 0 → 1 transition (building the SaaS MVP root architecture now)**

Built as a multi-tenant SaaS from day one (see ARCHITECTURE.md §0 "puzzle piece"
principle). Niloy is the only account for the first ~1 month, using it through a
real job search before any marketing starts.

## Phase 0 — MVP build (target: 1 month, using Google Antigravity)
Goal: Find → Apply → Monitor working end-to-end for one account (Niloy), on the
multi-tenant schema, with no shortcuts that would need rearchitecting later.

**Find (build first, validate before moving on):**
- [x] Multi-tenant schema live (`accounts`, `jobs`, `applications`, `cv_templates`,
      `account_cv_versions`, `subscription_plans`/`entitlements`, `llm_providers`)
      — initialized via Alembic migration and seeded with initial defaults (built 2026-10-26)
- [x] Adzuna + Remotive + RemoteOK API integration behind the `JobSource` interface
- [x] freehire.me API integration — built 2026-10-19, but Niloy-only per its ToS
      (ARCHITECTURE.md §4, Layer 1b) until a paid plan or self-hosted instance
      exists; needs the "via freehire.me" attribution UI before any public display
- [x] Greenhouse/Lever integration for the user's Target Company list — all Layer
      1/1b sources now complete (Adzuna, Remotive, RemoteOK, Greenhouse, Lever,
      freehire.me, LinkedIn public endpoint)
- [x] Greenhouse/Lever pagination (ARCHITECTURE.md §4) — full multi-page traversal loops implemented: Greenhouse follows RFC 5988 `Link` headers with `rel="next"` and circular loop guards; Lever utilizes offset pagination via `skip` and `limit` batches. Both enforced with configurable safety caps (`max_pages`, `max_postings`).
- [x] Posting integrity gate (ARCHITECTURE.md §4) — runs before any posting is persisted or sent to an LLM; fully wired into `JobIngestionService.ingest()`, flagging injection/instructions and marking status as `clean` or `flagged`.
- [x] Match scoring via Qdrant embedding similarity against MASTER_CV.tex + USER_PROFILE.md target roles — built 2026-10-19.
- [x] **Wire matching into the pipeline.** Wired synchronously at the end of `job_ingestion.py` — newly persisted clean jobs are automatically scored and gated upon ingestion, while flagged jobs are skipped from scoring until human review (built 2026-10-19). Ready to transition to a background worker later when volume demands it (ARCHITECTURE.md §9).
- [x] Language gate — evaluated by `LanguageGate` with 14 known languages, dynamically checked against the user's declared spoken languages (`SpokenLanguage` table). Hard-vetoes postings requiring undeclared languages.
- [x] Dealbreaker evaluation & Fit Evaluator — `POST /api/v1/applications/evaluate-fit` evaluates fit against profile target roles, skills, and free-text dealbreakers, returning matched skills, missing requirements, and dealbreaker red flags before tailoring.
- [x] Queue endpoint ranked by match score (`GET /api/v1/jobs` with default gating and review overrides) — built 2026-10-25.
- [x] Queue UI view (frontend dashboard in Obsidian & Cyber Emerald theme showing company, role, radial match score gauges, posting guard inspection, and RemoteOK/freehire attribution — built 2026-10-26).

**Apply (build second):**
- [x] CV template gallery (seeded with `01_MASTER_CV.tex` as admin default template #1)
- [x] CV tailoring pipeline (LLM interface behind provider-abstraction layer with Drafter + Reviewer two-pass generation, truth verification against verified fact ledger, and ATS text-layer check — built 2026-10-26)
- [x] Draft generation per channel (mail / form answers / DM / portal — built 2026-10-26)
- [x] Draft → review → Send UI (human-in-the-loop strictly enforced: application created in 'draft' with sent_at=None, confirmed only via human review gate — built 2026-10-26)

**Monitor (build third):**
- [x] Jobs table extended with status/follow-up fields (`applied_at`, `follow_up_due`, `notes`, Alembic migration `9fa848922c02` — built 2026-10-26)
- [x] Status summary view and Monitor pipeline dashboard (Total / Draft / Sent / Follow-ups Due / Responded / Interview / Offer / Rejected with 10-day follow-up drafting strictly capped at 2 and human-in-the-loop review gate — built 2026-10-26)

**Profile & Interview Coach (Phase 0 additions):**
- [x] Profile Management API & UI (`/api/v1/profile` + `ProfileView.jsx`) — CRUD for `UserProfile`, `TargetDesignation`, `TargetLocation`, `CompensationExpectation`, `SpokenLanguage`, and dealbreaker preferences.
- [x] STAR Interview Coach (`/api/v1/interview` + `InterviewCoachView.jsx`) — STAR story bank manager, question generator matching role requirements, and AI answer critique adhering to the verified fact ledger.

**Superadmin Control, Multi-Tenant RBAC & Auth Engine (Phase 0 additions):**
- [x] Multi-tenant role & status migration (`role`, `status` on `accounts` via Alembic `7b8e2b6659a9` on Supabase PostgreSQL).
- [x] Password authentication migration (`hashed_password` on `accounts` via Alembic `e57e51d71b2e` on Supabase PostgreSQL).
- [x] JWT Bearer Token Security Engine (`/api/v1/auth/login`, `register`, `me`) with bcrypt hashing and RBAC route protection.
- [x] Superadmin Control Center API (`/api/v1/admin/metrics`, `tenants`, `impersonate`, `llm-providers`, `sources`, `templates`, `flagged`).
- [x] Superadmin UI (`AdminView.jsx`) with Bento metrics, tenant management, dynamic LLM failover ping testing, and one-click "Test As Tenant" QA dogfooding mode with persistent banner.
- [x] Public SaaS Landing Page (`LandingPageView.jsx`) with live app preview mock, bento grid, lifecycle workflow, and pricing tiers.
- [x] Clean Portal Separation: General tenants (`niloy@example.com`) strictly access Candidate OS; Superadmins (`admin@jobeazy.com`) route directly to Ops Center with dedicated sidebar controls.
- [x] 151 total passing backend tests (100% green).

**Architecture & Tooling:**
- [x] Graphify Knowledge Graph (`graphify-out/`) — deterministic AST code parsing, interactive node graph (`graph.html`), Mermaid call-flow diagram (`job-agent-saas-callflow.html`), D3 collapsible tree (`GRAPH_TREE.html`), and 59 community wiki articles for fast agent reasoning.


**Infra (in parallel, not blocking):**
- [ ] Single VPS + Docker Compose set up (reuse Caddy VPS experience)
- [x] OpenAI API key wired through the LLM interface (not called directly anywhere — built 2026-10-26)
- [ ] Data retention limits + export/delete-account path stubbed in, even if manual

- Exit criteria: Niloy can run a real job search through the product end-to-end —
  find, tailor, apply, track — on the deployed MVP, for at least 2-3 weeks before
  evaluating whether it's ready to extend to other users.

## Phase 1 — Personal validation (the "1 month with my own data" period)
Goal: prove the product works by actually using it to land a job, and gather
real dashboard data on what the Find/Apply/Monitor loop looks like in practice.
- [ ] Run every real application Niloy sends through the product, not around it
- [ ] Track: time saved vs. the old manual flow, match-score accuracy vs. gut
      feel, response rate by channel
- [ ] Note every rough edge — these become the first post-MVP backlog, not
      scope creep into Phase 0
- Exit criteria: a job offer, or at minimum a clear read on which parts of the
  loop (Find/Apply/Monitor) are strong enough to show another user.

## Phase 2 — Expand job sourcing + add paying-user groundwork
Goal: broaden coverage and close the gaps found in Phase 1, without yet opening
signups.
- [ ] Add JSearch (RapidAPI) for LinkedIn/Indeed/Glassdoor coverage
      (ARCHITECTURE.md §4 — paid vendor decision, not free-tier default)
- [ ] User-facing preference settings (target roles, locations, dealbreakers) —
      the "easy to tweak" requirement from day one, now exposed in UI rather
      than edited in a markdown file
- [ ] Decide the pricing model (ARCHITECTURE.md §0/§7 — the deferred "puzzle
      piece"); this is the one major OPEN decision blocking Phase 3
- Exit criteria: the product works well enough that Niloy would be comfortable
  recommending it to another job seeker and charging them for it.

## Phase 3 — Open signups / SaaS launch
Goal: other people can use it and pay for it.
- [ ] Wire up Paddle (or chosen alternative) against the existing
      `subscription_plans`/`entitlements` tables
- [ ] Per-user OAuth for email sending (minimal scopes)
- [ ] Legal review of the JSearch aggregator layer's ToS exposure at real scale
- [ ] Rate limiting / cost caps per account
- [ ] Talk to 3-5 other job seekers (still hasn't happened — do this *during*
      Phase 1/2, not after building everything)
- Exit criteria: a paying user outside Niloy completes the full Find → Apply →
  Monitor loop without his manual help.

## Decision log
| Date | Phase | Decision | Why |
|---|---|---|---|
| 2026-10-04 | 0 | Build as multi-tenant SaaS from day one, not personal-tool-first | Avoid future rearchitecting; see ARCHITECTURE.md §0 |
| 2026-10-04 | 0 | Build order locked: Find → Apply → Monitor, validate each before the next | Bad matches poison everything downstream |
| 2026-10-04 | 0 | 1-month MVP target using Google Antigravity | Self-imposed deadline, no external pressure |

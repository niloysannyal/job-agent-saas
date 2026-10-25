# Roadmap — Job Application Agent SaaS

**Current phase: Phase 0 → 1 transition (building the SaaS MVP root architecture now)**

Built as a multi-tenant SaaS from day one (see ARCHITECTURE.md §0 "puzzle piece"
principle). Niloy is the only account for the first ~1 month, using it through a
real job search before any marketing starts.

## Phase 0 — MVP build (target: 1 month, using Google Antigravity)
Goal: Find → Apply → Monitor working end-to-end for one account (Niloy), on the
multi-tenant schema, with no shortcuts that would need rearchitecting later.

**Find (build first, validate before moving on):**
- [ ] Multi-tenant schema live (`accounts`, `jobs`, `applications`, `cv_templates`,
      `subscription_plans`/`entitlements` — unused but present)
- [x] Adzuna + Remotive + RemoteOK API integration behind the `JobSource` interface
- [x] freehire.me API integration — built 2026-10-19, but Niloy-only per its ToS
      (ARCHITECTURE.md §4, Layer 1b) until a paid plan or self-hosted instance
      exists; needs the "via freehire.me" attribution UI before any public display
- [x] Greenhouse/Lever integration for the user's Target Company list — all Layer
      1/1b sources now complete (Adzuna, Remotive, RemoteOK, Greenhouse, Lever,
      freehire.me, LinkedIn public endpoint)
- [ ] Greenhouse/Lever pagination (ARCHITECTURE.md §4) — both currently return
      only the first page for companies with large job boards (Greenhouse: Link
      header pagination unhandled; Lever: limit/skip pagination unhandled).
      Low priority until a target company's board actually exceeds one page, but
      don't let it get forgotten once real usage starts.
- [x] Posting integrity gate (ARCHITECTURE.md §4) — built 2026-10-xx, runs before
      any posting is persisted or sent to an LLM; not yet wired into the
      job-ingestion pipeline since that orchestration layer doesn't exist yet
- [x] Match scoring via Qdrant embedding similarity against MASTER_CV.tex +
      USER_PROFILE.md target roles — built 2026-10-19 (mocked embedding/Qdrant
      in tests)
- [ ] **Wire matching into the pipeline.** `score_and_gate_jobs()` exists but
      nothing calls it yet — `job_ingestion.py` only runs the posting guard and
      persists. Confirmed standalone as of 2026-10-19, same situation
      posting_guard was in before job_ingestion wired it up. Needs the same
      treatment: either called synchronously at the end of ingestion, or by a
      background worker once one exists (ARCHITECTURE.md §9 — Celery/Arq, not
      needed yet otherwise).
- [x] Language gate — built 2026-10-19, but hardcoded to 5 languages
      (ARCHITECTURE.md §4 — needs to be configurable before trusted for other
      users)
- [ ] **General dealbreaker gate — not implemented.** Only the language
      sub-case exists. USER_PROFILE.md's free-text "Dealbreakers:" line is
      captured but nothing is vetoed on it yet. Decide the approach (LLM rubric
      vs. structured fields) after Phase 1 real-usage data, per ARCHITECTURE.md
      §4 — don't guess at this without evidence.
- [ ] Queue view ranked by match score, highest first

**Apply (build second):**
- [ ] CV template gallery (seed with `01_MASTER_CV.tex` as template #1)
- [ ] CV tailoring pipeline (LLM interface behind the provider-abstraction layer,
      OpenAI as the only implementation for now)
- [ ] Draft generation per channel (mail / form answers / DM)
- [ ] Draft → review → Send UI (human-in-the-loop is non-negotiable — see
      ARCHITECTURE.md §3)

**Monitor (build third):**
- [ ] Jobs table extended with status/follow-up fields
- [ ] Status summary view (Total / Responded / Interview / Upcoming)

**Infra (in parallel, not blocking):**
- [ ] Single VPS + Docker Compose set up (reuse Caddy VPS experience)
- [ ] OpenAI API key wired through the LLM interface (not called directly anywhere)
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

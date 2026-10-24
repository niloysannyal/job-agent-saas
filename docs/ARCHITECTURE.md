# Architecture — Job Application Agent SaaS

Status: Core decisions below are now DECIDED (2026-10-04) based on Niloy's answers.
Remaining (OPEN) items are genuinely still open — don't guess at these.

## 0. Design principle: "missing puzzle piece"
Pricing and a few other business decisions are intentionally undecided right now.
Instead of blocking the build, every undecided area gets a real schema/interface
today, with a permissive default that changes nothing for a single free user. When
the decision is made later, it's a config change or a data insert — never a schema
migration or a refactor. Every section below marks where this applies.

## 1. Scope & rollout
- **Builder:** solo (Niloy), building with FastAPI + Google Antigravity as the dev tool.
- **Rollout:** build as a true multi-tenant SaaS from day one — Niloy is tenant #1,
  using it personally for ~1 month (through a real job search, including landing a job)
  before any marketing or paid signups. No "personal tool now, rearchitect for SaaS
  later" — that's explicitly what we're avoiding.
- **Target user (once it's sold):** general job seekers, not a narrow niche — but the
  product must let each user easily tweak their own preferences, target roles,
  locations, and goals. This means nothing about role/location/industry is
  hardcoded anywhere in the system; it's all per-user config from day one.
- **MVP deadline:** 1 month, for the root architecture + working MVP. No external
  deadline pressure beyond that self-imposed one.

## 2. Priority build order (confirmed)
1. **Find** — fetch jobs, score match, list in a queue ranked by highest match first.
2. **Apply** — tailor CV + draft outreach for the top of that queue.
3. **Monitor** — status tracking once Find + Apply are solid.

Build and validate Find fully before starting Apply. Don't parallelize the three —
a half-working Find module poisons everything downstream (bad matches → wasted
tailoring → bad applications).

## 3. Human-in-the-loop (now a locked decision, not OPEN)
**Draft → human reviews → Send. Always. No auto-send tier, ever**, even as a future
premium option. This isn't just a quality safeguard — it's the main legal/reputational
buffer against ToS violations and bad-application spam that competitors get flagged
for. Don't revisit this later under growth pressure without a full legal review first.

## 4. Module 1 — Find Job Opportunity (decision made)

**Decision:** no direct scraping of LinkedIn/Facebook, no stored third-party
passwords, ever, for the SaaS. This was OPEN before; it's now closed given the
"max performance + max data safety" answer. Layered sourcing instead:

| Layer | Source | Legal status | Coverage |
|---|---|---|---|
| 1 | **Adzuna API** (official) | Fully legal, direct | Broad, 19 countries, decent EU/remote coverage |
| 1 | **Remotive API**, **RemoteOK API** | Fully legal, direct | Remote-specific roles |
| 1 | **Greenhouse / Lever / Ashby public job-board APIs** | Fully legal, direct | Per-company — ideal for the user's "Target Company" list |
| 2 | **JSearch (via RapidAPI)** | Legal to *us* — it's a third-party vendor that aggregates LinkedIn/Indeed/Glassdoor/ZipRecruiter and resells structured data under its own ToS. We're a paying API customer, not a scraper. The scraping risk sits with the vendor, not with us. | Fills the LinkedIn/Indeed gap layer 1 can't reach |
| — | Direct LinkedIn/Facebook scraping or credential storage | **Never**, for the SaaS | N/A |

Start with Layer 1 only for the MVP (zero ToS exposure, enough coverage to prove the
product). Add JSearch in Phase 2+ once there's budget and the product needs broader
coverage — treat it as a paid vendor contract decision, not a build-time default.

**Puzzle piece:** the job-ingestion layer is a plugin interface
(`JobSource.fetch(query) -> list[JobPosting]`), so adding/removing a source later
(including dropping JSearch if its ToS risk becomes a problem) never touches the
rest of the pipeline.

**Match scoring:** embed the user's MASTER_CV.tex content + USER_PROFILE.md target
roles with a vector model, embed each job description, rank by cosine similarity
in Qdrant. Simple, explainable, and needs no training data — upgrade to an
LLM-scored fit later if similarity search proves too coarse.

## 5. Module 2 — Apply for the Job

Flow unchanged from the original sketch: tailor CV once per job → branch into
mail/form/DM → Draft → human review → Send. Two refinements now that this is a
multi-tenant product:

**CV templates (puzzle piece for the subscription plan):**
- MVP: an admin-curated set of LaTeX templates (reuse the tagged structure from
  `01_MASTER_CV.tex` as template #1). Users pick one from a gallery — no custom
  LaTeX editing yet.
- Schema from day one: `cv_templates` table (id, name, latex_source, is_admin_default)
  and `account_template_limit` on the accounts table (int, default = unlimited for
  now). When the subscription plan is decided, enforcing a limit is a single
  `WHERE` check against a column that already exists — not a new table, not a
  migration.

**Sending:** email via the user's own OAuth (Gmail/Outlook) once that's built; forms
stay browser-assisted or manual-paste for the MVP, since most have no send API.

## 6. Module 3 — Monitor Job Applications
Unchanged from the original design: jobs table extended with applied-date,
status, follow-up-due-date, notes. Status summary is a query, not new logic.

## 7. Data model — multi-tenant from day one (puzzle piece)
Every table carries an `account_id` from the start, even with one account:
- `accounts` (id, email, plan_tier *[default: 'free', unenforced]*, created_at)
- `cv_templates`, `account_cv_versions` (which tailored CV went to which job)
- `jobs` (account_id, company, role, salary, deadline, location_type, country,
  visa_required, target_company, match_score, status, source, apply_link, found_at)
- `applications` (job_id, channel, draft_content, sent_at, status, follow_up_due)
- `subscription_plans`, `entitlements` — **exist now, unused/all-access by default.**
  Turning on billing later means inserting plan rows and flipping one enforcement
  flag, not building a new subsystem under launch pressure.

## 8. Data retention & security (decision made)
Store user CVs, application history, and stats — but with limits, not unbounded
retention:
- Encrypt CV files and PII at rest (standard DB-level encryption is enough at this
  scale; no need for field-level encryption yet).
- Cap stored tailored-CV versions per user (e.g. last 20; configurable, same
  puzzle-piece pattern as the template limit).
- Never store job-site passwords — OAuth tokens only, scoped and revocable.
- Build a "export my data" / "delete my account" path now, even if manual at MVP
  size — retrofitting this after EU users sign up is far more painful than
  building it in from the start (GDPR applies the moment an EU user signs up,
  regardless of where the company is based).

## 9. Tech stack (confirmed)
- **Backend:** FastAPI (matches existing skillset; no reason to switch).
- **Primary DB:** PostgreSQL — relational data (accounts, jobs, applications) fits
  it better than a document store, and it's what the multi-tenant schema above
  assumes.
- **Cache / state:** Redis — session state, rate-limit counters, job-queue backing.
- **Vector search:** Qdrant — already proven in the Betopia Sales Agent, reuse the
  same operational knowledge for match scoring.
- **Task queue:** add Celery or a lighter alternative (e.g. Arq) once CV
  generation/email sending needs to run async instead of blocking a request —
  not needed for a single-user MVP, but the schema above doesn't block adding it.

## 10. Hosting (OPEN — still genuinely undecided)
Options, cheapest/simplest first:
1. **Single VPS + Docker Compose** (Hetzner, DigitalOcean) — matches your existing
   Caddy VPS experience directly; cheapest; fine until real concurrent-user load.
2. **Managed container platform** (Render, Railway, Fly.io) — less ops work, costs
   more per unit of compute, easier to scale incrementally.
3. **Full cloud (AWS/GCP) with managed Postgres/Redis** — only justified once
   you have paying users and uptime/SLA actually matters.
**Recommendation for the 1-month MVP:** option 1. You already know this stack from
the Caddy VPS deployment; don't add a new ops learning curve while also building
the product. Revisit at Phase 3 (SaaS launch) scale.

## 11. LLM provider strategy (confirmed)
- **MVP:** OpenAI only.
- **Planned:** OpenAI → Claude fallback chain.
- **Puzzle piece:** build the LLM call behind a single internal interface
  (`generate(prompt, context) -> text`) from day one, exactly like the Betopia
  Sales Agent's multi-provider router. Adding the Claude fallback later is then
  one new implementation of that interface plus a routing rule — not a rewrite
  of every place that currently calls OpenAI directly.

## 12. Payments (research complete — decision still yours to make)
**The constraint that matters:** Stripe does not accept businesses registered in
Bangladesh. This is settled, not a guess — check before building anything on the
assumption Stripe is available.

**What does work from Bangladesh:**
| Option | Model | Notes |
|---|---|---|
| **Paddle** | Merchant of Record | Explicitly supports Bangladesh-registered sellers; handles global tax compliance (VAT/GST/sales tax) for you — relevant the moment an EU user subscribes; standard MoR fee (~5% + $0.50/transaction) |
| **Dodo Payments** | Merchant of Record | Also explicitly targets solo/indie SaaS founders; priced competitively with Paddle; worth a side-by-side before committing |
| **Lemon Squeezy** | Merchant of Record | Technically works, but now owned by Stripe and being folded into "Stripe Managed Payments" — adopting it today means building on a product mid-transition |
| Stripe (direct) | Payment processor | **Not available** — Bangladesh isn't a supported seller country |

**Recommendation:** Paddle, for the MoR tax handling alone — once you have an EU
subscriber, you are legally liable for VAT unless something handles it for you.
Defer actually wiring this up (per your "set up later" answer) — but the
`subscription_plans`/`entitlements` tables in §7 are designed so Paddle's webhook
events slot in without a schema change when you're ready.

## 13. SaaS-only concerns still ahead (Phase 3+)
- Legal review of ToS exposure from the JSearch aggregator layer, once it's added.
- Per-user OAuth scopes for email sending — design the minimal scope set needed
  (send-only, not full inbox access) before requesting it from Google/Microsoft.
- Rate limiting and cost caps on LLM calls per account, before any paid tier exists
  (a free-tier abuse case is a real cost risk even pre-launch).

## 14. Decision log
| Date | Decision | Reasoning |
|---|---|---|
| 2026-10-04 | Build multi-tenant schema from day 1, single user initially | Avoid rearchitecting later; explicit goal stated |
| 2026-10-04 | No auto-send tier, ever | Legal/reputational buffer; locked, not revisit-under-pressure |
| 2026-10-04 | No direct LinkedIn/Facebook scraping or stored passwords for the SaaS | ToS risk unacceptable at multi-tenant scale |
| 2026-10-04 | Job sourcing: Adzuna/Remotive/RemoteOK/Greenhouse-Lever APIs for MVP; JSearch (RapidAPI) added later for LinkedIn/Indeed coverage | Zero-ToS-risk MVP, documented path to broader coverage |
| 2026-10-04 | Stack: FastAPI + Postgres + Redis + Qdrant | Matches skillset, proven in Betopia Sales Agent |
| 2026-10-04 | Hosting: single VPS + Docker Compose for MVP | Matches existing ops experience; revisit at scale |
| 2026-10-04 | Payments: Paddle recommended (Stripe unavailable from Bangladesh) | MoR handles global tax; setup deferred |
| 2026-10-04 | Pricing model, team structure beyond solo | Still OPEN — intentionally deferred, schema supports it |

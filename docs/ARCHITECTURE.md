# Architecture — Job Application Agent SaaS

Status: Core decisions below are now DECIDED (2026-10-04, updated 2026-10-18) based
on Niloy's answers and validated patterns from ai-job-search-dev/ai-job-search (MIT,
64k stars, author-verified outcome). Remaining (OPEN) items are genuinely still
open — don't guess at these.

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
- **Parallel personal use (decided 2026-10-18):** while this SaaS is being built,
  Niloy may also run his own job search through a private fork of
  ai-job-search-dev/ai-job-search (a separate, non-SaaS, Claude-Code-based tool).
  That fork never becomes part of this codebase and never touches this schema —
  it's a stopgap so the job search doesn't wait on the SaaS build, and a source of
  real-world lessons to feed back into this architecture before Phase 1 ends.

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
This extends to follow-ups (§6): drafted, never auto-sent.

## 4. Module 1 — Find Job Opportunity (decision made)

**Decision:** no direct scraping of LinkedIn/Facebook with stored passwords, ever,
for the SaaS. Layered sourcing instead:

| Layer | Source | Legal status | Coverage |
|---|---|---|---|
| 1 | **Adzuna API** (official) | Fully legal, direct | Broad, 19 countries, decent EU/remote coverage |
| 1 | **Remotive API**, **RemoteOK API** | Fully legal, direct | Remote-specific roles |
| 1 | **Greenhouse / Lever / Ashby public job-board APIs** | Fully legal, direct | Per-company — ideal for the user's "Target Company" list |
| 1 | **freehire.me aggregator API** (added 2026-10-18) | Fully legal, direct — public REST API, no key, MIT-licensed, self-hostable | Tech-focused (software/data/engineering/DevOps/remote), structured results (skills, seniority, category); validated in ai-job-search-dev/ai-job-search |
| 1b | **LinkedIn public `jobs-guest` endpoint** (added 2026-10-18) | Unauthenticated, no stored credentials — but LinkedIn's ToS still prohibits automated access. Fine for Niloy's own personal use (low volume); **do not expose this source to other SaaS users** without a separate legal review, since "no password stored" doesn't mean "ToS-compliant at multi-tenant volume." | LinkedIn listings, zero-cost |
| 2 | **JSearch (via RapidAPI)** | Legal to *us* — paid vendor aggregating LinkedIn/Indeed/Glassdoor/ZipRecruiter under its own ToS. We're a customer, not a scraper. | Fills gaps Layer 1 can't reach |
| — | Direct LinkedIn/Facebook scraping or credential storage | **Never**, for the SaaS | N/A |

Start with Layer 1 only for the MVP (zero ToS exposure, enough coverage to prove the
product). Layer 1b (LinkedIn public endpoint) may be used in Niloy's own account
only, behind a feature flag that defaults off for every other account — do not wire
it into the general `JobSource` rotation other users get. Add JSearch in Phase 2+
once there's budget and the product needs broader coverage.

**Puzzle piece:** the job-ingestion layer is a plugin interface
(`JobSource.fetch(query) -> list[JobPosting]`), so adding/removing a source later
never touches the rest of the pipeline.

**Security — posting integrity gate (added 2026-10-18, non-negotiable):** every
fetched job posting is untrusted input before it ever reaches an LLM. Before a
posting is scored, summarized, or tailored against, run it through an integrity
gate that strips hidden/invisible text and flags instruction-shaped lines (a
posting trying to tell the agent what to do). This is the same defense
ai-job-search-dev/ai-job-search ships as `posting_guard.py` — a job description is
exactly the kind of field a prompt-injection attempt would target, and nothing in
this architecture defended against that until now. The agents that fetch and
evaluate postings are read-only with respect to anything the posting asks them to
do; postings never grant tool access or change agent behavior.

**Match scoring — two layers, not one:**
1. **Coarse ranking:** embed MASTER_CV.tex + USER_PROFILE.md target roles, embed
   each job description, rank by cosine similarity in Qdrant. Cheap, explainable,
   needs no training data.
2. **Deal-breaker / language gate (added 2026-10-18):** a posting that fails a
   hard deal-breaker (declared in USER_PROFILE.md, free-text) is vetoed regardless
   of similarity score. Language is a dedicated, structured check: a posting
   requiring a language the user hasn't declared at all is hard-rejected; one
   asking for a higher level than the user declared is flagged (not auto-rejected)
   so a borderline case gets human judgment instead of a silent drop.
3. Upgrade path (unchanged): move coarse ranking to LLM-scored fit later if
   embedding similarity alone proves too coarse.

## 5. Module 2 — Apply for the Job

Flow: tailor CV once per job → branch into mail/form/DM → Draft → human review →
Send. Updated 2026-10-18 with a verification-loop design validated by
ai-job-search-dev/ai-job-search's production use:

**Generation — drafter + reviewer, not single-pass:**
- A "drafter" step produces the tailored CV/cover content from `01_MASTER_CV.tex` +
  `USER_PROFILE.md` + the job posting (post-integrity-gate).
- A separate "reviewer" pass (fresh context, can research the company) critiques
  the draft for missed keywords, weak framing, and generic language, then the
  drafter revises once. This catches what a single pass reliably misses.

**CV cutting — relevance-weighted, not a static order:**
- Replace the fixed "cut robotics first, then certs, then..." trim order with a
  per-line score = relevance-to-this-posting + uniqueness-in-the-document +
  whether-the-cover-letter-depends-on-it. When a tailored CV overflows the page
  limit, cut the lowest-scoring line first. An older bullet matching the posting's
  keywords should survive ahead of a recent one that doesn't — the static order in
  `01_MASTER_CV.tex`'s control block becomes a fallback/starting heuristic, not
  the final word.

**PDF verification loop (new, non-negotiable for any CV actually sent):**
- Compile the LaTeX, then programmatically inspect the rendered PDF: page count
  within target, no orphaned section headers, no font fallback artifacts. Iterate
  (`\needspace`, `\enlargethispage`, etc.) until clean. A `.tex` file that "looks
  fine in source" can still produce a broken PDF — this step catches what manual
  review of the source would miss.
- **ATS text-layer check:** extract the compiled PDF's text (`pdftotext` or
  equivalent) and verify it reads the way an ATS parser would see it — contact
  details present as literal text, no garbled glyphs, sane reading order — then
  score keyword coverage against the posting. A keyword the profile doesn't
  genuinely support is flagged as a gap, never silently stuffed in.

**CV templates (puzzle piece for the subscription plan — unchanged):**
- MVP: an admin-curated set of LaTeX templates (reuse the tagged structure from
  `01_MASTER_CV.tex` as template #1). Users pick one from a gallery.
- Schema from day one: `cv_templates` table (id, name, latex_source, is_admin_default)
  and `account_template_limit` on the accounts table (int, default = unlimited for
  now).

**Sending:** email via the user's own OAuth (Gmail/Outlook) once that's built; forms
stay browser-assisted or manual-paste for the MVP, since most have no send API.

## 6. Module 3 — Monitor Job Applications
Jobs table extended with applied-date, status, follow-up-due-date, notes. Status
summary is a query, not new logic.

**Follow-up drafting (added 2026-10-18):** an application with no response after a
configurable threshold (default 10 days) surfaces for a drafted follow-up in the
user's own writing style, using only claims already in the materials actually
submitted for that application. Draft-only, never auto-sent, and capped (default:
at most twice per application) so the feature can't turn into spam on the user's
behalf. Same human-in-the-loop gate as every other outbound message (§3).

## 7. Data model — multi-tenant from day one (puzzle piece)
Every table carries an `account_id` from the start, even with one account:
- `accounts` (id, email, plan_tier *[default: 'free', unenforced]*, created_at)
- `cv_templates`, `account_cv_versions` (which tailored CV went to which job)
- `jobs` (account_id, company, role, salary, deadline, location_type, country,
  visa_required, target_company, match_score, status, source, apply_link, found_at)
- `applications` (job_id, channel, draft_content, sent_at, status, follow_up_due,
  follow_up_count *[default 0, cap enforced in app logic per §6]*)
- `subscription_plans`, `entitlements` — **exist now, unused/all-access by default.**

## 8. Data retention & security (decision made)
- Encrypt CV files and PII at rest (standard DB-level encryption is enough at this
  scale; no need for field-level encryption yet).
- Cap stored tailored-CV versions per user (e.g. last 20; configurable).
- Never store job-site passwords — OAuth tokens only, scoped and revocable.
- Posting integrity gate (§4) runs before any posting content reaches an LLM or is
  persisted for display — treat stored posting text itself as still-untrusted on
  render (escape, don't execute).
- Build a "export my data" / "delete my account" path now, even if manual at MVP
  size.

## 9. Tech stack (confirmed)
- **Backend:** FastAPI.
- **Primary DB:** PostgreSQL.
- **Cache / state:** Redis.
- **Vector search:** Qdrant.
- **Task queue:** add Celery or Arq once CV generation/email sending needs to run
  async — not needed for a single-user MVP, but the schema doesn't block it.
- **PDF tooling (added 2026-10-18):** LaTeX compiler (`lualatex` recommended over
  `pdflatex` for modern font packages — see ai-job-search-dev/ai-job-search's
  SETUP.md for the specific font-expansion failure mode this avoids), plus
  `pdftotext` (Poppler) or `pypdf` for the ATS text-layer check in §5.

## 10. Hosting (OPEN — still genuinely undecided)
1. **Single VPS + Docker Compose** (Hetzner, DigitalOcean) — matches existing Caddy
   VPS experience; cheapest; fine until real concurrent-user load.
2. **Managed container platform** (Render, Railway, Fly.io).
3. **Full cloud (AWS/GCP)** — only justified once paying users exist.
**Recommendation for the 1-month MVP:** option 1.

## 11. LLM provider strategy (confirmed)
- **MVP:** OpenAI, selected via an admin-configurable `llm_providers` table
  (provider name, encrypted API key, active flag, priority) — not a hardcoded
  `.env` value, so a future admin screen can add/switch providers without a code
  change.
- **Planned:** OpenAI → Claude fallback chain, added as a second row in the same
  table plus a routing rule, never a rewrite of call sites.
- The drafter-reviewer pair in §5 can use the same provider interface for both
  roles, or different providers per role — the interface doesn't care.

## 12. Payments (research complete — decision still yours to make)
Stripe does not accept Bangladesh-registered businesses. Paddle (Merchant of
Record, explicitly supports Bangladesh, handles global VAT) is the recommendation;
Dodo Payments is a close alternative; Lemon Squeezy works but is mid-transition
into Stripe's own product. Setup deferred per Niloy's decision — the
`subscription_plans`/`entitlements` tables in §7 are designed so this slots in
without a schema change later.

## 13. SaaS-only concerns still ahead (Phase 3+)
- Legal review of ToS exposure from the JSearch aggregator layer, once added.
- Legal review specifically of whether Layer 1b (LinkedIn public endpoint, §4) can
  ever be offered to other users at all — current default is no, Niloy-only.
- Per-user OAuth scopes for email sending — minimal scope set, decided before
  requesting it from Google/Microsoft.
- Rate limiting and cost caps on LLM calls per account, before any paid tier exists.

## 14. Decision log
| Date | Decision | Reasoning |
|---|---|---|
| 2026-10-04 | Build multi-tenant schema from day 1, single user initially | Avoid rearchitecting later |
| 2026-10-04 | No auto-send tier, ever | Legal/reputational buffer; locked |
| 2026-10-04 | No direct LinkedIn/Facebook scraping or stored passwords for the SaaS | ToS risk unacceptable at multi-tenant scale |
| 2026-10-04 | Job sourcing: Adzuna/Remotive/RemoteOK/Greenhouse-Lever for MVP; JSearch added later | Zero-ToS-risk MVP, documented path to broader coverage |
| 2026-10-04 | Stack: FastAPI + Postgres + Redis + Qdrant | Matches skillset, proven in Betopia Sales Agent |
| 2026-10-04 | Hosting: single VPS + Docker Compose for MVP | Matches existing ops experience; revisit at scale |
| 2026-10-04 | Payments: Paddle recommended (Stripe unavailable from Bangladesh) | MoR handles global tax; setup deferred |
| 2026-10-04 | LLM: OpenAI first, admin-configurable provider table from day one | Flexibility without a future migration |
| 2026-10-18 | Adopted posting integrity gate, drafter-reviewer, PDF verification loop, ATS text-layer check, relevance-weighted CV cutting, language gate, capped follow-up drafting | Validated patterns from ai-job-search-dev/ai-job-search (MIT, author-verified outcome) |
| 2026-10-18 | Added freehire.me (Layer 1) and LinkedIn public jobs-guest endpoint (Layer 1b, Niloy-only) as sources | Zero-cost, legal (freehire.me) or low-risk personal-use (LinkedIn endpoint) coverage found via competitor research |
| 2026-10-18 | Niloy may run a parallel private fork of ai-job-search-dev/ai-job-search for his own job search during the build | Decouples "start applying now" from "SaaS build takes a month"; feeds real lessons back before Phase 1 ends |
| — | Pricing model, team structure beyond solo | Still OPEN — intentionally deferred, schema supports it |
| — | Hosting choice (§10) | Still OPEN |
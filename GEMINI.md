# Project: Job Application Agent SaaS

## What this is
A SaaS that automates a job search for the user: **Find** matching job postings,
**Apply** by tailoring a LaTeX CV and drafting outreach (email/form/DM), and
**Monitor** application status. Built by one solo developer (Niloy), currently
serving one account (himself) for ~1 month of real personal use before any other
user is onboarded. Despite that, it must be architected as true multi-tenant SaaS
from day one — see `docs/ARCHITECTURE.md` §0 for why (the "missing puzzle piece"
principle: every undecided business choice gets a real schema today with a
permissive default, so deciding it later is a data change, not a rebuild).

## Read these before writing code
- `docs/ARCHITECTURE.md` — the actual system design. This is the source of truth
  for every structural decision. If something here conflicts with it, this file
  is wrong and should be corrected, not the other way around.
- `docs/ROADMAP.md` — current phase and what's in scope right now vs. later.
  **Check "Current phase" before starting any task** — don't build Phase 2/3
  features while Phase 0 is incomplete.
- `docs/RESEARCH.md` — why certain external choices were made (job-data APIs,
  payments provider), so you don't re-litigate settled research.
- `cv_templates/01_MASTER_CV.tex` — the first CV template, tagged with the rules
  the CV-tailoring feature must follow (see its own control-block comments).

## Non-negotiables (do not redesign these without being asked)
1. **Human-in-the-loop on Send, always.** Every application flow ends at
   Draft → human reviews → Send. No auto-send path, no exceptions, no "premium
   tier" that skips it. (`ARCHITECTURE.md` §3)
2. **No LinkedIn/Facebook scraping, no stored third-party passwords.** Job
   sourcing uses only official/legal APIs (Adzuna, Remotive, RemoteOK,
   Greenhouse/Lever) for the MVP. (`ARCHITECTURE.md` §4)
3. **Multi-tenant schema from the first migration.** Every table carries
   `account_id`, even though there's one account right now. (`ARCHITECTURE.md` §7)
4. **LLM calls go through a single provider-abstraction interface,** never a
   direct OpenAI/Anthropic call scattered in business logic. Current plan: OpenAI
   only at MVP, with an **admin-configurable provider + API key** (not just a
   `.env` value) so a non-technical future admin screen can add/switch providers
   without a code change. Build the abstraction so adding a provider is a new
   implementation of the interface plus a config row — not a refactor.
5. **Never invent CV facts.** `01_MASTER_CV.tex` (or whichever template is active)
   is the only source of truth for a user's experience — the tailoring feature
   reorders/trims/rewords, it never adds a fact that isn't in the source file.

## Current priority (per ROADMAP.md Phase 0)
Build order is locked: **Find → Apply → Monitor**. Don't start Apply-module code
until Find is working end-to-end (job fetch → store → match-score → ranked
queue). A half-working Find module makes every downstream feature untestable.

## Tech stack (decided, don't re-propose alternatives)
FastAPI, PostgreSQL, Redis, Qdrant. Single VPS + Docker Compose for hosting at
MVP size (see `ARCHITECTURE.md` §9-10 for reasoning).

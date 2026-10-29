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

## Current priority (per ROADMAP.md Phase 0 → 1)
All three core modules (**Find → Apply → Monitor**) plus **STAR Interview Coach**,
**Profile Management**, **Superadmin Control Center** (with multi-tenant management,
dynamic LLM failover ping testing, and one-click "Test As Tenant" QA dogfooding mode),
**Public SaaS Landing Page**, and **Unified JWT Authentication Engine** (with bcrypt
password hashing and automatic role-based routing between SuperAdmin Ops Center and
Candidate OS) are built end-to-end with 151 passing tests and a live React dashboard
backed by Supabase PostgreSQL, protected by a bedrock `.env` LLM fallback chain, frosted glassmorphism overlays with intact sidebar, and an ECC-adapted 5-phase verification loop (`scripts/verify.py`). The current focus is running Niloy's live job search through
the system (Phase 1 personal validation), refining match scoring, and verifying outreach
quality while strictly maintaining the non-negotiables.

## Tech stack (decided, don't re-propose alternatives)
- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL (Supabase / local pooler) / SQLite (dev), Redis, Qdrant.
- **Frontend**: Vite, React 19, Vanilla CSS (Obsidian & Cyber Emerald design system).
- **Architecture Navigation**: Graphify (`graphify-out/` local AST knowledge graph).
- **Hosting**: Single VPS + Docker Compose for MVP (see `ARCHITECTURE.md` §9-10).


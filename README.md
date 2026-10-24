# Job Application Agent SaaS

Personal job-search automation (Find → Apply → Monitor), built multi-tenant
from day one. See `GEMINI.md` for project context and `docs/ARCHITECTURE.md`
for the full design.

## Current status
Phase 0 (MVP build) — see `docs/ROADMAP.md` for the live checklist.

## Local setup
1. `cp infra/.env.example infra/.env` and fill in your OpenAI API key and DB creds.
2. `docker compose -f infra/docker-compose.yml up -d` (Postgres, Redis, Qdrant).
3. `cd backend && pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`

## Docs index
- `docs/IDEA.md` — original concept
- `docs/ARCHITECTURE.md` — system design, decided + open items
- `docs/ROADMAP.md` — phases and current checklist
- `docs/RESEARCH.md` — competitor/API/payments research backing the decisions
- `docs/USER_PROFILE.md` — the account owner's own context (for CV tailoring tests)

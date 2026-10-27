# Job Application Agent SaaS

Personal job-search automation (Find → Apply → Monitor), built multi-tenant
from day one. See `GEMINI.md` for project context and `docs/ARCHITECTURE.md`
for the full design.

## Current status
Phase 0 → Phase 1 transition. Find, Apply, Monitor, STAR Interview Coach, Profile Management, and Superadmin Control Center are operational end-to-end with 142 passing tests and a React frontend dashboard connected to Supabase PostgreSQL.

## Local setup

### 1. Backend Setup
```bash
# Optional infra (Postgres, Redis, Qdrant)
docker compose -f infra/docker-compose.yml up -d

# Environment setup & dependencies
cd backend
pip install -r requirements.txt

# Run migrations & start dev server
uvicorn app.main:app --reload
```
API runs at `http://127.0.0.1:8000` (docs at `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
UI runs at `http://localhost:5173` with Obsidian & Cyber Emerald theme featuring:
- **Dashboard**: High-level metrics, funnel distribution, quick actions.
- **Jobs Queue**: Ranked by match score, radial gauges, posting guard inspections, attribution badges.
- **Application Studio**: Fit Evaluator, Drafter + Reviewer CV tailoring, ATS text-layer validation, LaTeX source editor, multi-channel outreach generator.
- **Pipeline Monitor**: Kanban tracker from Draft to Offer/Rejected, capped 10-day follow-up drafter.
- **STAR Interview Coach**: Story bank manager, question generator matching job requirements, AI answer critique.
- **Profile Settings**: Target designations, locations, compensation, spoken languages, dealbreakers.
- **Superadmin Control Center**: Multi-tenant metrics, tenant directory, dynamic LLM failover ping testing, LaTeX template manager, prompt injection audit log, and one-click "Test As Tenant" QA dogfooding mode.

### 3. Tests
```powershell
& "backend\.venv\Scripts\python.exe" -m pytest backend/tests/
```

### 4. Codebase Knowledge Graph (Graphify)
The codebase includes a local Graphify knowledge graph for architecture exploration and AST-level symbol resolution:
```bash
# Query architecture / dependency paths
python -m graphify query "How does job ingestion work?"
python -m graphify path "JobIngestionService" "MatchingService"

# Visualizations
open graphify-out/graph.html                  # Interactive 3D/2D node graph
open graphify-out/job-agent-saas-callflow.html # Mermaid architecture & call-flow diagrams
open graphify-out/GRAPH_TREE.html             # D3 collapsible tree view
open graphify-out/wiki/index.md               # Community wiki articles
```

## Docs index
- `docs/IDEA.md` — original concept
- `docs/ARCHITECTURE.md` — system design, decided + open items
- `docs/ROADMAP.md` — phases and current checklist
- `docs/RESEARCH.md` — competitor/API/payments research backing the decisions
- `docs/USER_PROFILE.md` — the account owner's own context (for CV tailoring tests)
- `graphify-out/GRAPH_REPORT.md` — AST knowledge graph report & community breakdown


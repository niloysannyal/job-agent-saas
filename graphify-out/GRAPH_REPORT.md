# Graph Report - job-agent-saas  (2026-10-28)

## Corpus Check
- 132 files · ~90,466 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 4, .css 2, .ini 1)

## Summary
- 1349 nodes · 3358 edges · 83 communities (67 shown, 16 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 400 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c2d8d285`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- Job
- api/profile.py
- models/__init__.py
- JobSearchQuery
- TestClient
- test_profile.py
- LLMService
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- evaluate_job_fit
- test_auth.py
- get_available_sources
- package.json
- LeverJobSource
- RemotiveJobSource
- api/interview.py
- matching/__init__.py
- typing
- TestClient
- job.py
- What You Must Do When Invoked
- alembic
- test_matching.py
- Architecture — Job Application Agent SaaS
- LanguageGate
- MatchingService
- Settings
- Account
- MockQdrantClient
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobPosting
- test_models.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_cv_tailor_service_end_to_end
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- LLMProviderConfig
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- client
- Project: Job Application Agent SaaS
- Roadmap — Job Application Agent SaaS
- Multi-Tenant SaaS Auditor
- Application
- attribution-and-scraping.md
- human-in-the-loop.md
- test_adzuna_fetch_with_mock_client
- compute_cosine_similarity
- plan_relevance_cuts
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- client
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- core/auth.py
- .generate
- audit_fact_integrity
- db_session
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- .to_dict
- theme.js
- devDependencies
- main.jsx
- prune_and_budget_latex
- .__init__

## God Nodes (most connected - your core abstractions)
1. `Account` - 115 edges
2. `JobPosting` - 74 edges
3. `JobSearchQuery` - 62 edges
4. `Job` - 61 edges
5. `Base` - 49 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 35 edges
8. `run_posting_guard()` - 32 edges
9. `Application` - 31 edges
10. `UserProfile` - 26 edges

## Surprising Connections (you probably didn't know these)
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `4. Module 1 — Find Job Opportunity (decision made)` --references--> `SpokenLanguage`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/models/profile.py

## Import Cycles
- None detected.

## Communities (83 total, 16 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.13
Nodes (21): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), JobDetailModal(), formatSalary() (+13 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.16
Nodes (20): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body(), Strips lines starting with %% (agent control notes) while preserving actual…, Escapes LaTeX special characters (% & $ # _) if they are not already escaped.… (+12 more)

### Community 3 - "Job"
Cohesion: 0.06
Nodes (58): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+50 more)

### Community 4 - "api/profile.py"
Cohesion: 0.08
Nodes (63): add_designation(), add_language(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation() (+55 more)

### Community 5 - "models/__init__.py"
Cohesion: 0.14
Nodes (27): ApplicationBase, ApplicationCreate, ApplicationUpdate, BaseModel, AccountCvVersionBase, AccountCvVersionUpdate, CvTemplateBase, CvTemplateCreate (+19 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.10
Nodes (19): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any (+11 more)

### Community 7 - "TestClient"
Cohesion: 0.12
Nodes (17): TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations., GET and PUT on compensation expectations., CRUD operations on spoken languages., Verify complete isolation between tenants A and B for profile and related…, GET /api/v1/profile returns null when account has no profile. (+9 more)

### Community 8 - "test_profile.py"
Cohesion: 0.10
Nodes (26): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+18 more)

### Community 9 - "LLMService"
Cohesion: 0.14
Nodes (19): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for… (+11 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Asynchronously fetch all open job postings for a company from Greenhouse. Pass… (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "evaluate_job_fit"
Cohesion: 0.07
Nodes (30): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_monitor_summary(), list_applications() (+22 more)

### Community 14 - "test_auth.py"
Cohesion: 0.09
Nodes (36): get_me(), login(), get, post, Session, Retrieve authenticated account profile and permissions from validated token., Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated… (+28 more)

### Community 15 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (20): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+12 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.10
Nodes (20): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+12 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.13
Nodes (29): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+21 more)

### Community 20 - "matching/__init__.py"
Cohesion: 0.11
Nodes (15): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+7 more)

### Community 21 - "typing"
Cohesion: 0.22
Nodes (9): MatchingResult, Summary of a match scoring run., dataclasses, logging, pathlib, pydantic_settings, qdrant_client_models, sys (+1 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 23 - "job.py"
Cohesion: 0.21
Nodes (16): asyncio, JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, JobSourceConfigError, JobSourceError, JobSourceHTTPError, Raised when an external job source HTTP request fails. (+8 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.11
Nodes (5): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 26 - "test_matching.py"
Cohesion: 0.11
Nodes (21): db_session(), asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']., Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+13 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (18): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed) (+10 more)

### Community 28 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 29 - "MatchingService"
Cohesion: 0.16
Nodes (12): ParsedProfile, ProfileParser, Path, Structured representation of parsed user profile and CV., Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, Extract readable text from LaTeX CV, stripping comments and common markup., MatchingService, Path (+4 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "Account"
Cohesion: 0.13
Nodes (17): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories. (+9 more)

### Community 32 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.20
Nodes (17): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+9 more)

### Community 40 - "JobPosting"
Cohesion: 0.15
Nodes (12): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobUpdate, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+4 more)

### Community 41 - "test_models.py"
Cohesion: 0.15
Nodes (31): get_llm_service(), Dependency provider for LLMService., Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, Base, Base SQLAlchemy declarative model. (+23 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.15
Nodes (28): create_admin_template(), create_tenant(), get_job_sources(), get_platform_metrics(), JobSourceInfo, list_admin_templates(), list_flagged_jobs(), list_tenants() (+20 more)

### Community 45 - "test_cv_tailor_service_end_to_end"
Cohesion: 0.27
Nodes (5): Any, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, test_cv_tailor_service_end_to_end()

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "LLMProviderConfig"
Cohesion: 0.26
Nodes (13): create_llm_provider(), delete_admin_template(), delete_llm_provider(), delete_tenant(), impersonate_tenant(), list_llm_providers(), delete, post (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 55 - "Application"
Cohesion: 0.11
Nodes (17): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Verify that deleting an account cascades to all tenant-scoped rows., Test seed_initial_data populates default templates, plans, entitlements, and… (+9 more)

### Community 58 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 59 - "compute_cosine_similarity"
Cohesion: 0.50
Nodes (4): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Verify cosine similarity calculation edge cases and bounds., test_compute_cosine_similarity()

### Community 60 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.35
Nodes (13): ApplicationStudio(), cleanLatexInline(), compactLatex(), compactLatexToTwoPages(), compileParsedLatexToPdf(), decodeHtmlEntities(), estimateItemHeight(), extractLinksFromLatex() (+5 more)

### Community 63 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 64 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 65 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 66 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 67 - "client"
Cohesion: 0.40
Nodes (3): api_test_db(), client(), fixture

### Community 70 - "core/auth.py"
Cohesion: 0.25
Nodes (8): decode_access_token(), get_current_account(), Session, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, Ensure the caller has superadmin role privileges., require_superadmin(), jwt

### Community 74 - "audit_fact_integrity"
Cohesion: 0.29
Nodes (5): audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, Verify that truth metrics pass and invented claims fail., test_fact_ledger_integrity()

### Community 75 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 84 - "main.jsx"
Cohesion: 0.50
Nodes (3): App(), frontend_src_index, react-dom

## Knowledge Gaps
- **144 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+139 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 543 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `Job`, `api/profile.py`, `models/__init__.py`, `TestClient`, `test_profile.py`, `test_auth.py`, `api/interview.py`, `TestClient`, `job.py`, `test_matching.py`, `test_admin.py`, `test_models.py`, `admin.py`, `test_cv_tailor_service_end_to_end`, `LLMProviderConfig`, `client`, `Application`, `core/auth.py`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `Job`, `models/__init__.py`, `JobSearchQuery`, `test_models.py`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `get_available_sources`, `LeverJobSource`, `RemotiveJobSource`, `typing`, `job.py`, `test_adzuna_fetch_with_mock_client`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `test_admin.py`, `models/__init__.py`, `test_profile.py`, `test_models.py`, `admin.py`, `evaluate_job_fit`, `test_cv_tailor_service_end_to_end`, `api/interview.py`, `typing`, `TestClient`, `job.py`, `Application`, `test_matching.py`, `MatchingService`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 69 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Job` (e.g. with `get_job_sources()` and `get_platform_metrics()`) actually correct?**
  _`Job` has 25 INFERRED edges - model-reasoned connections that need verification._
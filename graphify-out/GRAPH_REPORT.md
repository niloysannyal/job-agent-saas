# Graph Report - job-agent-saas  (2026-10-28)

## Corpus Check
- 126 files · ~86,106 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 4, .css 2, .ini 1)

## Summary
- 1293 nodes · 3205 edges · 81 communities (63 shown, 18 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 383 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c3ceff73`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- test_job_ingestion.py
- api/profile.py
- models/__init__.py
- JobSearchQuery
- Account
- env.py
- LLMService
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- tailor_application
- CvTemplate
- get_available_sources
- Job
- LeverJobSource
- RemotiveJobSource
- api/interview.py
- test_matching.py
- typing
- TestClient
- job.py
- What You Must Do When Invoked
- alembic
- test_matching_service_score_and_gate_clean_jobs
- Architecture — Job Application Agent SaaS
- LanguageGate
- MatchingService
- Settings
- TestClient
- MockQdrantClient
- User Profile — Niloy Sannyal
- .oxlintrc.json
- tenant_client
- tests/api/__init__.py
- Base
- account.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- CVTailorService
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- client
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- JobPosting
- Project: Job Application Agent SaaS
- Roadmap — Job Application Agent SaaS
- Multi-Tenant SaaS Auditor
- test_seed_initial_data
- attribution-and-scraping.md
- human-in-the-loop.md
- test_adzuna_fetch_with_mock_client
- trigger_ingestion
- plan_relevance_cuts
- graphify reference: extra exports and benchmark
- test_interview.py
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- client
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- get_current_account
- .generate
- .generate
- .generate
- db_session
- db_session
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- .to_dict
- .generate

## God Nodes (most connected - your core abstractions)
1. `Account` - 100 edges
2. `JobPosting` - 74 edges
3. `JobSearchQuery` - 62 edges
4. `Job` - 61 edges
5. `Base` - 47 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 35 edges
8. `run_posting_guard()` - 32 edges
9. `Application` - 31 edges
10. `UserProfile` - 26 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `4. Module 1 — Find Job Opportunity (decision made)` --references--> `SpokenLanguage`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/models/profile.py
- `Integration Checklist` --references--> `JobIngestionService`  [INFERRED]
  .agents/skills/job-source-integrator/SKILL.md → backend/app/services/job_ingestion.py
- `Integration Checklist` --references--> `JobSource`  [INFERRED]
  .agents/skills/job-source-integrator/SKILL.md → backend/app/services/job_sources/base.py

## Import Cycles
- None detected.

## Communities (81 total, 18 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.05
Nodes (60): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, oxlint, @types/react (+52 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.15
Nodes (20): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+12 more)

### Community 3 - "test_job_ingestion.py"
Cohesion: 0.10
Nodes (32): IngestionResult, JobIngestionService, Any, Session, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, db_session() (+24 more)

### Community 4 - "api/profile.py"
Cohesion: 0.09
Nodes (58): add_designation(), add_language(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation() (+50 more)

### Community 5 - "models/__init__.py"
Cohesion: 0.12
Nodes (35): AccountBase, AccountCreate, AccountRead, AccountUpdate, BaseModel, ApplicationBase, ApplicationCreate, ApplicationRead (+27 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.10
Nodes (19): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any (+11 more)

### Community 7 - "Account"
Cohesion: 0.11
Nodes (25): delete_admin_template(), delete_llm_provider(), delete_tenant(), delete, Ensure the caller has superadmin role privileges., require_superadmin(), Account, Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an… (+17 more)

### Community 8 - "env.py"
Cohesion: 0.20
Nodes (10): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), normalize_db_url(), Normalize database URL for driver compatibility., logging_config (+2 more)

### Community 9 - "LLMService"
Cohesion: 0.19
Nodes (16): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…, LLMService (+8 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Asynchronously fetch all open job postings for a company from Greenhouse. Pass… (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "tailor_application"
Cohesion: 0.10
Nodes (27): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_monitor_summary(), list_applications() (+19 more)

### Community 14 - "CvTemplate"
Cohesion: 0.32
Nodes (8): create_admin_template(), TemplateInput, update_admin_template(), CvTemplate, CvTemplateRead, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., test_cv_template_and_version_models()

### Community 15 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 16 - "Job"
Cohesion: 0.11
Nodes (25): mark_application_sent(), Strict Human-in-the-loop Send gate: Only a human can trigger this endpoint to…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, test_get_metrics(), Session (+17 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.10
Nodes (20): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+12 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.11
Nodes (31): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+23 more)

### Community 20 - "test_matching.py"
Cohesion: 0.11
Nodes (20): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+12 more)

### Community 21 - "typing"
Cohesion: 0.26
Nodes (8): MatchingResult, Summary of a match scoring run., dataclasses, logging, pathlib, pydantic_settings, qdrant_client_models, typing

### Community 22 - "TestClient"
Cohesion: 0.12
Nodes (17): TestClient, Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged)., include_flagged=True must include flagged postings (unless also vetoed)., show_all=True must include all jobs (both vetoed and flagged) for human review., Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…, Verify limit and offset pagination parameters work correctly. (+9 more)

### Community 23 - "job.py"
Cohesion: 0.21
Nodes (16): asyncio, JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, JobSourceConfigError, JobSourceError, JobSourceHTTPError, Raised when an external job source HTTP request fails. (+8 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.13
Nodes (5): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 26 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.11
Nodes (18): db_session(), asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']., Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+10 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (18): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed) (+10 more)

### Community 28 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 29 - "MatchingService"
Cohesion: 0.13
Nodes (14): ParsedProfile, ProfileParser, Path, Structured representation of parsed user profile and CV., Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, Extract readable text from LaTeX CV, stripping comments and common markup., MatchingService, Any (+6 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 32 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "tenant_client"
Cohesion: 0.36
Nodes (9): admin_client(), override_current_account(), override_get_db(), fixture, Session, regular_tenant_account(), superadmin_account(), tenant_client() (+1 more)

### Community 40 - "Base"
Cohesion: 0.09
Nodes (35): get_llm_service(), Dependency provider for LLMService., Base, Base SQLAlchemy declarative model., Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), get_db() (+27 more)

### Community 41 - "account.py"
Cohesion: 0.26
Nodes (15): TailorResponse, AccountCvVersion, AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionRead, AccountCvVersionUpdate, CvTemplateUpdate, BaseModel (+7 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.16
Nodes (31): create_llm_provider(), create_tenant(), get_job_sources(), get_platform_metrics(), impersonate_tenant(), JobSourceInfo, list_admin_templates(), list_flagged_jobs() (+23 more)

### Community 45 - "CVTailorService"
Cohesion: 0.12
Nodes (12): CVTailorResult, CVTailorService, prune_and_budget_latex(), Session, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Selects the best fact-verified Summary variant based on role keywords., Executes the full Drafter -> Reviewer -> Fact Audit -> Persistence pipeline…, Budgets and prunes the Master CV body to strictly 1-2 pages matching… (+4 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "client"
Cohesion: 0.22
Nodes (10): client(), fixture, Session, In-memory SQLite database session with static pool for testing., FastAPI TestClient with overridden get_db dependency., Seed test accounts for multi-tenant isolation tests., Seed a variety of jobs: - High match score, clean - Mid match score, clean -…, seeded_accounts() (+2 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "JobPosting"
Cohesion: 0.15
Nodes (12): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobUpdate, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+4 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 55 - "test_seed_initial_data"
Cohesion: 0.18
Nodes (11): Session, Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Test seed_initial_data populates default templates, plans, entitlements, and…, Test StarStory model creation, tags, and account cascade., Test Account model defaults and multi-tenant fields., Test Job model matches ARCHITECTURE.md §7: (account_id, company, role, salary,…, test_account_model(), test_job_model_matching_architecture_spec() (+3 more)

### Community 58 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 59 - "trigger_ingestion"
Cohesion: 0.18
Nodes (12): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+4 more)

### Community 60 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "test_interview.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

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

### Community 70 - "get_current_account"
Cohesion: 0.67
Nodes (3): get_current_account(), Session, Resolve the current authenticated account context. Checks X-Account-ID header…

### Community 74 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 75 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

## Knowledge Gaps
- **144 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+139 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 530 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `test_job_ingestion.py`, `models/__init__.py`, `JobSearchQuery`, `Base`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `get_available_sources`, `LeverJobSource`, `RemotiveJobSource`, `typing`, `job.py`, `test_adzuna_fetch_with_mock_client`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `test_job_ingestion.py`, `api/profile.py`, `models/__init__.py`, `tailor_application`, `CvTemplate`, `Job`, `test_matching.py`, `job.py`, `test_matching_service_score_and_gate_clean_jobs`, `TestClient`, `tenant_client`, `Base`, `account.py`, `admin.py`, `CVTailorService`, `client`, `test_seed_initial_data`, `test_interview.py`, `get_current_account`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `test_job_ingestion.py`, `models/__init__.py`, `Base`, `account.py`, `admin.py`, `tailor_application`, `CVTailorService`, `CvTemplate`, `client`, `api/interview.py`, `test_matching.py`, `typing`, `test_seed_initial_data`, `job.py`, `test_matching_service_score_and_gate_clean_jobs`, `trigger_ingestion`, `MatchingService`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Job` (e.g. with `get_job_sources()` and `get_platform_metrics()`) actually correct?**
  _`Job` has 25 INFERRED edges - model-reasoned connections that need verification._
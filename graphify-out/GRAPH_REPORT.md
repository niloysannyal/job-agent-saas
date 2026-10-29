# Graph Report - job-agent-saas  (2026-10-29)

## Corpus Check
- 151 files · ~98,757 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 4, .css 2, .ini 1)

## Summary
- 1458 nodes · 3494 edges · 91 communities (78 shown, 13 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 412 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c3cb3297`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobIngestionService
- api/profile.py
- Job
- JobSearchQuery
- client
- session.py
- LLMService
- JobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- test_auth.py
- account.py
- package.json
- lever.py
- RemotiveJobSource
- api/interview.py
- embedding.py
- typing
- test_jobs.py
- job.py
- What You Must Do When Invoked
- alembic
- test_matching.py
- Architecture — Job Application Agent SaaS
- LanguageGate
- .score_and_gate_jobs
- Settings
- api/auth.py
- JobPosting
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- LinkedInJobSource
- models/__init__.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_greenhouse_fetch_with_mock_client
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Account
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Roadmap — Job Application Agent SaaS
- Project: Job Application Agent SaaS
- UserProfile
- Multi-Tenant SaaS Auditor
- test_models.py
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- pathlib
- trigger_ingestion
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- TestClient
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- client
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- test_profile.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- FastAPI Backend Development Standards (adapted from ECC)
- React Frontend Development Standards (adapted from ECC)
- Security & Tenancy Policy (adapted from ECC AgentShield)
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- get_me
- db_session

## God Nodes (most connected - your core abstractions)
1. `Account` - 119 edges
2. `JobPosting` - 74 edges
3. `Job` - 64 edges
4. `JobSearchQuery` - 62 edges
5. `Base` - 49 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 35 edges
8. `run_posting_guard()` - 32 edges
9. `Application` - 31 edges
10. `UserProfile` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `4. Pydantic Schemas & Security` --references--> `LLMProviderRead`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/models/llm_provider.py

## Import Cycles
- None detected.

## Communities (91 total, 13 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.13
Nodes (21): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), JobDetailModal(), formatSalary() (+13 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.06
Nodes (47): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult (+39 more)

### Community 3 - "JobIngestionService"
Cohesion: 0.10
Nodes (28): IngestionResult, JobIngestionService, Any, Session, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, MockGeneralSource (+20 more)

### Community 4 - "api/profile.py"
Cohesion: 0.14
Nodes (32): add_designation(), add_language(), add_location(), create_profile(), _get_or_create_profile(), patch, post, Profile management API — CRUD for UserProfile, TargetDesignation,… (+24 more)

### Community 5 - "Job"
Cohesion: 0.19
Nodes (16): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+8 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.08
Nodes (28): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), Any, AsyncClient (+20 more)

### Community 7 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 8 - "session.py"
Cohesion: 0.14
Nodes (18): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+10 more)

### Community 9 - "LLMService"
Cohesion: 0.06
Nodes (39): Session, LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any (+31 more)

### Community 10 - "JobSource"
Cohesion: 0.11
Nodes (22): asyncio, JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date() (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.08
Nodes (40): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_llm_service(), get_monitor_summary() (+32 more)

### Community 14 - "test_auth.py"
Cohesion: 0.18
Nodes (19): create_access_token(), Generate a cryptographically signed JWT access token. Contains subject…, auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user() (+11 more)

### Community 15 - "account.py"
Cohesion: 0.28
Nodes (14): Base, Base SQLAlchemy declarative model., Multi-tenant STAR Interview Coach models. Stores STAR-format interview stories…, api_test_db(), api_test_db(), db_session(), In-memory SQLite session for testing ingestion., bcrypt (+6 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (20): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+12 more)

### Community 17 - "lever.py"
Cohesion: 0.11
Nodes (20): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+12 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.15
Nodes (27): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+19 more)

### Community 20 - "embedding.py"
Cohesion: 0.10
Nodes (17): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+9 more)

### Community 21 - "typing"
Cohesion: 0.19
Nodes (13): ParsedProfile, ProfileParser, Structured representation of parsed user profile and CV., Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, MatchingResult, MatchingService, Summary of a match scoring run., Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+5 more)

### Community 22 - "test_jobs.py"
Cohesion: 0.14
Nodes (19): TestClient, Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged)., include_flagged=True must include flagged postings (unless also vetoed)., show_all=True must include all jobs (both vetoed and flagged) for human review., Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…, Verify limit and offset pagination parameters work correctly. (+11 more)

### Community 23 - "job.py"
Cohesion: 0.18
Nodes (16): JobBase, JobCreate, JobUpdate, BaseModel, _parse_created_date(), datetime, Parse ISO formatted creation date from Adzuna response., JobSourceConfigError (+8 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.11
Nodes (5): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 26 - "test_matching.py"
Cohesion: 0.10
Nodes (22): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']. (+14 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.10
Nodes (20): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log (+12 more)

### Community 28 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 29 - ".score_and_gate_jobs"
Cohesion: 0.15
Nodes (10): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Path, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the… (+2 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "api/auth.py"
Cohesion: 0.17
Nodes (16): login(), post, Session, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register(), decode_access_token(), get_current_account() (+8 more)

### Community 32 - "JobPosting"
Cohesion: 0.19
Nodes (10): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, Test POST /api/v1/jobs/ingest triggers job sourcing, integrity guarding,…, test_trigger_ingestion_endpoint(), fetch(), MockPerCompanySource (+2 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "LinkedInJobSource"
Cohesion: 0.18
Nodes (9): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser() (+1 more)

### Community 41 - "models/__init__.py"
Cohesion: 0.13
Nodes (30): 4. Pydantic Schemas & Security, AccountBase, AccountCreate, AccountRead, ApplicationBase, ApplicationCreate, ApplicationUpdate, BaseModel (+22 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.14
Nodes (38): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+30 more)

### Community 45 - "test_greenhouse_fetch_with_mock_client"
Cohesion: 0.24
Nodes (8): asyncio, String company slug is normalized and targets the correct URL., Non-200 responses raise JobSourceHTTPError., Parse a realistic Greenhouse response via injected MockTransport., test_greenhouse_fetch_string_slug(), test_greenhouse_fetch_with_mock_client(), handler(), test_greenhouse_http_error()

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "Account"
Cohesion: 0.10
Nodes (26): delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), delete, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash. (+18 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "UserProfile"
Cohesion: 0.20
Nodes (17): delete_designation(), delete_language(), delete_location(), get_compensation(), get_current_account(), get_profile(), list_designations(), list_languages() (+9 more)

### Community 55 - "test_models.py"
Cohesion: 0.10
Nodes (39): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /… (+31 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "pathlib"
Cohesion: 0.12
Nodes (17): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+9 more)

### Community 60 - "trigger_ingestion"
Cohesion: 0.18
Nodes (12): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+4 more)

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

### Community 67 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 70 - "client"
Cohesion: 0.22
Nodes (10): client(), fixture, Session, In-memory SQLite database session with static pool for testing., FastAPI TestClient with overridden get_db dependency., Seed test accounts for multi-tenant isolation tests., Seed a variety of jobs: - High match score, clean - Mid match score, clean -…, seeded_accounts() (+2 more)

### Community 71 - "SaaS Review Checklist"
Cohesion: 0.22
Nodes (8): 1. Multi-Tenant Data Isolation (Critical), 2. Security & Credentials (Critical), 3. Async & Performance (High), 4. Human-in-the-Loop & Business Rules (Critical), 5. Frontend & UI/UX Standards (High), Code Review Context — Job Application Agent SaaS, Review Workflow, SaaS Review Checklist

### Community 72 - "Database Migrations Skill — Job Application Agent SaaS"
Cohesion: 0.50
Nodes (3): Core Rules, Database Migrations Skill — Job Application Agent SaaS, Verification

### Community 73 - "Hunt Targets"
Cohesion: 0.29
Nodes (6): 1. Bare `except:` or Empty Catch Blocks, 2. Dangerous Fallbacks in LLM & Ingestion, 3. Missing Transaction Rollbacks, 4. Frontend Unhandled Promise Rejections, Hunt Targets, Silent Failure Hunter Skill — Job Application Agent SaaS

### Community 74 - "test_profile.py"
Cohesion: 0.29
Nodes (8): create_app(), Create and configure FastAPI application., account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 75 - "Validation Scenarios"
Cohesion: 0.29
Nodes (6): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine, 4. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 84 - "main.jsx"
Cohesion: 0.50
Nodes (3): App(), frontend_src_index, react-dom

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

### Community 90 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

## Knowledge Gaps
- **189 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+184 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 611 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobIngestionService`, `api/profile.py`, `Job`, `client`, `session.py`, `applications.py`, `test_auth.py`, `account.py`, `test_jobs.py`, `job.py`, `test_matching.py`, `Architecture — Job Application Agent SaaS`, `api/auth.py`, `test_admin.py`, `models/__init__.py`, `admin.py`, `UserProfile`, `test_models.py`, `TestClient`, `client`, `test_profile.py`, `get_me`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `JobIngestionService`, `JobSearchQuery`, `LinkedInJobSource`, `models/__init__.py`, `JobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `test_greenhouse_fetch_with_mock_client`, `account.py`, `lever.py`, `RemotiveJobSource`, `typing`, `test_jobs.py`, `job.py`, `test_models.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `JobIngestionService`, `test_admin.py`, `client`, `session.py`, `models/__init__.py`, `admin.py`, `applications.py`, `account.py`, `Account`, `api/interview.py`, `typing`, `test_jobs.py`, `job.py`, `test_models.py`, `test_matching.py`, `trigger_ingestion`, `.score_and_gate_jobs`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 73 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
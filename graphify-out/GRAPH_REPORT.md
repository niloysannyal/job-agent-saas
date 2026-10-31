# Graph Report - job-agent-saas  (2026-10-31)

## Corpus Check
- 176 files · ~112,239 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 6, .css 2, .ini 1)

## Summary
- 1697 nodes · 4258 edges · 111 communities (93 shown, 18 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 498 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64abb43f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- posting_guard.py
- App.jsx
- test_cv_tailor.py
- Job
- models/__init__.py
- test_application_status_update
- JobSearchQuery
- client
- env.py
- llm/service.py
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- api/auth.py
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- UserProfile
- test_matching.py
- job.py
- TestClient
- Base
- What You Must Do When Invoked
- typing
- integrations.py
- Architecture — Job Application Agent SaaS
- .check
- google_service.py
- Settings
- test_auth.py
- Product Development Environment Guide — Job Application Agent SaaS
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobPosting
- test_models.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- run_posting_guard
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Account
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Roadmap — Job Application Agent SaaS
- Project: Job Application Agent SaaS
- Application
- Multi-Tenant SaaS Auditor
- dispatch_service.py
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- pathlib
- jobs.py
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- TestClient
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- TestInstructionDetection
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- client
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- llm_provider.py
- React Frontend Development Standards (adapted from ECC)
- Security & Tenancy Policy (adapted from ECC AgentShield)
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- plan_relevance_cuts
- GoogleIntegrationService
- test_matching_service_score_and_gate_clean_jobs
- .to_dict
- test_google_callback_and_status
- db_session
- test_monitor_followups_task
- ProfileParser
- parse_redis_settings
- test_adzuna_fetch_with_mock_client
- LLMService
- test_cv_tailor_service_end_to_end
- MatchingService
- .generate
- .generate
- subscription.py
- MockPerCompanySource
- deploy.sh
- test_account
- Pipeline Verification Checklist
- AccountCvVersion
- prune_and_budget_latex

## God Nodes (most connected - your core abstractions)
1. `Account` - 151 edges
2. `Job` - 74 edges
3. `JobPosting` - 74 edges
4. `JobSearchQuery` - 62 edges
5. `Base` - 61 edges
6. `UserProfile` - 49 edges
7. `Application` - 42 edges
8. `JobSourceHTTPError` - 36 edges
9. `JobSource` - 35 edges
10. `StarStory` - 32 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py

## Import Cycles
- None detected.

## Communities (111 total, 18 thin omitted)

### Community 0 - "posting_guard.py"
Cohesion: 0.12
Nodes (15): FlagKind, IntegrityFlag, _is_invisible(), _line_looks_like_instruction(), Enum, str, posting_guard.py — posting integrity gate (ARCHITECTURE.md §4, §8) Every…, Return True if the line matches any instruction-injection pattern. (+7 more)

### Community 1 - "App.jsx"
Cohesion: 0.13
Nodes (21): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), JobDetailModal(), formatSalary() (+13 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.13
Nodes (24): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+16 more)

### Community 3 - "Job"
Cohesion: 0.13
Nodes (27): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService, Any, Session, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run. (+19 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.10
Nodes (52): add_designation(), add_language(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation() (+44 more)

### Community 5 - "test_application_status_update"
Cohesion: 0.23
Nodes (12): Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer., Test Module 2 (Apply) application tailoring and strict human-in-the-loop Send…, test_application_status_update() (+4 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.10
Nodes (19): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any (+11 more)

### Community 7 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 8 - "env.py"
Cohesion: 0.29
Nodes (9): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_engine(), normalize_db_url(), Normalize database URL for driver compatibility. (+1 more)

### Community 9 - "llm/service.py"
Cohesion: 0.18
Nodes (14): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+6 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Asynchronously fetch all open job postings for a company from Greenhouse. Pass… (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.07
Nodes (50): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+42 more)

### Community 14 - "api/auth.py"
Cohesion: 0.17
Nodes (17): get_me(), login(), get, post, Session, Retrieve authenticated account profile and permissions from validated token., Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated… (+9 more)

### Community 15 - "tasks.py"
Cohesion: 0.13
Nodes (21): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories… (+13 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (20): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+12 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.10
Nodes (20): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+12 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (24): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps… (+16 more)

### Community 19 - "UserProfile"
Cohesion: 0.07
Nodes (55): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+47 more)

### Community 20 - "test_matching.py"
Cohesion: 0.08
Nodes (31): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+23 more)

### Community 21 - "job.py"
Cohesion: 0.21
Nodes (15): asyncio, JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, JobSourceConfigError, JobSourceError, JobSourceHTTPError, Raised when an external job source HTTP request fails. (+7 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 23 - "Base"
Cohesion: 0.14
Nodes (31): Base, Base SQLAlchemy declarative model., get_db(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application. (+23 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.08
Nodes (14): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade(), downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely. (+6 more)

### Community 26 - "integrations.py"
Cohesion: 0.17
Nodes (22): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+14 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (17): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN) (+9 more)

### Community 29 - "google_service.py"
Cohesion: 0.14
Nodes (17): decrypt_secret(), encrypt_secret(), _get_fernet_instance(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Verify secrets are encrypted and decrypted accurately., test_crypto_encryption_roundtrip() (+9 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "test_auth.py"
Cohesion: 0.18
Nodes (19): create_access_token(), Generate a cryptographically signed JWT access token. Contains subject…, auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user() (+11 more)

### Community 32 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "JobPosting"
Cohesion: 0.10
Nodes (20): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobUpdate, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+12 more)

### Community 41 - "test_models.py"
Cohesion: 0.09
Nodes (42): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /… (+34 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.13
Nodes (42): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+34 more)

### Community 45 - "run_posting_guard"
Cohesion: 0.17
Nodes (8): Run the posting integrity gate on a JobPosting DTO. Steps: 1. Strip…, run_posting_guard(), make_posting(), The instruction line must still be in the cleaned posting — not deleted., Return a minimal valid JobPosting with sensible defaults., TestCleanPosting, TestCombinedIssues, TestInvisibleCharacters

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "Account"
Cohesion: 0.09
Nodes (30): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint() (+22 more)

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

### Community 53 - "Application"
Cohesion: 0.12
Nodes (21): Application, ApplicationBase, ApplicationCreate, ApplicationFormAnswer, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationUpdate (+13 more)

### Community 55 - "dispatch_service.py"
Cohesion: 0.18
Nodes (15): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+7 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "pathlib"
Cohesion: 0.12
Nodes (17): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+9 more)

### Community 60 - "jobs.py"
Cohesion: 0.10
Nodes (27): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+19 more)

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

### Community 70 - "TestInstructionDetection"
Cohesion: 0.17
Nodes (3): GateResult, Return type from run_posting_guard(). posting — a new JobPosting copy with…, TestInstructionDetection

### Community 71 - "SaaS Review Checklist"
Cohesion: 0.22
Nodes (8): 1. Multi-Tenant Data Isolation (Critical), 2. Security & Credentials (Critical), 3. Async & Performance (High), 4. Human-in-the-Loop & Business Rules (Critical), 5. Frontend & UI/UX Standards (High), Code Review Context — Job Application Agent SaaS, Review Workflow, SaaS Review Checklist

### Community 72 - "Database Migrations Skill — Job Application Agent SaaS"
Cohesion: 0.50
Nodes (3): Core Rules, Database Migrations Skill — Job Application Agent SaaS, Verification

### Community 73 - "Hunt Targets"
Cohesion: 0.29
Nodes (6): 1. Bare `except:` or Empty Catch Blocks, 2. Dangerous Fallbacks in LLM & Ingestion, 3. Missing Transaction Rollbacks, 4. Frontend Unhandled Promise Rejections, Hunt Targets, Silent Failure Hunter Skill — Job Application Agent SaaS

### Community 74 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 75 - "Validation Scenarios"
Cohesion: 0.29
Nodes (6): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine, 4. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "llm_provider.py"
Cohesion: 0.19
Nodes (11): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), LLMProviderBase, LLMProviderCreate (+3 more)

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

### Community 88 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 90 - "GoogleIntegrationService"
Cohesion: 0.16
Nodes (9): get_google_auth_url(), Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and…, Exchange an OAuth authorization code for access and refresh tokens. Fetches the… (+1 more)

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.09
Nodes (19): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test embedding profile and upserting point into Qdrant. (+11 more)

### Community 93 - "test_google_callback_and_status"
Cohesion: 0.29
Nodes (8): Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and…, test_bookmarklet_generation(), test_google_auth_url_endpoint(), test_google_callback_and_status()

### Community 94 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 95 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 96 - "ProfileParser"
Cohesion: 0.14
Nodes (13): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser, Any, Path, Structured representation of parsed user profile and CV. (+5 more)

### Community 97 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 98 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 99 - "LLMService"
Cohesion: 0.15
Nodes (8): get_llm_service(), Dependency provider for LLMService., Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, client(), fixture

### Community 100 - "test_cv_tailor_service_end_to_end"
Cohesion: 0.50
Nodes (4): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, test_cv_tailor_service_end_to_end()

### Community 101 - "MatchingService"
Cohesion: 0.21
Nodes (8): MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 103 - ".generate"
Cohesion: 0.18
Nodes (8): Any, Execute generation across the provider chain with automatic fallback., Resolve ordered list of active providers from database or defaults., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 104 - "subscription.py"
Cohesion: 0.36
Nodes (9): EntitlementBase, EntitlementCreate, EntitlementRead, EntitlementUpdate, BaseModel, SubscriptionPlanBase, SubscriptionPlanCreate, SubscriptionPlanRead (+1 more)

### Community 105 - "MockPerCompanySource"
Cohesion: 0.33
Nodes (3): MockPerCompanySource, Any, Mock per-company ATS source (is_per_company = True).

### Community 107 - "test_account"
Cohesion: 0.40
Nodes (5): db_session(), fixture, In-memory SQLite session for testing ingestion., Create a test tenant account., test_account()

### Community 108 - "Pipeline Verification Checklist"
Cohesion: 0.50
Nodes (3): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner

### Community 109 - "AccountCvVersion"
Cohesion: 0.67
Nodes (3): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, CVTailorResult

## Knowledge Gaps
- **188 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 688 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `Job`, `models/__init__.py`, `test_application_status_update`, `client`, `applications.py`, `api/auth.py`, `tasks.py`, `test_matching.py`, `job.py`, `TestClient`, `Base`, `integrations.py`, `test_auth.py`, `test_admin.py`, `test_models.py`, `admin.py`, `Application`, `jobs.py`, `TestClient`, `client`, `llm_provider.py`, `GoogleIntegrationService`, `test_matching_service_score_and_gate_clean_jobs`, `test_google_callback_and_status`, `test_monitor_followups_task`, `test_cv_tailor_service_end_to_end`, `subscription.py`, `test_account`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `models/__init__.py`, `test_application_status_update`, `applications.py`, `tasks.py`, `UserProfile`, `test_matching.py`, `job.py`, `TestClient`, `Base`, `typing`, `test_admin.py`, `test_models.py`, `admin.py`, `Account`, `Application`, `jobs.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_monitor_followups_task`, `test_cv_tailor_service_end_to_end`, `MatchingService`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `posting_guard.py`, `test_adzuna_fetch_with_mock_client`, `Job`, `models/__init__.py`, `JobSearchQuery`, `TestInstructionDetection`, `test_models.py`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `run_posting_guard`, `MockPerCompanySource`, `LeverJobSource`, `RemotiveJobSource`, `job.py`, `Application`, `Base`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
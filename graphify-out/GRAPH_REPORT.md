# Graph Report - job-agent-saas  (2026-10-31)

## Corpus Check
- 176 files · ~113,176 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 6, .css 2, .ini 1)

## Summary
- 1701 nodes · 4278 edges · 110 communities (88 shown, 22 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 502 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ae9453ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobPosting
- api/profile.py
- Application
- AdzunaJobSource
- client
- env.py
- typing
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- BaseModel
- account.py
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- api/interview.py
- test_matching.py
- job.py
- TestClient
- Base
- What You Must Do When Invoked
- alembic
- create_gmail_draft
- Architecture — Job Application Agent SaaS
- UserProfile
- integrations.py
- Settings
- test_auth.py
- Product Development Environment Guide — Job Application Agent SaaS
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- LinkedInJobSource
- models/__init__.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- detective.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Account
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Roadmap — Job Application Agent SaaS
- Project: Job Application Agent SaaS
- applications.py
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
- experience_reflector.py
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- client
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- Session
- React Frontend Development Standards (adapted from ECC)
- Security & Tenancy Policy (adapted from ECC AgentShield)
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- plan_relevance_cuts
- get_current_account
- test_matching_service_score_and_gate_clean_jobs
- .to_dict
- run_live_dogfooding.py
- db_session
- test_generate_form_answers_api_endpoint
- .parse_from_db
- .generate
- db_session
- client
- test_cv_tailor_service_end_to_end
- matching/service.py
- .generate
- .generate
- get_llm_service
- JobSearchQuery
- deploy.sh
- .__init__
- .generate
- prune_and_budget_latex

## God Nodes (most connected - your core abstractions)
1. `Account` - 152 edges
2. `Job` - 76 edges
3. `JobPosting` - 74 edges
4. `JobSearchQuery` - 62 edges
5. `Base` - 61 edges
6. `UserProfile` - 50 edges
7. `Application` - 46 edges
8. `JobSourceHTTPError` - 36 edges
9. `JobSource` - 35 edges
10. `StarStory` - 32 edges

## Surprising Connections (you probably didn't know these)
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py

## Import Cycles
- None detected.

## Communities (110 total, 22 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.13
Nodes (21): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), JobDetailModal(), formatSalary() (+13 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.12
Nodes (25): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+17 more)

### Community 3 - "JobPosting"
Cohesion: 0.09
Nodes (38): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+30 more)

### Community 4 - "api/profile.py"
Cohesion: 0.10
Nodes (48): add_designation(), add_language(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation() (+40 more)

### Community 5 - "Application"
Cohesion: 0.12
Nodes (20): mark_application_sent(), Strict Human-in-the-loop Send gate: Only a human can trigger this endpoint to…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline… (+12 more)

### Community 6 - "AdzunaJobSource"
Cohesion: 0.08
Nodes (26): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+18 more)

### Community 7 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 8 - "env.py"
Cohesion: 0.29
Nodes (9): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_engine(), normalize_db_url(), Normalize database URL for driver compatibility. (+1 more)

### Community 9 - "typing"
Cohesion: 0.16
Nodes (18): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…, LLMService (+10 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Asynchronously fetch all open job postings for a company from Greenhouse. Pass… (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "BaseModel"
Cohesion: 0.06
Nodes (40): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+32 more)

### Community 14 - "account.py"
Cohesion: 0.24
Nodes (15): login(), post, Session, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register(), AccountBase, AccountCreate (+7 more)

### Community 15 - "tasks.py"
Cohesion: 0.08
Nodes (34): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), arq, arq_connections, Session (+26 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (20): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+12 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.10
Nodes (20): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+12 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 20 - "test_matching.py"
Cohesion: 0.10
Nodes (18): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+10 more)

### Community 21 - "job.py"
Cohesion: 0.21
Nodes (15): JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, JobSourceConfigError, JobSourceError, JobSourceHTTPError, Raised when an external job source HTTP request fails., Base exception for job source errors. (+7 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 23 - "Base"
Cohesion: 0.15
Nodes (28): Base, Base SQLAlchemy declarative model., get_db(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application. (+20 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.09
Nodes (9): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade(), downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely. (+1 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.09
Nodes (29): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+21 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.10
Nodes (20): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log (+12 more)

### Community 28 - "UserProfile"
Cohesion: 0.21
Nodes (16): generate_form_answers(), Harness² Recursive Form Q&A Generator. Applies Task-Level Recursion (Propose ->…, A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or… (+8 more)

### Community 29 - "integrations.py"
Cohesion: 0.13
Nodes (18): decrypt_secret(), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, OAuthConnection, OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead (+10 more)

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

### Community 35 - "Job"
Cohesion: 0.15
Nodes (23): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+15 more)

### Community 40 - "LinkedInJobSource"
Cohesion: 0.20
Nodes (8): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser()

### Community 41 - "models/__init__.py"
Cohesion: 0.11
Nodes (40): 4. Pydantic Schemas & Security, Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), ApplicationCreate, CvTemplateCreate, LLMProviderBase, LLMProviderCreate (+32 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.13
Nodes (44): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+36 more)

### Community 45 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "Account"
Cohesion: 0.08
Nodes (28): get_me(), get, Retrieve authenticated account profile and permissions from validated token., Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, TestClient (+20 more)

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

### Community 53 - "applications.py"
Cohesion: 0.16
Nodes (21): Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate (+13 more)

### Community 55 - "dispatch_service.py"
Cohesion: 0.10
Nodes (26): _get_fernet_instance(), Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's… (+18 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "pathlib"
Cohesion: 0.12
Nodes (17): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+9 more)

### Community 60 - "jobs.py"
Cohesion: 0.12
Nodes (21): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+13 more)

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

### Community 70 - "experience_reflector.py"
Cohesion: 0.17
Nodes (11): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT… (+3 more)

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
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 75 - "Validation Scenarios"
Cohesion: 0.29
Nodes (6): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine, 4. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "Session"
Cohesion: 0.18
Nodes (11): Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Test StarStory model creation, tags, and account cascade., Test Account model defaults and multi-tenant fields., Test Job model matches ARCHITECTURE.md §7: (account_id, company, role, salary,…, test_account_model(), test_cv_template_and_version_models() (+3 more)

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

### Community 90 - "get_current_account"
Cohesion: 0.33
Nodes (7): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 93 - "run_live_dogfooding.py"
Cohesion: 0.15
Nodes (13): asyncio, ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent… (+5 more)

### Community 94 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 95 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.60
Nodes (5): Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 96 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 98 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 100 - "test_cv_tailor_service_end_to_end"
Cohesion: 0.50
Nodes (4): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, test_cv_tailor_service_end_to_end()

### Community 101 - "matching/service.py"
Cohesion: 0.08
Nodes (24): Session, compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., MatchingResult (+16 more)

### Community 103 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 105 - "JobSearchQuery"
Cohesion: 0.24
Nodes (6): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., Any

## Knowledge Gaps
- **188 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 690 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobPosting`, `api/profile.py`, `Application`, `client`, `BaseModel`, `account.py`, `tasks.py`, `test_matching.py`, `job.py`, `TestClient`, `Base`, `create_gmail_draft`, `Architecture — Job Application Agent SaaS`, `UserProfile`, `integrations.py`, `test_auth.py`, `Job`, `models/__init__.py`, `admin.py`, `applications.py`, `jobs.py`, `TestClient`, `client`, `Session`, `get_current_account`, `test_matching_service_score_and_gate_clean_jobs`, `run_live_dogfooding.py`, `test_generate_form_answers_api_endpoint`, `test_cv_tailor_service_end_to_end`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `JobPosting`, `Application`, `BaseModel`, `account.py`, `tasks.py`, `api/interview.py`, `test_matching.py`, `job.py`, `TestClient`, `Base`, `models/__init__.py`, `admin.py`, `Account`, `applications.py`, `jobs.py`, `experience_reflector.py`, `Session`, `test_matching_service_score_and_gate_clean_jobs`, `run_live_dogfooding.py`, `test_cv_tailor_service_end_to_end`, `matching/service.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `AdzunaJobSource`, `LinkedInJobSource`, `models/__init__.py`, `JobSearchQuery`, `FreehireJobSource`, `GreenhouseJobSource`, `RemoteOKJobSource`, `LeverJobSource`, `RemotiveJobSource`, `job.py`, `Base`, `jobs.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
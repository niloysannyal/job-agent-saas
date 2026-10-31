# Graph Report - job-agent-saas  (2026-10-31)

## Corpus Check
- 183 files · ~125,569 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 1841 nodes · 4770 edges · 111 communities (94 shown, 17 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 616 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `863f9a0d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobIngestionService
- models/__init__.py
- Application
- AdzunaJobSource
- MatchingService
- env.py
- LLMService
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- jobs.py
- worker.py
- package.json
- LeverJobSource
- JobSearchQuery
- UserProfile
- EmbeddingClient
- job.py
- TestClient
- client
- What You Must Do When Invoked
- alembic
- create_gmail_draft
- Architecture — Job Application Agent SaaS
- Session
- Base
- Settings
- test_auth.py
- api/profile.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- JobPosting
- Account
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- _get_or_create_profile
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- test_profile.py
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- test_bookmarklet_generation_with_job_and_star_answers
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- models/profile.py
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- run_phase1_acceleration.py
- EmailDispatchService
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- TestClient
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- tasks.py
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- typing
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- trigger_ingestion
- React Frontend Development Standards (adapted from ECC)
- CVTemplateCompiler
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- GoogleIntegrationService
- dispatch_service.py
- test_matching_service_score_and_gate_clean_jobs
- SpokenLanguage
- decrypt_secret
- .generate
- test_generate_form_answers_api_endpoint
- .parse_from_db
- Product Development Environment Guide — Job Application Agent SaaS
- test_monitor_followups_task
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- test_matching.py
- api/auth.py
- set_compensation
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- parse_redis_settings
- deploy.sh
- add_language
- .generate
- downgrade
- upgrade

## God Nodes (most connected - your core abstractions)
1. `Account` - 157 edges
2. `Job` - 79 edges
3. `JobPosting` - 74 edges
4. `Base` - 66 edges
5. `JobSearchQuery` - 62 edges
6. `UserProfile` - 55 edges
7. `Application` - 47 edges
8. `JobSourceHTTPError` - 36 edges
9. `JobSource` - 35 edges
10. `LLMService` - 35 edges

## Surprising Connections (you probably didn't know these)
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `get_current_account()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py

## Import Cycles
- None detected.

## Communities (111 total, 17 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.14
Nodes (19): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+11 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.06
Nodes (50): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult (+42 more)

### Community 3 - "JobIngestionService"
Cohesion: 0.09
Nodes (33): IngestionResult, JobIngestionService, Any, Session, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, db_session() (+25 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.11
Nodes (29): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationUpdate, BaseModel (+21 more)

### Community 5 - "Application"
Cohesion: 0.12
Nodes (17): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, api_test_db(), client(), fixture, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications. (+9 more)

### Community 6 - "AdzunaJobSource"
Cohesion: 0.09
Nodes (26): AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime, Asynchronously fetch job postings matching the query from Adzuna. (+18 more)

### Community 7 - "MatchingService"
Cohesion: 0.31
Nodes (6): MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 8 - "env.py"
Cohesion: 0.28
Nodes (8): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), normalize_db_url(), Normalize database URL for driver compatibility., logging_config

### Community 9 - "LLMService"
Cohesion: 0.16
Nodes (12): Session, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, asyncio (+4 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.07
Nodes (52): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+44 more)

### Community 14 - "jobs.py"
Cohesion: 0.26
Nodes (9): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, FastAPI (+1 more)

### Community 15 - "worker.py"
Cohesion: 0.14
Nodes (18): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+10 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (19): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+11 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "JobSearchQuery"
Cohesion: 0.08
Nodes (27): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., _clean_html(), _parse_publication_date(), Any (+19 more)

### Community 19 - "UserProfile"
Cohesion: 0.07
Nodes (55): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+47 more)

### Community 20 - "EmbeddingClient"
Cohesion: 0.10
Nodes (13): EmbeddingClient, MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Abstract interface for text embedding generation., Generate embedding vector for a single text string., Generate embeddings for a list of text strings. (+5 more)

### Community 21 - "job.py"
Cohesion: 0.16
Nodes (22): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceError (+14 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 23 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.11
Nodes (5): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 26 - "create_gmail_draft"
Cohesion: 0.15
Nodes (19): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+11 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.10
Nodes (20): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log (+12 more)

### Community 28 - "Session"
Cohesion: 0.11
Nodes (31): create_profile(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+23 more)

### Community 29 - "Base"
Cohesion: 0.19
Nodes (26): Base, Base SQLAlchemy declarative model., get_db(), get_engine(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., lifespan(), ApplicationFormAnswer (+18 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "test_auth.py"
Cohesion: 0.22
Nodes (16): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+8 more)

### Community 32 - "api/profile.py"
Cohesion: 0.18
Nodes (22): add_work_experience(), patch, Profile management API — CRUD for UserProfile, TargetDesignation,…, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project() (+14 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "Job"
Cohesion: 0.13
Nodes (25): create_app(), Create and configure FastAPI application., Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db() (+17 more)

### Community 40 - "JobPosting"
Cohesion: 0.10
Nodes (20): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobUpdate, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+12 more)

### Community 41 - "Account"
Cohesion: 0.08
Nodes (40): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, AccountCvVersionCreate (+32 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.09
Nodes (53): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), _build_provider_read(), create_admin_template() (+45 more)

### Community 45 - "_get_or_create_profile"
Cohesion: 0.15
Nodes (23): add_education(), add_project(), add_skill(), apply_parsed_cv(), bulk_skills(), _get_or_create_profile(), list_educations(), list_projects() (+15 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "test_profile.py"
Cohesion: 0.10
Nodes (27): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+19 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.16
Nodes (13): api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent… (+5 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.11
Nodes (15): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+7 more)

### Community 55 - "models/profile.py"
Cohesion: 0.18
Nodes (18): add_certification(), add_designation(), add_location(), Certification, CertificationBase, CertificationCreate, CertificationRead, EducationBase (+10 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "run_phase1_acceleration.py"
Cohesion: 0.10
Nodes (19): asyncio, os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check() (+11 more)

### Community 60 - "EmailDispatchService"
Cohesion: 0.19
Nodes (13): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+5 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.33
Nodes (14): ApplicationStudio(), cleanLatexInline(), compactLatex(), compactLatexToTwoPages(), compileParsedLatexToPdf(), decodeHtmlEntities(), estimateItemHeight(), extractLinksFromLatex() (+6 more)

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

### Community 70 - "tasks.py"
Cohesion: 0.15
Nodes (16): get_embedding_client(), Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,… (+8 more)

### Community 71 - "SaaS Review Checklist"
Cohesion: 0.22
Nodes (8): 1. Multi-Tenant Data Isolation (Critical), 2. Security & Credentials (Critical), 3. Async & Performance (High), 4. Human-in-the-Loop & Business Rules (Critical), 5. Frontend & UI/UX Standards (High), Code Review Context — Job Application Agent SaaS, Review Workflow, SaaS Review Checklist

### Community 72 - "Database Migrations Skill — Job Application Agent SaaS"
Cohesion: 0.50
Nodes (3): Core Rules, Database Migrations Skill — Job Application Agent SaaS, Verification

### Community 73 - "Hunt Targets"
Cohesion: 0.29
Nodes (6): 1. Bare `except:` or Empty Catch Blocks, 2. Dangerous Fallbacks in LLM & Ingestion, 3. Missing Transaction Rollbacks, 4. Frontend Unhandled Promise Rejections, Hunt Targets, Silent Failure Hunter Skill — Job Application Agent SaaS

### Community 74 - "typing"
Cohesion: 0.25
Nodes (8): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…, pydantic_settings, typing

### Community 75 - "Validation Scenarios"
Cohesion: 0.29
Nodes (6): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine, 4. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "trigger_ingestion"
Cohesion: 0.17
Nodes (15): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+7 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

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

### Community 88 - "GoogleIntegrationService"
Cohesion: 0.18
Nodes (9): get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+1 more)

### Community 90 - "dispatch_service.py"
Cohesion: 0.22
Nodes (10): base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text, email_policy (+2 more)

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 92 - "SpokenLanguage"
Cohesion: 0.24
Nodes (11): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+3 more)

### Community 93 - "decrypt_secret"
Cohesion: 0.12
Nodes (15): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), decrypt_secret(), encrypt_secret(), _get_fernet_instance() (+7 more)

### Community 94 - ".generate"
Cohesion: 0.18
Nodes (8): Any, Execute generation across the provider chain with automatic fallback., Resolve ordered list of active providers from database or defaults., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.28
Nodes (8): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 96 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.60
Nodes (4): JobDetailModal(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "test_matching.py"
Cohesion: 0.12
Nodes (17): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared. (+9 more)

### Community 102 - "api/auth.py"
Cohesion: 0.15
Nodes (20): get_me(), login(), get, post, Session, Retrieve authenticated account profile and permissions from validated token., Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated… (+12 more)

### Community 103 - "set_compensation"
Cohesion: 0.50
Nodes (5): set_compensation(), CompensationBase, CompensationCreate, CompensationRead, put

### Community 104 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 105 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 107 - "add_language"
Cohesion: 0.67
Nodes (4): add_language(), SpokenLanguageBase, SpokenLanguageCreate, SpokenLanguageRead

## Knowledge Gaps
- **188 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 732 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobIngestionService`, `models/__init__.py`, `Application`, `applications.py`, `jobs.py`, `job.py`, `TestClient`, `client`, `create_gmail_draft`, `Architecture — Job Application Agent SaaS`, `Session`, `Base`, `test_auth.py`, `api/profile.py`, `Job`, `admin.py`, `test_profile.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `models/profile.py`, `TestClient`, `tasks.py`, `trigger_ingestion`, `GoogleIntegrationService`, `test_matching_service_score_and_gate_clean_jobs`, `SpokenLanguage`, `test_generate_form_answers_api_endpoint`, `test_monitor_followups_task`, `test_matching.py`, `api/auth.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `JobIngestionService`, `models/__init__.py`, `tasks.py`, `AdzunaJobSource`, `Account`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `LeverJobSource`, `JobSearchQuery`, `job.py`, `Base`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `JobIngestionService`, `models/__init__.py`, `Application`, `MatchingService`, `applications.py`, `jobs.py`, `worker.py`, `UserProfile`, `job.py`, `TestClient`, `Base`, `Account`, `admin.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `tasks.py`, `trigger_ingestion`, `test_matching_service_score_and_gate_clean_jobs`, `test_monitor_followups_task`, `test_matching.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 93 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 93 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 16 INFERRED edges - model-reasoned connections that need verification._
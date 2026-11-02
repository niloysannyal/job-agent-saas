# Graph Report - job-agent-saas  (2026-11-02)

## Corpus Check
- 186 files · ~129,472 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 1870 nodes · 4864 edges · 114 communities (99 shown, 15 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 634 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b4e826e8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobPosting
- models/__init__.py
- Job
- JobSearchQuery
- UserProfile
- session.py
- MockLLMProvider
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- detective.py
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- api/interview.py
- test_matching.py
- job.py
- test_jobs.py
- test_interview.py
- What You Must Do When Invoked
- alembic
- integrations.py
- Architecture — Job Application Agent SaaS
- api/profile.py
- Base
- Settings
- test_adzuna_fetch_with_mock_client
- WorkExperience
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- get_available_sources
- CvTemplate
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- _get_or_create_profile
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Account
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Application
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
- typing
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- llm/service.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- jobs.py
- React Frontend Development Standards (adapted from ECC)
- LLMService
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- GoogleIntegrationService
- dispatch_service.py
- test_matching_service_score_and_gate_clean_jobs
- seed_initial_data
- encrypt_secret
- .generate
- test_generate_form_answers_api_endpoint
- ProfileParser
- Product Development Environment Guide — Job Application Agent SaaS
- test_monitor_followups_task
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- MatchingService
- test_auth.py
- decrypt_secret
- JobRead
- parse_redis_settings
- deploy.sh
- test_profile.py
- .generate
- get_monitor_summary
- UserProfileRead
- FastAPI Backend Development Standards (adapted from ECC)
- Project
- update_application_status

## God Nodes (most connected - your core abstractions)
1. `Account` - 161 edges
2. `Job` - 79 edges
3. `JobPosting` - 74 edges
4. `Base` - 67 edges
5. `JobSearchQuery` - 62 edges
6. `UserProfile` - 60 edges
7. `Application` - 47 edges
8. `JobSourceHTTPError` - 36 edges
9. `JobSource` - 35 edges
10. `LLMService` - 35 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py

## Import Cycles
- None detected.

## Communities (114 total, 15 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.14
Nodes (19): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+11 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.06
Nodes (50): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+42 more)

### Community 3 - "JobPosting"
Cohesion: 0.11
Nodes (35): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, JobIngestionService, Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, Test POST /api/v1/jobs/ingest triggers job sourcing, integrity guarding,…, test_trigger_ingestion_endpoint() (+27 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.08
Nodes (43): 4. Pydantic Schemas & Security, ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationRead (+35 more)

### Community 5 - "Job"
Cohesion: 0.19
Nodes (16): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+8 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.09
Nodes (21): JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources., Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, AdzunaJobSource, _clean_text() (+13 more)

### Community 7 - "UserProfile"
Cohesion: 0.25
Nodes (14): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+6 more)

### Community 8 - "session.py"
Cohesion: 0.08
Nodes (35): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+27 more)

### Community 9 - "MockLLMProvider"
Cohesion: 0.26
Nodes (8): MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, asyncio, test_llm_service_failover_chain(), test_llm_service_with_explicit_provider(), test_mock_llm_provider(), test_openai_provider_missing_key()

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.12
Nodes (36): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+28 more)

### Community 14 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 15 - "tasks.py"
Cohesion: 0.14
Nodes (19): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories… (+11 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (19): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+11 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 20 - "test_matching.py"
Cohesion: 0.10
Nodes (22): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+14 more)

### Community 21 - "job.py"
Cohesion: 0.14
Nodes (25): JobBase, JobCreate, _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:… (+17 more)

### Community 22 - "test_jobs.py"
Cohesion: 0.09
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 23 - "test_interview.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.08
Nodes (9): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade(), downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely. (+1 more)

### Community 26 - "integrations.py"
Cohesion: 0.18
Nodes (21): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+13 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (17): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN) (+9 more)

### Community 28 - "api/profile.py"
Cohesion: 0.13
Nodes (34): delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill(), delete_work_experience() (+26 more)

### Community 29 - "Base"
Cohesion: 0.24
Nodes (16): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), Multi-tenant STAR Interview Coach models. Stores STAR-format interview stories…, Verify Arq WorkerSettings has expected functions, crons, and timeouts. (+8 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 32 - "WorkExperience"
Cohesion: 0.18
Nodes (13): add_work_experience(), patch, update_certification(), update_project(), update_skill(), update_work_experience(), Certification, Structured work experience entity for candidates across all industries.… (+5 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 41 - "CvTemplate"
Cohesion: 0.10
Nodes (21): AccountCvVersion, CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable… (+13 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.15
Nodes (37): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+29 more)

### Community 45 - "_get_or_create_profile"
Cohesion: 0.21
Nodes (17): add_education(), add_skill(), apply_parsed_cv(), bulk_skills(), _get_or_create_profile(), list_educations(), post, Ensure a UserProfile row exists for an account, auto-creating a clean default… (+9 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "Account"
Cohesion: 0.09
Nodes (30): delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), delete, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash. (+22 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "Application"
Cohesion: 0.13
Nodes (17): Application, ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, CVTailorService, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Session, TestClient (+9 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - "models/profile.py"
Cohesion: 0.14
Nodes (26): add_certification(), add_designation(), add_language(), add_location(), CertificationBase, CertificationCreate, CertificationRead, CertificationUpdate (+18 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "run_phase1_acceleration.py"
Cohesion: 0.10
Nodes (20): asyncio, os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check() (+12 more)

### Community 60 - "EmailDispatchService"
Cohesion: 0.21
Nodes (12): EmailDispatchService, EmailDraftProvider, EmailDraftResult, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on…, Generates a standard URL-encoded mailto: link for 1-click launch in default… (+4 more)

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

### Community 70 - "typing"
Cohesion: 0.20
Nodes (10): IngestionResult, Summary metrics of a job ingestion run., MatchingResult, Summary of a match scoring run., collections, dataclasses, logging, pydantic_settings (+2 more)

### Community 71 - "SaaS Review Checklist"
Cohesion: 0.22
Nodes (8): 1. Multi-Tenant Data Isolation (Critical), 2. Security & Credentials (Critical), 3. Async & Performance (High), 4. Human-in-the-Loop & Business Rules (Critical), 5. Frontend & UI/UX Standards (High), Code Review Context — Job Application Agent SaaS, Review Workflow, SaaS Review Checklist

### Community 72 - "Database Migrations Skill — Job Application Agent SaaS"
Cohesion: 0.50
Nodes (3): Core Rules, Database Migrations Skill — Job Application Agent SaaS, Verification

### Community 73 - "Hunt Targets"
Cohesion: 0.29
Nodes (6): 1. Bare `except:` or Empty Catch Blocks, 2. Dangerous Fallbacks in LLM & Ingestion, 3. Missing Transaction Rollbacks, 4. Frontend Unhandled Promise Rejections, Hunt Targets, Silent Failure Hunter Skill — Job Application Agent SaaS

### Community 74 - "llm/service.py"
Cohesion: 0.32
Nodes (6): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…

### Community 75 - "Validation Scenarios"
Cohesion: 0.29
Nodes (6): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine, 4. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "jobs.py"
Cohesion: 0.11
Nodes (26): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+18 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "LLMService"
Cohesion: 0.18
Nodes (10): Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and… (+2 more)

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
Cohesion: 0.20
Nodes (11): Enum, base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text (+3 more)

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.09
Nodes (19): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']. (+11 more)

### Community 92 - "seed_initial_data"
Cohesion: 0.21
Nodes (14): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in… (+6 more)

### Community 93 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 94 - ".generate"
Cohesion: 0.18
Nodes (8): Any, Execute generation across the provider chain with automatic fallback., Resolve ordered list of active providers from database or defaults., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.60
Nodes (5): Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 96 - "ProfileParser"
Cohesion: 0.14
Nodes (13): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser, Any, Path, Structured representation of parsed user profile and CV. (+5 more)

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

### Community 101 - "MatchingService"
Cohesion: 0.10
Nodes (17): Session, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.… (+9 more)

### Community 102 - "test_auth.py"
Cohesion: 0.06
Nodes (62): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+54 more)

### Community 103 - "decrypt_secret"
Cohesion: 0.22
Nodes (8): decrypt_secret(), _get_fernet_instance(), Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Refresh an expired access token using the stored encrypted refresh token., Verify code exchange, DB persistence with encryption, status check, and…, test_google_callback_and_status(), Fernet

### Community 104 - "JobRead"
Cohesion: 0.25
Nodes (5): JobRead, Any, Alias for role to maintain consistency across frontend and APIs., field_validator, model_validator

### Community 105 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 107 - "test_profile.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 109 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 110 - "UserProfileRead"
Cohesion: 0.33
Nodes (7): create_profile(), Create a user profile for an account (one per account)., Partial-update the user profile for an account (auto-creates if missing)., update_profile(), UserProfileBase, UserProfileCreate, UserProfileRead

### Community 111 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 112 - "Project"
Cohesion: 0.40
Nodes (6): add_project(), Project, ProjectBase, ProjectCreate, ProjectRead, Portfolio projects, open-source work, or major professional deliverables.

### Community 113 - "update_application_status"
Cohesion: 0.40
Nodes (5): patch, Update application status in the pipeline (e.g. responded, interview, offer,…, Module 3 (Monitor): Update application status across pipeline stages: draft ->…, StatusUpdateRequest, update_application_status()

## Knowledge Gaps
- **188 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 742 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobPosting`, `models/__init__.py`, `Job`, `session.py`, `applications.py`, `tasks.py`, `test_matching.py`, `job.py`, `test_jobs.py`, `test_interview.py`, `integrations.py`, `api/profile.py`, `Base`, `test_admin.py`, `CvTemplate`, `admin.py`, `Application`, `models/profile.py`, `TestClient`, `jobs.py`, `LLMService`, `GoogleIntegrationService`, `test_matching_service_score_and_gate_clean_jobs`, `seed_initial_data`, `test_generate_form_answers_api_endpoint`, `test_monitor_followups_task`, `test_auth.py`, `decrypt_secret`, `test_profile.py`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `models/__init__.py`, `typing`, `JobSearchQuery`, `get_available_sources`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `LeverJobSource`, `RemotiveJobSource`, `job.py`, `test_jobs.py`, `test_adzuna_fetch_with_mock_client`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `LLMService` connect `LLMService` to `test_cv_tailor.py`, `UserProfile`, `session.py`, `MockLLMProvider`, `llm/service.py`, `admin.py`, `applications.py`, `Application`, `cv_parser.py`, `api/profile.py`, `.generate`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 97 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 97 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 16 INFERRED edges - model-reasoned connections that need verification._
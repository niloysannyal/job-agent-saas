# Graph Report - job-agent-saas  (2026-10-29)

## Corpus Check
- 151 files · ~99,458 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 4, .css 2, .ini 1)

## Summary
- 1467 nodes · 3528 edges · 96 communities (81 shown, 15 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 416 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94b14fe4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobPosting
- api/profile.py
- client
- JobSourceHTTPError
- test_interview.py
- session.py
- LLMService
- greenhouse.py
- JobSearchQuery
- RemoteOKJobSource
- applications.py
- test_auth.py
- job.py
- package.json
- lever.py
- RemotiveJobSource
- api/interview.py
- matching/service.py
- job_ingestion.py
- test_jobs.py
- models/profile.py
- What You Must Do When Invoked
- typing
- test_matching_service_score_and_gate_clean_jobs
- Architecture — Job Application Agent SaaS
- test_matching.py
- MatchingService
- Settings
- plan_relevance_cuts
- Product Development Environment Guide — Job Application Agent SaaS
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- linkedin.py
- models/__init__.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- run_ats_text_layer_check
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Account
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Roadmap — Job Application Agent SaaS
- Project: Job Application Agent SaaS
- .generate
- Multi-Tenant SaaS Auditor
- CvTemplate
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
- .parse_from_db
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
- MockEmbeddingClient
- db_session
- MockQdrantClient
- test_cv_tailor_service_end_to_end
- .generate
- db_session
- .__init__

## God Nodes (most connected - your core abstractions)
1. `Account` - 124 edges
2. `JobPosting` - 74 edges
3. `Job` - 64 edges
4. `JobSearchQuery` - 62 edges
5. `Base` - 49 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 35 edges
8. `run_posting_guard()` - 32 edges
9. `Application` - 31 edges
10. `UserProfile` - 28 edges

## Surprising Connections (you probably didn't know these)
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `4. Pydantic Schemas & Security` --references--> `LLMProviderRead`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/models/llm_provider.py

## Import Cycles
- None detected.

## Communities (96 total, 15 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.13
Nodes (21): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), JobDetailModal(), formatSalary() (+13 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.14
Nodes (22): audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body(), Strips lines starting with %% (agent control notes) while preserving actual…, Escapes LaTeX special characters (% & $ # _) if they are not already escaped.… (+14 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (43): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+35 more)

### Community 4 - "api/profile.py"
Cohesion: 0.10
Nodes (44): add_designation(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation(), get_current_account() (+36 more)

### Community 5 - "client"
Cohesion: 0.16
Nodes (14): client(), fixture, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+6 more)

### Community 6 - "JobSourceHTTPError"
Cohesion: 0.08
Nodes (35): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+27 more)

### Community 7 - "test_interview.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 8 - "session.py"
Cohesion: 0.22
Nodes (13): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+5 more)

### Community 9 - "LLMService"
Cohesion: 0.14
Nodes (18): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+10 more)

### Community 10 - "greenhouse.py"
Cohesion: 0.10
Nodes (22): _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Asynchronously fetch all open job postings for a company from Greenhouse. Pass… (+14 more)

### Community 11 - "JobSearchQuery"
Cohesion: 0.10
Nodes (27): JobSearchQuery, BaseModel, Normalized query parameters for searching across job sources., _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any (+19 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.08
Nodes (39): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_llm_service(), get_monitor_summary() (+31 more)

### Community 14 - "test_auth.py"
Cohesion: 0.10
Nodes (33): get_me(), login(), get, post, Session, Retrieve authenticated account profile and permissions from validated token., Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated… (+25 more)

### Community 15 - "job.py"
Cohesion: 0.25
Nodes (15): Base, Base SQLAlchemy declarative model., Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, Multi-tenant STAR Interview Coach models. Stores STAR-format interview stories…, api_test_db() (+7 more)

### Community 16 - "package.json"
Cohesion: 0.10
Nodes (20): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+12 more)

### Community 17 - "lever.py"
Cohesion: 0.11
Nodes (21): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+13 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "api/interview.py"
Cohesion: 0.15
Nodes (27): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+19 more)

### Community 20 - "matching/service.py"
Cohesion: 0.14
Nodes (17): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+9 more)

### Community 21 - "job_ingestion.py"
Cohesion: 0.47
Nodes (4): IngestionResult, Summary metrics of a job ingestion run., MatchingResult, Summary of a match scoring run.

### Community 22 - "test_jobs.py"
Cohesion: 0.08
Nodes (33): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+25 more)

### Community 23 - "models/profile.py"
Cohesion: 0.18
Nodes (19): add_language(), Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CompensationExpectation, Multi-tenant User Profile models matching ARCHITECTURE.md §7. Captures…, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /… (+11 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.11
Nodes (7): alembic, downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade(), pydantic_settings, typing

### Community 26 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.11
Nodes (18): db_session(), asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']., Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+10 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (18): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed) (+10 more)

### Community 28 - "test_matching.py"
Cohesion: 0.13
Nodes (15): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., Verify cosine similarity calculation edge cases and bounds. (+7 more)

### Community 29 - "MatchingService"
Cohesion: 0.18
Nodes (9): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account. (+1 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

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
Cohesion: 0.17
Nodes (21): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+13 more)

### Community 40 - "linkedin.py"
Cohesion: 0.13
Nodes (14): asyncio, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio (+6 more)

### Community 41 - "models/__init__.py"
Cohesion: 0.11
Nodes (38): 4. Pydantic Schemas & Security, AccountBase, AccountCreate, AccountRead, ApplicationBase, ApplicationCreate, ApplicationRead, ApplicationUpdate (+30 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.15
Nodes (37): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+29 more)

### Community 45 - "run_ats_text_layer_check"
Cohesion: 0.25
Nodes (6): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), Verify ATS parser plain-text inspection and keyword coverage., test_ats_checker()

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

### Community 53 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 55 - "CvTemplate"
Cohesion: 0.12
Nodes (19): CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Verify that deleting an account cascades to all tenant-scoped rows., Test seed_initial_data populates default templates, plans, entitlements, and… (+11 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "pathlib"
Cohesion: 0.12
Nodes (17): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+9 more)

### Community 60 - "jobs.py"
Cohesion: 0.11
Nodes (25): IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+17 more)

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

### Community 70 - ".parse_from_db"
Cohesion: 0.31
Nodes (6): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup.

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
Cohesion: 0.21
Nodes (12): create_app(), lifespan(), Create and configure FastAPI application., account_a(), account_b(), api_test_db(), client(), fixture (+4 more)

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

### Community 88 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 90 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "test_cv_tailor_service_end_to_end"
Cohesion: 0.50
Nodes (4): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, test_cv_tailor_service_end_to_end()

### Community 94 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

## Knowledge Gaps
- **189 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+184 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 614 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobPosting`, `api/profile.py`, `client`, `test_interview.py`, `applications.py`, `test_auth.py`, `job.py`, `test_jobs.py`, `models/profile.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_matching.py`, `Job`, `models/__init__.py`, `admin.py`, `CvTemplate`, `jobs.py`, `TestClient`, `test_profile.py`, `test_cv_tailor_service_end_to_end`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `JobSourceHTTPError`, `linkedin.py`, `models/__init__.py`, `greenhouse.py`, `JobSearchQuery`, `RemoteOKJobSource`, `job.py`, `lever.py`, `RemotiveJobSource`, `job_ingestion.py`, `test_jobs.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `JobSearchQuery` connect `JobSearchQuery` to `JobPosting`, `JobSourceHTTPError`, `linkedin.py`, `models/__init__.py`, `greenhouse.py`, `RemoteOKJobSource`, `job.py`, `lever.py`, `RemotiveJobSource`, `job_ingestion.py`, `jobs.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 76 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 76 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `JobSearchQuery` (e.g. with `IngestionRequest` and `JobIngestionService`) actually correct?**
  _`JobSearchQuery` has 22 INFERRED edges - model-reasoned connections that need verification._
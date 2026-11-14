# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 282 files · ~207,853 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2899 nodes · 8040 edges · 147 communities (127 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1092 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fdee640b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- Job
- LatexLogParser
- TestClient
- FastAPI Backend Development Standards (adapted from ECC)
- api/profile.py
- SendGateway
- JobSourceHTTPError
- Base
- FreehireJobSource
- JobSearchQuery
- applications.py
- test_google_dispatch.py
- check_migrations.py
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- test_auth.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_apply_graph.py
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- What You Must Do When Invoked
- typing
- GoogleIntegrationService
- MatchingService
- create_app
- StarStory
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- test_decoupled_tools.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- api/auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- TenantScopedAsyncPostgresSaver
- Project: Job Application Agent SaaS
- TestClient
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- FormDetectiveService
- graphify reference: extra exports and benchmark
- latexCompiler.js
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- AgentEngine
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- dependencies
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- llm/service.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- trigger_ingestion
- React Frontend Development Standards (adapted from ECC)
- logging
- LanguageGate
- test_matching.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- config.py
- ProfileView.jsx
- Development Context — Job Application Agent SaaS
- matching/service.py
- tasks.py
- .generate
- tools.py
- JobPosting
- Product Development Environment Guide — Job Application Agent SaaS
- test_application_status_update
- ResumeBuilderView.jsx
- JobsView.jsx
- jobs.py
- adzuna.py
- MockQdrantClient
- ApplicationFormAnswer
- api/interview.py
- deploy.sh
- cv_parser.py
- application.py
- fit_analyzer.py
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- MimeBuilder
- .role
- apply_graph.py
- theme.js
- sse_adapter.py
- test_engine_approval_and_lifecycle.py
- test_educations_skills_and_preview
- devDependencies
- test_models.py
- Application
- client
- Account
- drafter_service.py
- test_monitor_followups_task
- Roadmap — Job Application Agent SaaS
- test_profile_compile_texlive.py
- CVTailorService
- texlive_compiler.py
- 6. Autonomy Policy Engine & Guardrails
- Security & Tenancy Policy (adapted from ECC AgentShield)
- LLMService
- LLMProviderBase
- 1. Executive Summary & Scope
- 9. Redesigned SSE Protocol Adapter & UI Integration
- 13. Strategic Options Analysis & Recommendation
- env.py
- plan_relevance_cuts
- .select_summary_variant
- parse_redis_settings
- prune_and_budget_latex
- .generate
- db_session
- 12. Dependency Plan & Environment Strategy
- .to_dict

## God Nodes (most connected - your core abstractions)
1. `Account` - 220 edges
2. `Job` - 115 edges
3. `Base` - 103 edges
4. `Application` - 79 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 72 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 55 edges
9. `SendGateway` - 53 edges
10. `LLMService` - 51 edges

## Surprising Connections (you probably didn't know these)
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.4 Model 4: `ModelPricing` (In `backend/app/models/model_pricing.py`)` --references--> `ModelPricing`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/model_pricing.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `7.2 Integration Strategy` --references--> `ApplicationStudio()`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → frontend/src/components/ApplicationStudio.jsx

## Import Cycles
- None detected.

## Communities (147 total, 20 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.13
Nodes (22): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+14 more)

### Community 3 - "Job"
Cohesion: 0.11
Nodes (34): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+26 more)

### Community 5 - "TestClient"
Cohesion: 0.10
Nodes (21): TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations., GET and PUT on compensation expectations., CRUD operations on spoken languages., Verify complete isolation between tenants A and B for profile and related…, Test full CRUD cycle for work experiences. (+13 more)

### Community 6 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 7 - "api/profile.py"
Cohesion: 0.10
Nodes (64): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+56 more)

### Community 8 - "SendGateway"
Cohesion: 0.07
Nodes (55): ApplicationPdfPayload, HoldQueueItem, Stores compiled PDF byte payloads outside applications table to prevent bloat., Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical… (+47 more)

### Community 9 - "JobSourceHTTPError"
Cohesion: 0.06
Nodes (40): JobSourceConfigError, JobSourceError, JobSourceHTTPError, Exception, Raised when an external job source HTTP request fails., Base exception for job source errors., Raised when job source credentials or settings are missing/invalid., _clean_html() (+32 more)

### Community 10 - "Base"
Cohesion: 0.21
Nodes (22): Base, Base SQLAlchemy declarative model., get_db(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.…, Multi-tenant STAR Interview Coach models. Stores STAR-format interview stories… (+14 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (26): classify_location_type(), Robust location classifier prioritizing: 1. Explicit work mode if provided…, _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient (+18 more)

### Community 12 - "JobSearchQuery"
Cohesion: 0.09
Nodes (28): JobSearchQuery, Normalized query parameters for searching across job sources., _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime (+20 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (46): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+38 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.07
Nodes (55): 2. Secrets & Encryption, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), encrypt_secret(), _get_legacy_fernet(), get_oauth_fernet() (+47 more)

### Community 15 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (29): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+21 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (24): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps… (+16 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.14
Nodes (15): Run underlying setup and enforce Row Level Security on checkpointer tables in…, 14. Milestone Roadmap & Effort Estimates, 15. Decision Register, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 7.1 Scope Classification & CASA Exemption, 7.2 Integration Strategy (+7 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.08
Nodes (33): CVReviewOutput, BaseModel, mock_llm_responses(), asyncio, fixture, backend/tests/agent/test_apply_graph.py Unit tests for Modular LangGraph…, Verifies resuming an interrupted graph with Command(resume=reject) terminates…, Verifies legitimate corporate email with trusted recipient executes… (+25 more)

### Community 23 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.05
Nodes (23): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+15 more)

### Community 26 - "GoogleIntegrationService"
Cohesion: 0.08
Nodes (31): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+23 more)

### Community 27 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 28 - "create_app"
Cohesion: 0.09
Nodes (16): create_app(), lifespan(), Create and configure FastAPI application., api_test_db(), client(), fixture, api_test_db(), client() (+8 more)

### Community 29 - "StarStory"
Cohesion: 0.23
Nodes (12): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field. (+4 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.14
Nodes (27): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+19 more)

### Community 32 - "api/agent.py"
Cohesion: 0.07
Nodes (48): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+40 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (35): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+27 more)

### Community 41 - "test_decoupled_tools.py"
Cohesion: 0.15
Nodes (23): Executes Pass 2 Senior Recruiter CV review. Audits for unverified claims,…, review_cv_endpoint(), CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput, prune_and_budget_latex(), BaseModel (+15 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.12
Nodes (47): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+39 more)

### Community 45 - "api/auth.py"
Cohesion: 0.06
Nodes (55): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+47 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "lucide-react"
Cohesion: 0.18
Nodes (16): 2. Current State Map (Codebase Ground Truth), CareerCopilotView(), FAST_CHIPS, formatInlineMarkdown(), STARTER_PROMPTS, TurnMarkdownContent(), FunnelInsight(), JobRadarCarousel() (+8 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "TenantScopedAsyncPostgresSaver"
Cohesion: 0.07
Nodes (35): AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), Any, backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph…, Deletes thread checkpoints and cleans up thread_accounts registry. Requires…, Factory creating a psycopg_pool.AsyncConnectionPool calibrated for Supabase… (+27 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (19): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 1. Scope & rollout (+11 more)

### Community 60 - "FormDetectiveService"
Cohesion: 0.18
Nodes (17): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+9 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "latexCompiler.js"
Cohesion: 0.19
Nodes (18): ApplicationStudio(), ResumeBuilderView(), ResumePreviewModal(), StudioApprovalGate(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), cleanLatexInline() (+10 more)

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

### Community 67 - "AgentEngine"
Cohesion: 0.13
Nodes (12): AgentEngine, Any, Session, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks. (+4 more)

### Community 70 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @codemirror/commands, @codemirror/language, @codemirror/legacy-modes, @codemirror/lint, @codemirror/search, @codemirror/state, @codemirror/view (+5 more)

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
Cohesion: 0.16
Nodes (15): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+7 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "trigger_ingestion"
Cohesion: 0.18
Nodes (13): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+5 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "logging"
Cohesion: 0.14
Nodes (19): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+11 more)

### Community 82 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 83 - "test_matching.py"
Cohesion: 0.06
Nodes (38): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+30 more)

### Community 84 - "test_agent.py"
Cohesion: 0.10
Nodes (26): BaseModel, SearchJobsInput, BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client() (+18 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "config.py"
Cohesion: 0.06
Nodes (36): argparse, asyncio, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), decimal, json (+28 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 92 - "matching/service.py"
Cohesion: 0.10
Nodes (22): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,… (+14 more)

### Community 93 - "tasks.py"
Cohesion: 0.15
Nodes (18): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+10 more)

### Community 94 - ".generate"
Cohesion: 0.13
Nodes (15): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 2.2 Tenancy Exemption in `scripts/check_migrations.py` (+7 more)

### Community 95 - "tools.py"
Cohesion: 0.12
Nodes (26): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+18 more)

### Community 96 - "JobPosting"
Cohesion: 0.08
Nodes (30): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobUpdate, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+22 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 98 - "test_application_status_update"
Cohesion: 0.23
Nodes (12): Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer., Test Module 2 (Apply) application tailoring and strict human-in-the-loop Send…, test_application_status_update() (+4 more)

### Community 99 - "ResumeBuilderView.jsx"
Cohesion: 0.20
Nodes (11): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+3 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "jobs.py"
Cohesion: 0.33
Nodes (6): get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Resolve the current authenticated account context. 1. Primary: Validates…, jwt

### Community 102 - "adzuna.py"
Cohesion: 0.09
Nodes (27): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+19 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "ApplicationFormAnswer"
Cohesion: 0.14
Nodes (15): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts. (+7 more)

### Community 105 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 108 - "application.py"
Cohesion: 0.36
Nodes (9): ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationRead, ApplicationUpdate (+1 more)

### Community 109 - "fit_analyzer.py"
Cohesion: 0.29
Nodes (7): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic…, langgraph_graph_message

### Community 110 - "test_tools_api.py"
Cohesion: 0.13
Nodes (21): account_a(), api_test_db(), client(), fixture, Session, TestClient, backend/tests/api/test_tools_api.py Unit and integration tests for Decoupled…, Test POST /api/v1/tools/detect-method discovers email application. (+13 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.10
Nodes (52): AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateUpdate, BaseModel, OAuthConnectionBase, OAuthConnectionCreate (+44 more)

### Community 113 - "MimeBuilder"
Cohesion: 0.10
Nodes (27): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, Encode raw MIME bytes to base64url string required by the Gmail API., Base exception for MIME construction and validation errors. (+19 more)

### Community 114 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 115 - "apply_graph.py"
Cohesion: 0.09
Nodes (43): TOFU Exact-Address allowlist. Email uniqueness is enforced case-insensitively…, TrustedRecipient, assemble_package_node(), autonomy_gate_edge(), build_apply_graph(), cv_drafter_node(), cv_reviewer_node(), detect_method_node() (+35 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "sse_adapter.py"
Cohesion: 0.13
Nodes (20): run_resume_background(), run_apply_background(), dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent… (+12 more)

### Community 118 - "test_engine_approval_and_lifecycle.py"
Cohesion: 0.07
Nodes (52): AccountQuotaOverride, AccountSubscription, AccountUsageCounter, QuotaReservation, Tracks tenant subscription plan association and billing cycles. One active…, Append-only usage ledger. scope separates tenant usage from platform background…, Administrative overrides for quota limits. Precedence: Override > Plan >…, Live aggregated balances per billing period. Updated transactionally with… (+44 more)

### Community 119 - "test_educations_skills_and_preview"
Cohesion: 0.28
Nodes (8): account_a(), account_b(), api_test_db(), client(), fixture, Session, Test educations, bulk skills, and preview CV generation., test_educations_skills_and_preview()

### Community 120 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 121 - "test_models.py"
Cohesion: 0.07
Nodes (57): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), ApplicationCreate, CvTemplate, CvTemplateCreate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, LLMProviderCreate (+49 more)

### Community 122 - "Application"
Cohesion: 0.10
Nodes (30): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountDispatchSettings, DispatchedAction, JobFeedback, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or… (+22 more)

### Community 123 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 124 - "Account"
Cohesion: 0.16
Nodes (18): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint() (+10 more)

### Community 125 - "drafter_service.py"
Cohesion: 0.23
Nodes (11): FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterOutput, OutreachDrafterService, Any, BaseModel, Enum (+3 more)

### Community 126 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 127 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 128 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 129 - "CVTailorService"
Cohesion: 0.13
Nodes (22): patch, update_certification(), update_education(), update_project(), update_skill(), update_work_experience(), Certification, Education (+14 more)

### Community 130 - "texlive_compiler.py"
Cohesion: 0.16
Nodes (15): compile_texlive(), build_sandboxed_tex_env(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Construct scrubbed environment for TeX compilation child processes. - Strips…, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine with strict… (+7 more)

### Community 131 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.40
Nodes (4): 1. Multi-Tenant Partitioning, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - "LLMService"
Cohesion: 0.15
Nodes (8): Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, test_cv_tailor_service_end_to_end()

### Community 134 - "LLMProviderBase"
Cohesion: 0.50
Nodes (4): 4. Pydantic Schemas & Security, LLMProviderBase, LLMProviderUpdate, BaseModel

### Community 135 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

### Community 136 - "9. Redesigned SSE Protocol Adapter & UI Integration"
Cohesion: 0.67
Nodes (3): 9.1 Custom Streaming Loop (Part Objects in Version "v2"), 9.2 Resume Endpoint & Minimal Frontend Contract, 9. Redesigned SSE Protocol Adapter & UI Integration

### Community 137 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 138 - "env.py"
Cohesion: 0.15
Nodes (20): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+12 more)

### Community 139 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 146 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 157 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 158 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1124 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `CVTailorService`, `tailor_service.py`, `Job`, `TestClient`, `LLMService`, `api/profile.py`, `SendGateway`, `Base`, `applications.py`, `test_google_dispatch.py`, `TestClient`, `test_auth.py`, `GoogleIntegrationService`, `create_app`, `api/agent.py`, `test_admin.py`, `test_decoupled_tools.py`, `admin.py`, `api/auth.py`, `TestClient`, `Architecture — Job Application Agent SaaS`, `trigger_ingestion`, `logging`, `test_matching.py`, `test_agent.py`, `matching/service.py`, `tasks.py`, `tools.py`, `JobPosting`, `test_application_status_update`, `jobs.py`, `ApplicationFormAnswer`, `application.py`, `test_tools_api.py`, `models/__init__.py`, `test_engine_approval_and_lifecycle.py`, `test_educations_skills_and_preview`, `test_models.py`, `Application`, `client`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `CVTailorService`, `tailor_service.py`, `LLMService`, `SendGateway`, `Base`, `applications.py`, `TestClient`, `MatchingService`, `engine.py`, `test_admin.py`, `admin.py`, `FormDetectiveService`, `AgentEngine`, `trigger_ingestion`, `logging`, `test_matching.py`, `test_agent.py`, `matching/service.py`, `tasks.py`, `tools.py`, `JobPosting`, `test_application_status_update`, `jobs.py`, `ApplicationFormAnswer`, `api/interview.py`, `application.py`, `fit_analyzer.py`, `test_tools_api.py`, `models/__init__.py`, `.role`, `apply_graph.py`, `test_engine_approval_and_lifecycle.py`, `test_models.py`, `Application`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `LLMService`, `test_decoupled_tools.py`, `Base`, `llm/service.py`, `test_google_dispatch.py`, `check_migrations.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `GoogleIntegrationService`, `MatchingService`, `matching/service.py`, `engine.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 139 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
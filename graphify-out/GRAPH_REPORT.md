# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 293 files · ~219,411 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 3022 nodes · 8594 edges · 160 communities (135 shown, 25 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1211 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06371840`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- typing
- Job
- LatexLogParser
- TestClient
- FormDetectiveService
- api/profile.py
- client
- GreenhouseJobSource
- Base
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- gateway.py
- Account
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- GoogleIntegrationService
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- seed_test_apply_graph_fixtures
- job.py
- What You Must Do When Invoked
- 3257c49a645d_add_agent_action_proposals_.py
- create_gmail_draft
- MatchingService
- test_oauth_integrations.py
- Education
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- create_app
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- ProfileSkill
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
- UserProfile
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
- test_llm.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- FastAPI Backend Development Standards (adapted from ECC)
- React Frontend Development Standards (adapted from ECC)
- StageApplicationProposalTool
- test_matching.py
- 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- email_service.py
- react
- alembic
- client
- dispatch_service.py
- Product Development Environment Guide — Job Application Agent SaaS
- tools.py
- client
- SpokenLanguage
- TargetDesignation
- StudioDrafterWorkspace.jsx
- JobsView.jsx
- test_engine_approval_and_lifecycle.py
- JobSearchQuery
- test_matching_service_score_and_gate_clean_jobs
- ApplicationFormAnswer
- api/interview.py
- deploy.sh
- cv_parser.py
- llm/service.py
- Application
- TestClient
- bug-workflow.md
- models/profile.py
- TargetLocation
- get_current_account
- apply_graph.py
- theme.js
- LangGraphSSEAdapter
- check_migrations.py
- AnthropicProvider
- LLMService
- models/__init__.py
- GeminiProvider
- test_cv_tailor_service_with_structured_profile
- client
- BaseAgentTool
- CvTemplate
- 74cebd545352_add_is_pinned_to_agent_conversations.py
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- a7c3e1f24b01_add_profile_and_interview_tables.py
- TeXLiveCompilerService
- experience_reflector.py
- Security & Tenancy Policy (adapted from ECC AgentShield)
- .generate
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
- .setup
- normalize_db_url
- tasks.py
- test_profile_compile_texlive.py
- get_available_sources
- SendGatewayException
- 6. Autonomy Policy Engine & Guardrails
- doctor.py
- Development Context — Job Application Agent SaaS
- LanguageGate
- e2e_account_and_job
- 13. Strategic Options Analysis & Recommendation
- .generate
- db_session
- 12. Dependency Plan & Environment Strategy
- 7. Gmail Integration Architecture (Scope Correction)
- 1. Executive Summary & Scope

## God Nodes (most connected - your core abstractions)
1. `Account` - 249 edges
2. `Job` - 124 edges
3. `Base` - 108 edges
4. `Application` - 85 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 74 edges
7. `JobSearchQuery` - 62 edges
8. `LLMService` - 57 edges
9. `AgentEngine` - 55 edges
10. `SendGateway` - 55 edges

## Surprising Connections (you probably didn't know these)
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.1 Model 1: `AccountSubscription` (Anchored Billing Periods)` --references--> `AccountSubscription`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle)` --references--> `QuotaReservation`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py

## Import Cycles
- None detected.

## Communities (160 total, 25 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "typing"
Cohesion: 0.04
Nodes (63): asyncio, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), format_sse_frame(), backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line. (+55 more)

### Community 3 - "Job"
Cohesion: 0.09
Nodes (41): Integration Checklist, Job Source Integrator, Job, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService (+33 more)

### Community 5 - "TestClient"
Cohesion: 0.07
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "FormDetectiveService"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 7 - "api/profile.py"
Cohesion: 0.14
Nodes (42): delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill(), delete_user_resume() (+34 more)

### Community 8 - "client"
Cohesion: 0.15
Nodes (15): api_test_db(), client(), fixture, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application… (+7 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "Base"
Cohesion: 0.12
Nodes (35): Base, Base SQLAlchemy declarative model., Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), get_db(), get_engine(), get_session_factory() (+27 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (46): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+38 more)

### Community 14 - "gateway.py"
Cohesion: 0.05
Nodes (81): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy… (+73 more)

### Community 15 - "Account"
Cohesion: 0.08
Nodes (43): list_jobs(), get, Fetch jobs for an account ordered by match_score descending. Excludes vetoed…, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, auth_client() (+35 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (35): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+27 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "GoogleIntegrationService"
Cohesion: 0.13
Nodes (17): auth_google_authorize(), get_me(), get, Retrieve authenticated account profile and permissions from validated token., get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition and outbound…, GoogleIntegrationService (+9 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.14
Nodes (15): CopilotState, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.2 Node Inventory Table & Tailor Refactoring (+7 more)

### Community 22 - "seed_test_apply_graph_fixtures"
Cohesion: 0.40
Nodes (5): mock_llm_responses(), fixture, Seeds test account and jobs in PostgreSQL to satisfy relational foreign key…, Mock LLMService.generate to return valid structured responses., seed_test_apply_graph_fixtures()

### Community 23 - "job.py"
Cohesion: 0.13
Nodes (28): JobBase, JobCreate, JobUpdate, BaseModel, _detect_location_type(), _parse_created_date(), datetime, Parse ISO formatted creation date from Adzuna response. (+20 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 26 - "create_gmail_draft"
Cohesion: 0.10
Nodes (30): auth_google_callback_get(), BookmarkletResponse, connect_smtp(), create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), disconnect_smtp() (+22 more)

### Community 27 - "MatchingService"
Cohesion: 0.15
Nodes (10): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+2 more)

### Community 28 - "test_oauth_integrations.py"
Cohesion: 0.18
Nodes (20): PlatformOAuthAppConfig, Platform-wide or tenant-specific OAuth application credentials (e.g. Google…, admin_client(), oauth_test_db(), fixture, Session, TestClient, Regular candidates cannot view or edit platform Google OAuth credentials. (+12 more)

### Community 29 - "Education"
Cohesion: 0.15
Nodes (15): add_education(), patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience() (+7 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.22
Nodes (14): Enum, str, ToolCategory, ToolResult, ApplicationTailoredEvent, DomainEventBus, Decoupled in-memory asynchronous pub/sub Event Bus for domain events. Allows…, AutonomousTailorCVTool (+6 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (43): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+35 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "create_app"
Cohesion: 0.12
Nodes (24): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+16 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (33): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+25 more)

### Community 41 - "ProfileSkill"
Cohesion: 0.22
Nodes (13): add_skill(), apply_parsed_cv(), bulk_skills(), compile_texlive(), post, update_skill(), ProfileSkill, ProfileSkillRead (+5 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.10
Nodes (54): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_google_oauth_config(), delete_admin_template(), delete_job(), delete_llm_provider() (+46 more)

### Community 45 - "api/auth.py"
Cohesion: 0.14
Nodes (27): auth_google_callback_post(), login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated… (+19 more)

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
Cohesion: 0.06
Nodes (39): AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), normalize_libpq_url(), Any, backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph…, Deletes thread checkpoints and cleans up thread_accounts registry. Requires… (+31 more)

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
Cohesion: 0.06
Nodes (34): check_job_liveness(), IngestionRequest, IngestionResponse, BaseModel, post, Session, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run. (+26 more)

### Community 60 - "UserProfile"
Cohesion: 0.18
Nodes (20): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, CVTailorService, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Selects the best fact-verified Summary variant based on role keywords or…, FormFieldQuestion (+12 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "latexCompiler.js"
Cohesion: 0.17
Nodes (24): ApplicationStudio(), SavedResumesTab(), ProfileView(), ResumeBuilderView(), TEMPLATES, ResumePreviewModal(), StudioApprovalGate(), downloadLatexSource() (+16 more)

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
Cohesion: 0.14
Nodes (12): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Executes human-in-the-loop approval of an action proposal. Enforces tenant… (+4 more)

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

### Community 74 - "test_llm.py"
Cohesion: 0.17
Nodes (14): MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, asyncio, Verify 3-tier failover: Gemini (priority 1 fails) -> Claude (priority 2 fails)…, test_anthropic_provider_generate_success(), test_anthropic_provider_missing_key(), test_gemini_provider_generate_success() (+6 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "StageApplicationProposalTool"
Cohesion: 0.19
Nodes (12): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, DomainEvent, JobIngestedEvent, ProposalCreatedEvent, BaseModel, BaseModel, StageApplicationProposalTool (+4 more)

### Community 82 - "test_matching.py"
Cohesion: 0.10
Nodes (23): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+15 more)

### Community 83 - "3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.40
Nodes (5): 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods), 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances), 3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle), 3.5 Model 5: `UsageEvent` (Scope Column Added), 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (34): ToolExecutionContext, ExperienceReflectorInput, ExperienceReflectorTool, BaseModel, BaseModel, SearchAndRankJobsTool, SearchJobsInput, BaseModel (+26 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "email_service.py"
Cohesion: 0.23
Nodes (10): generate_otp(), is_smtp_configured(), Check if outbound SMTP server credentials are fully configured., Generate a cryptographically secure 6-digit numeric OTP code., Send 6-digit OTP verification email to user. Falls back gracefully to secure…, send_otp_email(), email_mime_multipart, email_mime_text (+2 more)

### Community 90 - "react"
Cohesion: 0.14
Nodes (12): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileIntegrationsTab(), ProfileProjectModal(), ProfileProjectsTab() (+4 more)

### Community 91 - "alembic"
Cohesion: 0.25
Nodes (3): alembic, Upgrade schema to include platform_oauth_configs table., upgrade()

### Community 92 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 93 - "dispatch_service.py"
Cohesion: 0.16
Nodes (16): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+8 more)

### Community 94 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 95 - "tools.py"
Cohesion: 0.07
Nodes (54): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+46 more)

### Community 96 - "client"
Cohesion: 0.29
Nodes (7): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint()

### Community 97 - "SpokenLanguage"
Cohesion: 0.38
Nodes (7): add_language(), list_languages(), Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, SpokenLanguageBase, SpokenLanguageCreate, SpokenLanguageRead

### Community 98 - "TargetDesignation"
Cohesion: 0.13
Nodes (17): add_designation(), list_designations(), CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Salary / compensation expectations (one per profile). Marked sensitive — never…, TargetDesignation, TargetDesignationBase, TargetDesignationCreate (+9 more)

### Community 99 - "StudioDrafterWorkspace.jsx"
Cohesion: 0.21
Nodes (10): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics() (+2 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "test_engine_approval_and_lifecycle.py"
Cohesion: 0.07
Nodes (51): ApplicationPdfPayload, Stores compiled PDF byte payloads outside applications table to prevent bloat., AccountQuotaOverride, AccountSubscription, AccountUsageCounter, QuotaReservation, Tracks tenant subscription plan association and billing cycles. One active…, Append-only usage ledger. scope separates tenant usage from platform background… (+43 more)

### Community 102 - "JobSearchQuery"
Cohesion: 0.09
Nodes (28): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), Any, AsyncClient, Asynchronously fetch job postings matching the query from Adzuna. (+20 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - "ApplicationFormAnswer"
Cohesion: 0.20
Nodes (12): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and… (+4 more)

### Community 105 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.11
Nodes (16): parse_cv_file(), UploadFile, CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf. (+8 more)

### Community 108 - "llm/service.py"
Cohesion: 0.31
Nodes (6): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…

### Community 109 - "Application"
Cohesion: 0.04
Nodes (106): app_services_agent_checkpointer, app_services_agent_workflows_apply_graph, app_services_dispatch_gateway, mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountDispatchSettings (+98 more)

### Community 110 - "TestClient"
Cohesion: 0.10
Nodes (21): account_a(), api_test_db(), client(), fixture, Session, TestClient, Test POST /api/v1/tools/detect-method discovers email application., Test POST /api/v1/tools/draft-cv produces tailored LaTeX without mutation. (+13 more)

### Community 112 - "models/profile.py"
Cohesion: 0.13
Nodes (28): add_certification(), add_work_experience(), create_profile(), Create a user profile for an account (one per account)., CertificationBase, CertificationCreate, CertificationRead, CertificationUpdate (+20 more)

### Community 113 - "TargetLocation"
Cohesion: 0.38
Nodes (7): add_location(), list_locations(), Target work locations / regions a user is willing to work in. Supports remote /…, TargetLocation, TargetLocationBase, TargetLocationCreate, TargetLocationRead

### Community 114 - "get_current_account"
Cohesion: 0.33
Nodes (7): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…

### Community 115 - "apply_graph.py"
Cohesion: 0.05
Nodes (84): assemble_package_node(), autonomy_gate_edge(), build_apply_graph(), cv_drafter_node(), cv_reviewer_node(), detect_method_node(), dispatch_node(), fit_analyzer_node() (+76 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "LangGraphSSEAdapter"
Cohesion: 0.14
Nodes (16): run_apply_background(), dump_model(), get_field(), LangGraphSSEAdapter, Any, Serializes Pydantic models cleanly using model_dump() or dict()., Safely extracts field from either Pydantic model or dict., Translates LangGraph stream chunks into SSE events. (+8 more)

### Community 118 - "check_migrations.py"
Cohesion: 0.38
Nodes (6): 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 119 - "AnthropicProvider"
Cohesion: 0.33
Nodes (5): AnthropicProvider, Any, Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet /…, Verify that encrypted API keys stored in DB are decrypted and resolved into…, test_llm_service_db_provider_decryption_and_resolution()

### Community 120 - "LLMService"
Cohesion: 0.17
Nodes (6): Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, Verify that tenant-specific provider rows take precedence over global NULL…, test_llm_service_tenant_override_ordering_tiebreaker()

### Community 121 - "models/__init__.py"
Cohesion: 0.08
Nodes (48): 4. Pydantic Schemas & Security, add_project(), ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead (+40 more)

### Community 122 - "GeminiProvider"
Cohesion: 0.33
Nodes (4): GeminiProvider, Any, Google Gemini implementation of the LLMProvider interface (Gemini 2.5 Flash /…, Resolve ordered list of active providers from database or defaults.

### Community 123 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 124 - "client"
Cohesion: 0.40
Nodes (5): api_test_db(), client(), fixture, Session, test_account()

### Community 125 - "BaseAgentTool"
Cohesion: 0.13
Nodes (11): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an…, Session, AgentToolRegistry (+3 more)

### Community 126 - "CvTemplate"
Cohesion: 0.10
Nodes (22): CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test SubscriptionPlan and Entitlement models matching ARCHITECTURE.md §0 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Verify that deleting an account cascades to all tenant-scoped rows. (+14 more)

### Community 127 - "74cebd545352_add_is_pinned_to_agent_conversations.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations., upgrade()

### Community 128 - "7f7822f4eef9_add_github_url_to_projects_and_location_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade()

### Community 129 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.09
Nodes (25): build_sandboxed_tex_env(), ensure_latex_preamble_macros(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Detect available Docker container with pdflatex., Return True if a TeX compiler is installed and executable locally or in Docker., Compile LaTeX source into PDF inside a Docker worker container with TeX Live…, Compile LaTeX source into PDF using system TeX Live engine or Docker container… (+17 more)

### Community 131 - "experience_reflector.py"
Cohesion: 0.10
Nodes (21): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser (+13 more)

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - ".generate"
Cohesion: 0.10
Nodes (19): Any, Execute generation across the provider chain with automatic fallback., Return execution metadata from the last successful LLM call for…, 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope (+11 more)

### Community 134 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 136 - ".setup"
Cohesion: 0.40
Nodes (5): Run underlying setup and enforce Row Level Security on checkpointer tables in…, 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 138 - "normalize_db_url"
Cohesion: 0.12
Nodes (20): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+12 more)

### Community 141 - "tasks.py"
Cohesion: 0.10
Nodes (29): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+21 more)

### Community 144 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH or Docker, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 147 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 148 - "SendGatewayException"
Cohesion: 0.67
Nodes (3): Exception, Base exception for SendGateway dispatch failures., SendGatewayException

### Community 149 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 150 - "doctor.py"
Cohesion: 0.67
Nodes (3): check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor()

### Community 151 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 152 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 153 - "e2e_account_and_job"
Cohesion: 0.67
Nodes (3): e2e_account_and_job(), fixture, Seed real Account, Job, AccountDispatchSettings, and TrustedRecipient in test…

### Community 154 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 156 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 157 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

### Community 158 - "7. Gmail Integration Architecture (Scope Correction)"
Cohesion: 0.67
Nodes (3): 7.1 Scope Classification & CASA Exemption, 7.2 Integration Strategy, 7. Gmail Integration Architecture (Scope Correction)

### Community 162 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1162 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `typing`, `Job`, `TestClient`, `api/profile.py`, `client`, `Base`, `applications.py`, `gateway.py`, `tasks.py`, `TestClient`, `GoogleIntegrationService`, `seed_test_apply_graph_fixtures`, `job.py`, `e2e_account_and_job`, `create_gmail_draft`, `test_oauth_integrations.py`, `api/agent.py`, `create_app`, `ProfileSkill`, `admin.py`, `api/auth.py`, `TestClient`, `Architecture — Job Application Agent SaaS`, `UserProfile`, `StageApplicationProposalTool`, `test_matching.py`, `test_agent.py`, `client`, `tools.py`, `client`, `TargetDesignation`, `test_engine_approval_and_lifecycle.py`, `test_matching_service_score_and_gate_clean_jobs`, `ApplicationFormAnswer`, `Application`, `TestClient`, `models/profile.py`, `get_current_account`, `apply_graph.py`, `models/__init__.py`, `test_cv_tailor_service_with_structured_profile`, `client`, `CvTemplate`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `typing`, `experience_reflector.py`, `client`, `Base`, `applications.py`, `gateway.py`, `Account`, `tasks.py`, `TestClient`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `seed_test_apply_graph_fixtures`, `job.py`, `e2e_account_and_job`, `MatchingService`, `engine.py`, `create_app`, `admin.py`, `Architecture — Job Application Agent SaaS`, `UserProfile`, `AgentEngine`, `StageApplicationProposalTool`, `test_matching.py`, `test_agent.py`, `tools.py`, `test_engine_approval_and_lifecycle.py`, `test_matching_service_score_and_gate_clean_jobs`, `ApplicationFormAnswer`, `api/interview.py`, `Application`, `TestClient`, `apply_graph.py`, `models/__init__.py`, `test_cv_tailor_service_with_structured_profile`, `CvTemplate`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `ApplicationStudio()` connect `latexCompiler.js` to `App.jsx`, `JobsView.jsx`, `JobEazy: Milestone M1 & M1b Implementation Specification`, `Application`, `7. Gmail Integration Architecture (Scope Correction)`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 164 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 164 INFERRED edges - model-reasoned connections that need verification._
- **Are the 55 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 55 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 35 INFERRED edges - model-reasoned connections that need verification._
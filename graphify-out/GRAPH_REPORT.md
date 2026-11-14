# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 286 files · ~210,986 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2939 nodes · 8235 edges · 161 communities (137 shown, 24 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1127 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9b7d656c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobIngestionService
- LatexLogParser
- Account
- FormDetectiveService
- api/profile.py
- SendGateway
- asyncio
- typing
- FreehireJobSource
- test_remoteok_fetch_with_mock_client
- applications.py
- test_google_dispatch.py
- test_decoupled_tools.py
- package.json
- asyncio
- test_remotive_fetch_with_mock_client
- TestClient
- test_auth.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_apply_graph.py
- JobPosting
- What You Must Do When Invoked
- alembic
- integrations.py
- .__init__
- client
- Application
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- drafter_service.py
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
- api/interview.py
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
- trigger_ingestion
- React Frontend Development Standards (adapted from ECC)
- StageApplicationProposalTool
- test_matching.py
- .embed
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- pathlib
- ProfileView.jsx
- ProfileSkill
- .score_and_gate_jobs
- dispatch_service.py
- Product Development Environment Guide — Job Application Agent SaaS
- tools.py
- UserProfile
- MimeBuilder
- seed_initial_data
- ResumeBuilderView.jsx
- JobsView.jsx
- QuotaService
- test_adzuna_fetch_with_mock_client
- test_matching_service_score_and_gate_clean_jobs
- ApplicationFormAnswer
- core/auth.py
- deploy.sh
- cv_parser.py
- logging
- Base
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- google_service.py
- dispatch_poller.py
- apply_graph.py
- theme.js
- json
- .role
- .fetch
- LLMService
- Job
- test_monitor_followups_task
- .embed_batch
- test_apply_to_gateway_e2e.py
- AgentToolRegistry
- test_educations_skills_and_preview
- .fetch
- .fetch
- Education
- TeXLiveCompilerService
- ExperienceReflector
- Security & Tenancy Policy (adapted from ECC AgentShield)
- JobEazy: Milestone M1m Implementation Specification
- DispatchedAction
- .generate
- .setup
- client
- env.py
- Session
- devDependencies
- FastAPI Backend Development Standards (adapted from ECC)
- .queue_application_send
- 5.2 Node Inventory Table & Tailor Refactoring
- test_profile_compile_texlive.py
- test_cv_tailor_service_with_structured_profile
- db_session
- IngestionRequest
- AnthropicProvider
- parse_redis_settings
- client
- Development Context — Job Application Agent SaaS
- .check
- test_google_callback_and_status
- 13. Strategic Options Analysis & Recommendation
- .generate
- db_session
- 12. Dependency Plan & Environment Strategy
- .embed_batch
- .embed_batch
- .search_similar_jobs

## God Nodes (most connected - your core abstractions)
1. `Account` - 228 edges
2. `Job` - 120 edges
3. `Base` - 103 edges
4. `Application` - 83 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 72 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 55 edges
9. `SendGateway` - 55 edges
10. `LLMService` - 54 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py

## Import Cycles
- None detected.

## Communities (161 total, 24 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.08
Nodes (41): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), backend/app/services/cv_tailor/drafter.py Decoupled Senior Recruiter Drafter…, audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no… (+33 more)

### Community 3 - "JobIngestionService"
Cohesion: 0.08
Nodes (34): Integration Checklist, Job Source Integrator, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+26 more)

### Community 5 - "Account"
Cohesion: 0.07
Nodes (43): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations. (+35 more)

### Community 6 - "FormDetectiveService"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 7 - "api/profile.py"
Cohesion: 0.13
Nodes (41): create_profile(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+33 more)

### Community 8 - "SendGateway"
Cohesion: 0.07
Nodes (47): Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure., Handle retryable 429/5xx error by scheduling exponential backoff and releasing…, Atomically record successful external dispatch, evidence, and state transitions. (+39 more)

### Community 9 - "asyncio"
Cohesion: 0.12
Nodes (16): asyncio, String company slug is normalized and targets the correct URL., Non-200 responses raise JobSourceHTTPError., Traverse RFC 5988 Link headers across multiple pages until rel='next'…, Verify max_pages safely halts pagination even if next link exists., Verify max_postings stops accumulation as soon as cap is reached., Verify circular next links are detected and do not cause infinite loops., Parse a realistic Greenhouse response via injected MockTransport. (+8 more)

### Community 10 - "typing"
Cohesion: 0.06
Nodes (75): 4. Pydantic Schemas & Security, arq, arq_connections, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), get_db() (+67 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "test_remoteok_fetch_with_mock_client"
Cohesion: 0.13
Nodes (14): asyncio, A response with only the legal-notice element returns an empty list., String query is normalized; 'what' is sent as 'tag' param., Dict query is normalized and 'what' is sent as 'tag' param., Non-200 responses raise JobSourceHTTPError., Response with only legal notice yields empty list., Parse a realistic RemoteOK response via injected MockTransport., test_remoteok_empty_results() (+6 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (46): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+38 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.12
Nodes (31): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy… (+23 more)

### Community 15 - "test_decoupled_tools.py"
Cohesion: 0.14
Nodes (20): CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput, prune_and_budget_latex(), BaseModel, Executes Pass 1 (Senior Recruiter Drafter). Outputs tailored summary bullet,…, Selects the canonical summary bullet variant matching target job focus. (+12 more)

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "asyncio"
Cohesion: 0.13
Nodes (14): asyncio, String company slug is normalized and targets the correct URL., Non-200 responses raise JobSourceHTTPError., Verify offset pagination with skip parameter across multiple pages., Verify standard 100-batch pagination traversing to page 2 with skip=100., Verify max_pages safely terminates pagination even if full batches continue., Verify max_postings stops accumulation as soon as cap is reached., test_lever_fetch_string_slug() (+6 more)

### Community 18 - "test_remotive_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, String query is normalized and sent as 'search' param., Dict query is normalized; results_per_page is sent as 'limit'., Non-200 responses raise JobSourceHTTPError., Empty jobs array returns empty list., Parse a realistic Remotive response via injected MockTransport., test_remotive_empty_results(), test_remotive_fetch_dict_query() (+4 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "test_auth.py"
Cohesion: 0.15
Nodes (25): EmailVerification, Stores 6-digit OTP verification codes for user registration and email…, auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user() (+17 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.11
Nodes (18): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED] (+10 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.09
Nodes (33): CVReviewOutput, mock_llm_responses(), asyncio, fixture, backend/tests/agent/test_apply_graph.py Unit tests for Modular LangGraph…, Verifies resuming an interrupted graph with Command(resume=approve) runs…, Verifies resuming an interrupted graph with Command(resume=reject) terminates…, Verifies legitimate corporate email with trusted recipient executes… (+25 more)

### Community 23 - "JobPosting"
Cohesion: 0.05
Nodes (77): JobPosting, JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources., Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, AdzunaJobSource, _clean_text() (+69 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "integrations.py"
Cohesion: 0.16
Nodes (24): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+16 more)

### Community 28 - "client"
Cohesion: 0.29
Nodes (7): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint()

### Community 29 - "Application"
Cohesion: 0.11
Nodes (31): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, HoldQueueItem, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, SendAuthorization, assemble_package_node(), dispatch_node() (+23 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.13
Nodes (30): asyncio, BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous… (+22 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (43): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+35 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.13
Nodes (24): create_app(), lifespan(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture (+16 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (33): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+25 more)

### Community 41 - "drafter_service.py"
Cohesion: 0.12
Nodes (17): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic…, FormAnswerPair, OutreachChannelType (+9 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.11
Nodes (50): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+42 more)

### Community 45 - "api/auth.py"
Cohesion: 0.10
Nodes (35): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+27 more)

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
Nodes (40): AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), normalize_libpq_url(), Any, backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph…, Deletes thread checkpoints and cleans up thread_accounts registry. Requires… (+32 more)

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
Cohesion: 0.12
Nodes (16): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN), 4. Module 1 — Find Job Opportunity (decision made) (+8 more)

### Community 60 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

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

### Community 79 - "trigger_ingestion"
Cohesion: 0.29
Nodes (8): check_job_liveness(), list_jobs(), get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed…, Trigger job ingestion pipeline for an account., trigger_ingestion()

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "StageApplicationProposalTool"
Cohesion: 0.33
Nodes (8): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ProposalCreatedEvent, BaseModel, StageApplicationProposalTool, StageProposalInput, Test human-in-the-loop Send gate: 1. Tool creates AgentActionProposal with…, test_stage_proposal_and_approval_flow()

### Community 82 - "test_matching.py"
Cohesion: 0.09
Nodes (34): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+26 more)

### Community 84 - "test_agent.py"
Cohesion: 0.12
Nodes (22): BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client(), fixture, Session (+14 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "pathlib"
Cohesion: 0.07
Nodes (30): app_services_agent_checkpointer, decimal, os, pathlib, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables…, check_alembic_heads() (+22 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "ProfileSkill"
Cohesion: 0.13
Nodes (26): add_certification(), add_language(), add_location(), add_project(), add_skill(), add_work_experience(), apply_parsed_cv(), bulk_skills() (+18 more)

### Community 92 - ".score_and_gate_jobs"
Cohesion: 0.12
Nodes (15): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models:…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.… (+7 more)

### Community 93 - "dispatch_service.py"
Cohesion: 0.14
Nodes (18): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+10 more)

### Community 94 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 95 - "tools.py"
Cohesion: 0.10
Nodes (31): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+23 more)

### Community 96 - "UserProfile"
Cohesion: 0.15
Nodes (21): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+13 more)

### Community 97 - "MimeBuilder"
Cohesion: 0.10
Nodes (27): Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, backend/app/services/integrations/mime_builder.py RFC 2822 & RFC 2046 Compliant… (+19 more)

### Community 98 - "seed_initial_data"
Cohesion: 0.13
Nodes (19): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in… (+11 more)

### Community 99 - "ResumeBuilderView.jsx"
Cohesion: 0.20
Nodes (11): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+3 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "QuotaService"
Cohesion: 0.16
Nodes (14): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+6 more)

### Community 102 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - "ApplicationFormAnswer"
Cohesion: 0.15
Nodes (13): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts. (+5 more)

### Community 105 - "core/auth.py"
Cohesion: 0.23
Nodes (11): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Ensure the caller has superadmin role privileges., Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+3 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.11
Nodes (15): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+7 more)

### Community 108 - "logging"
Cohesion: 0.25
Nodes (8): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, GeminiProvider, Any, Google Gemini implementation of the LLMProvider interface (Gemini 2.5 Flash /…, logging, pydantic_settings

### Community 109 - "Base"
Cohesion: 0.08
Nodes (46): Base, Base SQLAlchemy declarative model., AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.…, AccountDispatchSettings, ApplicationPdfPayload, JobFeedback, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or… (+38 more)

### Community 110 - "test_tools_api.py"
Cohesion: 0.12
Nodes (24): Tenant ownership registry for LangGraph state threads. Guarantees strict multi-…, ThreadAccount, account_a(), api_test_db(), client(), fixture, Session, TestClient (+16 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.11
Nodes (46): add_designation(), ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, BaseModel (+38 more)

### Community 113 - "google_service.py"
Cohesion: 0.11
Nodes (19): GmailApiNotConfiguredException, GmailServerErrorException, GoogleIntegrationService, Any, Refresh an expired access token using the stored encrypted refresh token. Uses…, Send an outbound email message via official Gmail API messages.send. Args:…, Raised on 403 accessNotConfigured (Gmail API not enabled in GCP Console)., Raised on HTTP 5xx errors from Google servers. (+11 more)

### Community 114 - "dispatch_poller.py"
Cohesion: 0.16
Nodes (15): claim_pending_batch(), main(), poll_and_dispatch_batch(), Session, backend/app/workers/dispatch_poller.py PostgreSQL DB Outbox Poller Worker…, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Periodic 30-second sweeper per Section 3.2 of specification: 1. Stale claimed… (+7 more)

### Community 115 - "apply_graph.py"
Cohesion: 0.13
Nodes (30): autonomy_gate_edge(), build_apply_graph(), cv_drafter_node(), cv_reviewer_node(), detect_method_node(), fit_analyzer_node(), hitl_approval_gate_node(), needs_edit_node() (+22 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "json"
Cohesion: 0.14
Nodes (20): dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line., Serializes Pydantic models cleanly using model_dump() or dict(). (+12 more)

### Community 118 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 119 - ".fetch"
Cohesion: 0.13
Nodes (12): _clean_html(), _do_fetch(), _parse_iso_date(), Any, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.…, Asynchronously fetch all open job postings for a company from Greenhouse,…, Unescape Greenhouse's double-encoded HTML content field. The field is HTML-… (+4 more)

### Community 120 - "LLMService"
Cohesion: 0.16
Nodes (10): Session, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, Resolve ordered list of active providers from database or defaults. (+2 more)

### Community 121 - "Job"
Cohesion: 0.13
Nodes (21): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, BaseModel, SearchAndRankJobsTool, SearchJobsInput, Verify tool registration and schema generation., Test job search tool returns JobRadarCarousel widget., test_agent_tools_registry() (+13 more)

### Community 122 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 124 - "test_apply_to_gateway_e2e.py"
Cohesion: 0.16
Nodes (12): compute_content_hash(), backend/app/services/dispatch/hash_utils.py Canonical length-prefixed content…, Computes deterministic SHA-256 over length-prefixed fields:…, e2e_account_and_job(), asyncio, fixture, backend/tests/agent/test_apply_to_gateway_e2e.py End-to-End Verification of…, Seed real Account, Job, AccountDispatchSettings, and TrustedRecipient in test… (+4 more)

### Community 125 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 126 - "test_educations_skills_and_preview"
Cohesion: 0.28
Nodes (8): account_a(), account_b(), api_test_db(), client(), fixture, Session, Test educations, bulk skills, and preview CV generation., test_educations_skills_and_preview()

### Community 127 - ".fetch"
Cohesion: 0.21
Nodes (8): _clean_html(), _do_fetch(), _parse_created_at(), Any, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch all open job postings for a company from Lever, traversing…, Parse createdAt which Lever provides as epoch milliseconds or ISO string.

### Community 128 - ".fetch"
Cohesion: 0.20
Nodes (9): _clean_html(), _format_salary(), _parse_date(), Any, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO 8601 date string from RemoteOK (e.g. '2026-10-24T00:00:02+00:00'). (+1 more)

### Community 129 - "Education"
Cohesion: 0.18
Nodes (13): add_education(), patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience() (+5 more)

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.15
Nodes (16): compile_texlive(), download_user_resume(), build_sandboxed_tex_env(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Construct scrubbed environment for TeX compilation child processes. - Strips…, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable. (+8 more)

### Community 131 - "ExperienceReflector"
Cohesion: 0.18
Nodes (9): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, Session, test_experience_reflector_conversion_and_multipliers() (+1 more)

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - "JobEazy: Milestone M1m Implementation Specification"
Cohesion: 0.18
Nodes (10): 2.2 Tenancy Exemption in `scripts/check_migrations.py`, 2. Reuse of Existing Subscription Schema & Tenancy Audits, 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation, 5. In-Service Context Propagation (`contextvars`) & Provider Accounting, 6. Superadmin Control Center & Impersonation Safety, 7. Concrete Test Plan & Verified Models (`test_m1_models_and_migration.py`) (+2 more)

### Community 134 - "DispatchedAction"
Cohesion: 0.31
Nodes (9): DispatchedAction, Sequenced idempotency barrier. Partial unique index excludes aborted/failed so…, Advisor Review 9 Item 7 & 11: Verifies that an account with SendEvidence,…, Advisor Review 9 Item 11: Verifies that autonomous cap checks block claims once…, Advisor Review 9 Item 8 & 11: Verifies that the partial unique index on…, test_account_deletion_with_audit_fks(), test_concurrent_claims_vs_caps(), test_partial_unique_retry_after_abort() (+1 more)

### Community 135 - ".generate"
Cohesion: 0.22
Nodes (8): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 8. Milestone Implementation & Effort

### Community 136 - ".setup"
Cohesion: 0.33
Nodes (6): Run underlying setup and enforce Row Level Security on checkpointer tables in…, 15. Decision Register, 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 137 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 138 - "env.py"
Cohesion: 0.14
Nodes (20): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+12 more)

### Community 139 - "Session"
Cohesion: 0.29
Nodes (7): Session, Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test SubscriptionPlan and Entitlement models matching ARCHITECTURE.md §0 & §7., Verify that deleting an account cascades to all tenant-scoped rows., test_application_model_and_human_in_the_loop_gate(), test_multi_tenant_cascade_deletes(), test_subscription_plans_and_entitlements()

### Community 140 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 141 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 142 - ".queue_application_send"
Cohesion: 0.33
Nodes (6): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., Enqueues an application for outbound dispatch with an undo hold window.…, SendGatewayException

### Community 143 - "5.2 Node Inventory Table & Tailor Refactoring"
Cohesion: 0.33
Nodes (6): CopilotState, 16. Document Changelog, 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.2 Node Inventory Table & Tailor Refactoring, 5.3 Bounded Review Loop & Recursion Limit, 5. State Schemas, Nodes, and Interrupt Catalogs

### Community 144 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 145 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 146 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 147 - "IngestionRequest"
Cohesion: 0.40
Nodes (5): IngestionRequest, IngestionResponse, BaseModel, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run.

### Community 148 - "AnthropicProvider"
Cohesion: 0.50
Nodes (3): AnthropicProvider, Any, Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet /…

### Community 149 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 150 - "client"
Cohesion: 0.40
Nodes (3): api_test_db(), client(), fixture

### Community 151 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 153 - "test_google_callback_and_status"
Cohesion: 0.33
Nodes (4): Verify secrets are encrypted and decrypted accurately., Verify code exchange, DB persistence with encryption, status check, and…, test_crypto_encryption_roundtrip(), test_google_callback_and_status()

### Community 154 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 156 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 157 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1138 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `ExperienceReflector`, `JobIngestionService`, `DispatchedAction`, `api/profile.py`, `SendGateway`, `client`, `typing`, `Session`, `applications.py`, `test_google_dispatch.py`, `test_cv_tailor_service_with_structured_profile`, `TestClient`, `test_auth.py`, `test_apply_graph.py`, `test_google_callback_and_status`, `integrations.py`, `client`, `Application`, `api/agent.py`, `test_admin.py`, `admin.py`, `api/auth.py`, `TestClient`, `trigger_ingestion`, `StageApplicationProposalTool`, `test_matching.py`, `test_agent.py`, `ProfileSkill`, `tools.py`, `UserProfile`, `seed_initial_data`, `test_matching_service_score_and_gate_clean_jobs`, `ApplicationFormAnswer`, `core/auth.py`, `Base`, `test_tools_api.py`, `models/__init__.py`, `apply_graph.py`, `Job`, `test_monitor_followups_task`, `test_apply_to_gateway_e2e.py`, `test_educations_skills_and_preview`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `SendGateway` connect `SendGateway` to `MimeBuilder`, `AgentEngine`, `QuotaService`, `DispatchedAction`, `13. Strategic Options Analysis & Recommendation`, `JobEazy: Milestone M1 & M1b Implementation Specification`, `Base`, `applications.py`, `.queue_application_send`, `google_service.py`, `dispatch_poller.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `Job`, `integrations.py`, `test_apply_to_gateway_e2e.py`, `Application`, `engine.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `ExperienceReflector`, `Base`, `test_decoupled_tools.py`, `google_service.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `LLMService`, `integrations.py`, `pathlib`, `.score_and_gate_jobs`, `engine.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 144 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 144 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 33 INFERRED edges - model-reasoned connections that need verification._
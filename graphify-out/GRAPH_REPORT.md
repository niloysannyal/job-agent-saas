# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 288 files · ~212,394 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2953 nodes · 8310 edges · 166 communities (139 shown, 27 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1151 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `740953d9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- typing
- JobPosting
- LatexLogParser
- Account
- FormDetectiveService
- api/profile.py
- SendAuthorization
- GreenhouseJobSource
- Job
- test_freehire_bearer_auth
- RemoteOKJobSource
- BaseModel
- crypto.py
- test_decoupled_tools.py
- package.json
- LeverJobSource
- RemotiveJobSource
- test_auth.py
- Session
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_apply_graph.py
- JobSourceHTTPError
- What You Must Do When Invoked
- alembic
- GoogleIntegrationService
- MatchingService
- test_form_qa_api.py
- HoldQueueItem
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
- account.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- TenantScopedAsyncPostgresSaver
- Project: Job Application Agent SaaS
- 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)
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
- email_service.py
- React Frontend Development Standards (adapted from ECC)
- stage_proposal_tool.py
- test_matching.py
- dispatch_service.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- run_live_dogfooding_tests.py
- ProfileView.jsx
- WorkExperience
- .parse_from_db
- EmailDispatchService
- Product Development Environment Guide — Job Application Agent SaaS
- tools.py
- file_extractor.py
- test_google_dispatch.py
- TargetDesignation
- react
- JobsView.jsx
- QuotaService
- JobSearchQuery
- test_matching_service_score_and_gate_clean_jobs
- test_bookmarklet_generation_with_job_and_star_answers
- session.py
- deploy.sh
- cv_parser.py
- llm/service.py
- Base
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- .send_gmail_message
- poll_and_dispatch_batch
- apply_graph.py
- theme.js
- json
- check_migrations.py
- get_monitor_summary
- LLMService
- ApplicationFormAnswerBase
- test_monitor_followups_task
- MockEmbeddingClient
- SendGateway
- BaseAgentTool
- test_profile.py
- LogText
- set_compensation
- Project
- TeXLiveCompilerService
- logging
- Security & Tenancy Policy (adapted from ECC AgentShield)
- .generate
- 3257c49a645d_add_agent_action_proposals_.py
- 74cebd545352_add_is_pinned_to_agent_conversations.py
- .setup
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- env.py
- a7c3e1f24b01_add_profile_and_interview_tables.py
- devDependencies
- SessionLocal
- .queue_application_send
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- test_profile_compile_texlive.py
- create_email_draft
- db_session
- get_available_sources
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
- 6. Autonomy Policy Engine & Guardrails
- doctor.py
- Development Context — Job Application Agent SaaS
- LanguageGate
- 13. Strategic Options Analysis & Recommendation
- .generate
- db_session
- 12. Dependency Plan & Environment Strategy
- 1. Executive Summary & Scope
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- install_hooks.py
- review.py

## God Nodes (most connected - your core abstractions)
1. `Account` - 231 edges
2. `Job` - 122 edges
3. `Base` - 103 edges
4. `Application` - 84 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 72 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 55 edges
9. `SendGateway` - 55 edges
10. `LLMService` - 55 edges

## Surprising Connections (you probably didn't know these)
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `7.2 Integration Strategy` --references--> `ApplicationStudio()`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → frontend/src/components/ApplicationStudio.jsx
- `9.2 Resume Endpoint & Minimal Frontend Contract` --references--> `SendApprovalGate()`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → frontend/src/components/agent/widgets/SendApprovalGate.jsx

## Import Cycles
- None detected.

## Communities (166 total, 27 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "typing"
Cohesion: 0.09
Nodes (38): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+30 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (42): Integration Checklist, Job Source Integrator, JobPosting, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any (+34 more)

### Community 5 - "Account"
Cohesion: 0.05
Nodes (56): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, account_a(), account_b(), api_test_db(), client() (+48 more)

### Community 6 - "FormDetectiveService"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 7 - "api/profile.py"
Cohesion: 0.11
Nodes (58): add_certification(), add_designation(), add_education(), add_location(), add_project(), add_skill(), apply_parsed_cv(), bulk_skills() (+50 more)

### Community 8 - "SendAuthorization"
Cohesion: 0.13
Nodes (22): Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, SendAuthorization, create_test_hierarchy(), asyncio, Session, Verify that an active account kill_switch aborts dispatch., Verify that an administrative account suspension aborts dispatch., Verify that the global emergency kill switch aborts dispatch. (+14 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "Job"
Cohesion: 0.07
Nodes (60): get_llm_service(), Dependency provider for LLMService., Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, check_job_liveness(), list_jobs() (+52 more)

### Community 11 - "test_freehire_bearer_auth"
Cohesion: 0.16
Nodes (12): asyncio, Verify that Authorization Bearer header is sent when api_key is set, and…, Verify offset is omitted for page 1 and correctly calculated as (page - 1) *…, Verify country and salary_min query filters serialization., Non-200 responses raise JobSourceHTTPError., Verify field mapping and HTML cleaning from realistic freehire response., test_freehire_bearer_auth(), test_freehire_fetch_data_normalization() (+4 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "BaseModel"
Cohesion: 0.19
Nodes (14): detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FormAnswerModel (+6 more)

### Community 14 - "crypto.py"
Cohesion: 0.12
Nodes (28): decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy…, Derive a deterministic 32-byte URL-safe base64 Fernet key from secret string. (+20 more)

### Community 15 - "test_decoupled_tools.py"
Cohesion: 0.15
Nodes (22): cv_drafter_node(), Executes Pass 1 (Senior Recruiter Drafter) with dynamic section budgeting., CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput, prune_and_budget_latex(), BaseModel (+14 more)

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "test_auth.py"
Cohesion: 0.05
Nodes (53): create_access_token(), Generate a cryptographically signed JWT access token. Contains subject…, auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user() (+45 more)

### Community 20 - "Session"
Cohesion: 0.18
Nodes (13): cancel_application_send(), draft_follow_up(), FollowUpDraftResponse, mark_follow_up_sent(), patch, post, Session, Candidate Undo/Cancel Gate: Cancels an application currently in the undo… (+5 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.11
Nodes (19): ApprovalGateResumePayload, CopilotState, BaseModel, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology (+11 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.07
Nodes (41): TOFU Exact-Address allowlist. Email uniqueness is enforced case-insensitively…, TrustedRecipient, backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, CVReviewOutput, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel (+33 more)

### Community 23 - "JobSourceHTTPError"
Cohesion: 0.09
Nodes (33): _detect_location_type(), _parse_created_date(), datetime, Parse ISO formatted creation date from Adzuna response., Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC (+25 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 26 - "GoogleIntegrationService"
Cohesion: 0.09
Nodes (28): create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_google_auth_url(), get_google_status(), google_oauth_callback(), GoogleAuthUrlResponse (+20 more)

### Community 27 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 28 - "test_form_qa_api.py"
Cohesion: 0.33
Nodes (8): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 29 - "HoldQueueItem"
Cohesion: 0.17
Nodes (20): HoldQueueItem, Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, client(), create_approval_fixture(), asyncio, fixture, Session, TestClient (+12 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.21
Nodes (17): GenerativeUIWidget, BaseModel, Enum, str, Executes the autonomous tool action and returns structured data along with an…, ToolCategory, ToolExecutionContext, ToolResult (+9 more)

### Community 32 - "api/agent.py"
Cohesion: 0.10
Nodes (39): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+31 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.15
Nodes (21): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+13 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.09
Nodes (22): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 3.1 Single Atomic Transaction Before External Call, 3.2 Periodic Sweeper (Stale Claimed & Stale Sending), 3.3 Mid-Hold Cancel & Autonomy Toggle Off, 3. Send State Machine & Outbox Poller (+14 more)

### Community 41 - "drafter_service.py"
Cohesion: 0.23
Nodes (10): FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterService, Any, BaseModel, Enum, str (+2 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.12
Nodes (47): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+39 more)

### Community 45 - "account.py"
Cohesion: 0.15
Nodes (27): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+19 more)

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
Nodes (41): app_services_agent_checkpointer, AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), normalize_libpq_url(), Any, backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph… (+33 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "2.1 Table Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.15
Nodes (13): 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped), Table 1: `account_dispatch_settings` (Tenant Autonomy, Safety Caps & Kill Switches), Table 2: `user_commands` (Authority to Attempt), Table 3: `send_authorizations` (Content-Pinned Authorization), Table 4: `application_pdf_payloads` (Dedicated PDF Byte Storage) (+5 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (19): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 1. Scope & rollout (+11 more)

### Community 60 - "UserProfile"
Cohesion: 0.06
Nodes (58): generate_form_answers(), Harness² Recursive Form Q&A Generator. Applies Task-Level Recursion (Propose ->…, create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse (+50 more)

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

### Community 79 - "email_service.py"
Cohesion: 0.23
Nodes (10): generate_otp(), is_smtp_configured(), Check if outbound SMTP server credentials are fully configured., Generate a cryptographically secure 6-digit numeric OTP code., Send 6-digit OTP verification email to user. Falls back gracefully to secure…, send_otp_email(), email_mime_multipart, email_mime_text (+2 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "stage_proposal_tool.py"
Cohesion: 0.17
Nodes (16): asyncio, AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+8 more)

### Community 82 - "test_matching.py"
Cohesion: 0.11
Nodes (19): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+11 more)

### Community 83 - "dispatch_service.py"
Cohesion: 0.27
Nodes (8): EmailDraftProvider, EmailDraftResult, Enum, str, Result of an email draft creation operation., email_message, email_mime_application, email_policy

### Community 84 - "test_agent.py"
Cohesion: 0.10
Nodes (28): BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput, account_a(), account_b() (+20 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "run_live_dogfooding_tests.py"
Cohesion: 0.07
Nodes (38): app_services_agent_workflows_apply_graph, app_services_dispatch_gateway, argparse, normalize_db_url(), Normalize database URL for driver compatibility., OAuthConnection, Multi-tenant OAuth Connection model. Stores authorized OAuth 2.0 access and…, assert_safe_test_database_url() (+30 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "WorkExperience"
Cohesion: 0.29
Nodes (8): add_work_experience(), Structured work experience entity for candidates across all industries.…, WorkExperience, WorkExperienceBase, WorkExperienceCreate, WorkExperienceRead, Test that ProfileParser.parse_from_db synthesizes structured profile data +…, test_profile_parser_from_db_structured()

### Community 92 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models:…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 93 - "EmailDispatchService"
Cohesion: 0.29
Nodes (8): EmailDispatchService, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on…, Generates a standard URL-encoded mailto: link for 1-click launch in default…, Builds a standard RFC 822 .eml message with optional PDF attachment. When…, test_create_draft_rfc822(), test_generate_eml_message_with_pdf_attachment(), test_generate_mailto_link()

### Community 94 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 95 - "tools.py"
Cohesion: 0.10
Nodes (32): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+24 more)

### Community 96 - "file_extractor.py"
Cohesion: 0.22
Nodes (8): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, csv, io

### Community 97 - "test_google_dispatch.py"
Cohesion: 0.10
Nodes (30): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, backend/app/services/integrations/mime_builder.py RFC 2822 & RFC 2046 Compliant…, Encode raw MIME bytes to base64url string required by the Gmail API. (+22 more)

### Community 98 - "TargetDesignation"
Cohesion: 0.14
Nodes (16): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+8 more)

### Community 99 - "react"
Cohesion: 0.18
Nodes (12): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+4 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "QuotaService"
Cohesion: 0.16
Nodes (14): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+6 more)

### Community 102 - "JobSearchQuery"
Cohesion: 0.09
Nodes (28): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), Any, AsyncClient, Asynchronously fetch job postings matching the query from Adzuna. (+20 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.16
Nodes (13): api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent… (+5 more)

### Community 105 - "session.py"
Cohesion: 0.10
Nodes (28): BookmarkletResponse, get_autofill_bookmarklet(), Generate an intelligent JavaScript bookmarklet code tailored to the current…, get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Resolve the current authenticated account context. 1. Primary: Validates… (+20 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.12
Nodes (15): parse_cv_file(), UploadFile, CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf. (+7 more)

### Community 108 - "llm/service.py"
Cohesion: 0.16
Nodes (13): AnthropicProvider, Any, Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet /…, LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, GeminiProvider, Any (+5 more)

### Community 109 - "Base"
Cohesion: 0.05
Nodes (73): Base, Base SQLAlchemy declarative model., AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountDispatchSettings, ApplicationPdfPayload (+65 more)

### Community 110 - "test_tools_api.py"
Cohesion: 0.11
Nodes (25): Tenant ownership registry for LangGraph state threads. Guarantees strict multi-…, ThreadAccount, account_a(), api_test_db(), client(), fixture, Session, TestClient (+17 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.08
Nodes (55): add_language(), create_profile(), Create a user profile for an account (one per account)., AccountCvVersionUpdate, CvTemplateBase, CvTemplateUpdate, BaseModel, JobBase (+47 more)

### Community 113 - ".send_gmail_message"
Cohesion: 0.16
Nodes (19): GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, Exception, Send an outbound email message via official Gmail API messages.send. Args:… (+11 more)

### Community 114 - "poll_and_dispatch_batch"
Cohesion: 0.18
Nodes (11): main(), poll_and_dispatch_batch(), Session, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Periodic 30-second sweeper per Section 3.2 of specification: 1. Stale claimed…, run_poller_daemon(), sweep_stale_items() (+3 more)

### Community 115 - "apply_graph.py"
Cohesion: 0.14
Nodes (30): assemble_package_node(), autonomy_gate_edge(), build_apply_graph(), cv_reviewer_node(), detect_method_node(), dispatch_node(), fit_analyzer_node(), hitl_approval_gate_node() (+22 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "json"
Cohesion: 0.14
Nodes (20): dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line., Serializes Pydantic models cleanly using model_dump() or dict(). (+12 more)

### Community 118 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 119 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 120 - "LLMService"
Cohesion: 0.15
Nodes (7): LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, client(), fixture, Verify that encrypted API keys stored in DB are decrypted and resolved into…, test_llm_service_db_provider_decryption_and_resolution()

### Community 121 - "ApplicationFormAnswerBase"
Cohesion: 0.29
Nodes (7): ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate, BaseModel

### Community 122 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 123 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 124 - "SendGateway"
Cohesion: 0.18
Nodes (13): Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure., Handle retryable 429/5xx error by scheduling exponential backoff and releasing…, Atomically record successful external dispatch, evidence, and state transitions. (+5 more)

### Community 125 - "BaseAgentTool"
Cohesion: 0.15
Nodes (10): BaseAgentTool, ABC, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /… (+2 more)

### Community 126 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 128 - "set_compensation"
Cohesion: 0.50
Nodes (5): set_compensation(), CompensationBase, CompensationCreate, CompensationRead, put

### Community 129 - "Project"
Cohesion: 0.18
Nodes (11): patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience(), Certification (+3 more)

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.12
Nodes (19): build_sandboxed_tex_env(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Construct scrubbed environment for TeX compilation child processes. - Strips…, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine with strict…, TeXLiveCompilerService (+11 more)

### Community 131 - "logging"
Cohesion: 0.15
Nodes (16): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT… (+8 more)

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - ".generate"
Cohesion: 0.12
Nodes (16): Any, Execute generation across the provider chain with automatic fallback., Return execution metadata from the last successful LLM call for…, 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope (+8 more)

### Community 134 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 135 - "74cebd545352_add_is_pinned_to_agent_conversations.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations., upgrade()

### Community 136 - ".setup"
Cohesion: 0.29
Nodes (7): Run underlying setup and enforce Row Level Security on checkpointer tables in…, 14. Milestone Roadmap & Effort Estimates, 8.1 Hold Queue: PostgreSQL DB Outbox vs Arq/Redis Comparison, 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 137 - "7f7822f4eef9_add_github_url_to_projects_and_location_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade()

### Community 138 - "env.py"
Cohesion: 0.31
Nodes (9): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+1 more)

### Community 139 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 140 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 141 - "SessionLocal"
Cohesion: 0.07
Nodes (29): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), arq, arq_connections (+21 more)

### Community 142 - ".queue_application_send"
Cohesion: 0.33
Nodes (6): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., Enqueues an application for outbound dispatch with an undo hold window.…, SendGatewayException

### Community 143 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 144 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 145 - "create_email_draft"
Cohesion: 0.50
Nodes (4): create_email_draft(), DraftEmailRequest, DraftEmailResponse, Phase 3: Minimal-Effort Dispatch. Generates a pre-populated draft with 1-click…

### Community 146 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 147 - "get_available_sources"
Cohesion: 0.10
Nodes (18): IngestionRequest, IngestionResponse, BaseModel, post, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run., Trigger job ingestion pipeline for an account., trigger_ingestion() (+10 more)

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

### Community 154 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 156 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 157 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

### Community 162 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

### Community 163 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1142 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `typing`, `JobPosting`, `api/profile.py`, `SendAuthorization`, `Job`, `BaseModel`, `crypto.py`, `create_email_draft`, `get_available_sources`, `test_auth.py`, `test_apply_graph.py`, `GoogleIntegrationService`, `test_form_qa_api.py`, `HoldQueueItem`, `api/agent.py`, `test_admin.py`, `admin.py`, `account.py`, `Architecture — Job Application Agent SaaS`, `UserProfile`, `test_matching.py`, `test_agent.py`, `run_live_dogfooding_tests.py`, `WorkExperience`, `tools.py`, `file_extractor.py`, `test_google_dispatch.py`, `TargetDesignation`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `session.py`, `Base`, `test_tools_api.py`, `models/__init__.py`, `apply_graph.py`, `test_monitor_followups_task`, `test_profile.py`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `typing`, `AgentEngine`, `logging`, `llm/service.py`, `Base`, `test_decoupled_tools.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `check_migrations.py`, `run_live_dogfooding_tests.py`, `GoogleIntegrationService`, `MatchingService`, `LLMService`, `engine.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `typing`, `logging`, `JobPosting`, `Account`, `SendAuthorization`, `BaseModel`, `SessionLocal`, `test_auth.py`, `Session`, `test_apply_graph.py`, `MatchingService`, `HoldQueueItem`, `engine.py`, `test_admin.py`, `admin.py`, `account.py`, `UserProfile`, `AgentEngine`, `stage_proposal_tool.py`, `test_matching.py`, `test_agent.py`, `run_live_dogfooding_tests.py`, `tools.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `Base`, `test_tools_api.py`, `models/__init__.py`, `test_monitor_followups_task`, `SendGateway`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 147 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 147 INFERRED edges - model-reasoned connections that need verification._
- **Are the 53 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 53 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 34 INFERRED edges - model-reasoned connections that need verification._
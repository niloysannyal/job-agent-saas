# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 284 files · ~209,853 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2918 nodes · 8148 edges · 147 communities (123 shown, 24 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1117 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3bce50c3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- typing
- JobPosting
- LatexLogParser
- TestClient
- FormDetectiveService
- api/profile.py
- SendGateway
- GreenhouseJobSource
- account.py
- JobSearchQuery
- RemoteOKJobSource
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
- job.py
- What You Must Do When Invoked
- alembic
- integrations.py
- MatchingService
- test_generate_form_answers_api_endpoint
- Application
- config.py
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
- react
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
- ResumeBuilderView.jsx
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
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- jobs.py
- React Frontend Development Standards (adapted from ECC)
- stage_proposal_tool.py
- test_matching.py
- embedding.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- os
- ProfileView.jsx
- ProfileSkill
- .parse_from_db
- dispatch_service.py
- .generate
- tools.py
- StarStory
- .build_message
- TargetDesignation
- StudioDrafterWorkspace.jsx
- JobsView.jsx
- matching/service.py
- AdzunaJobSource
- test_matching_service_score_and_gate_clean_jobs
- test_google_callback_and_status
- core/auth.py
- deploy.sh
- CVParserService
- client
- Base
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- google_service.py
- email_service.py
- apply_graph.py
- theme.js
- logging
- .role
- LinkedInJobSource
- ApplicationBase
- Account
- test_monitor_followups_task
- MockEmbeddingClient
- test_profile_resumes.py
- AgentToolRegistry
- client
- Roadmap — Job Application Agent SaaS
- 3257c49a645d_add_agent_action_proposals_.py
- Project
- TeXLiveCompilerService
- 74cebd545352_add_is_pinned_to_agent_conversations.py
- encrypt_secret
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- a7c3e1f24b01_add_profile_and_interview_tables.py
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
- get_me
- env.py
- SendGatewayException
- db_session

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
10. `LLMService` - 51 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py

## Import Cycles
- None detected.

## Communities (147 total, 24 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.12
Nodes (19): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+11 more)

### Community 2 - "typing"
Cohesion: 0.07
Nodes (44): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), prune_and_budget_latex(), backend/app/services/cv_tailor/drafter.py Decoupled Senior Recruiter Drafter…, Budgets and prunes the Master CV body to strictly 1-2 pages matching…, audit_fact_integrity() (+36 more)

### Community 3 - "JobPosting"
Cohesion: 0.07
Nodes (45): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+37 more)

### Community 5 - "TestClient"
Cohesion: 0.10
Nodes (21): TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations., GET and PUT on compensation expectations., CRUD operations on spoken languages., Verify complete isolation between tenants A and B for profile and related…, Test full CRUD cycle for work experiences. (+13 more)

### Community 6 - "FormDetectiveService"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 7 - "api/profile.py"
Cohesion: 0.11
Nodes (57): add_certification(), add_designation(), add_education(), add_language(), add_work_experience(), create_profile(), delete_certification(), delete_designation() (+49 more)

### Community 8 - "SendGateway"
Cohesion: 0.05
Nodes (91): AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Stores compiled PDF byte payloads outside applications table to prevent bloat. (+83 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.06
Nodes (32): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+24 more)

### Community 10 - "account.py"
Cohesion: 0.07
Nodes (55): arq, arq_connections, Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), get_db(), get_engine(), get_session_factory() (+47 more)

### Community 11 - "JobSearchQuery"
Cohesion: 0.12
Nodes (21): JobSearchQuery, Normalized query parameters for searching across job sources., _clean_html(), FreehireJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+13 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+20 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (47): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+39 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.12
Nodes (31): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy… (+23 more)

### Community 15 - "check_migrations.py"
Cohesion: 0.60
Nodes (4): check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 16 - "package.json"
Cohesion: 0.05
Nodes (38): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+30 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.11
Nodes (19): TestClient, Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged)., include_flagged=True must include flagged postings (unless also vetoed)., show_all=True must include all jobs (both vetoed and flagged) for human review., Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…, Verify limit and offset pagination parameters work correctly. (+11 more)

### Community 20 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.07
Nodes (31): Run underlying setup and enforce Row Level Security on checkpointer tables in…, CopilotState, 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy (+23 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.12
Nodes (14): mock_llm_responses(), fixture, backend/tests/agent/test_apply_graph.py Unit tests for Modular LangGraph…, Verifies legitimate corporate email with trusted recipient executes…, Mock LLMService.generate to return valid structured responses., test_apply_graph_autonomous_flow_passes_gates(), Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns… (+6 more)

### Community 23 - "job.py"
Cohesion: 0.12
Nodes (28): JobBase, JobCreate, JobRead, JobUpdate, BaseModel, _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type() (+20 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 26 - "integrations.py"
Cohesion: 0.10
Nodes (31): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+23 more)

### Community 27 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 28 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.60
Nodes (5): Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 29 - "Application"
Cohesion: 0.12
Nodes (25): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountUsageCounter, Live aggregated balances per billing period. Updated transactionally with…, client(), create_approval_fixture() (+17 more)

### Community 30 - "config.py"
Cohesion: 0.22
Nodes (6): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings, pydantic_settings

### Community 31 - "engine.py"
Cohesion: 0.20
Nodes (21): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+13 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (41): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+33 more)

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
Nodes (34): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+26 more)

### Community 41 - "drafter_service.py"
Cohesion: 0.09
Nodes (32): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, CandidateCareerContext, CVDraftOutput, CVReviewerService, CVReviewInput, Executes Pass 2 (Senior Recruiter Reviewer & Fact Auditor). Audits for…, DimensionDiagnostic, FitAnalyzerInput (+24 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.09
Nodes (54): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), _build_provider_read(), create_admin_template() (+46 more)

### Community 45 - "api/auth.py"
Cohesion: 0.15
Nodes (26): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+18 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "react"
Cohesion: 0.15
Nodes (19): 2. Current State Map (Codebase Ground Truth), 9.1 Custom Streaming Loop (Part Objects in Version "v2"), 9.2 Resume Endpoint & Minimal Frontend Contract, 9. Redesigned SSE Protocol Adapter & UI Integration, CareerCopilotView(), FAST_CHIPS, formatInlineMarkdown(), STARTER_PROMPTS (+11 more)

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
Cohesion: 0.12
Nodes (16): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN), 4. Module 1 — Find Job Opportunity (decision made) (+8 more)

### Community 60 - "api/interview.py"
Cohesion: 0.15
Nodes (22): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+14 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ResumeBuilderView.jsx"
Cohesion: 0.21
Nodes (12): 7.1 Scope Classification & CASA Exemption, 7.2 Integration Strategy, 7. Gmail Integration Architecture (Scope Correction), ApplicationStudio(), ResumeBuilderView(), TEMPLATES, ResumePreviewModal(), StudioApprovalGate() (+4 more)

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
Cohesion: 0.12
Nodes (15): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Executes human-in-the-loop approval of an action proposal. Enforces tenant… (+7 more)

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

### Community 74 - "LLMService"
Cohesion: 0.10
Nodes (27): Session, LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any (+19 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "jobs.py"
Cohesion: 0.17
Nodes (15): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+7 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "stage_proposal_tool.py"
Cohesion: 0.14
Nodes (19): asyncio, AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+11 more)

### Community 82 - "test_matching.py"
Cohesion: 0.13
Nodes (16): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared. (+8 more)

### Community 83 - "embedding.py"
Cohesion: 0.13
Nodes (13): EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation., Generate embedding vector for a single text string., Generate embeddings for a list of text strings. (+5 more)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (30): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, BaseModel, SearchJobsInput, BaseModel, StarCoachInput, account_a(), account_b() (+22 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "os"
Cohesion: 0.09
Nodes (21): app_services_agent_checkpointer, decimal, os, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables…, check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+13 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.11
Nodes (25): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+17 more)

### Community 91 - "ProfileSkill"
Cohesion: 0.39
Nodes (8): add_skill(), bulk_skills(), update_skill(), ProfileSkill, ProfileSkillBase, ProfileSkillCreate, ProfileSkillRead, Structured skill entity with taxonomy categorization and proficiency.

### Community 92 - ".parse_from_db"
Cohesion: 0.14
Nodes (12): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…, Any, Path, Dynamically extracts candidate profile and CV data from database models:…, Extract readable text from LaTeX CV, stripping comments and common markup., Path (+4 more)

### Community 93 - "dispatch_service.py"
Cohesion: 0.14
Nodes (18): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+10 more)

### Community 94 - ".generate"
Cohesion: 0.06
Nodes (32): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start, 2. The 5-Phase Verification Loop (+24 more)

### Community 95 - "tools.py"
Cohesion: 0.09
Nodes (33): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+25 more)

### Community 96 - "StarStory"
Cohesion: 0.23
Nodes (12): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field. (+4 more)

### Community 97 - ".build_message"
Cohesion: 0.12
Nodes (19): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilderException, Exception, Base exception for MIME construction and validation errors., Raised when recipient email fails RFC 5322 validation., Raised when PDF bytes do not match valid %PDF-1. magic header. (+11 more)

### Community 98 - "TargetDesignation"
Cohesion: 0.21
Nodes (12): add_location(), CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation (+4 more)

### Community 99 - "StudioDrafterWorkspace.jsx"
Cohesion: 0.21
Nodes (10): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics() (+2 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "matching/service.py"
Cohesion: 0.19
Nodes (10): ParsedProfile, ProfileParser, Structured representation of parsed user profile and CV., Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, MatchingResult, Summary of a match scoring run., dataclasses, pathlib (+2 more)

### Community 102 - "AdzunaJobSource"
Cohesion: 0.09
Nodes (24): AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime, Asynchronously fetch job postings matching the query from Adzuna. (+16 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - "test_google_callback_and_status"
Cohesion: 0.18
Nodes (11): api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and… (+3 more)

### Community 105 - "core/auth.py"
Cohesion: 0.23
Nodes (11): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Ensure the caller has superadmin role privileges., Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+3 more)

### Community 107 - "CVParserService"
Cohesion: 0.17
Nodes (9): CVParserService, Any, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON., Strip markdown fences (```json ... ```) from output. (+1 more)

### Community 108 - "client"
Cohesion: 0.22
Nodes (10): client(), fixture, Session, In-memory SQLite database session with static pool for testing., FastAPI TestClient with overridden get_db dependency., Seed test accounts for multi-tenant isolation tests., Seed a variety of jobs: - High match score, clean - Mid match score, clean -…, seeded_accounts() (+2 more)

### Community 109 - "Base"
Cohesion: 0.05
Nodes (59): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.… (+51 more)

### Community 110 - "test_tools_api.py"
Cohesion: 0.12
Nodes (23): account_a(), api_test_db(), client(), fixture, Session, TestClient, backend/tests/api/test_tools_api.py Unit and integration tests for Decoupled…, Test POST /api/v1/tools/detect-method discovers email application. (+15 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.09
Nodes (54): add_project(), AccountCvVersionBase, AccountCvVersionUpdate, CvTemplateBase, CvTemplateUpdate, BaseModel, OAuthConnectionBase, OAuthConnectionCreate (+46 more)

### Community 113 - "google_service.py"
Cohesion: 0.11
Nodes (27): GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, Exception, Send an outbound email message via official Gmail API messages.send. Args:… (+19 more)

### Community 114 - "email_service.py"
Cohesion: 0.29
Nodes (8): generate_otp(), is_smtp_configured(), Check if outbound SMTP server credentials are fully configured., Generate a cryptographically secure 6-digit numeric OTP code., Send 6-digit OTP verification email to user. Falls back gracefully to secure…, send_otp_email(), secrets, smtplib

### Community 115 - "apply_graph.py"
Cohesion: 0.07
Nodes (54): autonomy_gate_edge(), build_apply_graph(), cv_drafter_node(), cv_reviewer_node(), detect_method_node(), fit_analyzer_node(), hitl_approval_gate_node(), needs_edit_node() (+46 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "logging"
Cohesion: 0.09
Nodes (28): run_resume_background(), run_apply_background(), dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent… (+20 more)

### Community 118 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 119 - "LinkedInJobSource"
Cohesion: 0.19
Nodes (8): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser()

### Community 120 - "ApplicationBase"
Cohesion: 0.25
Nodes (8): ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate, BaseModel

### Community 121 - "Account"
Cohesion: 0.05
Nodes (70): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, ApplicationCreate, ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, AccountCvVersion (+62 more)

### Community 122 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 123 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 124 - "test_profile_resumes.py"
Cohesion: 0.15
Nodes (20): Structured work experience entity for candidates across all industries.…, WorkExperience, api_test_db(), client(), create_minimal_pdf_bytes(), fixture, Session, TestClient (+12 more)

### Community 125 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 126 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 127 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 128 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 129 - "Project"
Cohesion: 0.20
Nodes (12): apply_parsed_cv(), patch, update_certification(), update_education(), update_project(), update_work_experience(), Certification, Education (+4 more)

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.16
Nodes (15): compile_texlive(), build_sandboxed_tex_env(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Construct scrubbed environment for TeX compilation child processes. - Strips…, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine with strict… (+7 more)

### Community 131 - "74cebd545352_add_is_pinned_to_agent_conversations.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations., upgrade()

### Community 132 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a general sensitive plaintext secret (e.g. LLM API key, SMTP password)…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 133 - "7f7822f4eef9_add_github_url_to_projects_and_location_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade()

### Community 134 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 135 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 137 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

### Community 138 - "env.py"
Cohesion: 0.14
Nodes (20): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+12 more)

### Community 142 - "SendGatewayException"
Cohesion: 0.67
Nodes (3): Exception, Base exception for SendGateway dispatch failures., SendGatewayException

### Community 146 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1133 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `typing`, `JobPosting`, `TestClient`, `api/profile.py`, `SendGateway`, `get_me`, `account.py`, `applications.py`, `test_google_dispatch.py`, `test_auth.py`, `test_apply_graph.py`, `job.py`, `integrations.py`, `test_generate_form_answers_api_endpoint`, `Application`, `api/agent.py`, `test_admin.py`, `admin.py`, `api/auth.py`, `TestClient`, `LLMService`, `jobs.py`, `stage_proposal_tool.py`, `test_matching.py`, `test_agent.py`, `tools.py`, `TargetDesignation`, `test_matching_service_score_and_gate_clean_jobs`, `test_google_callback_and_status`, `core/auth.py`, `client`, `Base`, `test_tools_api.py`, `models/__init__.py`, `apply_graph.py`, `test_monitor_followups_task`, `test_profile_resumes.py`, `client`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `Job` connect `Account` to `typing`, `JobPosting`, `SendGateway`, `GreenhouseJobSource`, `account.py`, `applications.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `test_apply_graph.py`, `job.py`, `MatchingService`, `Application`, `engine.py`, `test_admin.py`, `drafter_service.py`, `admin.py`, `api/interview.py`, `AgentEngine`, `LLMService`, `jobs.py`, `stage_proposal_tool.py`, `test_matching.py`, `test_agent.py`, `tools.py`, `matching/service.py`, `test_matching_service_score_and_gate_clean_jobs`, `client`, `Base`, `test_tools_api.py`, `models/__init__.py`, `.role`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `react` to `typing`, `AgentEngine`, `SendGateway`, `LLMService`, `Base`, `check_migrations.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `Account`, `integrations.py`, `MatchingService`, `engine.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 144 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 144 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 33 INFERRED edges - model-reasoned connections that need verification._
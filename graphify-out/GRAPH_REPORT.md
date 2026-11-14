# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 293 files · ~219,995 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 3031 nodes · 8618 edges · 158 communities (129 shown, 29 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1215 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0dfd267`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- Account
- StarStory
- api/profile.py
- Job
- GreenhouseJobSource
- Base
- FreehireJobSource
- RemoteOKJobSource
- BaseModel
- test_google_dispatch.py
- apply_graph.py
- package.json
- LeverJobSource
- .fetch
- TestClient
- GoogleIntegrationService
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- google_service.py
- typing
- What You Must Do When Invoked
- 3257c49a645d_add_agent_action_proposals_.py
- integrations.py
- QuotaService
- .send_gmail_message
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
- SendAuthorization
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- dispatch_poller.py
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
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- FastAPI Backend Development Standards (adapted from ECC)
- React Frontend Development Standards (adapted from ECC)
- stage_proposal_tool.py
- test_matching.py
- gateway.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- dispatch_service.py
- ProfileView.jsx
- alembic
- client
- EmailDispatchService
- drafter_service.py
- tools.py
- 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)
- StarCoachTool
- Roadmap — Job Application Agent SaaS
- react
- JobsView.jsx
- Application
- AdzunaJobSource
- MockQdrantClient
- test_bookmarklet_generation_with_job_and_star_answers
- api/interview.py
- deploy.sh
- cv_parser.py
- .generate
- SendGateway
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- subscription.py
- jobs.py
- test_apply_graph.py
- theme.js
- sse_adapter.py
- check_migrations.py
- .generate
- test_decoupled_tools.py
- test_pydantic_schemas
- .generate
- MockLLMProvider
- posting_guard.py
- BaseAgentTool
- test_models.py
- 74cebd545352_add_is_pinned_to_agent_conversations.py
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- a7c3e1f24b01_add_profile_and_interview_tables.py
- TeXLiveCompilerService
- Session
- Security & Tenancy Policy (adapted from ECC AgentShield)
- .generate
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
- get_monitor_summary
- env.py
- test_monitor_followups_task
- decrypt_secret
- get_available_sources
- .queue_application_send
- tailor_application
- os
- parse_redis_settings
- create_email_draft
- update_application_status
- .to_base64url
- .generate
- .__init__
- 1. Executive Summary & Scope

## God Nodes (most connected - your core abstractions)
1. `Account` - 250 edges
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
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py

## Import Cycles
- None detected.

## Communities (158 total, 29 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.06
Nodes (22): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, _is_invisible(), _line_looks_like_instruction(), Enum, str (+14 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.07
Nodes (42): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult (+34 more)

### Community 3 - "JobPosting"
Cohesion: 0.05
Nodes (58): Integration Checklist, Job Source Integrator, arq, arq_connections, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService (+50 more)

### Community 5 - "Account"
Cohesion: 0.04
Nodes (67): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, client(), fixture, Session, TestClient (+59 more)

### Community 6 - "StarStory"
Cohesion: 0.09
Nodes (38): delete_story(), get_story(), list_stories(), list_tags(), delete, get, Session, Extract all unique tags across the account's STAR stories. (+30 more)

### Community 7 - "api/profile.py"
Cohesion: 0.10
Nodes (63): add_certification(), add_designation(), add_language(), add_location(), add_project(), apply_parsed_cv(), compile_texlive(), create_profile() (+55 more)

### Community 8 - "Job"
Cohesion: 0.19
Nodes (15): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application… (+7 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "Base"
Cohesion: 0.13
Nodes (34): app_services_agent_workflows_apply_graph, app_services_dispatch_gateway, argparse, get_llm_service(), Dependency provider for LLMService., Base, Base SQLAlchemy declarative model., get_db() (+26 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "BaseModel"
Cohesion: 0.17
Nodes (16): detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FormAnswerModel (+8 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.14
Nodes (27): decrypt_oauth_token(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Derive a deterministic 32-byte URL-safe base64 Fernet key from secret string., Legacy Fernet instance derived from JWT_SECRET_KEY., Construct MultiFernet instance for OAuth token encryption/decryption. Supports… (+19 more)

### Community 15 - "apply_graph.py"
Cohesion: 0.11
Nodes (39): Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), assemble_package_node(), autonomy_gate_edge(), build_apply_graph(), cv_drafter_node(), cv_reviewer_node() (+31 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (36): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+28 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.07
Nodes (30): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+22 more)

### Community 18 - ".fetch"
Cohesion: 0.24
Nodes (7): _clean_html(), _parse_publication_date(), Any, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC).

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "GoogleIntegrationService"
Cohesion: 0.15
Nodes (16): get_google_auth_url(), Generate Google OAuth 2.0 consent URL for Gmail Draft composition and outbound…, PlatformOAuthAppConfig, Platform-wide or tenant-specific OAuth application credentials (e.g. Google…, GoogleIntegrationService, Any, Generate the Google OAuth 2.0 consent URL requesting offline access and full…, Exchange an OAuth authorization code for access and refresh tokens. Fetches the… (+8 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.08
Nodes (28): Run underlying setup and enforce Row Level Security on checkpointer tables in…, CopilotState, 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy (+20 more)

### Community 22 - "google_service.py"
Cohesion: 0.11
Nodes (24): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, backend/app/services/integrations/mime_builder.py RFC 2822 & RFC 2046 Compliant…, Base exception for MIME construction and validation errors. (+16 more)

### Community 23 - "typing"
Cohesion: 0.09
Nodes (43): JobBase, JobCreate, JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources., classify_location_type(), JobSource (+35 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 26 - "integrations.py"
Cohesion: 0.07
Nodes (56): BookmarkletResponse, connect_smtp(), create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), disconnect_smtp(), generate_oauth_state() (+48 more)

### Community 27 - "QuotaService"
Cohesion: 0.16
Nodes (14): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+6 more)

### Community 28 - ".send_gmail_message"
Cohesion: 0.16
Nodes (19): GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, Exception, Base exception for Gmail API transmission and authorization failures. (+11 more)

### Community 29 - "Education"
Cohesion: 0.22
Nodes (11): add_education(), patch, update_certification(), update_education(), update_project(), update_work_experience(), Education, EducationBase (+3 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.22
Nodes (16): GenerativeUIWidget, BaseModel, Enum, str, Executes the autonomous tool action and returns structured data along with an…, ToolCategory, ToolExecutionContext, ToolResult (+8 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (39): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+31 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "create_app"
Cohesion: 0.14
Nodes (22): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+14 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.09
Nodes (22): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 3.1 Single Atomic Transaction Before External Call, 3.2 Periodic Sweeper (Stale Claimed & Stale Sending), 3.3 Mid-Hold Cancel & Autonomy Toggle Off, 3. Send State Machine & Outbox Poller (+14 more)

### Community 41 - "ProfileSkill"
Cohesion: 0.23
Nodes (12): add_skill(), bulk_skills(), update_skill(), ProfileSkill, ProfileSkillBase, ProfileSkillCreate, ProfileSkillRead, Structured work experience entity for candidates across all industries.… (+4 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.11
Nodes (51): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_google_oauth_config(), delete_admin_template(), delete_job(), delete_llm_provider() (+43 more)

### Community 45 - "api/auth.py"
Cohesion: 0.06
Nodes (63): auth_google_authorize(), auth_google_callback_get(), auth_google_callback_post(), get_me(), login(), get, post, Session (+55 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "lucide-react"
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

### Community 53 - "SendAuthorization"
Cohesion: 0.15
Nodes (19): DispatchedAction, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Sequenced idempotency barrier. Partial unique index excludes aborted/failed so…, SendAuthorization, UserCommand, asyncio, Executes full ApplyGraph pipeline to dispatch, then feeds the generated… (+11 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.06
Nodes (31): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, post, Generate tailored interview prep questions for a specific role or job posting,…, Ensure the caller has superadmin role privileges. (+23 more)

### Community 60 - "dispatch_poller.py"
Cohesion: 0.16
Nodes (16): main(), poll_and_dispatch_batch(), Session, backend/app/workers/dispatch_poller.py PostgreSQL DB Outbox Poller Worker…, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Periodic 30-second sweeper per Section 3.2 of specification: 1. Stale claimed…, run_poller_daemon() (+8 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "latexCompiler.js"
Cohesion: 0.16
Nodes (22): 7.1 Scope Classification & CASA Exemption, 7.2 Integration Strategy, 7. Gmail Integration Architecture (Scope Correction), ApplicationStudio(), ResumeBuilderView(), TEMPLATES, ResumePreviewModal(), StudioApprovalGate() (+14 more)

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
Cohesion: 0.11
Nodes (19): AgentConversation, AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, Conversation session between user and Career OS Agent., AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is… (+11 more)

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
Cohesion: 0.12
Nodes (31): test_llm_provider(), AnthropicProvider, Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet /…, LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, GeminiProvider, Google Gemini implementation of the LLMProvider interface (Gemini 2.5 Flash /… (+23 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "stage_proposal_tool.py"
Cohesion: 0.18
Nodes (15): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+7 more)

### Community 82 - "test_matching.py"
Cohesion: 0.03
Nodes (76): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+68 more)

### Community 83 - "gateway.py"
Cohesion: 0.09
Nodes (37): AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.…, AccountDispatchSettings, ApplicationPdfPayload, JobFeedback, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Stores compiled PDF byte payloads outside applications table to prevent bloat., Immutable audit evidence of external transmission. Uses NO ACTION DEFERRABLE… (+29 more)

### Community 84 - "test_agent.py"
Cohesion: 0.11
Nodes (26): BaseModel, SearchJobsInput, BaseModel, StageProposalInput, account_a(), account_b(), api_test_db(), client() (+18 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "dispatch_service.py"
Cohesion: 0.21
Nodes (10): EmailDraftProvider, EmailDraftResult, Enum, str, Result of an email draft creation operation., email_message, email_mime_application, email_mime_multipart (+2 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.11
Nodes (16): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileIntegrationsTab(), ProfileProjectModal(), ProfileProjectsTab() (+8 more)

### Community 91 - "alembic"
Cohesion: 0.25
Nodes (3): alembic, Upgrade schema to include platform_oauth_configs table., upgrade()

### Community 92 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 93 - "EmailDispatchService"
Cohesion: 0.29
Nodes (8): EmailDispatchService, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on…, Generates a standard URL-encoded mailto: link for 1-click launch in default…, Builds a standard RFC 822 .eml message with optional PDF attachment. When…, test_create_draft_rfc822(), test_generate_eml_message_with_pdf_attachment(), test_generate_mailto_link()

### Community 94 - "drafter_service.py"
Cohesion: 0.21
Nodes (11): FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterOutput, OutreachDrafterService, Any, BaseModel, Enum (+3 more)

### Community 95 - "tools.py"
Cohesion: 0.10
Nodes (30): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+22 more)

### Community 96 - "2.1 Table Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.15
Nodes (13): 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped), Table 1: `account_dispatch_settings` (Tenant Autonomy, Safety Caps & Kill Switches), Table 2: `user_commands` (Authority to Attempt), Table 3: `send_authorizations` (Content-Pinned Authorization), Table 4: `application_pdf_payloads` (Dedicated PDF Byte Storage) (+5 more)

### Community 97 - "StarCoachTool"
Cohesion: 0.20
Nodes (8): Session, BaseModel, StarCoachInput, StarCoachTool, Test STAR interview coach tool aligns story to competency., Verify tool registration and schema generation., test_agent_tools_registry(), test_star_coach_tool()

### Community 98 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 99 - "react"
Cohesion: 0.19
Nodes (10): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics(), lintLatexSource() (+2 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "Application"
Cohesion: 0.15
Nodes (22): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountUsageCounter, Live aggregated balances per billing period. Updated transactionally with…, client(), create_approval_fixture(), asyncio, fixture (+14 more)

### Community 102 - "AdzunaJobSource"
Cohesion: 0.08
Nodes (26): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+18 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.18
Nodes (11): api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent… (+3 more)

### Community 105 - "api/interview.py"
Cohesion: 0.33
Nodes (9): create_story(), patch, STAR Interview Coach API — CRUD for interview stories + tag-based querying. All…, update_story(), BaseModel, StarStoryBase, StarStoryCreate, StarStoryRead (+1 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 109 - "SendGateway"
Cohesion: 0.10
Nodes (38): HoldQueueItem, Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure. (+30 more)

### Community 110 - "test_tools_api.py"
Cohesion: 0.08
Nodes (31): Tenant ownership registry for LangGraph state threads. Guarantees strict multi-…, ThreadAccount, Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH or Docker, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable(), account_a() (+23 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.12
Nodes (43): add_work_experience(), OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, PlatformOAuthAppConfigInput, PlatformOAuthAppConfigRead, BaseModel, CertificationBase (+35 more)

### Community 113 - "subscription.py"
Cohesion: 0.36
Nodes (9): EntitlementBase, EntitlementCreate, EntitlementRead, EntitlementUpdate, BaseModel, SubscriptionPlanBase, SubscriptionPlanCreate, SubscriptionPlanRead (+1 more)

### Community 114 - "jobs.py"
Cohesion: 0.11
Nodes (23): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+15 more)

### Community 115 - "test_apply_graph.py"
Cohesion: 0.07
Nodes (41): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, CVReviewOutput, BaseModel, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic… (+33 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "sse_adapter.py"
Cohesion: 0.15
Nodes (19): dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line., Serializes Pydantic models cleanly using model_dump() or dict(). (+11 more)

### Community 118 - "check_migrations.py"
Cohesion: 0.60
Nodes (4): check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 120 - "test_decoupled_tools.py"
Cohesion: 0.14
Nodes (21): CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput, prune_and_budget_latex(), BaseModel, backend/app/services/cv_tailor/drafter.py Decoupled Senior Recruiter Drafter…, Executes Pass 1 (Senior Recruiter Drafter). Outputs tailored summary bullet,… (+13 more)

### Community 121 - "test_pydantic_schemas"
Cohesion: 0.08
Nodes (27): 4. Pydantic Schemas & Security, AccountBase, AccountCreate, AccountRead, ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase (+19 more)

### Community 123 - "MockLLMProvider"
Cohesion: 0.15
Nodes (11): MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, client(), fixture, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-… (+3 more)

### Community 124 - "posting_guard.py"
Cohesion: 0.24
Nodes (7): GateResult, IntegrityFlag, posting_guard.py — posting integrity gate (ARCHITECTURE.md §4, §8) Every…, A single issue found during the integrity check. kind — what category of issue…, Return type from run_posting_guard(). posting — a new JobPosting copy with…, Tests for backend/app/services/posting_guard.py Coverage: - A completely clean…, unicodedata

### Community 125 - "BaseAgentTool"
Cohesion: 0.22
Nodes (7): BaseAgentTool, ABC, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 126 - "test_models.py"
Cohesion: 0.08
Nodes (43): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /… (+35 more)

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
Cohesion: 0.12
Nodes (20): build_sandboxed_tex_env(), ensure_latex_preamble_macros(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Detect available Docker container with pdflatex., Return True if a TeX compiler is installed and executable locally or in Docker., Compile LaTeX source into PDF inside a Docker worker container with TeX Live…, Compile LaTeX source into PDF using system TeX Live engine or Docker container… (+12 more)

### Community 131 - "Session"
Cohesion: 0.28
Nodes (9): cancel_application_send(), draft_follow_up(), FollowUpDraftResponse, mark_follow_up_sent(), post, Session, Candidate Undo/Cancel Gate: Cancels an application currently in the undo…, Module 3 (Monitor): Generates a personalized follow-up email draft. Strictly… (+1 more)

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - ".generate"
Cohesion: 0.06
Nodes (33): Any, Execute generation across the provider chain with automatic fallback., Return execution metadata from the last successful LLM call for…, Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start (+25 more)

### Community 134 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 136 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 138 - "env.py"
Cohesion: 0.15
Nodes (19): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+11 more)

### Community 141 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 144 - "decrypt_secret"
Cohesion: 0.33
Nodes (6): decrypt_secret(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy…, Verify secrets are encrypted and decrypted accurately., Verify code exchange, DB persistence with encryption, status check, and…, test_crypto_encryption_roundtrip(), test_google_callback_and_status()

### Community 147 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 148 - ".queue_application_send"
Cohesion: 0.18
Nodes (10): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., Enqueues an application for outbound dispatch with an undo hold window.…, SendGatewayException, compute_content_hash(), backend/app/services/dispatch/hash_utils.py Canonical length-prefixed content… (+2 more)

### Community 149 - "tailor_application"
Cohesion: 0.50
Nodes (5): Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, AccountCvVersionRead

### Community 150 - "os"
Cohesion: 0.06
Nodes (34): app_services_agent_checkpointer, asyncio, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), csv, decimal (+26 more)

### Community 151 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 152 - "create_email_draft"
Cohesion: 0.50
Nodes (4): create_email_draft(), DraftEmailRequest, DraftEmailResponse, Phase 3: Minimal-Effort Dispatch. Generates a pre-populated draft with 1-click…

### Community 153 - "update_application_status"
Cohesion: 0.50
Nodes (4): patch, Module 3 (Monitor): Update application status across pipeline stages: draft ->…, StatusUpdateRequest, update_application_status()

### Community 154 - ".to_base64url"
Cohesion: 0.50
Nodes (3): Encode raw MIME bytes to base64url string required by the Gmail API., Verify basic plaintext MIME message construction., test_mime_builder_plain_message()

### Community 162 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1166 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobPosting`, `api/profile.py`, `Job`, `Base`, `BaseModel`, `test_google_dispatch.py`, `apply_graph.py`, `decrypt_secret`, `test_monitor_followups_task`, `TestClient`, `GoogleIntegrationService`, `tailor_application`, `typing`, `create_email_draft`, `integrations.py`, `api/agent.py`, `create_app`, `ProfileSkill`, `admin.py`, `api/auth.py`, `SendAuthorization`, `Architecture — Job Application Agent SaaS`, `dispatch_poller.py`, `LLMService`, `test_matching.py`, `gateway.py`, `test_agent.py`, `client`, `tools.py`, `StarCoachTool`, `Application`, `test_bookmarklet_generation_with_job_and_star_answers`, `SendGateway`, `test_tools_api.py`, `models/__init__.py`, `subscription.py`, `jobs.py`, `test_apply_graph.py`, `MockLLMProvider`, `test_models.py`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `Session`, `JobPosting`, `StarStory`, `Base`, `BaseModel`, `test_monitor_followups_task`, `LeverJobSource`, `TestClient`, `tailor_application`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `typing`, `engine.py`, `create_app`, `admin.py`, `SendAuthorization`, `Architecture — Job Application Agent SaaS`, `dispatch_poller.py`, `AgentEngine`, `stage_proposal_tool.py`, `test_matching.py`, `gateway.py`, `test_agent.py`, `tools.py`, `Application`, `test_bookmarklet_generation_with_job_and_star_answers`, `api/interview.py`, `SendGateway`, `test_tools_api.py`, `models/__init__.py`, `jobs.py`, `test_apply_graph.py`, `MockLLMProvider`, `test_models.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `Base`, `LLMService`, `test_matching.py`, `GoogleIntegrationService`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `check_migrations.py`, `test_decoupled_tools.py`, `integrations.py`, `engine.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 165 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 165 INFERRED edges - model-reasoned connections that need verification._
- **Are the 55 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 55 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 35 INFERRED edges - model-reasoned connections that need verification._
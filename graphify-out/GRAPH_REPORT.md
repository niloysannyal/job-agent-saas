# Graph Report - job-agent-saas  (2026-11-12)

## Corpus Check
- 280 files · ~204,652 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2852 nodes · 7905 edges · 160 communities (133 shown, 27 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1076 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ca4298d5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- test_profile.py
- FastAPI Backend Development Standards (adapted from ECC)
- api/profile.py
- SendGateway
- GreenhouseJobSource
- typing
- FreehireJobSource
- JobSearchQuery
- BaseModel
- test_google_dispatch.py
- check_migrations.py
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- matching/service.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_apply_graph.py
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- What You Must Do When Invoked
- alembic
- integrations.py
- MatchingService
- dispatch_service.py
- .fetch
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- apply_graph.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- Account
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- checkpointer.py
- Project: Job Application Agent SaaS
- poll_and_dispatch_batch
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
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- jobs.py
- React Frontend Development Standards (adapted from ECC)
- stage_proposal_tool.py
- LanguageGate
- test_matching.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- logging
- ProfileView.jsx
- Development Context — Job Application Agent SaaS
- .parse_from_db
- tasks.py
- .generate
- tools.py
- LinkedInJobSource
- Product Development Environment Guide — Job Application Agent SaaS
- Job
- ResumeBuilderView.jsx
- JobsView.jsx
- applications.py
- test_adzuna_fetch_with_mock_client
- MockQdrantClient
- session.py
- UserProfile
- deploy.sh
- cv_parser.py
- AgentToolRegistry
- ProfileSkill
- test_tools_api.py
- bug-workflow.md
- models/__init__.py
- google_service.py
- MockEmbeddingClient
- build_apply_graph
- theme.js
- sse_adapter.py
- QuotaService
- get_monitor_summary
- devDependencies
- Base
- Application
- 8. Persistence, Checkpointers & Hold-Queue Architecture
- test_profile_resumes.py
- drafter_service.py
- test_monitor_followups_task
- TargetDesignation
- .reflect_for_account
- Education
- UserResume
- 6. Autonomy Policy Engine & Guardrails
- mark_application_sent
- CVTailorService
- Session
- EmailDispatchService
- Session
- 13. Strategic Options Analysis & Recommendation
- env.py
- plan_relevance_cuts
- set_compensation
- 3257c49a645d_add_agent_action_proposals_.py
- 74cebd545352_add_is_pinned_to_agent_conversations.py
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- a7c3e1f24b01_add_profile_and_interview_tables.py
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- parse_redis_settings
- create_email_draft
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
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
- `8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`` --references--> `Base`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/db/base.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `7.2 Integration Strategy` --references--> `ApplicationStudio()`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → frontend/src/components/ApplicationStudio.jsx

## Import Cycles
- None detected.

## Communities (160 total, 27 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.06
Nodes (25): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, IntegrityFlag, _is_invisible(), _line_looks_like_instruction(), Enum (+17 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.13
Nodes (22): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+14 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (43): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+35 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 7 - "api/profile.py"
Cohesion: 0.15
Nodes (38): add_certification(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+30 more)

### Community 8 - "SendGateway"
Cohesion: 0.06
Nodes (73): AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Stores compiled PDF byte payloads outside applications table to prevent bloat. (+65 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "typing"
Cohesion: 0.14
Nodes (26): AdzunaJobSource, AsyncClient, Adzuna API implementation of the JobSource interface (ARCHITECTURE.md §4).…, classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided… (+18 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "JobSearchQuery"
Cohesion: 0.07
Nodes (31): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., _clean_html(), _format_salary(), _parse_date() (+23 more)

### Community 13 - "BaseModel"
Cohesion: 0.17
Nodes (16): detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FormAnswerModel (+8 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.08
Nodes (37): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), argparse, decrypt_oauth_token(), decrypt_secret() (+29 more)

### Community 15 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "matching/service.py"
Cohesion: 0.14
Nodes (15): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+7 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.12
Nodes (15): 14. Milestone Roadmap & Effort Estimates, 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 7.1 Scope Classification & CASA Exemption (+7 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.08
Nodes (32): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, CVReviewOutput, BaseModel, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic… (+24 more)

### Community 23 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 26 - "integrations.py"
Cohesion: 0.10
Nodes (33): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+25 more)

### Community 27 - "MatchingService"
Cohesion: 0.15
Nodes (10): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+2 more)

### Community 28 - "dispatch_service.py"
Cohesion: 0.21
Nodes (10): EmailDraftProvider, EmailDraftResult, Enum, str, Result of an email draft creation operation., email_message, email_mime_application, email_mime_multipart (+2 more)

### Community 29 - ".fetch"
Cohesion: 0.16
Nodes (11): _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, datetime, Asynchronously fetch job postings matching the query from Adzuna., Strip HTML tags and normalize whitespace. (+3 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.20
Nodes (21): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+13 more)

### Community 32 - "api/agent.py"
Cohesion: 0.08
Nodes (46): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+38 more)

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

### Community 41 - "apply_graph.py"
Cohesion: 0.13
Nodes (27): cv_drafter_node(), cv_reviewer_node(), backend/app/services/agent/workflows/apply_graph.py Modular LangGraph…, Executes Pass 1 (Senior Recruiter Drafter) with dynamic section budgeting., Executes Pass 2 (Senior Recruiter Reviewer & Fact Auditor)., CandidateCareerContext, CVDrafterService, CVDraftInput (+19 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "Account"
Cohesion: 0.11
Nodes (53): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+45 more)

### Community 45 - "test_auth.py"
Cohesion: 0.06
Nodes (59): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+51 more)

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

### Community 51 - "checkpointer.py"
Cohesion: 0.09
Nodes (27): AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph…, Factory creating a psycopg_pool.AsyncConnectionPool calibrated for Supabase…, Initializes and sets up the TenantScopedAsyncPostgresSaver., Raised when an account attempts to access a thread belonging to another tenant. (+19 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "poll_and_dispatch_batch"
Cohesion: 0.25
Nodes (7): main(), poll_and_dispatch_batch(), Session, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, run_poller_daemon(), Event

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
Cohesion: 0.17
Nodes (18): detect_method_node(), Classifies apply channel and extracts form questions or recruiter email., ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text. (+10 more)

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
Cohesion: 0.15
Nodes (11): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Executes human-in-the-loop approval of an action proposal. Enforces tenant… (+3 more)

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
Nodes (18): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+10 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "jobs.py"
Cohesion: 0.13
Nodes (20): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+12 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "stage_proposal_tool.py"
Cohesion: 0.18
Nodes (14): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+6 more)

### Community 82 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 83 - "test_matching.py"
Cohesion: 0.12
Nodes (18): db_session(), asyncio, fixture, Session, Verify cosine similarity calculation edge cases and bounds., Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs…, In-memory SQLite session for testing matching. (+10 more)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (30): BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput, account_a(), account_b() (+22 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "logging"
Cohesion: 0.05
Nodes (44): asyncio, normalize_db_url(), Normalize database URL for driver compatibility., TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, assert_safe_test_database_url(), fixture, Enforces local development and test boundary per Advisor Review 9. Blocks test…, Verify database safety before running any tests. (+36 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 92 - ".parse_from_db"
Cohesion: 0.21
Nodes (10): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models:…, Path, Test that missing languages section defaults to ['english']., Test extracting clean text from LaTeX CV and markdown profile. (+2 more)

### Community 93 - "tasks.py"
Cohesion: 0.12
Nodes (21): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+13 more)

### Community 94 - ".generate"
Cohesion: 0.13
Nodes (15): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 2.2 Tenancy Exemption in `scripts/check_migrations.py` (+7 more)

### Community 95 - "tools.py"
Cohesion: 0.11
Nodes (30): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+22 more)

### Community 96 - "LinkedInJobSource"
Cohesion: 0.19
Nodes (8): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser()

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 98 - "Job"
Cohesion: 0.12
Nodes (23): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications. (+15 more)

### Community 99 - "ResumeBuilderView.jsx"
Cohesion: 0.20
Nodes (11): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+3 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "applications.py"
Cohesion: 0.18
Nodes (16): get_llm_service(), Dependency provider for LLMService., Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, decode_access_token(), get_current_account() (+8 more)

### Community 102 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.16
Nodes (12): asyncio, Test async fetch using string and dict queries., Test that missing credentials raise JobSourceConfigError., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "session.py"
Cohesion: 0.05
Nodes (62): get_db(), get_engine(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application., ApplicationFormAnswer (+54 more)

### Community 105 - "UserProfile"
Cohesion: 0.08
Nodes (45): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+37 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.11
Nodes (16): parse_cv_file(), UploadFile, CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf. (+8 more)

### Community 108 - "AgentToolRegistry"
Cohesion: 0.16
Nodes (7): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…, Verify tool registration and schema generation., test_agent_tools_registry()

### Community 109 - "ProfileSkill"
Cohesion: 0.17
Nodes (16): add_project(), add_skill(), add_work_experience(), apply_parsed_cv(), bulk_skills(), create_profile(), post, Create a user profile for an account (one per account). (+8 more)

### Community 110 - "test_tools_api.py"
Cohesion: 0.13
Nodes (21): account_a(), api_test_db(), client(), fixture, Session, TestClient, backend/tests/api/test_tools_api.py Unit and integration tests for Decoupled…, Test POST /api/v1/tools/detect-method discovers email application. (+13 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.12
Nodes (43): ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, BaseModel, CertificationBase (+35 more)

### Community 113 - "google_service.py"
Cohesion: 0.07
Nodes (40): GmailApiException, GmailApiNotConfiguredException, GmailServerErrorException, Exception, Send an outbound email message via official Gmail API messages.send. Args:…, Base exception for Gmail API transmission and authorization failures., Raised on 403 accessNotConfigured (Gmail API not enabled in GCP Console)., Raised on HTTP 5xx errors from Google servers. (+32 more)

### Community 114 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 115 - "build_apply_graph"
Cohesion: 0.11
Nodes (28): assemble_package_node(), autonomy_gate_edge(), build_apply_graph(), dispatch_node(), fit_analyzer_node(), hitl_approval_gate_node(), post_approval_edge(), Any (+20 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "sse_adapter.py"
Cohesion: 0.15
Nodes (19): dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line., Serializes Pydantic models cleanly using model_dump() or dict(). (+11 more)

### Community 118 - "QuotaService"
Cohesion: 0.16
Nodes (14): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+6 more)

### Community 119 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 120 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 121 - "Base"
Cohesion: 0.05
Nodes (88): 4. Pydantic Schemas & Security, Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), Session (+80 more)

### Community 122 - "Application"
Cohesion: 0.13
Nodes (23): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, claim_pending_batch(), Claim a batch of eligible hold items using SELECT ... FOR UPDATE SKIP LOCKED.…, client(), create_approval_fixture(), asyncio, fixture (+15 more)

### Community 123 - "8. Persistence, Checkpointers & Hold-Queue Architecture"
Cohesion: 0.50
Nodes (4): 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 124 - "test_profile_resumes.py"
Cohesion: 0.23
Nodes (14): api_test_db(), client(), create_minimal_pdf_bytes(), fixture, Session, TestClient, Generate a minimal valid 1-page PDF file in memory using pypdf., test_account() (+6 more)

### Community 125 - "drafter_service.py"
Cohesion: 0.19
Nodes (14): outreach_drafter_node(), Generates tailored outreach matching the discovered channel., FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterOutput, OutreachDrafterService, Any (+6 more)

### Community 126 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 127 - "TargetDesignation"
Cohesion: 0.12
Nodes (19): add_designation(), add_language(), add_location(), CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in… (+11 more)

### Community 128 - ".reflect_for_account"
Cohesion: 0.40
Nodes (3): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…

### Community 129 - "Education"
Cohesion: 0.15
Nodes (15): add_education(), patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience() (+7 more)

### Community 130 - "UserResume"
Cohesion: 0.16
Nodes (14): compile_texlive(), save_builder_resume(), Saved candidate resume/CV documents (uploaded PDFs or built via LaTeX Resume…, UserResume, Any, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine. Returns dict with… (+6 more)

### Community 131 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 132 - "mark_application_sent"
Cohesion: 0.40
Nodes (5): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., SendGatewayException

### Community 133 - "CVTailorService"
Cohesion: 0.20
Nodes (10): CVTailorService, Session, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Selects the best fact-verified Summary variant based on role keywords or…, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and… (+2 more)

### Community 134 - "Session"
Cohesion: 0.18
Nodes (13): cancel_application_send(), draft_follow_up(), FollowUpDraftResponse, mark_follow_up_sent(), patch, post, Session, Candidate Undo/Cancel Gate: Cancels an application currently in the undo… (+5 more)

### Community 135 - "EmailDispatchService"
Cohesion: 0.29
Nodes (8): EmailDispatchService, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on…, Generates a standard URL-encoded mailto: link for 1-click launch in default…, Builds a standard RFC 822 .eml message with optional PDF attachment. When…, test_create_draft_rfc822(), test_generate_eml_message_with_pdf_attachment(), test_generate_mailto_link()

### Community 136 - "Session"
Cohesion: 0.18
Nodes (11): Session, Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Test StarStory model creation, tags, and account cascade., Test Account model defaults and multi-tenant fields., Test Job model matches ARCHITECTURE.md §7: (account_id, company, role, salary,…, test_account_model(), test_application_model_and_human_in_the_loop_gate() (+3 more)

### Community 137 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 138 - "env.py"
Cohesion: 0.31
Nodes (9): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+1 more)

### Community 139 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 140 - "set_compensation"
Cohesion: 0.50
Nodes (5): set_compensation(), CompensationBase, CompensationCreate, CompensationRead, put

### Community 141 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 142 - "74cebd545352_add_is_pinned_to_agent_conversations.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations., upgrade()

### Community 143 - "7f7822f4eef9_add_github_url_to_projects_and_location_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade()

### Community 144 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 145 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 146 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 147 - "create_email_draft"
Cohesion: 0.50
Nodes (4): create_email_draft(), DraftEmailRequest, DraftEmailResponse, Phase 3: Minimal-Effort Dispatch. Generates a pre-populated draft with 1-click…

### Community 157 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 158 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

## Knowledge Gaps
- **261 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+256 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1113 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobPosting`, `UserResume`, `CVTailorService`, `test_profile.py`, `api/profile.py`, `SendGateway`, `Session`, `typing`, `BaseModel`, `test_google_dispatch.py`, `create_email_draft`, `TestClient`, `integrations.py`, `api/agent.py`, `test_admin.py`, `test_auth.py`, `Architecture — Job Application Agent SaaS`, `jobs.py`, `test_matching.py`, `test_agent.py`, `tasks.py`, `tools.py`, `Job`, `applications.py`, `session.py`, `test_tools_api.py`, `models/__init__.py`, `Base`, `Application`, `test_profile_resumes.py`, `test_monitor_followups_task`, `TargetDesignation`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `CVTailorService`, `Session`, `SendGateway`, `Session`, `typing`, `BaseModel`, `TestClient`, `matching/service.py`, `test_apply_graph.py`, `MatchingService`, `engine.py`, `test_admin.py`, `Account`, `AgentEngine`, `jobs.py`, `stage_proposal_tool.py`, `test_matching.py`, `test_agent.py`, `tasks.py`, `tools.py`, `applications.py`, `session.py`, `UserProfile`, `test_tools_api.py`, `models/__init__.py`, `build_apply_graph`, `Base`, `Application`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `Job`, `apply_graph.py`, `LLMService`, `check_migrations.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `Base`, `integrations.py`, `MatchingService`, `engine.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 139 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
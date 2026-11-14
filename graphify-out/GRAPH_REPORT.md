# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 283 files · ~209,696 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2911 nodes · 8133 edges · 134 communities (116 shown, 18 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1115 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `17b73ada`
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
- Session
- SendGateway
- GreenhouseJobSource
- Base
- FreehireJobSource
- RemoteOKJobSource
- BaseModel
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
- create_gmail_draft
- MatchingService
- test_generate_form_answers_api_endpoint
- test_engine_approval_and_lifecycle.py
- Settings
- typing
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- logging
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- Account
- account.py
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
- StarStory
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
- llm/service.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- trigger_ingestion
- React Frontend Development Standards (adapted from ECC)
- StageApplicationProposalTool
- LanguageGate
- test_matching.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- pathlib
- ProfileView.jsx
- api/profile.py
- ProfileParser
- dispatch_service.py
- .generate
- tools.py
- .dispatch_hold_item
- Product Development Environment Guide — Job Application Agent SaaS
- drafter_service.py
- StudioDrafterWorkspace.jsx
- JobsView.jsx
- fit_analyzer.py
- JobSearchQuery
- test_matching_service_score_and_gate_clean_jobs
- test_bookmarklet_generation_with_job_and_star_answers
- LLMService
- deploy.sh
- cv_parser.py
- client
- QuotaService
- TestClient
- bug-workflow.md
- models/__init__.py
- google_service.py
- .generate
- apply_graph.py
- theme.js
- sse_adapter.py
- 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)
- get_available_sources
- e2e_account_and_job
- UserProfile
- Application
- dispatch_poller.py
- test_profile_resumes.py
- AgentToolRegistry
- .generate
- Roadmap — Job Application Agent SaaS
- CVTailorService
- TeXLiveCompilerService
- encrypt_secret
- json
- env.py
- mark_application_sent

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
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.1 Model 1: `AccountSubscription` (Anchored Billing Periods)` --references--> `AccountSubscription`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle)` --references--> `QuotaReservation`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.5 Model 5: `UsageEvent` (Scope Column Added)` --references--> `UsageEvent`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py

## Import Cycles
- None detected.

## Communities (134 total, 18 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.12
Nodes (19): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+11 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.08
Nodes (37): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+29 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (39): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+31 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 7 - "Session"
Cohesion: 0.12
Nodes (41): add_certification(), add_education(), add_location(), add_project(), add_work_experience(), create_profile(), delete_user_resume(), download_user_resume() (+33 more)

### Community 8 - "SendGateway"
Cohesion: 0.07
Nodes (67): AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Stores compiled PDF byte payloads outside applications table to prevent bloat. (+59 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.06
Nodes (33): _clean_html(), _detect_location_type(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime (+25 more)

### Community 10 - "Base"
Cohesion: 0.07
Nodes (68): get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Resolve the current authenticated account context. 1. Primary: Validates…, Base, Base SQLAlchemy declarative model., get_db() (+60 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+20 more)

### Community 13 - "BaseModel"
Cohesion: 0.06
Nodes (46): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+38 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.11
Nodes (33): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy… (+25 more)

### Community 15 - "check_migrations.py"
Cohesion: 0.60
Nodes (4): check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 16 - "package.json"
Cohesion: 0.05
Nodes (38): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+30 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.07
Nodes (30): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+22 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 20 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.09
Nodes (24): CopilotState, 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy, 15. Decision Register (+16 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.09
Nodes (32): CVReviewOutput, BaseModel, mock_llm_responses(), asyncio, fixture, backend/tests/agent/test_apply_graph.py Unit tests for Modular LangGraph…, Verifies resuming an interrupted graph with Command(resume=approve) runs…, Verifies resuming an interrupted graph with Command(resume=reject) terminates… (+24 more)

### Community 23 - "job.py"
Cohesion: 0.15
Nodes (23): JobBase, JobCreate, JobRead, JobUpdate, BaseModel, _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type() (+15 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.10
Nodes (23): create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_google_auth_url(), get_google_status(), google_oauth_callback(), GoogleAuthUrlResponse (+15 more)

### Community 27 - "MatchingService"
Cohesion: 0.15
Nodes (10): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+2 more)

### Community 28 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.32
Nodes (7): client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 29 - "test_engine_approval_and_lifecycle.py"
Cohesion: 0.19
Nodes (18): client(), create_approval_fixture(), asyncio, fixture, Session, TestClient, Verify Task 4 Human-in-the-Loop on Send: 1. Proposal approved. 2. Application…, Verify Candidate Undo Window: When a user cancels within the 30s countdown: 1.… (+10 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "typing"
Cohesion: 0.20
Nodes (22): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+14 more)

### Community 32 - "api/agent.py"
Cohesion: 0.10
Nodes (38): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+30 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "Job"
Cohesion: 0.08
Nodes (39): create_app(), Create and configure FastAPI application., Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db() (+31 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (30): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+22 more)

### Community 41 - "logging"
Cohesion: 0.11
Nodes (29): Executes Pass 2 Senior Recruiter CV review. Audits for unverified claims,…, review_cv_endpoint(), cv_reviewer_node(), Executes Pass 2 (Senior Recruiter Reviewer & Fact Auditor)., CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput (+21 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "Account"
Cohesion: 0.11
Nodes (53): 4. Pydantic Schemas & Security, _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider() (+45 more)

### Community 45 - "account.py"
Cohesion: 0.14
Nodes (30): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+22 more)

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
Nodes (41): AsyncConnectionPool, AsyncPostgresSaver, create_checkpointer_pool(), init_tenant_checkpointer(), Any, backend/app/services/agent/checkpointer.py Multi-Tenant Scoped LangGraph…, Deletes thread checkpoints and cleans up thread_accounts registry. Requires…, Run underlying setup and enforce Row Level Security on checkpointer tables in… (+33 more)

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

### Community 60 - "StarStory"
Cohesion: 0.05
Nodes (60): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+52 more)

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

### Community 74 - "llm/service.py"
Cohesion: 0.20
Nodes (13): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for… (+5 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "trigger_ingestion"
Cohesion: 0.18
Nodes (13): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+5 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "StageApplicationProposalTool"
Cohesion: 0.19
Nodes (13): asyncio, AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+5 more)

### Community 82 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 83 - "test_matching.py"
Cohesion: 0.10
Nodes (23): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+15 more)

### Community 84 - "test_agent.py"
Cohesion: 0.08
Nodes (34): BaseModel, SearchAndRankJobsTool, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput, StarCoachTool (+26 more)

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
Cohesion: 0.09
Nodes (25): decimal, os, pathlib, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables…, check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+17 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.11
Nodes (25): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+17 more)

### Community 91 - "api/profile.py"
Cohesion: 0.14
Nodes (25): add_language(), add_skill(), bulk_skills(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location() (+17 more)

### Community 92 - "ProfileParser"
Cohesion: 0.16
Nodes (11): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser, Any, Path, Structured representation of parsed user profile and CV. (+3 more)

### Community 93 - "dispatch_service.py"
Cohesion: 0.05
Nodes (43): arq, arq_connections, EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's… (+35 more)

### Community 94 - ".generate"
Cohesion: 0.09
Nodes (22): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 10. Observability & Cost Controls, 1.1 Goal (+14 more)

### Community 95 - "tools.py"
Cohesion: 0.14
Nodes (23): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+15 more)

### Community 96 - ".dispatch_hold_item"
Cohesion: 0.21
Nodes (8): Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure., Handle retryable 429/5xx error by scheduling exponential backoff and releasing…, Atomically record successful external dispatch, evidence, and state transitions.

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 98 - "drafter_service.py"
Cohesion: 0.23
Nodes (11): FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterOutput, OutreachDrafterService, Any, BaseModel, Enum (+3 more)

### Community 99 - "StudioDrafterWorkspace.jsx"
Cohesion: 0.21
Nodes (10): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics() (+2 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "fit_analyzer.py"
Cohesion: 0.25
Nodes (8): backend/app/services/agent/workflows/state.py Decoupled State Schemas for…, DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, BaseModel, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic…, dataclasses, langgraph_graph_message

### Community 102 - "JobSearchQuery"
Cohesion: 0.07
Nodes (29): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient (+21 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.09
Nodes (21): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']. (+13 more)

### Community 104 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.18
Nodes (12): client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and… (+4 more)

### Community 105 - "LLMService"
Cohesion: 0.18
Nodes (5): Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, Resolve ordered list of active providers from database or defaults.

### Community 107 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 108 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 109 - "QuotaService"
Cohesion: 0.13
Nodes (18): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+10 more)

### Community 110 - "TestClient"
Cohesion: 0.10
Nodes (20): account_a(), client(), fixture, Session, TestClient, Test POST /api/v1/tools/detect-method discovers email application., Test POST /api/v1/tools/draft-cv produces tailored LaTeX without mutation., Test POST /api/v1/tools/review-cv audits fact integrity and ATS score. (+12 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.10
Nodes (51): add_designation(), ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, AccountCvVersionBase, AccountCvVersionUpdate, CvTemplateUpdate, BaseModel (+43 more)

### Community 113 - "google_service.py"
Cohesion: 0.06
Nodes (44): GmailApiNotConfiguredException, GmailServerErrorException, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Send an outbound email message via official Gmail API messages.send. Args:…, Raised on 403 accessNotConfigured (Gmail API not enabled in GCP Console)., Raised on HTTP 5xx errors from Google servers. (+36 more)

### Community 115 - "apply_graph.py"
Cohesion: 0.09
Nodes (43): Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), TOFU Exact-Address allowlist. Email uniqueness is enforced case-insensitively…, TrustedRecipient, QuotaReservation, Multi-dimensional atomic reservation lifecycle (reserved -> settled | released…, assemble_package_node() (+35 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "sse_adapter.py"
Cohesion: 0.13
Nodes (20): run_resume_background(), run_apply_background(), dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent… (+12 more)

### Community 118 - "3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.33
Nodes (6): 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods), 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances), 3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle), 3.4 Model 4: `ModelPricing` (In `backend/app/models/model_pricing.py`), 3.5 Model 5: `UsageEvent` (Scope Column Added), 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)

### Community 119 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 120 - "e2e_account_and_job"
Cohesion: 0.67
Nodes (3): e2e_account_and_job(), fixture, Seed real Account, Job, AccountDispatchSettings, and TrustedRecipient in test…

### Community 121 - "UserProfile"
Cohesion: 0.06
Nodes (61): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountCvVersion, AccountCvVersionCreate, CvTemplate, CvTemplateBase, CvTemplateCreate (+53 more)

### Community 122 - "Application"
Cohesion: 0.08
Nodes (22): BookmarkletResponse, get_autofill_bookmarklet(), Generate an intelligent JavaScript bookmarklet code tailored to the current…, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories… (+14 more)

### Community 123 - "dispatch_poller.py"
Cohesion: 0.19
Nodes (13): claim_pending_batch(), main(), poll_and_dispatch_batch(), Session, backend/app/workers/dispatch_poller.py PostgreSQL DB Outbox Poller Worker…, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Periodic 30-second sweeper per Section 3.2 of specification: 1. Stale claimed… (+5 more)

### Community 124 - "test_profile_resumes.py"
Cohesion: 0.23
Nodes (14): api_test_db(), client(), create_minimal_pdf_bytes(), fixture, Session, TestClient, Generate a minimal valid 1-page PDF file in memory using pypdf., test_account() (+6 more)

### Community 125 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 127 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 129 - "CVTailorService"
Cohesion: 0.11
Nodes (25): apply_parsed_cv(), patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience() (+17 more)

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.16
Nodes (15): compile_texlive(), build_sandboxed_tex_env(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Construct scrubbed environment for TeX compilation child processes. - Strips…, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine with strict… (+7 more)

### Community 132 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a general sensitive plaintext secret (e.g. LLM API key, SMTP password)…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 135 - "json"
Cohesion: 0.13
Nodes (13): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), extract_file_content() (+5 more)

### Community 138 - "env.py"
Cohesion: 0.15
Nodes (18): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+10 more)

### Community 142 - "mark_application_sent"
Cohesion: 0.40
Nodes (5): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., SendGatewayException

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1130 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `CVTailorService`, `tailor_service.py`, `JobPosting`, `test_profile.py`, `json`, `Session`, `SendGateway`, `Base`, `BaseModel`, `test_google_dispatch.py`, `TestClient`, `test_auth.py`, `test_apply_graph.py`, `job.py`, `create_gmail_draft`, `test_generate_form_answers_api_endpoint`, `test_engine_approval_and_lifecycle.py`, `api/agent.py`, `Job`, `logging`, `account.py`, `TestClient`, `Architecture — Job Application Agent SaaS`, `trigger_ingestion`, `test_matching.py`, `test_agent.py`, `api/profile.py`, `tools.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `client`, `TestClient`, `models/__init__.py`, `apply_graph.py`, `e2e_account_and_job`, `UserProfile`, `Application`, `test_profile_resumes.py`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `CVTailorService`, `tailor_service.py`, `JobPosting`, `SendGateway`, `Base`, `BaseModel`, `LeverJobSource`, `TestClient`, `test_apply_graph.py`, `job.py`, `MatchingService`, `test_engine_approval_and_lifecycle.py`, `typing`, `logging`, `Account`, `account.py`, `StarStory`, `AgentEngine`, `trigger_ingestion`, `StageApplicationProposalTool`, `test_matching.py`, `test_agent.py`, `dispatch_service.py`, `tools.py`, `fit_analyzer.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `TestClient`, `models/__init__.py`, `apply_graph.py`, `e2e_account_and_job`, `UserProfile`, `Application`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `SendGateway` connect `SendGateway` to `.dispatch_hold_item`, `AgentEngine`, `Job`, `JobEazy: Milestone M1 & M1b Implementation Specification`, `Base`, `QuotaService`, `mark_application_sent`, `test_google_dispatch.py`, `google_service.py`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `Application`, `dispatch_poller.py`, `test_engine_approval_and_lifecycle.py`, `typing`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 144 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 144 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 33 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - job-agent-saas  (2026-11-12)

## Corpus Check
- 265 files · ~194,597 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2627 nodes · 7231 edges · 132 communities (116 shown, 16 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 969 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6d914f0b`
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
- JobSourceHTTPError
- FreehireJobSource
- RemoteOKJobSource
- BaseModel
- crypto.py
- check_migrations.py
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- matching/service.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_generate_form_answers_api_endpoint
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- What You Must Do When Invoked
- typing
- integrations.py
- MatchingService
- dispatch_service.py
- JobSearchQuery
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- generator.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- Account
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- Project: Job Application Agent SaaS
- dispatch_poller.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- detective.py
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
- main.py
- React Frontend Development Standards (adapted from ECC)
- event_bus.py
- test_matching.py
- test_matching_service_score_and_gate_clean_jobs
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- config.py
- ProfileView.jsx
- Development Context — Job Application Agent SaaS
- .parse_from_db
- worker.py
- .generate
- test_bookmarklet_generation_with_job_and_star_answers
- get_available_sources
- Product Development Environment Guide — Job Application Agent SaaS
- ResumeBuilderView.jsx
- JobsView.jsx
- applications.py
- test_adzuna_fetch_with_mock_client
- MockQdrantClient
- Base
- StarStory
- deploy.sh
- AgentToolRegistry
- Education
- bug-workflow.md
- models/__init__.py
- gateway.py
- MockEmbeddingClient
- 5.2 Node Inventory Table & Tailor Refactoring
- theme.js
- 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)
- TestClient
- get_monitor_summary
- devDependencies
- test_models.py
- test_engine_approval_and_lifecycle.py
- 8. Persistence, Checkpointers & Hold-Queue Architecture
- UserProfile
- test_profile_compile_texlive.py
- test_monitor_followups_task
- Roadmap — Job Application Agent SaaS
- .reflect_for_account
- client
- apply_parsed_cv
- 6. Autonomy Policy Engine & Guardrails
- QuotaExceededException
- update_application_status
- 1. Executive Summary & Scope
- 13. Strategic Options Analysis & Recommendation

## God Nodes (most connected - your core abstractions)
1. `Account` - 208 edges
2. `Job` - 105 edges
3. `Base` - 100 edges
4. `Application` - 79 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 66 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 55 edges
9. `SendGateway` - 53 edges
10. `react` - 49 edges

## Surprising Connections (you probably didn't know these)
- `8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`` --references--> `Base`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/db/base.py
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

## Communities (132 total, 16 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.07
Nodes (44): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult (+36 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (40): Integration Checklist, Job Source Integrator, JobPosting, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any (+32 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 7 - "api/profile.py"
Cohesion: 0.11
Nodes (48): add_skill(), bulk_skills(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project() (+40 more)

### Community 8 - "SendGateway"
Cohesion: 0.08
Nodes (56): AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Stores compiled PDF byte payloads outside applications table to prevent bloat. (+48 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "JobSourceHTTPError"
Cohesion: 0.12
Nodes (30): AdzunaJobSource, _detect_location_type(), AsyncClient, Infer location type (remote, hybrid, on-site) using centralized classifier., Adzuna API implementation of the JobSource interface (ARCHITECTURE.md §4).…, classify_location_type(), JobSource, ABC (+22 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "BaseModel"
Cohesion: 0.10
Nodes (31): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+23 more)

### Community 14 - "crypto.py"
Cohesion: 0.07
Nodes (39): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), argparse, decrypt_oauth_token(), decrypt_secret() (+31 more)

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
Nodes (24): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+16 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 20 - "matching/service.py"
Cohesion: 0.14
Nodes (15): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+7 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.12
Nodes (16): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology (+8 more)

### Community 22 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.32
Nodes (7): client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 23 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.04
Nodes (28): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+20 more)

### Community 26 - "integrations.py"
Cohesion: 0.14
Nodes (25): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+17 more)

### Community 27 - "MatchingService"
Cohesion: 0.15
Nodes (10): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+2 more)

### Community 28 - "dispatch_service.py"
Cohesion: 0.14
Nodes (19): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+11 more)

### Community 29 - "JobSearchQuery"
Cohesion: 0.13
Nodes (14): JobSearchQuery, Normalized query parameters for searching across job sources., _clean_text(), _format_salary(), _parse_created_date(), Any, datetime, Asynchronously fetch job postings matching the query from Adzuna. (+6 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.19
Nodes (25): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+17 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (44): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+36 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "Job"
Cohesion: 0.06
Nodes (47): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db() (+39 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (33): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+25 more)

### Community 41 - "generator.py"
Cohesion: 0.23
Nodes (10): FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field., Full questionnaire result containing all tailored field answers., Harness² Recursive Form Q&A Generator. Applies Task-Level Recursion (Propose ->… (+2 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "Account"
Cohesion: 0.12
Nodes (48): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+40 more)

### Community 45 - "test_auth.py"
Cohesion: 0.07
Nodes (57): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+49 more)

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

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "dispatch_poller.py"
Cohesion: 0.21
Nodes (11): claim_pending_batch(), main(), poll_and_dispatch_batch(), Session, backend/app/workers/dispatch_poller.py PostgreSQL DB Outbox Poller Worker…, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Claim a batch of eligible hold items using SELECT ... FOR UPDATE SKIP LOCKED.… (+3 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.05
Nodes (41): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, post, Generate tailored interview prep questions for a specific role or job posting,…, check_job_liveness() (+33 more)

### Community 60 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

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
Nodes (12): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated… (+4 more)

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
Cohesion: 0.05
Nodes (43): parse_cv_file(), UploadFile, Session, LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every… (+35 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "main.py"
Cohesion: 0.12
Nodes (18): list_jobs(), get, Fetch jobs for an account ordered by match_score descending. Excludes vetoed…, get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Resolve the current authenticated account context. 1. Primary: Validates… (+10 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "event_bus.py"
Cohesion: 0.16
Nodes (13): asyncio, Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+5 more)

### Community 82 - "test_matching.py"
Cohesion: 0.13
Nodes (15): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., Verify cosine similarity calculation edge cases and bounds. (+7 more)

### Community 83 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.14
Nodes (13): db_session(), asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs…, In-memory SQLite session for testing matching., Test OpenAIEmbeddingClient with mocked httpx response. (+5 more)

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

### Community 88 - "config.py"
Cohesion: 0.05
Nodes (50): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+42 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 92 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models:…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 93 - "worker.py"
Cohesion: 0.12
Nodes (16): arq, arq_connections, embed_jobs_batch_task(), Any, Worker task to run Experience Reflector and update learning insights., Background worker task to compute vector embeddings and gate jobs., reflect_experience_task(), parse_redis_settings() (+8 more)

### Community 94 - ".generate"
Cohesion: 0.13
Nodes (15): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 2.2 Tenancy Exemption in `scripts/check_migrations.py` (+7 more)

### Community 95 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.18
Nodes (12): client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and… (+4 more)

### Community 96 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 99 - "ResumeBuilderView.jsx"
Cohesion: 0.20
Nodes (11): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+3 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "applications.py"
Cohesion: 0.26
Nodes (13): Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, ApplicationRead, AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionRead (+5 more)

### Community 102 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.19
Nodes (10): asyncio, Test async fetch using string and dict queries., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations(), test_adzuna_fetch_with_mock_client() (+2 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "Base"
Cohesion: 0.09
Nodes (55): Base, Base SQLAlchemy declarative model., get_db(), get_engine(), get_session_factory(), Session, FastAPI dependency that yields a SQLAlchemy database session., Create a new database session instance outside of FastAPI request lifecycle… (+47 more)

### Community 105 - "StarStory"
Cohesion: 0.16
Nodes (23): create_story(), delete_story(), get_story(), list_stories(), list_tags(), delete, get, patch (+15 more)

### Community 108 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 109 - "Education"
Cohesion: 0.18
Nodes (12): add_certification(), add_designation(), add_education(), add_location(), create_profile(), post, Create a user profile for an account (one per account)., Education (+4 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.12
Nodes (43): add_language(), add_project(), add_work_experience(), JobUpdate, CertificationBase, CertificationCreate, CertificationRead, CertificationUpdate (+35 more)

### Community 113 - "gateway.py"
Cohesion: 0.07
Nodes (55): backend/app/services/dispatch/gateway.py SendGateway: Operational Outbound…, GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, GoogleIntegrationService (+47 more)

### Community 114 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 115 - "5.2 Node Inventory Table & Tailor Refactoring"
Cohesion: 0.50
Nodes (4): 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.2 Node Inventory Table & Tailor Refactoring, 5.3 Bounded Review Loop & Recursion Limit, 5. State Schemas, Nodes, and Interrupt Catalogs

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.33
Nodes (6): 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods), 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances), 3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle), 3.4 Model 4: `ModelPricing` (In `backend/app/models/model_pricing.py`), 3.5 Model 5: `UsageEvent` (Scope Column Added), 3. Database Schema Definitions (SQLAlchemy 2.0 Declarative)

### Community 118 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 119 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 120 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 121 - "test_models.py"
Cohesion: 0.06
Nodes (52): 4. Pydantic Schemas & Security, Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountCreate, ApplicationCreate, CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system… (+44 more)

### Community 122 - "test_engine_approval_and_lifecycle.py"
Cohesion: 0.09
Nodes (39): AccountUsageCounter, QuotaReservation, Append-only usage ledger. scope separates tenant usage from platform background…, Live aggregated balances per billing period. Updated transactionally with…, Multi-dimensional atomic reservation lifecycle (reserved -> settled | released…, UsageEvent, Any, datetime (+31 more)

### Community 123 - "8. Persistence, Checkpointers & Hold-Queue Architecture"
Cohesion: 0.40
Nodes (5): 8.1 Hold Queue: PostgreSQL DB Outbox vs Arq/Redis Comparison, 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 124 - "UserProfile"
Cohesion: 0.08
Nodes (40): CompensationExpectation, Structured work experience entity for candidates across all industries.…, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, Saved candidate resume/CV documents (uploaded PDFs or built via LaTeX Resume… (+32 more)

### Community 125 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 126 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 127 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 128 - ".reflect_for_account"
Cohesion: 0.40
Nodes (3): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…

### Community 129 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 130 - "apply_parsed_cv"
Cohesion: 0.14
Nodes (18): apply_parsed_cv(), compile_texlive(), download_user_resume(), list_user_resumes(), Any, _resolve_target_account_id(), save_builder_resume(), set_compensation() (+10 more)

### Community 131 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 132 - "QuotaExceededException"
Cohesion: 0.22
Nodes (8): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., SendGatewayException, Exception, QuotaExceededException, Raised when an account exceeds its allocated usage quota.

### Community 134 - "update_application_status"
Cohesion: 0.50
Nodes (4): patch, Module 3 (Monitor): Update application status across pipeline stages: draft ->…, StatusUpdateRequest, update_application_status()

### Community 136 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

### Community 137 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

## Knowledge Gaps
- **264 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+259 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1030 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `client`, `apply_parsed_cv`, `tailor_service.py`, `JobPosting`, `test_profile.py`, `api/profile.py`, `SendGateway`, `BaseModel`, `crypto.py`, `TestClient`, `test_generate_form_answers_api_endpoint`, `integrations.py`, `api/agent.py`, `Job`, `test_auth.py`, `Architecture — Job Application Agent SaaS`, `LLMService`, `main.py`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `applications.py`, `Base`, `StarStory`, `models/__init__.py`, `gateway.py`, `TestClient`, `test_models.py`, `test_engine_approval_and_lifecycle.py`, `UserProfile`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `SendGateway`, `BaseModel`, `TestClient`, `matching/service.py`, `MatchingService`, `engine.py`, `Account`, `Architecture — Job Application Agent SaaS`, `AgentEngine`, `LLMService`, `main.py`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `worker.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `applications.py`, `Base`, `StarStory`, `models/__init__.py`, `gateway.py`, `5.2 Node Inventory Table & Tailor Refactoring`, `test_models.py`, `test_engine_approval_and_lifecycle.py`, `UserProfile`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `Base` connect `Base` to `tailor_service.py`, `JobPosting`, `test_profile.py`, `api/profile.py`, `SendGateway`, `check_migrations.py`, `TestClient`, `integrations.py`, `api/agent.py`, `Job`, `Account`, `test_auth.py`, `lucide-react`, `AgentEngine`, `main.py`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `config.py`, `applications.py`, `StarStory`, `Education`, `models/__init__.py`, `test_models.py`, `test_engine_approval_and_lifecycle.py`, `8. Persistence, Checkpointers & Hold-Queue Architecture`, `UserProfile`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 129 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 129 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - job-agent-saas  (2026-11-12)

## Corpus Check
- 260 files · ~1,380,644 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2580 nodes · 7005 edges · 138 communities (115 shown, 23 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 942 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f6db4f2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- Account
- models/__init__.py
- Session
- test_send_gateway.py
- job.py
- .fetch
- FreehireJobSource
- RemoteOKJobSource
- dispatch_service.py
- config.py
- Base
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- test_matching.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- sqlalchemy
- test_auth.py
- What You Must Do When Invoked
- typing
- integrations.py
- .parse_from_db
- review.py
- AdzunaJobSource
- Settings
- Job
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- UserProfile
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- api/auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- test_cv_tailor_service_with_structured_profile
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- MatchingService
- graphify reference: extra exports and benchmark
- ProfileView.jsx
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
- event_bus.py
- .check
- json
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- env.py
- test_monitor_followups_task
- Development Context — Job Application Agent SaaS
- LogText
- tasks.py
- .generate
- 13. Strategic Options Analysis & Recommendation
- JobSearchQuery
- Product Development Environment Guide — Job Application Agent SaaS
- QuotaService
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- lucide-react
- TestClient
- test_matching_service_score_and_gate_clean_jobs
- logging
- StarStory
- deploy.sh
- .generate
- AgentToolRegistry
- check_migrations.py
- sys
- bug-workflow.md
- models/profile.py
- gateway.py
- .to_dict
- theme.js
- db_session
- client
- plan_relevance_cuts
- 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)
- test_models.py
- Application
- 8. Persistence, Checkpointers & Hold-Queue Architecture
- Education
- test_application_status_update
- ProfileSkill
- UserProfileRead
- core/auth.py
- post
- MockEmbeddingClient
- FastAPI Backend Development Standards (adapted from ECC)
- Certification
- api/profile.py
- WorkExperience
- parse_redis_settings
- client
- SendGatewayException
- .__init__

## God Nodes (most connected - your core abstractions)
1. `Account` - 198 edges
2. `Job` - 106 edges
3. `Base` - 97 edges
4. `Application` - 78 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 64 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 57 edges
9. `SendGateway` - 47 edges
10. `react` - 46 edges

## Surprising Connections (you probably didn't know these)
- `8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`` --references--> `Base`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/db/base.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `11.1 Test Suite Specifications (`backend/tests/agent/`)` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `1.1 Decision D1 Resolution & Architectural Intent` --references--> `SendGateway`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/services/dispatch/gateway.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py

## Import Cycles
- None detected.

## Communities (138 total, 23 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.11
Nodes (27): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+19 more)

### Community 3 - "JobPosting"
Cohesion: 0.10
Nodes (37): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+29 more)

### Community 5 - "Account"
Cohesion: 0.07
Nodes (41): delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), delete, get_me(), get, Retrieve authenticated account profile and permissions from validated token. (+33 more)

### Community 6 - "models/__init__.py"
Cohesion: 0.09
Nodes (43): Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM). Executes…, tailor_application(), TailorRequest, TailorResponse, AccountBase, AccountCreate, AccountRead, AccountUpdate (+35 more)

### Community 7 - "Session"
Cohesion: 0.21
Nodes (19): get_compensation(), get_current_user_profile(), get_experience_insights(), _get_or_create_profile(), get_profile(), list_certifications(), list_designations(), list_educations() (+11 more)

### Community 8 - "test_send_gateway.py"
Cohesion: 0.08
Nodes (49): HoldQueueItem, Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, Any, Session, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure., Handle retryable 429/5xx error by scheduling exponential backoff and releasing… (+41 more)

### Community 9 - "job.py"
Cohesion: 0.10
Nodes (32): classify_location_type(), Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError, JobSourceError, JobSourceHTTPError, Exception, Raised when an external job source HTTP request fails., Base exception for job source errors. (+24 more)

### Community 10 - ".fetch"
Cohesion: 0.12
Nodes (14): _clean_html(), _detect_location_type(), _do_fetch(), _parse_iso_date(), Any, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.…, Asynchronously fetch all open job postings for a company from Greenhouse,… (+6 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "dispatch_service.py"
Cohesion: 0.05
Nodes (57): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+49 more)

### Community 14 - "config.py"
Cohesion: 0.07
Nodes (38): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), argparse, decrypt_oauth_token(), decrypt_secret() (+30 more)

### Community 15 - "Base"
Cohesion: 0.08
Nodes (43): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.… (+35 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (35): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+27 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (29): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+21 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "test_matching.py"
Cohesion: 0.08
Nodes (25): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+17 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.08
Nodes (24): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy, 14. Milestone Roadmap & Effort Estimates, 15. Decision Register, 16. Document Changelog, 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph (+16 more)

### Community 22 - "sqlalchemy"
Cohesion: 0.09
Nodes (38): get_db(), get_engine(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application., api_test_db() (+30 more)

### Community 23 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.05
Nodes (23): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+15 more)

### Community 26 - "integrations.py"
Cohesion: 0.14
Nodes (25): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+17 more)

### Community 27 - ".parse_from_db"
Cohesion: 0.21
Nodes (9): Any, Path, Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']., Test extracting clean text from LaTeX CV and markdown profile., test_profile_parser_cv_and_profile_extraction() (+1 more)

### Community 29 - "AdzunaJobSource"
Cohesion: 0.08
Nodes (26): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+18 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "Job"
Cohesion: 0.16
Nodes (30): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str (+22 more)

### Community 32 - "api/agent.py"
Cohesion: 0.10
Nodes (38): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+30 more)

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
Cohesion: 0.09
Nodes (22): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 3.1 Single Atomic Transaction Before External Call, 3.2 Periodic Sweeper (Stale Claimed & Stale Sending), 3.3 Mid-Hold Cancel & Autonomy Toggle Off, 3. Send State Machine & Outbox Poller (+14 more)

### Community 41 - "UserProfile"
Cohesion: 0.08
Nodes (39): Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, ApplyChannelType, FormDetectiveService, FormFieldQuestion, FormInspectionResult, Enum, str (+31 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.15
Nodes (37): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+29 more)

### Community 45 - "api/auth.py"
Cohesion: 0.11
Nodes (32): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+24 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "react"
Cohesion: 0.18
Nodes (16): 2. Current State Map (Codebase Ground Truth), CareerCopilotView(), FAST_CHIPS, formatInlineMarkdown(), STARTER_PROMPTS, TurnMarkdownContent(), FunnelInsight(), JobRadarCarousel() (+8 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.07
Nodes (24): Ensure the caller has superadmin role privileges., require_superadmin(), Any, Alias for role to maintain consistency across frontend and APIs., 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make) (+16 more)

### Community 60 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ProfileView.jsx"
Cohesion: 0.09
Nodes (31): ApplicationStudio(), ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab() (+23 more)

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
Cohesion: 0.17
Nodes (10): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,… (+2 more)

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
Cohesion: 0.13
Nodes (20): get_llm_service(), Dependency provider for LLMService., LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can… (+12 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "jobs.py"
Cohesion: 0.13
Nodes (20): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+12 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "event_bus.py"
Cohesion: 0.24
Nodes (8): asyncio, ApplicationTailoredEvent, DomainEvent, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent, BaseModel, EventHandler

### Community 83 - "json"
Cohesion: 0.20
Nodes (9): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, csv, io (+1 more)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (32): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput (+24 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "env.py"
Cohesion: 0.08
Nodes (31): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+23 more)

### Community 90 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 93 - "tasks.py"
Cohesion: 0.15
Nodes (18): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+10 more)

### Community 94 - ".generate"
Cohesion: 0.09
Nodes (22): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.2 Node Inventory Table & Tailor Refactoring, 5.3 Bounded Review Loop & Recursion Limit, 5. State Schemas, Nodes, and Interrupt Catalogs, 1.1 Goal (+14 more)

### Community 95 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 96 - "JobSearchQuery"
Cohesion: 0.10
Nodes (18): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, JobSource, ABC, Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR… (+10 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 98 - "QuotaService"
Cohesion: 0.16
Nodes (14): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+6 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "lucide-react"
Cohesion: 0.22
Nodes (11): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics() (+3 more)

### Community 102 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - "logging"
Cohesion: 0.12
Nodes (20): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, LanguageGate, Evaluates whether a job description requires a spoken language not declared in… (+12 more)

### Community 105 - "StarStory"
Cohesion: 0.14
Nodes (28): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+20 more)

### Community 108 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 109 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 110 - "sys"
Cohesion: 0.13
Nodes (15): decimal, os, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables…, check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor() (+7 more)

### Community 112 - "models/profile.py"
Cohesion: 0.14
Nodes (25): add_designation(), add_language(), add_location(), set_compensation(), CertificationUpdate, CompensationBase, CompensationCreate, CompensationRead (+17 more)

### Community 113 - "gateway.py"
Cohesion: 0.07
Nodes (55): backend/app/services/dispatch/gateway.py SendGateway: Operational Outbound…, GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, GoogleIntegrationService (+47 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 118 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 119 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 120 - "2.1 Table Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.15
Nodes (13): 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped), Table 1: `account_dispatch_settings` (Tenant Autonomy, Safety Caps & Kill Switches), Table 2: `user_commands` (Authority to Attempt), Table 3: `send_authorizations` (Content-Pinned Authorization), Table 4: `application_pdf_payloads` (Dedicated PDF Byte Storage) (+5 more)

### Community 121 - "test_models.py"
Cohesion: 0.07
Nodes (47): 4. Pydantic Schemas & Security, Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, LLMProviderBase, LLMProviderConfig (+39 more)

### Community 122 - "Application"
Cohesion: 0.07
Nodes (48): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,… (+40 more)

### Community 123 - "8. Persistence, Checkpointers & Hold-Queue Architecture"
Cohesion: 0.50
Nodes (4): 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 124 - "Education"
Cohesion: 0.40
Nodes (6): add_education(), Education, EducationBase, EducationCreate, EducationRead, Structured education background (degrees, high school, certifications,…

### Community 125 - "test_application_status_update"
Cohesion: 0.23
Nodes (12): Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer., Test Module 2 (Apply) application tailoring and strict human-in-the-loop Send…, test_application_status_update() (+4 more)

### Community 126 - "ProfileSkill"
Cohesion: 0.39
Nodes (8): add_skill(), bulk_skills(), update_skill(), ProfileSkill, ProfileSkillBase, ProfileSkillCreate, ProfileSkillRead, Structured skill entity with taxonomy categorization and proficiency.

### Community 127 - "UserProfileRead"
Cohesion: 0.33
Nodes (7): create_profile(), Create a user profile for an account (one per account)., Partial-update the user profile for an account (auto-creates if missing)., update_profile(), UserProfileBase, UserProfileCreate, UserProfileRead

### Community 129 - "core/auth.py"
Cohesion: 0.31
Nodes (8): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, jwt

### Community 130 - "post"
Cohesion: 0.20
Nodes (11): apply_parsed_cv(), compile_texlive(), parse_cv_file(), Any, post, UploadFile, Any, Detect available TeX compiler binary on PATH. (+3 more)

### Community 131 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 132 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 134 - "Certification"
Cohesion: 0.22
Nodes (11): add_certification(), patch, update_certification(), update_education(), update_project(), update_work_experience(), Certification, CertificationBase (+3 more)

### Community 135 - "api/profile.py"
Cohesion: 0.21
Nodes (16): add_project(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+8 more)

### Community 136 - "WorkExperience"
Cohesion: 0.40
Nodes (6): add_work_experience(), Structured work experience entity for candidates across all industries.…, WorkExperience, WorkExperienceBase, WorkExperienceCreate, WorkExperienceRead

### Community 137 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 145 - "SendGatewayException"
Cohesion: 0.67
Nodes (3): Exception, Base exception for SendGateway dispatch failures., SendGatewayException

## Knowledge Gaps
- **263 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1022 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `core/auth.py`, `tailor_service.py`, `JobPosting`, `models/__init__.py`, `api/profile.py`, `Session`, `job.py`, `test_send_gateway.py`, `dispatch_service.py`, `config.py`, `Base`, `TestClient`, `test_matching.py`, `sqlalchemy`, `test_auth.py`, `integrations.py`, `api/agent.py`, `test_admin.py`, `UserProfile`, `admin.py`, `api/auth.py`, `test_cv_tailor_service_with_structured_profile`, `Architecture — Job Application Agent SaaS`, `jobs.py`, `json`, `test_agent.py`, `test_monitor_followups_task`, `tasks.py`, `TestClient`, `test_matching_service_score_and_gate_clean_jobs`, `StarStory`, `models/profile.py`, `gateway.py`, `client`, `test_models.py`, `Application`, `test_application_status_update`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `Account`, `models/__init__.py`, `test_send_gateway.py`, `job.py`, `dispatch_service.py`, `Base`, `TestClient`, `test_matching.py`, `sqlalchemy`, `test_admin.py`, `UserProfile`, `admin.py`, `test_cv_tailor_service_with_structured_profile`, `Architecture — Job Application Agent SaaS`, `MatchingService`, `AgentEngine`, `jobs.py`, `test_agent.py`, `test_monitor_followups_task`, `tasks.py`, `.generate`, `JobSearchQuery`, `test_matching_service_score_and_gate_clean_jobs`, `logging`, `StarStory`, `gateway.py`, `test_models.py`, `Application`, `test_application_status_update`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `Base` connect `Base` to `tailor_service.py`, `JobPosting`, `Account`, `models/__init__.py`, `Certification`, `test_send_gateway.py`, `job.py`, `api/profile.py`, `WorkExperience`, `TestClient`, `test_matching.py`, `sqlalchemy`, `test_auth.py`, `integrations.py`, `Job`, `api/agent.py`, `test_admin.py`, `UserProfile`, `api/auth.py`, `react`, `test_agent.py`, `env.py`, `test_monitor_followups_task`, `test_matching_service_score_and_gate_clean_jobs`, `StarStory`, `check_migrations.py`, `models/profile.py`, `db_session`, `client`, `test_models.py`, `Application`, `8. Persistence, Checkpointers & Hold-Queue Architecture`, `Education`, `ProfileSkill`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 120 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 120 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
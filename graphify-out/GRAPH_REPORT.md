# Graph Report - job-agent-saas  (2026-11-12)

## Corpus Check
- 260 files · ~1,380,878 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2582 nodes · 7023 edges · 142 communities (122 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 943 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a2b363e6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- Account
- subscription.py
- api/profile.py
- SendGateway
- GreenhouseJobSource
- JobSourceHTTPError
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- test_google_dispatch.py
- AccountSubscription
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- typing
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- Base
- test_auth.py
- What You Must Do When Invoked
- alembic
- integrations.py
- test_m1_models_and_migration.py
- dispatch_service.py
- JobSearchQuery
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- create_app
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- UserProfile
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- api/auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
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
- detective.py
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
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
- .check
- .send_gmail_message
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- env.py
- ProfileView.jsx
- Development Context — Job Application Agent SaaS
- GoogleIntegrationService
- worker.py
- .generate
- ApplicationFormAnswer
- get_available_sources
- Product Development Environment Guide — Job Application Agent SaaS
- gateway.py
- SpokenLanguage
- JobsView.jsx
- react
- dispatch_poller.py
- MockQdrantClient
- texlive_compiler.py
- api/interview.py
- deploy.sh
- .generate
- BaseAgentTool
- check_migrations.py
- encrypt_secret
- bug-workflow.md
- models/__init__.py
- google_service.py
- run_ats_text_layer_check
- .role
- theme.js
- db_session
- client
- client
- 2.1 Table Definitions (SQLAlchemy 2.0 Declarative)
- Entitlement
- test_engine_approval_and_lifecycle.py
- 8. Persistence, Checkpointers & Hold-Queue Architecture
- WorkExperience
- Job
- test_profile_compile_texlive.py
- UserProfileRead
- add_location
- 5.2 Node Inventory Table & Tailor Refactoring
- post
- 6. Autonomy Policy Engine & Guardrails
- db_session
- 12. Dependency Plan & Environment Strategy
- Certification
- Project
- 1. Executive Summary & Scope
- 9. Redesigned SSE Protocol Adapter & UI Integration
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- client
- mark_application_sent
- .__init__

## God Nodes (most connected - your core abstractions)
1. `Account` - 198 edges
2. `Job` - 105 edges
3. `Base` - 97 edges
4. `Application` - 79 edges
5. `JobPosting` - 74 edges
6. `UserProfile` - 64 edges
7. `JobSearchQuery` - 62 edges
8. `AgentEngine` - 55 edges
9. `SendGateway` - 53 edges
10. `react` - 46 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`` --references--> `Base`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/db/base.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle)` --references--> `QuotaReservation`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py

## Import Cycles
- None detected.

## Communities (142 total, 20 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.10
Nodes (31): audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body(), Strips lines starting with %% (agent control notes) while preserving actual…, Escapes LaTeX special characters (% & $ # _) if they are not already escaped.… (+23 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (41): Integration Checklist, Job Source Integrator, JobPosting, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any (+33 more)

### Community 5 - "Account"
Cohesion: 0.06
Nodes (43): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint() (+35 more)

### Community 6 - "subscription.py"
Cohesion: 0.10
Nodes (26): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), AccountCvVersionUpdate, CvTemplateBase (+18 more)

### Community 7 - "api/profile.py"
Cohesion: 0.15
Nodes (34): delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill(), delete_work_experience() (+26 more)

### Community 8 - "SendGateway"
Cohesion: 0.11
Nodes (38): HoldQueueItem, Durable PostgreSQL DB Outbox queue polled with SELECT ... FOR UPDATE SKIP…, Any, Session, Execute dispatch for a claimed hold_queue_item. Returns True if sent…, Executes pre-checks, checks send caps and kill switches, verifies canonical…, Atomically abort hold queue item and release associated resources., Handle non-retryable fatal dispatch failure. (+30 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), GreenhouseJobSource, _do_fetch(), Any, AsyncClient, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.…, Asynchronously fetch all open job postings for a company from Greenhouse,…, Unescape Greenhouse's double-encoded HTML content field. The field is HTML-… (+20 more)

### Community 10 - "JobSourceHTTPError"
Cohesion: 0.12
Nodes (28): _detect_location_type(), _parse_created_date(), datetime, Parse ISO formatted creation date from Adzuna response., Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC (+20 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (46): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+38 more)

### Community 14 - "test_google_dispatch.py"
Cohesion: 0.13
Nodes (27): decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy…, Derive a deterministic 32-byte URL-safe base64 Fernet key from secret string. (+19 more)

### Community 15 - "AccountSubscription"
Cohesion: 0.17
Nodes (12): AdminAuditLog, Platform-wide immutable audit trail for superadmin operations across tenants.…, AccountSubscription, Tracks tenant subscription plan association and billing cycles. One active…, ModelPricing, Platform-wide model pricing catalog tracking input/output costs per 1M tokens…, 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods), 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances) (+4 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (35): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react, name (+27 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "typing"
Cohesion: 0.03
Nodes (82): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+74 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.12
Nodes (15): 13. Strategic Options Analysis & Recommendation, 14. Milestone Roadmap & Effort Estimates, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 7.1 Scope Classification & CASA Exemption (+7 more)

### Community 22 - "Base"
Cohesion: 0.13
Nodes (40): Base, Base SQLAlchemy declarative model., get_db(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., AccountBase, AccountCreate, AccountRead (+32 more)

### Community 23 - "test_auth.py"
Cohesion: 0.15
Nodes (26): create_access_token(), Generate a cryptographically signed JWT access token. Contains subject…, auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user() (+18 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "integrations.py"
Cohesion: 0.17
Nodes (22): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+14 more)

### Community 27 - "test_m1_models_and_migration.py"
Cohesion: 0.14
Nodes (24): AccountDispatchSettings, DispatchedAction, JobFeedback, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Immutable audit evidence of external transmission. Uses NO ACTION DEFERRABLE…, Sequenced idempotency barrier. Partial unique index excludes aborted/failed so… (+16 more)

### Community 28 - "dispatch_service.py"
Cohesion: 0.14
Nodes (18): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+10 more)

### Community 29 - "JobSearchQuery"
Cohesion: 0.09
Nodes (28): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), Any, AsyncClient, Asynchronously fetch job postings matching the query from Adzuna. (+20 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.23
Nodes (16): GenerativeUIWidget, BaseModel, Enum, str, Executes the autonomous tool action and returns structured data along with an…, ToolCategory, ToolExecutionContext, ToolResult (+8 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (42): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+34 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "create_app"
Cohesion: 0.08
Nodes (26): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), fixture, Session, TestClient (+18 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.09
Nodes (22): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 3.1 Single Atomic Transaction Before External Call, 3.2 Periodic Sweeper (Stale Claimed & Stale Sending), 3.3 Mid-Hold Cancel & Autonomy Toggle Off, 3. Send State Machine & Outbox Poller (+14 more)

### Community 41 - "UserProfile"
Cohesion: 0.23
Nodes (16): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+8 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.13
Nodes (41): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+33 more)

### Community 45 - "api/auth.py"
Cohesion: 0.11
Nodes (31): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+23 more)

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

### Community 51 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.12
Nodes (16): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN), 4. Module 1 — Find Job Opportunity (decision made) (+8 more)

### Community 60 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.20
Nodes (21): ApplicationStudio(), ProfileView(), StudioApprovalGate(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext(), cleanLatexInline() (+13 more)

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
Nodes (14): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, AgentEngine, Any, Session, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands. (+6 more)

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
Cohesion: 0.14
Nodes (18): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+10 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "jobs.py"
Cohesion: 0.10
Nodes (27): list_flagged_jobs(), check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post (+19 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "stage_proposal_tool.py"
Cohesion: 0.15
Nodes (18): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+10 more)

### Community 83 - ".send_gmail_message"
Cohesion: 0.16
Nodes (19): GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, Exception, Send an outbound email message via official Gmail API messages.send. Args:… (+11 more)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (30): BaseModel, SearchAndRankJobsTool, SearchJobsInput, BaseModel, StarCoachInput, StarCoachTool, account_a(), account_b() (+22 more)

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
Cohesion: 0.05
Nodes (47): argparse, asyncio, assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode. (+39 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.15
Nodes (10): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+2 more)

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 92 - "GoogleIntegrationService"
Cohesion: 0.12
Nodes (12): GoogleIntegrationService, Any, Refresh an expired access token using the stored encrypted refresh token. Uses…, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 authentication, human-in-the-loop Gmail Draft…, Generate the Google OAuth 2.0 consent URL requesting offline access and full…, Exchange an OAuth authorization code for access and refresh tokens. Fetches the…, Encode raw MIME bytes to base64url string required by the Gmail API. (+4 more)

### Community 93 - "worker.py"
Cohesion: 0.08
Nodes (27): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), monitor_followups_task(), Any (+19 more)

### Community 94 - ".generate"
Cohesion: 0.13
Nodes (15): Any, Execute generation across the provider chain with automatic fallback., 10. Observability & Cost Controls, 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 2.2 Tenancy Exemption in `scripts/check_migrations.py` (+7 more)

### Community 95 - "ApplicationFormAnswer"
Cohesion: 0.15
Nodes (14): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is… (+6 more)

### Community 96 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 98 - "gateway.py"
Cohesion: 0.11
Nodes (24): AccountQuotaOverride, QuotaReservation, Append-only usage ledger. scope separates tenant usage from platform background…, Administrative overrides for quota limits. Precedence: Override > Plan >…, Multi-dimensional atomic reservation lifecycle (reserved -> settled | released…, UsageEvent, backend/app/services/dispatch/gateway.py SendGateway: Operational Outbound…, Any (+16 more)

### Community 99 - "SpokenLanguage"
Cohesion: 0.14
Nodes (16): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+8 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "react"
Cohesion: 0.22
Nodes (11): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics() (+3 more)

### Community 102 - "dispatch_poller.py"
Cohesion: 0.21
Nodes (11): claim_pending_batch(), main(), poll_and_dispatch_batch(), Session, backend/app/workers/dispatch_poller.py PostgreSQL DB Outbox Poller Worker…, Poll, claim, and execute dispatch for one batch of hold items. Returns count of…, Continuous poller daemon loop. Runs every `poll_interval` seconds until…, Claim a batch of eligible hold items using SELECT ... FOR UPDATE SKIP LOCKED.… (+3 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "texlive_compiler.py"
Cohesion: 0.20
Nodes (9): TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, main(), Path, Verification Loop — Job Application Agent SaaS Adapted from ECC's verification-…, run_step(), shutil, subprocess, tempfile (+1 more)

### Community 105 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 108 - "BaseAgentTool"
Cohesion: 0.22
Nodes (7): BaseAgentTool, ABC, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 109 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 110 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a general sensitive plaintext secret (e.g. LLM API key, SMTP password)…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.11
Nodes (38): add_designation(), add_language(), add_skill(), add_work_experience(), bulk_skills(), update_skill(), ApplicationFormAnswerBase, ApplicationFormAnswerCreate (+30 more)

### Community 113 - "google_service.py"
Cohesion: 0.11
Nodes (24): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, backend/app/services/integrations/mime_builder.py RFC 2822 & RFC 2046 Compliant…, Base exception for MIME construction and validation errors. (+16 more)

### Community 114 - "run_ats_text_layer_check"
Cohesion: 0.25
Nodes (6): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), Verify ATS parser plain-text inspection and keyword coverage., test_ats_checker()

### Community 115 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 118 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 119 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 120 - "2.1 Table Definitions (SQLAlchemy 2.0 Declarative)"
Cohesion: 0.15
Nodes (13): 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped), Table 1: `account_dispatch_settings` (Tenant Autonomy, Safety Caps & Kill Switches), Table 2: `user_commands` (Authority to Attempt), Table 3: `send_authorizations` (Content-Pinned Authorization), Table 4: `application_pdf_payloads` (Dedicated PDF Byte Storage) (+5 more)

### Community 121 - "Entitlement"
Cohesion: 0.10
Nodes (26): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), lifespan(), Entitlement, Subscription plan catalog model matching ARCHITECTURE.md §0 & §7. Deferred…, Account entitlement model matching ARCHITECTURE.md §7: All-access by default…, SubscriptionPlan (+18 more)

### Community 122 - "test_engine_approval_and_lifecycle.py"
Cohesion: 0.13
Nodes (26): ApplicationPdfPayload, Stores compiled PDF byte payloads outside applications table to prevent bloat., AccountUsageCounter, Live aggregated balances per billing period. Updated transactionally with…, OAuthConnection, Multi-tenant OAuth Connection model. Stores authorized OAuth 2.0 access and…, compute_content_hash(), backend/app/services/dispatch/hash_utils.py Canonical length-prefixed content… (+18 more)

### Community 123 - "8. Persistence, Checkpointers & Hold-Queue Architecture"
Cohesion: 0.50
Nodes (4): 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 124 - "WorkExperience"
Cohesion: 0.18
Nodes (13): add_education(), patch, update_certification(), update_education(), update_project(), update_work_experience(), Education, EducationBase (+5 more)

### Community 125 - "Job"
Cohesion: 0.10
Nodes (27): get_job_sources(), get_platform_metrics(), list_tenants(), get, TenantSummary, update_tenant(), Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,… (+19 more)

### Community 126 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 127 - "UserProfileRead"
Cohesion: 0.33
Nodes (7): create_profile(), Create a user profile for an account (one per account)., Partial-update the user profile for an account (auto-creates if missing)., update_profile(), UserProfileBase, UserProfileCreate, UserProfileRead

### Community 128 - "add_location"
Cohesion: 0.67
Nodes (4): add_location(), TargetLocationBase, TargetLocationCreate, TargetLocationRead

### Community 129 - "5.2 Node Inventory Table & Tailor Refactoring"
Cohesion: 0.50
Nodes (4): 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.2 Node Inventory Table & Tailor Refactoring, 5.3 Bounded Review Loop & Recursion Limit, 5. State Schemas, Nodes, and Interrupt Catalogs

### Community 130 - "post"
Cohesion: 0.20
Nodes (11): apply_parsed_cv(), compile_texlive(), parse_cv_file(), Any, post, UploadFile, Any, Detect available TeX compiler binary on PATH. (+3 more)

### Community 131 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 132 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 133 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

### Community 134 - "Certification"
Cohesion: 0.40
Nodes (6): add_certification(), Certification, CertificationBase, CertificationCreate, CertificationRead, Professional certifications, licenses, and credentials.

### Community 135 - "Project"
Cohesion: 0.40
Nodes (6): add_project(), Project, ProjectBase, ProjectCreate, ProjectRead, Portfolio projects, open-source work, or major professional deliverables.

### Community 136 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

### Community 137 - "9. Redesigned SSE Protocol Adapter & UI Integration"
Cohesion: 0.67
Nodes (3): 9.1 Custom Streaming Loop (Part Objects in Version "v2"), 9.2 Resume Endpoint & Minimal Frontend Contract, 9. Redesigned SSE Protocol Adapter & UI Integration

### Community 138 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

### Community 145 - "mark_application_sent"
Cohesion: 0.40
Nodes (5): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Exception, Base exception for SendGateway dispatch failures., SendGatewayException

## Knowledge Gaps
- **263 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1023 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobPosting`, `subscription.py`, `api/profile.py`, `SendGateway`, `applications.py`, `test_google_dispatch.py`, `TestClient`, `typing`, `Base`, `test_auth.py`, `integrations.py`, `test_m1_models_and_migration.py`, `api/agent.py`, `create_app`, `admin.py`, `api/auth.py`, `test_cv_tailor_service_with_structured_profile`, `jobs.py`, `stage_proposal_tool.py`, `test_agent.py`, `worker.py`, `ApplicationFormAnswer`, `SpokenLanguage`, `models/__init__.py`, `client`, `client`, `Entitlement`, `test_engine_approval_and_lifecycle.py`, `Job`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `5.2 Node Inventory Table & Tailor Refactoring`, `tailor_service.py`, `JobPosting`, `SendGateway`, `applications.py`, `TestClient`, `typing`, `Base`, `test_m1_models_and_migration.py`, `engine.py`, `create_app`, `UserProfile`, `admin.py`, `test_cv_tailor_service_with_structured_profile`, `AgentEngine`, `jobs.py`, `stage_proposal_tool.py`, `test_agent.py`, `worker.py`, `ApplicationFormAnswer`, `gateway.py`, `api/interview.py`, `models/__init__.py`, `.role`, `Entitlement`, `test_engine_approval_and_lifecycle.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `LLMService`, `check_migrations.py`, `typing`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `Base`, `test_engine_approval_and_lifecycle.py`, `GoogleIntegrationService`, `engine.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 120 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 120 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
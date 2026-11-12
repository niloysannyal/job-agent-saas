# Graph Report - job-agent-saas  (2026-11-12)

## Corpus Check
- 264 files · ~1,395,773 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2624 nodes · 7224 edges · 140 communities (119 shown, 21 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 968 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec942e37`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- test_profile.py
- llm_provider.py
- api/profile.py
- SendGateway
- GreenhouseJobSource
- job.py
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- config.py
- session.py
- package.json
- LeverJobSource
- RemotiveJobSource
- test_jobs.py
- matching/service.py
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- main.py
- Account
- What You Must Do When Invoked
- Base
- integrations.py
- MatchingService
- dispatch_service.py
- JobSearchQuery
- Settings
- Job
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobEazy: Milestone M1 & M1b Implementation Specification
- generator.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- account.py
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
- logging
- test_matching.py
- test_matching_service_score_and_gate_clean_jobs
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- run_phase1_acceleration.py
- react
- Development Context — Job Application Agent SaaS
- .parse_from_db
- worker.py
- .generate
- test_bookmarklet_generation_with_job_and_star_answers
- get_available_sources
- Product Development Environment Guide — Job Application Agent SaaS
- QuotaService
- UserProfile
- JobsView.jsx
- os
- plan_relevance_cuts
- MockQdrantClient
- ApplicationBase
- StarStory
- deploy.sh
- .generate
- .get_tool_definitions
- check_migrations.py
- Security & Tenancy Policy (adapted from ECC AgentShield)
- bug-workflow.md
- models/__init__.py
- gateway.py
- MockEmbeddingClient
- conftest.py
- theme.js
- db_session
- test_interview.py
- get_monitor_summary
- devDependencies
- test_models.py
- Application
- 8. Persistence, Checkpointers & Hold-Queue Architecture
- test_profile_resumes.py
- client
- LogText
- Roadmap — Job Application Agent SaaS
- .reflect_for_account
- JobBase
- Any
- 6. Autonomy Policy Engine & Guardrails
- get_me
- 12. Dependency Plan & Environment Strategy
- prune_and_budget_latex
- 7. Gmail Integration Architecture (Scope Correction)
- 1. Executive Summary & Scope
- 9. Redesigned SSE Protocol Adapter & UI Integration
- 4. QuotaService Interface, Settle Branching & Counter Mutation
- .__init__

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
10. `react` - 48 edges

## Surprising Connections (you probably didn't know these)
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`` --references--> `Base`  [INFERRED]
  docs/plans/langgraph-migration-plan.md → backend/app/db/base.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `3.1 Model 1: `AccountSubscription` (Anchored Billing Periods)` --references--> `AccountSubscription`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.5 Model 5: `UsageEvent` (Scope Column Added)` --references--> `UsageEvent`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py

## Import Cycles
- None detected.

## Communities (140 total, 21 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (21): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+13 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.10
Nodes (28): CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult (+20 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (39): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+31 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "llm_provider.py"
Cohesion: 0.21
Nodes (10): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), LLMProviderBase, LLMProviderCreate (+2 more)

### Community 7 - "api/profile.py"
Cohesion: 0.10
Nodes (56): add_certification(), add_designation(), add_education(), add_language(), add_project(), add_skill(), apply_parsed_cv(), bulk_skills() (+48 more)

### Community 8 - "SendGateway"
Cohesion: 0.05
Nodes (76): mark_application_sent(), Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, AccountDispatchSettings, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,… (+68 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "job.py"
Cohesion: 0.15
Nodes (25): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError (+17 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.11
Nodes (39): cancel_application_send(), create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse (+31 more)

### Community 14 - "config.py"
Cohesion: 0.07
Nodes (35): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), encrypt_secret(), _get_legacy_fernet(), get_oauth_fernet() (+27 more)

### Community 15 - "session.py"
Cohesion: 0.14
Nodes (22): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+14 more)

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (29): name, private, scripts, build, dev, lint, preview, type (+21 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+16 more)

### Community 19 - "test_jobs.py"
Cohesion: 0.09
Nodes (32): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+24 more)

### Community 20 - "matching/service.py"
Cohesion: 0.14
Nodes (15): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+7 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.13
Nodes (14): 13. Strategic Options Analysis & Recommendation, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.3 Bounded Review Loop & Recursion Limit (+6 more)

### Community 22 - "main.py"
Cohesion: 0.11
Nodes (20): create_app(), lifespan(), Create and configure FastAPI application., api_test_db(), client(), fixture, Session, TestClient (+12 more)

### Community 23 - "Account"
Cohesion: 0.11
Nodes (33): create_access_token(), Generate a cryptographically signed JWT access token. Contains subject…, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, auth_client(), auth_test_db() (+25 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "Base"
Cohesion: 0.04
Nodes (62): alembic, Base, Base SQLAlchemy declarative model., downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade() (+54 more)

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
Cohesion: 0.07
Nodes (29): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient (+21 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "Job"
Cohesion: 0.12
Nodes (33): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str (+25 more)

### Community 32 - "api/agent.py"
Cohesion: 0.09
Nodes (44): approve_proposal(), cancel_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete (+36 more)

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

### Community 44 - "admin.py"
Cohesion: 0.13
Nodes (44): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+36 more)

### Community 45 - "account.py"
Cohesion: 0.12
Nodes (32): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+24 more)

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
Cohesion: 0.13
Nodes (12): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+4 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.07
Nodes (24): Ensure the caller has superadmin role privileges., require_superadmin(), Any, Alias for role to maintain consistency across frontend and APIs., 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make) (+16 more)

### Community 60 - "detective.py"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "latexCompiler.js"
Cohesion: 0.17
Nodes (24): ApplicationStudio(), SavedResumesTab(), ProfileView(), ResumeBuilderView(), TEMPLATES, StudioApprovalGate(), downloadLatexSource(), downloadPdfDocument() (+16 more)

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
Cohesion: 0.16
Nodes (11): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Mid-hold cancel during undo countdown window. Reverts application to 'draft',… (+3 more)

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

### Community 81 - "logging"
Cohesion: 0.16
Nodes (15): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+7 more)

### Community 82 - "test_matching.py"
Cohesion: 0.13
Nodes (15): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., Verify cosine similarity calculation edge cases and bounds. (+7 more)

### Community 83 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.14
Nodes (13): db_session(), asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs…, In-memory SQLite session for testing matching., Test OpenAIEmbeddingClient with mocked httpx response. (+5 more)

### Community 84 - "test_agent.py"
Cohesion: 0.11
Nodes (26): BaseModel, StageProposalInput, BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client() (+18 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "run_phase1_acceleration.py"
Cohesion: 0.10
Nodes (19): asyncio, decimal, pathlib, check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor(), export_database(), json_serializer() (+11 more)

### Community 90 - "react"
Cohesion: 0.11
Nodes (20): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+12 more)

### Community 91 - "Development Context — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step

### Community 92 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models:…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 93 - "worker.py"
Cohesion: 0.09
Nodes (25): arq, arq_connections, embed_jobs_batch_task(), monitor_followups_task(), Any, Worker task to run Experience Reflector and update learning insights., Background worker task to compute vector embeddings and gate jobs., Cron / periodic worker task to identify applications awaiting response > 7… (+17 more)

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

### Community 98 - "QuotaService"
Cohesion: 0.13
Nodes (17): Any, datetime, Exception, Session, QuotaExceededException, QuotaService, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.… (+9 more)

### Community 99 - "UserProfile"
Cohesion: 0.14
Nodes (23): list_designations(), list_languages(), list_locations(), Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), CompensationExpectation, Core profile for a user (one-to-one with Account). Stores identity, narrative,… (+15 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "os"
Cohesion: 0.21
Nodes (8): csv, json, os, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables…, Restore Data to Local PostgreSQL — Job Application Agent SaaS Restores a JSON…, sqlalchemy_ext_asyncio

### Community 102 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 103 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 104 - "ApplicationBase"
Cohesion: 0.25
Nodes (8): ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate, BaseModel

### Community 105 - "StarStory"
Cohesion: 0.14
Nodes (28): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+20 more)

### Community 109 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 110 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 112 - "models/__init__.py"
Cohesion: 0.09
Nodes (52): add_location(), add_work_experience(), OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, BaseModel, CertificationBase, CertificationCreate (+44 more)

### Community 113 - "gateway.py"
Cohesion: 0.07
Nodes (55): backend/app/services/dispatch/gateway.py SendGateway: Operational Outbound…, GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, GoogleIntegrationService (+47 more)

### Community 114 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 115 - "conftest.py"
Cohesion: 0.36
Nodes (7): assert_safe_test_database_url(), fixture, Enforces local development and test boundary per Advisor Review 9. Blocks test…, Verify database safety before running any tests., Provides a transactional database session against the safe local test database., test_db_session(), verify_test_db_safety()

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 118 - "test_interview.py"
Cohesion: 0.14
Nodes (19): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, Test filtering STAR stories by tag and verified_only flag. (+11 more)

### Community 119 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 120 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 121 - "test_models.py"
Cohesion: 0.08
Nodes (36): ApplicationCreate, AccountCvVersion, AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateCreate, CvTemplateUpdate (+28 more)

### Community 122 - "Application"
Cohesion: 0.10
Nodes (34): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, ApplicationPdfPayload, Stores compiled PDF byte payloads outside applications table to prevent bloat., AccountUsageCounter, QuotaReservation, Live aggregated balances per billing period. Updated transactionally with…, Multi-dimensional atomic reservation lifecycle (reserved -> settled | released… (+26 more)

### Community 123 - "8. Persistence, Checkpointers & Hold-Queue Architecture"
Cohesion: 0.50
Nodes (4): 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 124 - "test_profile_resumes.py"
Cohesion: 0.13
Nodes (24): Structured work experience entity for candidates across all industries.…, Saved candidate resume/CV documents (uploaded PDFs or built via LaTeX Resume…, UserResume, WorkExperience, ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, api_test_db(), client() (+16 more)

### Community 125 - "client"
Cohesion: 0.15
Nodes (15): api_test_db(), client(), fixture, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application… (+7 more)

### Community 127 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 128 - ".reflect_for_account"
Cohesion: 0.40
Nodes (3): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…

### Community 129 - "JobBase"
Cohesion: 0.50
Nodes (4): JobBase, JobCreate, JobUpdate, BaseModel

### Community 130 - "Any"
Cohesion: 0.09
Nodes (26): compile_texlive(), download_user_resume(), get_current_user_profile(), get_user_resume(), list_user_resumes(), parse_cv_file(), preview_cv(), Any (+18 more)

### Community 131 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 132 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

### Community 133 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

### Community 135 - "7. Gmail Integration Architecture (Scope Correction)"
Cohesion: 0.67
Nodes (3): 7.1 Scope Classification & CASA Exemption, 7.2 Integration Strategy, 7. Gmail Integration Architecture (Scope Correction)

### Community 136 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

### Community 137 - "9. Redesigned SSE Protocol Adapter & UI Integration"
Cohesion: 0.67
Nodes (3): 9.1 Custom Streaming Loop (Part Objects in Version "v2"), 9.2 Resume Endpoint & Minimal Frontend Contract, 9. Redesigned SSE Protocol Adapter & UI Integration

### Community 138 - "4. QuotaService Interface, Settle Branching & Counter Mutation"
Cohesion: 0.67
Nodes (3): 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting, 4. QuotaService Interface, Settle Branching & Counter Mutation

## Knowledge Gaps
- **264 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+259 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1028 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `Any`, `tailor_service.py`, `get_me`, `test_profile.py`, `llm_provider.py`, `api/profile.py`, `SendGateway`, `JobPosting`, `job.py`, `applications.py`, `config.py`, `test_jobs.py`, `main.py`, `Base`, `integrations.py`, `Job`, `api/agent.py`, `test_admin.py`, `admin.py`, `account.py`, `test_cv_tailor_service_with_structured_profile`, `Architecture — Job Application Agent SaaS`, `LLMService`, `jobs.py`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `worker.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `UserProfile`, `StarStory`, `models/__init__.py`, `gateway.py`, `test_interview.py`, `test_models.py`, `Application`, `test_profile_resumes.py`, `client`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `SendGateway`, `job.py`, `applications.py`, `session.py`, `test_jobs.py`, `matching/service.py`, `Base`, `MatchingService`, `test_admin.py`, `admin.py`, `account.py`, `test_cv_tailor_service_with_structured_profile`, `Architecture — Job Application Agent SaaS`, `detective.py`, `AgentEngine`, `LLMService`, `jobs.py`, `logging`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `worker.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `UserProfile`, `StarStory`, `models/__init__.py`, `gateway.py`, `test_models.py`, `Application`, `client`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `Base` connect `Base` to `tailor_service.py`, `JobPosting`, `test_profile.py`, `llm_provider.py`, `api/profile.py`, `SendGateway`, `job.py`, `session.py`, `test_jobs.py`, `main.py`, `Account`, `integrations.py`, `Job`, `api/agent.py`, `test_admin.py`, `admin.py`, `account.py`, `lucide-react`, `LLMService`, `logging`, `test_matching.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `worker.py`, `UserProfile`, `StarStory`, `check_migrations.py`, `models/__init__.py`, `db_session`, `test_interview.py`, `test_models.py`, `Application`, `8. Persistence, Checkpointers & Hold-Queue Architecture`, `test_profile_resumes.py`, `client`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 129 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 129 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 32 INFERRED edges - model-reasoned connections that need verification._
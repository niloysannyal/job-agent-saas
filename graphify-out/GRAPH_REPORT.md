# Graph Report - job-agent-saas  (2026-11-14)

## Corpus Check
- 290 files · ~214,389 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2972 nodes · 8394 edges · 145 communities (127 shown, 18 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1180 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3a90f1e9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- LatexLogParser
- Account
- FormDetectiveService
- api/profile.py
- Job
- GreenhouseJobSource
- Base
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- crypto.py
- logging
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- QuotaExceededException
- JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan
- test_apply_graph.py
- job.py
- What You Must Do When Invoked
- typing
- GoogleIntegrationService
- MatchingService
- test_matching.py
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
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- TenantScopedAsyncPostgresSaver
- Project: Job Application Agent SaaS
- fit_analyzer.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- generator.py
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
- FastAPI Backend Development Standards (adapted from ECC)
- React Frontend Development Standards (adapted from ECC)
- event_bus.py
- embedding.py
- UsageEvent
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- run_live_dogfooding_tests.py
- ProfileView.jsx
- MockQdrantClient
- client
- dispatch_service.py
- Product Development Environment Guide — Job Application Agent SaaS
- tools.py
- Roadmap — Job Application Agent SaaS
- google_service.py
- TargetDesignation
- ResumeBuilderView.jsx
- JobsView.jsx
- .ensure_counter_exists
- JobSearchQuery
- test_matching_service_score_and_gate_clean_jobs
- test_bookmarklet_generation_with_job_and_star_answers
- session.py
- deploy.sh
- cv_parser.py
- llm/service.py
- SendGateway
- TestClient
- bug-workflow.md
- models/__init__.py
- test_google_dispatch.py
- UserProfileRead
- apply_graph.py
- theme.js
- state.py
- check_migrations.py
- Session
- LLMService
- test_pydantic_schemas
- test_monitor_followups_task
- MockEmbeddingClient
- parse_redis_settings
- AgentToolRegistry
- test_llm_provider_config_model
- TeXLiveCompilerService
- UserProfile
- Security & Tenancy Policy (adapted from ECC AgentShield)
- JobEazy: Milestone M1m Implementation Specification
- .setup
- env.py
- devDependencies
- tasks.py
- test_profile_compile_texlive.py
- get_available_sources
- 6. Autonomy Policy Engine & Guardrails
- pathlib
- .generate
- matching/service.py
- 13. Strategic Options Analysis & Recommendation
- .generate
- 12. Dependency Plan & Environment Strategy
- 1. Executive Summary & Scope

## God Nodes (most connected - your core abstractions)
1. `Account` - 233 edges
2. `Job` - 124 edges
3. `Base` - 105 edges
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
- `3.1 Model 1: `AccountSubscription` (Anchored Billing Periods)` --references--> `AccountSubscription`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances)` --references--> `AccountUsageCounter`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py
- `3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle)` --references--> `QuotaReservation`  [INFERRED]
  docs/plans/m1m-metering-quotas-spec.md → backend/app/models/metering.py

## Import Cycles
- None detected.

## Communities (145 total, 18 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.08
Nodes (37): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+29 more)

### Community 3 - "JobPosting"
Cohesion: 0.09
Nodes (39): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+31 more)

### Community 5 - "Account"
Cohesion: 0.04
Nodes (74): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, e2e_account_and_job(), fixture, Seed real Account, Job, AccountDispatchSettings, and TrustedRecipient in test…, Session (+66 more)

### Community 6 - "FormDetectiveService"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 7 - "api/profile.py"
Cohesion: 0.10
Nodes (63): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+55 more)

### Community 8 - "Job"
Cohesion: 0.07
Nodes (37): AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, BaseModel, TailorCVInput, CVTailorService, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.… (+29 more)

### Community 9 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 10 - "Base"
Cohesion: 0.08
Nodes (58): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.… (+50 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.16
Nodes (26): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, DraftEmailRequest, DraftEmailResponse, evaluate_job_fit(), FitDimension (+18 more)

### Community 14 - "crypto.py"
Cohesion: 0.11
Nodes (30): argparse, decrypt_oauth_token(), decrypt_secret(), _derive_legacy_key(), encrypt_oauth_token(), _get_legacy_fernet(), get_oauth_fernet(), Decrypt an encrypted secret at rest. Gracefully falls back between legacy… (+22 more)

### Community 15 - "logging"
Cohesion: 0.15
Nodes (22): CandidateCareerContext, CVDrafterService, CVDraftInput, CVDraftOutput, prune_and_budget_latex(), BaseModel, backend/app/services/cv_tailor/drafter.py Decoupled Senior Recruiter Drafter…, Executes Pass 1 (Senior Recruiter Drafter). Outputs tailored summary bullet,… (+14 more)

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+20 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "QuotaExceededException"
Cohesion: 0.15
Nodes (13): cancel_application_send(), draft_follow_up(), FollowUpDraftResponse, mark_application_sent(), mark_follow_up_sent(), post, Supervised Send Gate with Undo Window: Transitions application from 'draft' to…, Candidate Undo/Cancel Gate: Cancels an application currently in the undo… (+5 more)

### Community 21 - "JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan"
Cohesion: 0.12
Nodes (17): CopilotState, 15. Decision Register, 16. Document Changelog, 3. Decision D1 Resolution Text (for `docs/ARCHITECTURE.md §3`), 4.1 System Topology Diagram, 4. Target Architecture: Split Graphs & Topology, 5.1 Decoupled Graph States (`CopilotState` vs `ApplyState`), 5.3 Bounded Review Loop & Recursion Limit (+9 more)

### Community 22 - "test_apply_graph.py"
Cohesion: 0.08
Nodes (34): CVReviewOutput, BaseModel, mock_llm_responses(), asyncio, fixture, backend/tests/agent/test_apply_graph.py Unit tests for Modular LangGraph…, Verifies resuming an interrupted graph with Command(resume=approve) runs…, Verifies resuming an interrupted graph with Command(resume=reject) terminates… (+26 more)

### Community 23 - "job.py"
Cohesion: 0.14
Nodes (26): JobBase, JobCreate, _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:… (+18 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.05
Nodes (23): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+15 more)

### Community 26 - "GoogleIntegrationService"
Cohesion: 0.09
Nodes (28): create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_google_auth_url(), get_google_status(), google_oauth_callback(), GoogleAuthUrlResponse (+20 more)

### Community 27 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 28 - "test_matching.py"
Cohesion: 0.15
Nodes (13): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., Verify cosine similarity calculation edge cases and bounds., Test get_embedding_client factory switches between Mock and OpenAI based on key., test_compute_cosine_similarity() (+5 more)

### Community 29 - "Application"
Cohesion: 0.18
Nodes (14): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, create_approval_fixture(), asyncio, Session, TestClient, Verify Candidate Undo Window: When a user cancels within the 30s countdown: 1.…, Verify cancel is rejected if dispatch has already been claimed or is sending. (+6 more)

### Community 30 - "config.py"
Cohesion: 0.22
Nodes (6): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings, pydantic_settings

### Community 31 - "engine.py"
Cohesion: 0.19
Nodes (24): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+16 more)

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
Cohesion: 0.11
Nodes (25): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+17 more)

### Community 40 - "JobEazy: Milestone M1 & M1b Implementation Specification"
Cohesion: 0.06
Nodes (34): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Sub-Milestones, 1. Executive Summary & Architecture Scope, 2.1 Table Definitions (SQLAlchemy 2.0 Declarative), 2.2 Cap-Count Queries, 2.3 Application and Entitlement Model Modifications, 2. Database Schema (All Tables Tenant-Scoped) (+26 more)

### Community 41 - "drafter_service.py"
Cohesion: 0.23
Nodes (11): FormAnswerPair, OutreachChannelType, OutreachDrafterInput, OutreachDrafterOutput, OutreachDrafterService, Any, BaseModel, Enum (+3 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.12
Nodes (47): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+39 more)

### Community 45 - "test_auth.py"
Cohesion: 0.06
Nodes (60): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+52 more)

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

### Community 53 - "fit_analyzer.py"
Cohesion: 0.23
Nodes (9): DimensionDiagnostic, FitAnalyzerInput, FitAnalyzerOutput, FitAnalyzerService, BaseModel, Session, backend/app/services/matching/fit_analyzer.py Standalone 4-Dimension Diagnostic…, Decoupled diagnostic fit analysis engine for candidate-job matching. (+1 more)

### Community 55 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.05
Nodes (44): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, post, Generate tailored interview prep questions for a specific role or job posting,…, check_job_liveness() (+36 more)

### Community 60 - "generator.py"
Cohesion: 0.23
Nodes (10): FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field., Full questionnaire result containing all tailored field answers., Harness² Recursive Form Q&A Generator. Applies Task-Level Recursion (Propose ->… (+2 more)

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
Cohesion: 0.17
Nodes (10): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated…, Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Mid-hold cancel during undo countdown window. Reverts application to 'draft',… (+2 more)

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

### Community 79 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.20
Nodes (10): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), LLMProviderBase, LLMProviderCreate (+2 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "event_bus.py"
Cohesion: 0.22
Nodes (10): Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent, BaseModel (+2 more)

### Community 82 - "embedding.py"
Cohesion: 0.14
Nodes (12): EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation., Generate embedding vector for a single text string., Generate embeddings for a list of text strings. (+4 more)

### Community 83 - "UsageEvent"
Cohesion: 0.20
Nodes (10): Append-only usage ledger. scope separates tenant usage from platform background…, UsageEvent, ModelPricing, Platform-wide model pricing catalog tracking input/output costs per 1M tokens…, 3.1 Model 1: `AccountSubscription` (Anchored Billing Periods), 3.2 Model 2: `AccountUsageCounter` (BigInteger Aggregated Balances), 3.3 Model 3: `QuotaReservation` (Multi-Dimensional Lifecycle), 3.4 Model 4: `ModelPricing` (In `backend/app/models/model_pricing.py`) (+2 more)

### Community 84 - "test_agent.py"
Cohesion: 0.09
Nodes (30): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput (+22 more)

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
Cohesion: 0.12
Nodes (21): app_services_agent_workflows_apply_graph, app_services_dispatch_gateway, asyncio, decimal, os, backup_data(), json_serializer(), Backup Supabase Data — Job Application Agent SaaS Extracts all public tables… (+13 more)

### Community 90 - "ProfileView.jsx"
Cohesion: 0.12
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 93 - "dispatch_service.py"
Cohesion: 0.14
Nodes (18): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+10 more)

### Community 94 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.18
Nodes (10): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), 5. Non-Negotiables, Diagnose Environment Health, Install Automated Git Pre-Commit Hook (+2 more)

### Community 95 - "tools.py"
Cohesion: 0.12
Nodes (28): analyze_fit_endpoint(), AnalyzeFitRequest, detect_method_endpoint(), DetectMethodRequest, draft_cv_endpoint(), draft_outreach_endpoint(), DraftCVRequest, DraftOutreachRequest (+20 more)

### Community 96 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 97 - "google_service.py"
Cohesion: 0.10
Nodes (27): InvalidEmailRecipientException, InvalidPdfPayloadException, MessageSizeExceededException, MimeBuilder, MimeBuilderException, Exception, backend/app/services/integrations/mime_builder.py RFC 2822 & RFC 2046 Compliant…, Encode raw MIME bytes to base64url string required by the Gmail API. (+19 more)

### Community 98 - "TargetDesignation"
Cohesion: 0.24
Nodes (11): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+3 more)

### Community 99 - "ResumeBuilderView.jsx"
Cohesion: 0.20
Nodes (11): ProfileTemplatesTab(), TEMPLATES, CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor() (+3 more)

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - ".ensure_counter_exists"
Cohesion: 0.21
Nodes (9): Any, datetime, Session, Resolves effective quota limit using precedence hierarchy: 1.…, Atomically reserves multi-dimensional quota within a database transaction.…, Atomically transitions reservation to 'settled', updates permanent usage…, Rolls back an unconsumed reservation: decrements reserved counters and marks…, Determines the current billing period boundaries: Anchors on active… (+1 more)

### Community 102 - "JobSearchQuery"
Cohesion: 0.07
Nodes (31): JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date() (+23 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.11
Nodes (18): db_session(), asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']., Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+10 more)

### Community 104 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.18
Nodes (12): client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, Verify code exchange, DB persistence with encryption, status check, and… (+4 more)

### Community 105 - "session.py"
Cohesion: 0.07
Nodes (49): BookmarkletResponse, get_autofill_bookmarklet(), Generate an intelligent JavaScript bookmarklet code tailored to the current…, create_story(), delete_story(), get_story(), list_stories(), list_tags() (+41 more)

### Community 107 - "cv_parser.py"
Cohesion: 0.08
Nodes (21): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, CVParserService, Any (+13 more)

### Community 108 - "llm/service.py"
Cohesion: 0.20
Nodes (10): AnthropicProvider, Any, Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet /…, LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, GeminiProvider, Any (+2 more)

### Community 109 - "SendGateway"
Cohesion: 0.05
Nodes (94): AccountDispatchSettings, ApplicationPdfPayload, DispatchedAction, HoldQueueItem, Immutable authority-to-attempt minted by UI clicks, verified chat intent, or…, Tenant-scoped dispatch settings, safety caps, and kill switches. Users can…, Content-pinned authorization. Binds exact recipient, content hash, tracking id,…, Stores compiled PDF byte payloads outside applications table to prevent bloat. (+86 more)

### Community 110 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test POST /api/v1/tools/detect-method discovers email application., Test POST /api/v1/tools/draft-cv produces tailored LaTeX without mutation., Test POST /api/v1/tools/review-cv audits fact integrity and ATS score., Test POST /api/v1/tools/draft-outreach synthesizes tailored copy., Test POST /api/v1/tools/apply-workflow/start emits SSE stream with thoughts and…, Test POST /api/v1/tools/analyze-fit returns 4-dimension diagnostic., test_tools_analyze_fit_endpoint() (+5 more)

### Community 112 - "models/__init__.py"
Cohesion: 0.11
Nodes (45): set_compensation(), OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, BaseModel, CertificationBase, CertificationCreate, CertificationRead (+37 more)

### Community 113 - "test_google_dispatch.py"
Cohesion: 0.15
Nodes (22): GmailApiException, GmailApiNotConfiguredException, GmailInsufficientPermissionsException, GmailNetworkTimeoutException, GmailRateLimitException, GmailServerErrorException, Exception, Send an outbound email message via official Gmail API messages.send. Args:… (+14 more)

### Community 114 - "UserProfileRead"
Cohesion: 0.50
Nodes (5): create_profile(), Create a user profile for an account (one per account)., UserProfileBase, UserProfileCreate, UserProfileRead

### Community 115 - "apply_graph.py"
Cohesion: 0.11
Nodes (39): Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), TOFU Exact-Address allowlist. Email uniqueness is enforced case-insensitively…, TrustedRecipient, assemble_package_node(), autonomy_gate_edge(), build_apply_graph() (+31 more)

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "state.py"
Cohesion: 0.11
Nodes (25): dump_model(), format_sse_frame(), get_field(), LangGraphSSEAdapter, Any, backend/app/services/agent/workflows/sse_adapter.py LangGraph to Server-Sent…, Formats a Python dictionary as a standard SSE data line., Serializes Pydantic models cleanly using model_dump() or dict(). (+17 more)

### Community 118 - "check_migrations.py"
Cohesion: 0.32
Nodes (7): 11.1 Test Suite Specifications (`backend/tests/agent/`), 11.2 Verification Loop Integration (`scripts/verify.py`), 11. Test Plan & Verification Gate Integration, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 119 - "Session"
Cohesion: 0.15
Nodes (13): get_llm_service(), get_monitor_summary(), list_applications(), get, patch, Session, Dependency provider for LLMService., Module 3 (Monitor): Aggregated status summary view across all pipeline stages.… (+5 more)

### Community 120 - "LLMService"
Cohesion: 0.10
Nodes (13): Session, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, client() (+5 more)

### Community 121 - "test_pydantic_schemas"
Cohesion: 0.08
Nodes (26): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate (+18 more)

### Community 122 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 123 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 124 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 125 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 130 - "TeXLiveCompilerService"
Cohesion: 0.09
Nodes (26): compile_texlive(), build_sandboxed_tex_env(), ensure_latex_preamble_macros(), Any, TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, Detect available Docker container with pdflatex., Return True if a TeX compiler is installed and executable locally or in Docker., Compile LaTeX source into PDF inside a Docker worker container with TeX Live… (+18 more)

### Community 131 - "UserProfile"
Cohesion: 0.09
Nodes (30): get_compensation(), get_current_user_profile(), get_experience_insights(), get_profile(), list_designations(), list_languages(), list_locations(), preview_cv() (+22 more)

### Community 132 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 133 - "JobEazy: Milestone M1m Implementation Specification"
Cohesion: 0.14
Nodes (13): 1.1 Goal, 1.2 Frozen Canonical Vocabulary, 1.3 Phased Delivery (M1m-a vs M1m-b), 1. Executive Summary & Phased Delivery Scope, 2.2 Tenancy Exemption in `scripts/check_migrations.py`, 2. Reuse of Existing Subscription Schema & Tenancy Audits, 4.1 Interface Specification, 4.2 Thresholds & Batch Budgeting (+5 more)

### Community 136 - ".setup"
Cohesion: 0.29
Nodes (7): Run underlying setup and enforce Row Level Security on checkpointer tables in…, 14. Milestone Roadmap & Effort Estimates, 8.1 Hold Queue: PostgreSQL DB Outbox vs Arq/Redis Comparison, 8.2 Supabase Connection Pooler Setup, 8.3 Checkpoint Encryption & Lifecycle Retention, 8.4 Multi-Tenant Boundary: Checkpoint Tables vs `thread_accounts`, 8. Persistence, Checkpointers & Hold-Queue Architecture

### Community 138 - "env.py"
Cohesion: 0.09
Nodes (26): assert_safe_database_url(), get_database_url(), include_object(), Enforces local development boundary per Advisor Review 9. Blocks remote host…, Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online() (+18 more)

### Community 140 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 141 - "tasks.py"
Cohesion: 0.16
Nodes (16): arq, arq_connections, embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task(), Any, Worker task to run Experience Reflector and update learning insights., Background worker task to fetch fresh job postings from enabled sources,… (+8 more)

### Community 144 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH or Docker, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 147 - "get_available_sources"
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 149 - "6. Autonomy Policy Engine & Guardrails"
Cohesion: 0.50
Nodes (4): 6.1 Database-Backed Authorization Model & Content Pinning [SUPERSEDED], 6.2 Trust-On-First-Use (TOFU) Recipient Validation & Public-Mail Block [SUPERSEDED], 6.3 Resilient SendGateway & Idempotency Key, 6. Autonomy Policy Engine & Guardrails

### Community 150 - "pathlib"
Cohesion: 0.20
Nodes (6): pathlib, check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor(), Git Pre-Commit Hook Installer — Job Application Agent SaaS Adapted from ECC's…, Automated Code Quality & Hygiene Reviewer — Job Application Agent SaaS Adapted…

### Community 151 - ".generate"
Cohesion: 0.15
Nodes (10): Any, Execute generation across the provider chain with automatic fallback., Return execution metadata from the last successful LLM call for…, Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 10. Observability & Cost Controls (+2 more)

### Community 152 - "matching/service.py"
Cohesion: 0.22
Nodes (7): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., MatchingResult, Summary of a match scoring run., qdrant_client_models

### Community 154 - "13. Strategic Options Analysis & Recommendation"
Cohesion: 0.50
Nodes (4): 13. Strategic Options Analysis & Recommendation, Lead Architect Recommendation, Option A: The Full LangGraph Migration Plan (M1 → M0 → M2-M6), Option B: Real Dispatch (M1) + Legacy Engine Autonomy Policy + Delayed Port Decision

### Community 157 - "12. Dependency Plan & Environment Strategy"
Cohesion: 0.67
Nodes (3): 12.1 Lockfile Strategy in Milestone M0, 12.2 Known Baseline Constraints (Retrieved 2026-11-10), 12. Dependency Plan & Environment Strategy

### Community 162 - "1. Executive Summary & Scope"
Cohesion: 0.67
Nodes (3): 1.1 Decision D1 Resolution & Architectural Intent, 1.2 Go / No-Go Verdict: What NOT to Move to LangGraph, 1. Executive Summary & Scope

## Knowledge Gaps
- **260 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1150 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `UserProfile`, `JobPosting`, `api/profile.py`, `Job`, `Base`, `applications.py`, `tasks.py`, `crypto.py`, `TestClient`, `test_apply_graph.py`, `job.py`, `GoogleIntegrationService`, `test_matching.py`, `Application`, `api/agent.py`, `test_admin.py`, `admin.py`, `test_auth.py`, `Architecture — Job Application Agent SaaS`, `test_agent.py`, `run_live_dogfooding_tests.py`, `client`, `tools.py`, `TargetDesignation`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `session.py`, `cv_parser.py`, `SendGateway`, `models/__init__.py`, `test_google_dispatch.py`, `apply_graph.py`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `UserProfile`, `Account`, `Base`, `applications.py`, `tasks.py`, `LeverJobSource`, `TestClient`, `QuotaExceededException`, `test_apply_graph.py`, `job.py`, `matching/service.py`, `MatchingService`, `test_matching.py`, `Application`, `engine.py`, `test_admin.py`, `admin.py`, `fit_analyzer.py`, `Architecture — Job Application Agent SaaS`, `AgentEngine`, `test_agent.py`, `run_live_dogfooding_tests.py`, `tools.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_bookmarklet_generation_with_job_and_star_answers`, `session.py`, `SendGateway`, `TestClient`, `models/__init__.py`, `state.py`, `test_monitor_followups_task`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `2. Current State Map (Codebase Ground Truth)` connect `lucide-react` to `tailor_service.py`, `AgentEngine`, `UserProfile`, `Base`, `SendGateway`, `logging`, `JobEazy: LangGraph Migration & Per-Account Autonomy Architecture Plan`, `check_migrations.py`, `LLMService`, `GoogleIntegrationService`, `MatchingService`, `engine.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 149 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 149 INFERRED edges - model-reasoned connections that need verification._
- **Are the 55 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 55 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Application` (e.g. with `get_platform_metrics()` and `list_tenants()`) actually correct?**
  _`Application` has 35 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - job-agent-saas  (2026-11-05)

## Corpus Check
- 230 files · ~145,586 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2105 nodes · 5673 edges · 127 communities (108 shown, 19 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 734 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dda73f55`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobIngestionService
- Job
- Account
- JobSourceHTTPError
- CVTemplateCompiler
- TestClient
- Session
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- run_phase1_acceleration.py
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- UserProfile
- matching/__init__.py
- react
- TestClient
- detective.py
- What You Must Do When Invoked
- alembic
- create_gmail_draft
- Architecture — Job Application Agent SaaS
- api/profile.py
- JobSearchQuery
- Settings
- test_agent.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- tenant_client
- tests/api/__init__.py
- JobPosting
- engine.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- logging
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- generate_interview_prep
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- CVTailorService
- EmailDispatchService
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- AgentEngine
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- env.py
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- test_seed_initial_data
- React Frontend Development Standards (adapted from ECC)
- MatchingService
- theme.js
- models/profile.py
- AgentToolRegistry
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- decrypt_secret
- get_available_sources
- test_matching.py
- session.py
- GoogleIntegrationService
- .generate
- Session
- models/__init__.py
- Product Development Environment Guide — Job Application Agent SaaS
- trigger_ingestion
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- matching/service.py
- _get_or_create_profile
- db_session
- WorkExperience
- dispatch_service.py
- deploy.sh
- test_interview.py
- typing
- LLMProviderConfig
- SpokenLanguage
- bug-workflow.md
- Application
- FastAPI Backend Development Standards (adapted from ECC)
- stage_proposal_tool.py
- api/interview.py
- plan_relevance_cuts
- Certification
- prune_and_budget_latex
- .generate
- db_session
- Education
- Project
- client
- compute_cosine_similarity
- .to_dict

## God Nodes (most connected - your core abstractions)
1. `Account` - 181 edges
2. `Job` - 93 edges
3. `JobPosting` - 74 edges
4. `Base` - 73 edges
5. `UserProfile` - 64 edges
6. `JobSearchQuery` - 62 edges
7. `Application` - 58 edges
8. `react` - 44 edges
9. `LLMService` - 41 edges
10. `StarStory` - 37 edges

## Surprising Connections (you probably didn't know these)
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `get_current_account()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py

## Import Cycles
- None detected.

## Communities (127 total, 19 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (18): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+10 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.12
Nodes (24): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+16 more)

### Community 3 - "JobIngestionService"
Cohesion: 0.10
Nodes (24): IngestionResult, JobIngestionService, Any, Session, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, db_session() (+16 more)

### Community 4 - "Job"
Cohesion: 0.14
Nodes (24): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_test_db(), TestClient, test_admin_templates_lifecycle(), test_flagged_jobs_dismiss_and_purge(), test_get_metrics(), test_job_sources_list() (+16 more)

### Community 5 - "Account"
Cohesion: 0.08
Nodes (32): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint() (+24 more)

### Community 6 - "JobSourceHTTPError"
Cohesion: 0.15
Nodes (24): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError (+16 more)

### Community 7 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 8 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 9 - "Session"
Cohesion: 0.22
Nodes (11): create_story(), delete_story(), get_story(), list_stories(), list_tags(), delete, get, post (+3 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (47): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+39 more)

### Community 14 - "run_phase1_acceleration.py"
Cohesion: 0.11
Nodes (18): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+10 more)

### Community 15 - "tasks.py"
Cohesion: 0.09
Nodes (30): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+22 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (31): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+23 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "UserProfile"
Cohesion: 0.24
Nodes (15): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+7 more)

### Community 20 - "matching/__init__.py"
Cohesion: 0.11
Nodes (15): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+7 more)

### Community 21 - "react"
Cohesion: 0.13
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 23 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.05
Nodes (18): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations. (+10 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.15
Nodes (19): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+11 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (19): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 1. Scope & rollout (+11 more)

### Community 28 - "api/profile.py"
Cohesion: 0.16
Nodes (29): delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill(), delete_work_experience() (+21 more)

### Community 29 - "JobSearchQuery"
Cohesion: 0.07
Nodes (29): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient (+21 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "test_agent.py"
Cohesion: 0.13
Nodes (32): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+24 more)

### Community 32 - "api/agent.py"
Cohesion: 0.12
Nodes (32): approve_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get (+24 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "tenant_client"
Cohesion: 0.36
Nodes (9): admin_client(), override_current_account(), override_get_db(), fixture, Session, regular_tenant_account(), superadmin_account(), tenant_client() (+1 more)

### Community 40 - "JobPosting"
Cohesion: 0.13
Nodes (17): Integration Checklist, Job Source Integrator, JobPosting, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, Test POST /api/v1/jobs/ingest triggers job sourcing, integrity guarding,…, test_trigger_ingestion_endpoint(), fetch() (+9 more)

### Community 41 - "engine.py"
Cohesion: 0.20
Nodes (13): asyncio, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, BaseModel, Decoupled in-memory asynchronous pub/sub Event Bus for domain events. Allows… (+5 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.12
Nodes (41): create_admin_template(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), dismiss_job_flag(), get_job_sources() (+33 more)

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
Cohesion: 0.21
Nodes (13): CareerCopilotView(), FAST_CHIPS, STARTER_PROMPTS, FunnelInsight(), JobRadarCarousel(), SendApprovalGate(), STARStoryMatch(), TailorDiffReview() (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "logging"
Cohesion: 0.12
Nodes (17): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser (+9 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - "generate_interview_prep"
Cohesion: 0.16
Nodes (11): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, Generate tailored interview prep questions for a specific role or job posting,…, Any, Alias for role to maintain consistency across frontend and APIs. (+3 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "CVTailorService"
Cohesion: 0.20
Nodes (10): CVTailorService, Session, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Selects the best fact-verified Summary variant based on role keywords or…, asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and… (+2 more)

### Community 60 - "EmailDispatchService"
Cohesion: 0.19
Nodes (13): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+5 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.19
Nodes (20): ApplicationStudio(), ProfileView(), StudioApprovalGate(), StudioDrafterWorkspace(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext() (+12 more)

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
Cohesion: 0.22
Nodes (7): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Fast-track common one-click prompt chips and unambiguous commands., Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Executes human-in-the-loop approval of an action proposal. Enforces tenant…, Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,…

### Community 70 - "env.py"
Cohesion: 0.28
Nodes (8): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), normalize_db_url(), Normalize database URL for driver compatibility., logging_config

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

### Community 79 - "test_seed_initial_data"
Cohesion: 0.11
Nodes (19): Session, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Verify that deleting an account cascades to all tenant-scoped rows., Test seed_initial_data populates default templates, plans, entitlements, and…, Test UserProfile and related models (designations, locations, compensation,…, Test StarStory model creation, tags, and account cascade. (+11 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "MatchingService"
Cohesion: 0.19
Nodes (9): MatchingResult, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Summary of a match scoring run., Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account. (+1 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "models/profile.py"
Cohesion: 0.16
Nodes (21): add_language(), set_compensation(), update_skill(), CertificationUpdate, CompensationBase, CompensationCreate, CompensationRead, EducationUpdate (+13 more)

### Community 84 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "decrypt_secret"
Cohesion: 0.12
Nodes (15): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), decrypt_secret(), encrypt_secret(), _get_fernet_instance() (+7 more)

### Community 90 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 91 - "test_matching.py"
Cohesion: 0.09
Nodes (24): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']. (+16 more)

### Community 92 - "session.py"
Cohesion: 0.07
Nodes (44): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, Session (+36 more)

### Community 93 - "GoogleIntegrationService"
Cohesion: 0.18
Nodes (9): get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+1 more)

### Community 94 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "Session"
Cohesion: 0.18
Nodes (11): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, Test SSE streaming response from /api/v1/agent/chat. (+3 more)

### Community 96 - "models/__init__.py"
Cohesion: 0.12
Nodes (25): create_profile(), Create a user profile for an account (one per account)., ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead (+17 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "trigger_ingestion"
Cohesion: 0.18
Nodes (13): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+5 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "matching/service.py"
Cohesion: 0.14
Nodes (11): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+3 more)

### Community 102 - "_get_or_create_profile"
Cohesion: 0.24
Nodes (13): add_location(), add_skill(), apply_parsed_cv(), bulk_skills(), _get_or_create_profile(), list_skills(), post, Ensure a UserProfile row exists for an account, auto-creating a clean default… (+5 more)

### Community 103 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 104 - "WorkExperience"
Cohesion: 0.18
Nodes (13): add_work_experience(), patch, Partial-update the user profile for an account (auto-creates if missing)., update_certification(), update_education(), update_profile(), update_project(), update_work_experience() (+5 more)

### Community 105 - "dispatch_service.py"
Cohesion: 0.22
Nodes (10): base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text, email_policy (+2 more)

### Community 107 - "test_interview.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 108 - "typing"
Cohesion: 0.12
Nodes (38): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), ApplicationCreate, AccountCvVersionCreate (+30 more)

### Community 109 - "LLMProviderConfig"
Cohesion: 0.30
Nodes (12): 4. Pydantic Schemas & Security, _build_provider_read(), create_llm_provider(), list_llm_providers(), reorder_llm_providers(), update_llm_provider(), LLMProviderBase, LLMProviderConfig (+4 more)

### Community 110 - "SpokenLanguage"
Cohesion: 0.20
Nodes (11): add_designation(), Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetDesignationBase, TargetDesignationCreate (+3 more)

### Community 112 - "Application"
Cohesion: 0.13
Nodes (15): Application, ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is… (+7 more)

### Community 113 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 114 - "stage_proposal_tool.py"
Cohesion: 0.36
Nodes (8): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ProposalCreatedEvent, BaseModel, StageApplicationProposalTool, StageProposalInput, Test human-in-the-loop Send gate: 1. Tool creates AgentActionProposal with…, test_stage_proposal_and_approval_flow()

### Community 115 - "api/interview.py"
Cohesion: 0.33
Nodes (8): patch, STAR Interview Coach API — CRUD for interview stories + tag-based querying. All…, update_story(), BaseModel, StarStoryBase, StarStoryCreate, StarStoryRead, StarStoryUpdate

### Community 116 - "plan_relevance_cuts"
Cohesion: 0.29
Nodes (7): extract_keywords_from_job(), plan_relevance_cuts(), any, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, Verify relevance scoring and trimming plan., test_relevance_scorer_and_cuts()

### Community 117 - "Certification"
Cohesion: 0.40
Nodes (6): add_certification(), Certification, CertificationBase, CertificationCreate, CertificationRead, Professional certifications, licenses, and credentials.

### Community 120 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

### Community 121 - "Education"
Cohesion: 0.40
Nodes (6): add_education(), Education, EducationBase, EducationCreate, EducationRead, Structured education background (degrees, high school, certifications,…

### Community 122 - "Project"
Cohesion: 0.40
Nodes (6): add_project(), Project, ProjectBase, ProjectCreate, ProjectRead, Portfolio projects, open-source work, or major professional deliverables.

### Community 123 - "client"
Cohesion: 0.40
Nodes (3): api_test_db(), client(), fixture

### Community 124 - "compute_cosine_similarity"
Cohesion: 0.50
Nodes (4): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Verify cosine similarity calculation edge cases and bounds., test_compute_cosine_similarity()

## Knowledge Gaps
- **197 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 803 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobIngestionService`, `Job`, `TestClient`, `applications.py`, `tasks.py`, `TestClient`, `create_gmail_draft`, `Architecture — Job Application Agent SaaS`, `api/profile.py`, `test_agent.py`, `api/agent.py`, `tenant_client`, `JobPosting`, `admin.py`, `test_auth.py`, `CVTailorService`, `test_seed_initial_data`, `models/profile.py`, `test_matching.py`, `session.py`, `GoogleIntegrationService`, `Session`, `models/__init__.py`, `trigger_ingestion`, `test_interview.py`, `typing`, `LLMProviderConfig`, `Application`, `stage_proposal_tool.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `models/__init__.py`, `run_posting_guard`, `JobIngestionService`, `JobSourceHTTPError`, `GreenhouseJobSource`, `FreehireJobSource`, `typing`, `RemoteOKJobSource`, `LeverJobSource`, `RemotiveJobSource`, `get_available_sources`, `session.py`, `JobSearchQuery`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobIngestionService`, `applications.py`, `tasks.py`, `UserProfile`, `TestClient`, `test_agent.py`, `JobPosting`, `engine.py`, `admin.py`, `logging`, `generate_interview_prep`, `CVTailorService`, `AgentEngine`, `test_seed_initial_data`, `MatchingService`, `test_matching.py`, `session.py`, `Session`, `models/__init__.py`, `trigger_ingestion`, `matching/service.py`, `typing`, `Application`, `stage_proposal_tool.py`, `api/interview.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 114 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 114 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
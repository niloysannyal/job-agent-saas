# Graph Report - job-agent-saas  (2026-11-04)

## Corpus Check
- 229 files · ~143,668 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2096 nodes · 5655 edges · 122 communities (104 shown, 18 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 730 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `da94068b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- Job
- Application
- Account
- job.py
- CVTemplateCompiler
- TestClient
- models/interview.py
- GreenhouseJobSource
- JobSearchQuery
- RemoteOKJobSource
- applications.py
- run_phase1_acceleration.py
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- UserProfile
- test_matching.py
- lucide-react
- TestClient
- detective.py
- What You Must Do When Invoked
- alembic
- integrations.py
- Architecture — Job Application Agent SaaS
- models/__init__.py
- JobSourceHTTPError
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- JobPosting
- event_bus.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- decrypt_secret
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- .role
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- test_cv_tailor_service_with_structured_profile
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
- session.py
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- typing
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- test_models.py
- React Frontend Development Standards (adapted from ECC)
- dispatch_service.py
- theme.js
- Session
- AgentToolRegistry
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- GoogleIntegrationService
- logging
- MockQdrantClient
- Base
- encrypt_secret
- .generate
- test_agent.py
- core/auth.py
- Product Development Environment Guide — Job Application Agent SaaS
- IngestionRequest
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- MatchingService
- api/auth.py
- db_session
- test_form_qa_api.py
- create_app
- deploy.sh
- get_monitor_summary
- FastAPI Backend Development Standards (adapted from ECC)
- AccountCvVersionBase
- 3257c49a645d_add_agent_action_proposals_.py
- bug-workflow.md
- test_bookmarklet_generation_with_job_and_star_answers
- a7c3e1f24b01_add_profile_and_interview_tables.py
- f82a17d49b21_add_universal_career_tables_and_job_dates.py
- update_application_status
- llm_provider.py
- list_jobs
- prune_and_budget_latex
- .generate
- db_session
- .__init__

## God Nodes (most connected - your core abstractions)
1. `Account` - 179 edges
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
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `4. Pydantic Schemas & Security` --references--> `LLMProviderRead`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/models/llm_provider.py

## Import Cycles
- None detected.

## Communities (122 total, 18 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.12
Nodes (16): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+8 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.09
Nodes (35): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+27 more)

### Community 3 - "Job"
Cohesion: 0.11
Nodes (33): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+25 more)

### Community 4 - "Application"
Cohesion: 0.14
Nodes (14): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+6 more)

### Community 5 - "Account"
Cohesion: 0.08
Nodes (32): dismiss_job_flag(), impersonate_tenant(), post, test_llm_provider(), toggle_job_source(), Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash. (+24 more)

### Community 6 - "job.py"
Cohesion: 0.10
Nodes (32): JobBase, JobCreate, JobUpdate, BaseModel, classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:… (+24 more)

### Community 7 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 8 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 9 - "models/interview.py"
Cohesion: 0.14
Nodes (26): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+18 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), GreenhouseJobSource, _do_fetch(), Any, AsyncClient, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.…, Asynchronously fetch all open job postings for a company from Greenhouse,…, Unescape Greenhouse's double-encoded HTML content field. The field is HTML-… (+20 more)

### Community 11 - "JobSearchQuery"
Cohesion: 0.09
Nodes (25): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., _clean_html(), FreehireJobSource, Any (+17 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.10
Nodes (23): _clean_html(), _format_salary(), Any, AsyncClient, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace., Format RemoteOK's numeric salary_min/salary_max into a display string., RemoteOK API implementation of the JobSource interface (ARCHITECTURE.md §4).… (+15 more)

### Community 13 - "applications.py"
Cohesion: 0.16
Nodes (26): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, DraftEmailRequest, DraftEmailResponse, evaluate_job_fit(), FitDimension (+18 more)

### Community 14 - "run_phase1_acceleration.py"
Cohesion: 0.10
Nodes (19): os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's… (+11 more)

### Community 15 - "tasks.py"
Cohesion: 0.10
Nodes (29): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+21 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (31): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+23 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.11
Nodes (19): _clean_html(), Any, AsyncClient, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Remotive API implementation of the JobSource interface (ARCHITECTURE.md §4).…, RemotiveJobSource, asyncio (+11 more)

### Community 19 - "UserProfile"
Cohesion: 0.21
Nodes (16): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+8 more)

### Community 20 - "test_matching.py"
Cohesion: 0.06
Nodes (40): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+32 more)

### Community 21 - "lucide-react"
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
Cohesion: 0.07
Nodes (10): alembic, downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade(), downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely. (+2 more)

### Community 26 - "integrations.py"
Cohesion: 0.18
Nodes (21): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+13 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.12
Nodes (16): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN), 4. Module 1 — Find Job Opportunity (decision made) (+8 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.06
Nodes (107): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+99 more)

### Community 29 - "JobSourceHTTPError"
Cohesion: 0.08
Nodes (35): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+27 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.19
Nodes (24): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+16 more)

### Community 32 - "api/agent.py"
Cohesion: 0.10
Nodes (34): approve_proposal(), chat_with_agent(), get_conversation(), list_action_proposals(), list_conversations(), get, post, Session (+26 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "JobPosting"
Cohesion: 0.10
Nodes (18): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace. (+10 more)

### Community 41 - "event_bus.py"
Cohesion: 0.16
Nodes (13): asyncio, Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent (+5 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.14
Nodes (40): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+32 more)

### Community 45 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "react"
Cohesion: 0.21
Nodes (13): CareerAgentDock(), QUICK_CHIPS, FunnelInsight(), JobRadarCarousel(), SendApprovalGate(), STARStoryMatch(), TailorDiffReview(), RenderWidget() (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "decrypt_secret"
Cohesion: 0.22
Nodes (8): decrypt_secret(), _get_fernet_instance(), Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Refresh an expired access token using the stored encrypted refresh token., Verify code exchange, DB persistence with encryption, status check, and…, test_google_callback_and_status(), Fernet

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 60 - "EmailDispatchService"
Cohesion: 0.21
Nodes (12): EmailDispatchService, EmailDraftProvider, EmailDraftResult, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on…, Generates a standard URL-encoded mailto: link for 1-click launch in default… (+4 more)

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
Nodes (8): AgentConversation, Conversation session between user and Career OS Agent., AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Fast-track common one-click prompt chips and unambiguous commands., Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,…

### Community 70 - "session.py"
Cohesion: 0.24
Nodes (12): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+4 more)

### Community 71 - "SaaS Review Checklist"
Cohesion: 0.22
Nodes (8): 1. Multi-Tenant Data Isolation (Critical), 2. Security & Credentials (Critical), 3. Async & Performance (High), 4. Human-in-the-Loop & Business Rules (Critical), 5. Frontend & UI/UX Standards (High), Code Review Context — Job Application Agent SaaS, Review Workflow, SaaS Review Checklist

### Community 72 - "Database Migrations Skill — Job Application Agent SaaS"
Cohesion: 0.50
Nodes (3): Core Rules, Database Migrations Skill — Job Application Agent SaaS, Verification

### Community 73 - "Hunt Targets"
Cohesion: 0.29
Nodes (6): 1. Bare `except:` or Empty Catch Blocks, 2. Dangerous Fallbacks in LLM & Ingestion, 3. Missing Transaction Rollbacks, 4. Frontend Unhandled Promise Rejections, Hunt Targets, Silent Failure Hunter Skill — Job Application Agent SaaS

### Community 74 - "typing"
Cohesion: 0.12
Nodes (20): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+12 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "test_models.py"
Cohesion: 0.07
Nodes (53): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountCreate, ApplicationCreate, CvTemplate, CvTemplateCreate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system… (+45 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "dispatch_service.py"
Cohesion: 0.20
Nodes (11): Enum, base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text (+3 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "Session"
Cohesion: 0.22
Nodes (11): draft_follow_up(), FollowUpDraftResponse, get_llm_service(), mark_application_sent(), mark_follow_up_sent(), post, Session, Dependency provider for LLMService. (+3 more)

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

### Community 88 - "GoogleIntegrationService"
Cohesion: 0.18
Nodes (9): get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+1 more)

### Community 90 - "logging"
Cohesion: 0.11
Nodes (21): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, ProfileParser (+13 more)

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "Base"
Cohesion: 0.14
Nodes (32): Base, Base SQLAlchemy declarative model., AccountBase, AccountRead, ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswer, ApplicationFormAnswerBase (+24 more)

### Community 93 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 94 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "test_agent.py"
Cohesion: 0.12
Nodes (24): BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput, account_a(), account_b() (+16 more)

### Community 96 - "core/auth.py"
Cohesion: 0.23
Nodes (11): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Ensure the caller has superadmin role privileges., Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+3 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "IngestionRequest"
Cohesion: 0.40
Nodes (5): IngestionRequest, IngestionResponse, BaseModel, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run.

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "MatchingService"
Cohesion: 0.09
Nodes (18): Session, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.… (+10 more)

### Community 102 - "api/auth.py"
Cohesion: 0.10
Nodes (34): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+26 more)

### Community 103 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 104 - "test_form_qa_api.py"
Cohesion: 0.33
Nodes (8): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 105 - "create_app"
Cohesion: 0.11
Nodes (17): create_app(), lifespan(), Create and configure FastAPI application., client(), fixture, account_a(), account_b(), client() (+9 more)

### Community 107 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

### Community 108 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 109 - "AccountCvVersionBase"
Cohesion: 0.33
Nodes (6): AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateUpdate, BaseModel

### Community 110 - "3257c49a645d_add_agent_action_proposals_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade()

### Community 112 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.20
Nodes (10): client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, test_bookmarklet_generation() (+2 more)

### Community 113 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 114 - "f82a17d49b21_add_universal_career_tables_and_job_dates.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade()

### Community 115 - "update_application_status"
Cohesion: 0.50
Nodes (4): patch, Module 3 (Monitor): Update application status across pipeline stages: draft ->…, StatusUpdateRequest, update_application_status()

### Community 116 - "llm_provider.py"
Cohesion: 0.53
Nodes (5): 4. Pydantic Schemas & Security, LLMProviderBase, LLMProviderCreate, LLMProviderUpdate, BaseModel

### Community 117 - "list_jobs"
Cohesion: 0.67
Nodes (3): list_jobs(), get, Fetch jobs for an account ordered by match_score descending. Excludes vetoed…

### Community 120 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables for testing models.

## Knowledge Gaps
- **195 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+190 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 796 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `Job`, `Application`, `job.py`, `TestClient`, `models/interview.py`, `applications.py`, `tasks.py`, `test_matching.py`, `TestClient`, `integrations.py`, `models/__init__.py`, `JobSourceHTTPError`, `api/agent.py`, `test_admin.py`, `admin.py`, `test_auth.py`, `decrypt_secret`, `test_cv_tailor_service_with_structured_profile`, `test_models.py`, `GoogleIntegrationService`, `logging`, `Base`, `test_agent.py`, `core/auth.py`, `api/auth.py`, `test_form_qa_api.py`, `create_app`, `test_bookmarklet_generation_with_job_and_star_answers`, `llm_provider.py`, `list_jobs`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `Job`, `job.py`, `GreenhouseJobSource`, `JobSearchQuery`, `RemoteOKJobSource`, `Base`, `test_models.py`, `LeverJobSource`, `RemotiveJobSource`, `models/__init__.py`, `JobSourceHTTPError`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `Application`, `Account`, `job.py`, `models/interview.py`, `applications.py`, `run_phase1_acceleration.py`, `tasks.py`, `UserProfile`, `test_matching.py`, `TestClient`, `models/__init__.py`, `JobSourceHTTPError`, `engine.py`, `api/agent.py`, `test_admin.py`, `admin.py`, `.role`, `test_cv_tailor_service_with_structured_profile`, `AgentEngine`, `test_models.py`, `Session`, `logging`, `Base`, `test_agent.py`, `MatchingService`, `test_bookmarklet_generation_with_job_and_star_answers`, `list_jobs`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 112 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
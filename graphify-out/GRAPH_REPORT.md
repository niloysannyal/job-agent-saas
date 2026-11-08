# Graph Report - job-agent-saas  (2026-11-08)

## Corpus Check
- 231 files · ~149,856 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2130 nodes · 5734 edges · 112 communities (96 shown, 16 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 744 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `efa67f2b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- Job
- test_application_status_update
- TestClient
- job.py
- test_auth.py
- TestClient
- detective.py
- JobPosting
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- sys
- test_workers.py
- package.json
- LeverJobSource
- RemotiveJobSource
- StarStory
- test_matching.py
- react
- TestClient
- api/interview.py
- What You Must Do When Invoked
- typing
- integrations.py
- application.py
- models/__init__.py
- JobSearchQuery
- Settings
- ToolExecutionContext
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- get_available_sources
- engine.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- account.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- tasks.py
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- Account
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- dispatch_service.py
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- AgentEngine
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- Application
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- llm/service.py
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- test_models.py
- React Frontend Development Standards (adapted from ECC)
- MatchingService
- theme.js
- MockLLMProvider
- BaseAgentTool
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- Security & Tenancy Policy (adapted from ECC AgentShield)
- .generate
- MockQdrantClient
- session.py
- create_gmail_draft
- LLMService
- test_agent.py
- .role
- Product Development Environment Guide — Job Application Agent SaaS
- subscription.py
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- LanguageGate
- test_profile.py
- JobBase
- get_me
- google_service.py
- deploy.sh
- .generate
- Base
- bug-workflow.md
- FastAPI Backend Development Standards (adapted from ECC)
- stage_proposal_tool.py

## God Nodes (most connected - your core abstractions)
1. `Account` - 186 edges
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
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `get_current_account()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py

## Import Cycles
- None detected.

## Communities (112 total, 16 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (18): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+10 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.06
Nodes (48): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+40 more)

### Community 3 - "Job"
Cohesion: 0.12
Nodes (31): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.… (+23 more)

### Community 4 - "test_application_status_update"
Cohesion: 0.23
Nodes (12): Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer., Test Module 2 (Apply) application tailoring and strict human-in-the-loop Send…, test_application_status_update() (+4 more)

### Community 5 - "TestClient"
Cohesion: 0.09
Nodes (23): TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations., GET and PUT on compensation expectations., CRUD operations on spoken languages., Verify complete isolation between tenants A and B for profile and related…, Test full CRUD cycle for work experiences. (+15 more)

### Community 6 - "job.py"
Cohesion: 0.14
Nodes (25): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceError (+17 more)

### Community 7 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

### Community 8 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 9 - "detective.py"
Cohesion: 0.19
Nodes (16): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+8 more)

### Community 10 - "JobPosting"
Cohesion: 0.06
Nodes (38): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, _clean_html(), GreenhouseJobSource, _do_fetch(), Any (+30 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.10
Nodes (41): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+33 more)

### Community 14 - "sys"
Cohesion: 0.11
Nodes (16): os, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor() (+8 more)

### Community 15 - "test_workers.py"
Cohesion: 0.09
Nodes (30): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+22 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (31): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+23 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "StarStory"
Cohesion: 0.23
Nodes (12): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field. (+4 more)

### Community 20 - "test_matching.py"
Cohesion: 0.06
Nodes (40): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+32 more)

### Community 21 - "react"
Cohesion: 0.13
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 23 - "api/interview.py"
Cohesion: 0.15
Nodes (24): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+16 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.05
Nodes (23): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+15 more)

### Community 26 - "integrations.py"
Cohesion: 0.18
Nodes (19): BookmarkletResponse, CreateGmailDraftRequest, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status(), google_oauth_callback(), GoogleAuthUrlResponse (+11 more)

### Community 27 - "application.py"
Cohesion: 0.36
Nodes (9): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate (+1 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.05
Nodes (128): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+120 more)

### Community 29 - "JobSearchQuery"
Cohesion: 0.07
Nodes (33): IngestionRequest, Payload for triggering a job ingestion run., JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date() (+25 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "ToolExecutionContext"
Cohesion: 0.13
Nodes (27): GenerativeUIWidget, ABC, BaseModel, Enum, str, Executes the autonomous tool action and returns structured data along with an…, ToolCategory, ToolExecutionContext (+19 more)

### Community 32 - "api/agent.py"
Cohesion: 0.06
Nodes (51): approve_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get (+43 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 41 - "engine.py"
Cohesion: 0.19
Nodes (14): asyncio, Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, BaseModel (+6 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.14
Nodes (40): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+32 more)

### Community 45 - "account.py"
Cohesion: 0.11
Nodes (37): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+29 more)

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

### Community 51 - "tasks.py"
Cohesion: 0.12
Nodes (18): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT… (+10 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 55 - "Account"
Cohesion: 0.14
Nodes (17): delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), delete, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash. (+9 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (19): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 1. Scope & rollout (+11 more)

### Community 60 - "dispatch_service.py"
Cohesion: 0.14
Nodes (19): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+11 more)

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
Cohesion: 0.17
Nodes (10): AgentConversation, Conversation session between user and Career OS Agent., AgentEngine, Any, Session, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands. (+2 more)

### Community 70 - "Application"
Cohesion: 0.15
Nodes (8): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…

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
Cohesion: 0.32
Nodes (6): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, OpenAIProvider, Any, OpenAI implementation of the LLMProvider interface. Uses httpx.AsyncClient for…

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "test_models.py"
Cohesion: 0.06
Nodes (49): 4. Pydantic Schemas & Security, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AccountCvVersion, AccountCvVersionBase, AccountCvVersionCreate (+41 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "MatchingService"
Cohesion: 0.12
Nodes (14): Session, ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., MatchingService (+6 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "MockLLMProvider"
Cohesion: 0.26
Nodes (8): MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, asyncio, test_llm_service_failover_chain(), test_llm_service_with_explicit_provider(), test_mock_llm_provider(), test_openai_provider_missing_key()

### Community 84 - "BaseAgentTool"
Cohesion: 0.23
Nodes (6): BaseAgentTool, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 90 - ".generate"
Cohesion: 0.18
Nodes (8): Any, Execute generation across the provider chain with automatic fallback., Resolve ordered list of active providers from database or defaults., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "session.py"
Cohesion: 0.09
Nodes (31): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, get_database_url() (+23 more)

### Community 93 - "create_gmail_draft"
Cohesion: 0.16
Nodes (10): create_gmail_draft(), CreateGmailDraftResponse, Create a Draft in the user's Gmail box. Non-negotiable: Human-in-the-loop on…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+2 more)

### Community 94 - "LLMService"
Cohesion: 0.20
Nodes (6): Session, LLMService, Session, LLM service router matching ARCHITECTURE.md §11 & AGENTS.md. Every model call…, client(), fixture

### Community 95 - "test_agent.py"
Cohesion: 0.12
Nodes (21): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, account_a(), account_b(), api_test_db(), client(), fixture, Session (+13 more)

### Community 96 - ".role"
Cohesion: 0.22
Nodes (5): Any, Alias for role to maintain consistency across frontend and APIs., 14. Decision log, field_validator, model_validator

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "subscription.py"
Cohesion: 0.39
Nodes (8): EntitlementBase, EntitlementRead, EntitlementUpdate, BaseModel, SubscriptionPlanBase, SubscriptionPlanCreate, SubscriptionPlanRead, SubscriptionPlanUpdate

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "LanguageGate"
Cohesion: 0.15
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 102 - "test_profile.py"
Cohesion: 0.43
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 103 - "JobBase"
Cohesion: 0.50
Nodes (4): JobBase, JobCreate, JobUpdate, BaseModel

### Community 104 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

### Community 105 - "google_service.py"
Cohesion: 0.19
Nodes (13): decrypt_secret(), encrypt_secret(), _get_fernet_instance(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Verify secrets are encrypted and decrypted accurately., test_crypto_encryption_roundtrip() (+5 more)

### Community 108 - "Base"
Cohesion: 0.09
Nodes (38): Base, Base SQLAlchemy declarative model., create_app(), Create and configure FastAPI application., ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, OAuthConnection, Multi-tenant OAuth Connection model. Stores authorized OAuth 2.0 access and… (+30 more)

### Community 113 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 114 - "stage_proposal_tool.py"
Cohesion: 0.36
Nodes (8): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ProposalCreatedEvent, BaseModel, StageApplicationProposalTool, StageProposalInput, Test human-in-the-loop Send gate: 1. Tool creates AgentActionProposal with…, test_stage_proposal_and_approval_flow()

## Knowledge Gaps
- **197 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 815 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `Job`, `test_application_status_update`, `TestClient`, `job.py`, `test_auth.py`, `TestClient`, `applications.py`, `test_workers.py`, `test_matching.py`, `TestClient`, `integrations.py`, `application.py`, `models/__init__.py`, `ToolExecutionContext`, `api/agent.py`, `test_admin.py`, `admin.py`, `account.py`, `tasks.py`, `Architecture — Job Application Agent SaaS`, `test_models.py`, `session.py`, `create_gmail_draft`, `test_agent.py`, `subscription.py`, `test_profile.py`, `get_me`, `Base`, `stage_proposal_tool.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `Job`, `job.py`, `JobBase`, `get_available_sources`, `FreehireJobSource`, `RemoteOKJobSource`, `Base`, `test_models.py`, `LeverJobSource`, `RemotiveJobSource`, `tasks.py`, `models/__init__.py`, `JobSearchQuery`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `test_application_status_update`, `job.py`, `detective.py`, `applications.py`, `test_workers.py`, `test_matching.py`, `TestClient`, `api/interview.py`, `application.py`, `models/__init__.py`, `ToolExecutionContext`, `api/agent.py`, `test_admin.py`, `engine.py`, `admin.py`, `account.py`, `tasks.py`, `Account`, `AgentEngine`, `test_models.py`, `MatchingService`, `session.py`, `test_agent.py`, `.role`, `Base`, `stage_proposal_tool.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
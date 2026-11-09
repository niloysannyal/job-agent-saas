# Graph Report - job-agent-saas  (2026-11-09)

## Corpus Check
- 236 files · ~156,503 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2204 nodes · 5873 edges · 126 communities (107 shown, 19 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 746 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `37e14758`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobPosting
- LatexLogParser
- TestClient
- dispatch_service.py
- models/__init__.py
- TestClient
- test_bookmarklet_generation_with_job_and_star_answers
- greenhouse.py
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- env.py
- worker.py
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- matching/__init__.py
- ProfileView.jsx
- Base
- StarStory
- What You Must Do When Invoked
- alembic
- create_gmail_draft
- test_pydantic_schemas
- api/profile.py
- JobSourceHTTPError
- config.py
- typing
- AgentConversation
- User Profile — Niloy Sannyal
- .oxlintrc.json
- tenant_client
- tests/api/__init__.py
- pytest
- api/agent.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- .reflect_for_account
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- resolve_tenant_id
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
- Application
- React Frontend Development Standards (adapted from ECC)
- list_jobs
- test_matching.py
- chat_with_agent
- Session
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- test_educations_skills_and_preview
- devDependencies
- MockQdrantClient
- Job
- UserProfile
- FastAPI Backend Development Standards (adapted from ECC)
- google_service.py
- JobSearchQuery
- Product Development Environment Guide — Job Application Agent SaaS
- test_generate_form_answers_api_endpoint
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- react
- GoogleIntegrationService
- test_matching_service_score_and_gate_clean_jobs
- .parse_from_db
- encrypt_secret
- deploy.sh
- .generate
- Account
- .score_and_gate_jobs
- Project
- bug-workflow.md
- SpokenLanguage
- get_current_account
- run_ats_text_layer_check
- MockEmbeddingClient
- UserProfileRead
- db_session
- Education
- WorkExperience
- json
- client
- test_profile_compile_texlive.py
- test_cv_tailor_service_with_structured_profile
- client
- prune_and_budget_latex

## God Nodes (most connected - your core abstractions)
1. `Account` - 186 edges
2. `Job` - 93 edges
3. `JobPosting` - 74 edges
4. `Base` - 73 edges
5. `UserProfile` - 64 edges
6. `JobSearchQuery` - 62 edges
7. `Application` - 58 edges
8. `react` - 46 edges
9. `LLMService` - 41 edges
10. `lucide-react` - 39 edges

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

## Communities (126 total, 19 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.10
Nodes (24): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LandingPageView(), LoginModal() (+16 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.11
Nodes (26): audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body(), Strips lines starting with %% (agent control notes) while preserving actual…, Escapes LaTeX special characters (% & $ # _) if they are not already escaped.… (+18 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (43): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Session (+35 more)

### Community 5 - "TestClient"
Cohesion: 0.10
Nodes (21): TestClient, PATCH /api/v1/profile updates fields partially., CRUD operations on target designations., CRUD operations on target locations., GET and PUT on compensation expectations., CRUD operations on spoken languages., Verify complete isolation between tenants A and B for profile and related…, Test full CRUD cycle for work experiences. (+13 more)

### Community 6 - "dispatch_service.py"
Cohesion: 0.18
Nodes (15): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+7 more)

### Community 7 - "models/__init__.py"
Cohesion: 0.11
Nodes (41): set_compensation(), AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateCreate, CvTemplateUpdate, BaseModel (+33 more)

### Community 8 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 9 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.16
Nodes (13): api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent… (+5 more)

### Community 10 - "greenhouse.py"
Cohesion: 0.07
Nodes (33): _clean_html(), _detect_location_type(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime (+25 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (25): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+17 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.05
Nodes (72): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+64 more)

### Community 14 - "env.py"
Cohesion: 0.06
Nodes (34): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_engine(), normalize_db_url(), Normalize database URL for driver compatibility. (+26 more)

### Community 15 - "worker.py"
Cohesion: 0.13
Nodes (12): arq, arq_connections, parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Arq Worker settings configuration., WorkerSettings, Verify URL parsing for Arq Redis connection settings., Verify Arq WorkerSettings has expected functions, crons, and timeouts. (+4 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (32): name, private, scripts, build, dev, lint, preview, type (+24 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.07
Nodes (33): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), Robust location classifier prioritizing: 1. Explicit work mode if provided…, _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch() (+25 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 20 - "matching/__init__.py"
Cohesion: 0.15
Nodes (12): EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation., Generate embedding vector for a single text string., Generate embeddings for a list of text strings. (+4 more)

### Community 21 - "ProfileView.jsx"
Cohesion: 0.13
Nodes (14): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+6 more)

### Community 22 - "Base"
Cohesion: 0.15
Nodes (30): Base, Base SQLAlchemy declarative model., get_db(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application., ApplicationFormAnswer (+22 more)

### Community 23 - "StarStory"
Cohesion: 0.19
Nodes (21): create_story(), delete_story(), get_story(), list_stories(), list_tags(), delete, get, patch (+13 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.15
Nodes (19): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+11 more)

### Community 27 - "test_pydantic_schemas"
Cohesion: 0.11
Nodes (20): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate (+12 more)

### Community 28 - "api/profile.py"
Cohesion: 0.12
Nodes (47): add_certification(), add_designation(), add_language(), add_location(), add_skill(), apply_parsed_cv(), bulk_skills(), compile_texlive() (+39 more)

### Community 29 - "JobSourceHTTPError"
Cohesion: 0.10
Nodes (27): AdzunaJobSource, _parse_created_date(), AsyncClient, datetime, Parse ISO formatted creation date from Adzuna response., Adzuna API implementation of the JobSource interface (ARCHITECTURE.md §4).…, JobSourceConfigError, JobSourceError (+19 more)

### Community 30 - "config.py"
Cohesion: 0.22
Nodes (6): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings, pydantic_settings

### Community 31 - "typing"
Cohesion: 0.08
Nodes (57): asyncio, BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous… (+49 more)

### Community 32 - "AgentConversation"
Cohesion: 0.17
Nodes (16): delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get, patch, Session (+8 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "tenant_client"
Cohesion: 0.15
Nodes (18): admin_client(), override_current_account(), override_get_db(), fixture, Session, TestClient, regular_tenant_account(), superadmin_account() (+10 more)

### Community 40 - "pytest"
Cohesion: 0.13
Nodes (13): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser() (+5 more)

### Community 41 - "api/agent.py"
Cohesion: 0.27
Nodes (13): AgentActionProposal, AgentActionProposalBase, AgentActionProposalRead, AgentChatRequest, AgentConversationRead, AgentConversationUpdate, AgentMessage, AgentMessageRead (+5 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.16
Nodes (29): _build_provider_read(), create_admin_template(), create_llm_provider(), get_platform_metrics(), list_llm_providers(), list_tenants(), LLMProviderInput, LLMProviderReorderInput (+21 more)

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

### Community 51 - ".reflect_for_account"
Cohesion: 0.40
Nodes (3): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…

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
Nodes (28): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, post, Generate tailored interview prep questions for a specific role or job posting,…, Any (+20 more)

### Community 60 - "resolve_tenant_id"
Cohesion: 0.21
Nodes (12): check_job_liveness(), IngestionRequest, IngestionResponse, BaseModel, post, Session, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run. (+4 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.21
Nodes (17): ApplicationStudio(), StudioApprovalGate(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext(), cleanLatexInline(), compactLatex() (+9 more)

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
Cohesion: 0.19
Nodes (9): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Executes human-in-the-loop approval of an action proposal. Enforces tenant…, Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,… (+1 more)

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
Nodes (20): Session, Session, LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can… (+12 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "Application"
Cohesion: 0.12
Nodes (19): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, CVTailorResult, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications. (+11 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "list_jobs"
Cohesion: 0.22
Nodes (9): get_job_sources(), JobSourceInfo, list_admin_templates(), list_flagged_jobs(), get, list_jobs(), get, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+1 more)

### Community 82 - "test_matching.py"
Cohesion: 0.14
Nodes (13): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., Test get_embedding_client factory switches between Mock and OpenAI based on key. (+5 more)

### Community 83 - "chat_with_agent"
Cohesion: 0.14
Nodes (13): approve_proposal(), chat_with_agent(), post, UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, Human-in-the-Loop Approval Gate: Validates candidate authorization, marks…, Candidate rejection or request for revision of a staged proposal., Real-time streaming agent conversation endpoint. Emits Server-Sent Events (SSE)… (+5 more)

### Community 84 - "Session"
Cohesion: 0.14
Nodes (15): account_a(), account_b(), client(), fixture, Session, TestClient, Test SSE streaming response from /api/v1/agent/chat., Test listing, fetching, and deleting agent conversations with isolation. (+7 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "test_educations_skills_and_preview"
Cohesion: 0.32
Nodes (7): account_a(), account_b(), client(), fixture, Session, Test educations, bulk skills, and preview CV generation., test_educations_skills_and_preview()

### Community 90 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "Job"
Cohesion: 0.11
Nodes (31): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), get_session_factory(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,… (+23 more)

### Community 93 - "UserProfile"
Cohesion: 0.09
Nodes (37): Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories… (+29 more)

### Community 94 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.20
Nodes (10): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), LLMProviderBase, LLMProviderCreate (+2 more)

### Community 95 - "google_service.py"
Cohesion: 0.14
Nodes (14): decrypt_secret(), _get_fernet_instance(), Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, base64, cryptography_fernet, csv, email (+6 more)

### Community 96 - "JobSearchQuery"
Cohesion: 0.15
Nodes (12): JobSearchQuery, BaseModel, Normalized query parameters for searching across job sources., _clean_text(), _format_salary(), Any, Asynchronously fetch job postings matching the query from Adzuna., Strip HTML tags and normalize whitespace. (+4 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (16): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start, 2. The 5-Phase Verification Loop (+8 more)

### Community 98 - "test_generate_form_answers_api_endpoint"
Cohesion: 0.28
Nodes (8): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "react"
Cohesion: 0.23
Nodes (10): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), StudioDrafterWorkspace(), StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics(), lintLatexSource() (+2 more)

### Community 102 - "GoogleIntegrationService"
Cohesion: 0.15
Nodes (10): get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+2 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.14
Nodes (13): db_session(), asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs…, In-memory SQLite session for testing matching., Test OpenAIEmbeddingClient with mocked httpx response. (+5 more)

### Community 104 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 105 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 108 - "Account"
Cohesion: 0.18
Nodes (18): create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), dismiss_job_flag(), impersonate_tenant(), delete (+10 more)

### Community 109 - ".score_and_gate_jobs"
Cohesion: 0.17
Nodes (10): compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, MatchingResult, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Summary of a match scoring run., Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the… (+2 more)

### Community 110 - "Project"
Cohesion: 0.22
Nodes (11): add_project(), patch, update_certification(), update_education(), update_project(), update_work_experience(), Project, ProjectBase (+3 more)

### Community 112 - "SpokenLanguage"
Cohesion: 0.24
Nodes (11): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+3 more)

### Community 113 - "get_current_account"
Cohesion: 0.22
Nodes (10): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Ensure the caller has superadmin role privileges., Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+2 more)

### Community 114 - "run_ats_text_layer_check"
Cohesion: 0.25
Nodes (6): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), Verify ATS parser plain-text inspection and keyword coverage., test_ats_checker()

### Community 115 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 116 - "UserProfileRead"
Cohesion: 0.33
Nodes (7): create_profile(), Create a user profile for an account (one per account)., Partial-update the user profile for an account (auto-creates if missing)., update_profile(), UserProfileBase, UserProfileCreate, UserProfileRead

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 118 - "Education"
Cohesion: 0.40
Nodes (6): add_education(), Education, EducationBase, EducationCreate, EducationRead, Structured education background (degrees, high school, certifications,…

### Community 119 - "WorkExperience"
Cohesion: 0.40
Nodes (6): add_work_experience(), Structured work experience entity for candidates across all industries.…, WorkExperience, WorkExperienceBase, WorkExperienceCreate, WorkExperienceRead

### Community 120 - "json"
Cohesion: 0.33
Nodes (5): downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), json

### Community 121 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 122 - "test_profile_compile_texlive.py"
Cohesion: 0.33
Nodes (5): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable()

### Community 123 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

## Knowledge Gaps
- **213 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+208 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 843 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobPosting`, `TestClient`, `models/__init__.py`, `TestClient`, `test_bookmarklet_generation_with_job_and_star_answers`, `applications.py`, `TestClient`, `Base`, `StarStory`, `create_gmail_draft`, `api/profile.py`, `typing`, `AgentConversation`, `tenant_client`, `api/agent.py`, `admin.py`, `test_auth.py`, `resolve_tenant_id`, `Application`, `list_jobs`, `test_matching.py`, `chat_with_agent`, `Session`, `test_educations_skills_and_preview`, `Job`, `UserProfile`, `test_generate_form_answers_api_endpoint`, `GoogleIntegrationService`, `test_matching_service_score_and_gate_clean_jobs`, `SpokenLanguage`, `get_current_account`, `client`, `test_cv_tailor_service_with_structured_profile`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `JobPosting`, `models/__init__.py`, `test_bookmarklet_generation_with_job_and_star_answers`, `applications.py`, `TestClient`, `Base`, `StarStory`, `typing`, `tenant_client`, `admin.py`, `Architecture — Job Application Agent SaaS`, `resolve_tenant_id`, `AgentEngine`, `Application`, `list_jobs`, `test_matching.py`, `Session`, `UserProfile`, `test_matching_service_score_and_gate_clean_jobs`, `Account`, `.score_and_gate_jobs`, `test_cv_tailor_service_with_structured_profile`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `JobSearchQuery`, `run_posting_guard`, `models/__init__.py`, `pytest`, `greenhouse.py`, `FreehireJobSource`, `RemoteOKJobSource`, `LeverJobSource`, `RemotiveJobSource`, `UserProfile`, `Base`, `test_pydantic_schemas`, `Job`, `JobSourceHTTPError`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
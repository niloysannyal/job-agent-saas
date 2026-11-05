# Graph Report - job-agent-saas  (2026-11-05)

## Corpus Check
- 231 files · ~147,784 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2127 nodes · 5724 edges · 106 communities (91 shown, 15 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 742 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e47db991`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- test_ingest_automatically_runs_matching_and_gating
- Application
- Account
- typing
- file_extractor.py
- TestClient
- decrypt_secret
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- sys
- tasks.py
- package.json
- LeverJobSource
- JobSearchQuery
- test_monitor_followups_task
- test_matching.py
- react
- TestClient
- StarStory
- What You Must Do When Invoked
- alembic
- integrations.py
- ApplicationBase
- models/__init__.py
- AdzunaJobSource
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
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- logging
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- parse_redis_settings
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
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
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- Job
- React Frontend Development Standards (adapted from ECC)
- .score_and_gate_jobs
- theme.js
- AgentToolRegistry
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- encrypt_secret
- test_matching_service_score_and_gate_clean_jobs
- session.py
- GoogleIntegrationService
- test_agent.py
- AccountCvVersionBase
- Product Development Environment Guide — Job Application Agent SaaS
- trigger_ingestion
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- LanguageGate
- dispatch_service.py
- deploy.sh
- client
- Base
- LLMProviderCreate
- bug-workflow.md
- test_bookmarklet_generation_with_job_and_star_answers
- FastAPI Backend Development Standards (adapted from ECC)
- StageApplicationProposalTool

## God Nodes (most connected - your core abstractions)
1. `Account` - 185 edges
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

## Communities (106 total, 15 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (18): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+10 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.05
Nodes (58): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+50 more)

### Community 3 - "test_ingest_automatically_runs_matching_and_gating"
Cohesion: 0.15
Nodes (17): db_session(), asyncio, fixture, Session, Test that posting integrity gate runs before persistence: - Invisible…, In-memory SQLite session for testing ingestion., Test deduplication: - Same source_job_id in the same batch is skipped. - Same…, Create a test tenant account. (+9 more)

### Community 4 - "Application"
Cohesion: 0.16
Nodes (14): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+6 more)

### Community 5 - "Account"
Cohesion: 0.07
Nodes (42): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint() (+34 more)

### Community 6 - "typing"
Cohesion: 0.13
Nodes (29): JobBase, JobCreate, JobUpdate, BaseModel, _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource (+21 more)

### Community 7 - "file_extractor.py"
Cohesion: 0.20
Nodes (9): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, csv, io (+1 more)

### Community 8 - "TestClient"
Cohesion: 0.15
Nodes (13): TestClient, Test filtering STAR stories by tag and verified_only flag., GET /api/v1/interview/tags returns deduplicated sorted tags., Verify tenant isolation on STAR stories., GET /api/v1/interview/stories returns empty list when none exist., POST /api/v1/interview/stories creates STAR story and GET retrieves it., PATCH and DELETE endpoints for STAR stories., test_create_and_get_story() (+5 more)

### Community 9 - "decrypt_secret"
Cohesion: 0.22
Nodes (8): decrypt_secret(), _get_fernet_instance(), Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Refresh an expired access token using the stored encrypted refresh token., Verify code exchange, DB persistence with encryption, status check, and…, test_google_callback_and_status(), Fernet

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (47): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+39 more)

### Community 14 - "sys"
Cohesion: 0.11
Nodes (16): os, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor() (+8 more)

### Community 15 - "tasks.py"
Cohesion: 0.08
Nodes (30): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), IngestionResult, JobIngestionService, Any (+22 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (31): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+23 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.09
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "JobSearchQuery"
Cohesion: 0.09
Nodes (24): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., _clean_html(), Any, AsyncClient (+16 more)

### Community 19 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 20 - "test_matching.py"
Cohesion: 0.10
Nodes (22): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+14 more)

### Community 21 - "react"
Cohesion: 0.13
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 23 - "StarStory"
Cohesion: 0.07
Nodes (54): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+46 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "integrations.py"
Cohesion: 0.18
Nodes (21): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+13 more)

### Community 27 - "ApplicationBase"
Cohesion: 0.33
Nodes (6): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationJobRead, ApplicationUpdate, BaseModel

### Community 28 - "models/__init__.py"
Cohesion: 0.06
Nodes (123): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+115 more)

### Community 29 - "AdzunaJobSource"
Cohesion: 0.09
Nodes (26): AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime, Asynchronously fetch job postings matching the query from Adzuna. (+18 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.20
Nodes (21): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+13 more)

### Community 32 - "api/agent.py"
Cohesion: 0.11
Nodes (34): approve_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get (+26 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.14
Nodes (23): create_app(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+15 more)

### Community 40 - "JobPosting"
Cohesion: 0.08
Nodes (25): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace. (+17 more)

### Community 41 - "event_bus.py"
Cohesion: 0.18
Nodes (12): Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent, BaseModel (+4 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.06
Nodes (69): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+61 more)

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
Cohesion: 0.21
Nodes (13): CareerCopilotView(), FAST_CHIPS, STARTER_PROMPTS, FunnelInsight(), JobRadarCarousel(), SendApprovalGate(), STARStoryMatch(), TailorDiffReview() (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "logging"
Cohesion: 0.13
Nodes (16): asyncio, ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ProfileParser (+8 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (13): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+5 more)

### Community 55 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

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
Nodes (8): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Fast-track common one-click prompt chips and unambiguous commands., Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,…

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
Cohesion: 0.10
Nodes (23): LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can… (+15 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "Job"
Cohesion: 0.08
Nodes (45): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountCreate, CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,… (+37 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - ".score_and_gate_jobs"
Cohesion: 0.12
Nodes (15): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.… (+7 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 84 - "AgentToolRegistry"
Cohesion: 0.16
Nodes (7): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…, Verify tool registration and schema generation., test_agent_tools_registry()

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 92 - "session.py"
Cohesion: 0.12
Nodes (24): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, get_database_url() (+16 more)

### Community 93 - "GoogleIntegrationService"
Cohesion: 0.18
Nodes (9): get_google_auth_url(), GoogleAuthUrlResponse, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and… (+1 more)

### Community 95 - "test_agent.py"
Cohesion: 0.10
Nodes (26): BaseModel, SearchJobsInput, BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client() (+18 more)

### Community 96 - "AccountCvVersionBase"
Cohesion: 0.29
Nodes (7): AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateCreate, CvTemplateUpdate, BaseModel

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (16): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start, 2. The 5-Phase Verification Loop (+8 more)

### Community 98 - "trigger_ingestion"
Cohesion: 0.18
Nodes (13): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+5 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "LanguageGate"
Cohesion: 0.15
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 105 - "dispatch_service.py"
Cohesion: 0.20
Nodes (11): Enum, base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text (+3 more)

### Community 107 - "client"
Cohesion: 0.47
Nodes (5): account_a(), account_b(), client(), fixture, Session

### Community 108 - "Base"
Cohesion: 0.15
Nodes (28): Base, Base SQLAlchemy declarative model., downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AccountBase, AccountRead (+20 more)

### Community 109 - "LLMProviderCreate"
Cohesion: 0.50
Nodes (5): 4. Pydantic Schemas & Security, LLMProviderBase, LLMProviderCreate, LLMProviderUpdate, BaseModel

### Community 112 - "test_bookmarklet_generation_with_job_and_star_answers"
Cohesion: 0.20
Nodes (10): client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts., Verify bookmarklet JS generation bundles custom STAR answers when job_id is…, Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent…, test_bookmarklet_generation() (+2 more)

### Community 113 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 114 - "StageApplicationProposalTool"
Cohesion: 0.36
Nodes (7): AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, BaseModel, StageApplicationProposalTool, StageProposalInput, Test human-in-the-loop Send gate: 1. Tool creates AgentActionProposal with…, test_stage_proposal_and_approval_flow()

## Knowledge Gaps
- **197 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 813 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `test_ingest_automatically_runs_matching_and_gating`, `Application`, `typing`, `file_extractor.py`, `TestClient`, `decrypt_secret`, `applications.py`, `tasks.py`, `test_monitor_followups_task`, `test_matching.py`, `TestClient`, `integrations.py`, `models/__init__.py`, `api/agent.py`, `test_admin.py`, `JobPosting`, `admin.py`, `test_auth.py`, `Job`, `test_matching_service_score_and_gate_clean_jobs`, `session.py`, `GoogleIntegrationService`, `test_agent.py`, `trigger_ingestion`, `client`, `Base`, `test_bookmarklet_generation_with_job_and_star_answers`, `StageApplicationProposalTool`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `test_ingest_automatically_runs_matching_and_gating`, `Application`, `Account`, `typing`, `applications.py`, `tasks.py`, `test_monitor_followups_task`, `test_matching.py`, `TestClient`, `StarStory`, `models/__init__.py`, `engine.py`, `test_admin.py`, `JobPosting`, `admin.py`, `logging`, `AgentEngine`, `.score_and_gate_jobs`, `test_matching_service_score_and_gate_clean_jobs`, `session.py`, `test_agent.py`, `trigger_ingestion`, `Base`, `test_bookmarklet_generation_with_job_and_star_answers`, `StageApplicationProposalTool`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `test_ingest_automatically_runs_matching_and_gating`, `typing`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `Base`, `tasks.py`, `Job`, `LeverJobSource`, `JobSearchQuery`, `models/__init__.py`, `AdzunaJobSource`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 118 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 118 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - job-agent-saas  (2026-11-10)

## Corpus Check
- 236 files · ~157,623 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2210 nodes · 5883 edges · 128 communities (107 shown, 21 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 746 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e289df2e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobIngestionService
- LatexLogParser
- test_profile.py
- dispatch_service.py
- models/__init__.py
- test_interview.py
- job.py
- GreenhouseJobSource
- test_freehire_bearer_auth
- RemoteOKJobSource
- applications.py
- env.py
- worker.py
- package.json
- LeverJobSource
- RemotiveJobSource
- TestClient
- test_matching.py
- ProfileView.jsx
- account.py
- StarStoryRead
- What You Must Do When Invoked
- typing
- create_gmail_draft
- test_pydantic_schemas
- api/profile.py
- JobSearchQuery
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Job
- tests/api/__init__.py
- JobPosting
- detective.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- matching/service.py
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- trigger_ingestion
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
- StarStory
- React Frontend Development Standards (adapted from ECC)
- event_bus.py
- LanguageGate
- file_extractor.py
- test_agent.py
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- generate_interview_prep
- devDependencies
- .fetch
- Base
- tasks.py
- FastAPI Backend Development Standards (adapted from ECC)
- config.py
- JobBase
- Product Development Environment Guide — Job Application Agent SaaS
- Account
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- StudioDrafterWorkspace.jsx
- GoogleIntegrationService
- test_matching_service_score_and_gate_clean_jobs
- .parse_from_db
- Security & Tenancy Policy (adapted from ECC AgentShield)
- deploy.sh
- .generate
- AgentToolRegistry
- MatchingService
- ApplicationBase
- bug-workflow.md
- TargetDesignation
- session.py
- .to_dict
- TeXLiveCompilerService
- theme.js
- db_session
- _get_or_create_profile
- plan_relevance_cuts
- texlive_compiler.py
- set_compensation
- test_profile_compile_texlive.py
- test_cv_tailor_service_with_structured_profile
- client
- prune_and_budget_latex
- test_star_coach_tool
- .__init__

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

## Communities (128 total, 21 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (22): App(), CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal() (+14 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.11
Nodes (27): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+19 more)

### Community 3 - "JobIngestionService"
Cohesion: 0.11
Nodes (29): IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:…, Summary metrics of a job ingestion run., Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.…, db_session(), MockGeneralSource (+21 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "dispatch_service.py"
Cohesion: 0.16
Nodes (16): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+8 more)

### Community 7 - "models/__init__.py"
Cohesion: 0.13
Nodes (37): add_certification(), add_project(), create_profile(), Create a user profile for an account (one per account)., OAuthConnectionBase, OAuthConnectionCreate, OAuthConnectionRead, BaseModel (+29 more)

### Community 8 - "test_interview.py"
Cohesion: 0.14
Nodes (19): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, Test filtering STAR stories by tag and verified_only flag. (+11 more)

### Community 9 - "job.py"
Cohesion: 0.15
Nodes (25): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError (+17 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.06
Nodes (33): _clean_html(), _detect_location_type(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime (+25 more)

### Community 11 - "test_freehire_bearer_auth"
Cohesion: 0.16
Nodes (12): asyncio, Verify that Authorization Bearer header is sent when api_key is set, and…, Verify offset is omitted for page 1 and correctly calculated as (page - 1) *…, Verify country and salary_min query filters serialization., Non-200 responses raise JobSourceHTTPError., Verify field mapping and HTML cleaning from realistic freehire response., test_freehire_bearer_auth(), test_freehire_fetch_data_normalization() (+4 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (28): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+20 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (47): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+39 more)

### Community 14 - "env.py"
Cohesion: 0.09
Nodes (24): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), normalize_db_url(), Normalize database URL for driver compatibility., logging_config (+16 more)

### Community 15 - "worker.py"
Cohesion: 0.13
Nodes (12): arq, arq_connections, parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Arq Worker settings configuration., WorkerSettings, Verify URL parsing for Arq Redis connection settings., Verify Arq WorkerSettings has expected functions, crons, and timeouts. (+4 more)

### Community 16 - "package.json"
Cohesion: 0.07
Nodes (28): name, private, scripts, build, dev, lint, preview, type (+20 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "TestClient"
Cohesion: 0.11
Nodes (19): TestClient, Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged)., include_flagged=True must include flagged postings (unless also vetoed)., show_all=True must include all jobs (both vetoed and flagged) for human review., Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…, Verify limit and offset pagination parameters work correctly. (+11 more)

### Community 20 - "test_matching.py"
Cohesion: 0.09
Nodes (22): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+14 more)

### Community 21 - "ProfileView.jsx"
Cohesion: 0.15
Nodes (10): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+2 more)

### Community 22 - "account.py"
Cohesion: 0.08
Nodes (39): BookmarkletResponse, get_autofill_bookmarklet(), Generate an intelligent JavaScript bookmarklet code tailored to the current…, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), Application (+31 more)

### Community 23 - "StarStoryRead"
Cohesion: 0.16
Nodes (18): create_story(), delete_story(), get_story(), list_stories(), list_tags(), delete, get, patch (+10 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.05
Nodes (23): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+15 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.19
Nodes (15): create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_google_status(), google_oauth_callback(), GoogleCallbackRequest, IntegrationStatusResponse (+7 more)

### Community 27 - "test_pydantic_schemas"
Cohesion: 0.10
Nodes (22): 4. Pydantic Schemas & Security, AccountCvVersionBase, AccountCvVersionUpdate, CvTemplateBase, CvTemplateCreate, CvTemplateUpdate, BaseModel, LLMProviderBase (+14 more)

### Community 28 - "api/profile.py"
Cohesion: 0.11
Nodes (43): compile_texlive(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+35 more)

### Community 29 - "JobSearchQuery"
Cohesion: 0.07
Nodes (29): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient (+21 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.16
Nodes (29): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+21 more)

### Community 32 - "api/agent.py"
Cohesion: 0.11
Nodes (36): approve_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get (+28 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "Job"
Cohesion: 0.07
Nodes (49): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session (+41 more)

### Community 40 - "JobPosting"
Cohesion: 0.10
Nodes (18): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace. (+10 more)

### Community 41 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.12
Nodes (45): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+37 more)

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
Nodes (15): CareerCopilotView(), FAST_CHIPS, formatInlineMarkdown(), STARTER_PROMPTS, TurnMarkdownContent(), FunnelInsight(), JobRadarCarousel(), SendApprovalGate() (+7 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "matching/service.py"
Cohesion: 0.16
Nodes (13): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT… (+5 more)

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
Cohesion: 0.11
Nodes (19): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 1. Scope & rollout (+11 more)

### Community 60 - "trigger_ingestion"
Cohesion: 0.18
Nodes (13): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+5 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.18
Nodes (22): ApplicationStudio(), ProfileView(), StudioApprovalGate(), StudioDrafterWorkspace(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext() (+14 more)

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
Nodes (10): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands., Enforce strict SaaS scope boundary: The Career Copilot agent is dedicated… (+2 more)

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

### Community 79 - "StarStory"
Cohesion: 0.25
Nodes (12): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator, FormQAResult, A tailored answer for a single form questionnaire field. (+4 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "event_bus.py"
Cohesion: 0.17
Nodes (11): asyncio, Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent, BaseModel (+3 more)

### Community 82 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 83 - "file_extractor.py"
Cohesion: 0.22
Nodes (8): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, csv, io

### Community 84 - "test_agent.py"
Cohesion: 0.10
Nodes (26): create_app(), Create and configure FastAPI application., BaseModel, StageProposalInput, account_a(), account_b(), api_test_db(), client() (+18 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "generate_interview_prep"
Cohesion: 0.16
Nodes (11): generate_interview_prep(), InterviewPrepRequest, InterviewPrepResponse, PrepQuestion, BaseModel, Generate tailored interview prep questions for a specific role or job posting,…, Any, Alias for role to maintain consistency across frontend and APIs. (+3 more)

### Community 90 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 91 - ".fetch"
Cohesion: 0.18
Nodes (9): _clean_html(), _detect_location_type(), _parse_iso_date(), Any, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is…, Parse ISO 8601 date string with timezone. (+1 more)

### Community 92 - "Base"
Cohesion: 0.08
Nodes (46): Base, Base SQLAlchemy declarative model., Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountCvVersionCreate, CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system… (+38 more)

### Community 93 - "tasks.py"
Cohesion: 0.19
Nodes (15): Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), monitor_followups_task(), Any, Worker task to run Experience Reflector and update learning insights., Background worker task to compute vector embeddings and gate jobs., Cron / periodic worker task to identify applications awaiting response > 7… (+7 more)

### Community 94 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 95 - "config.py"
Cohesion: 0.14
Nodes (16): decrypt_secret(), encrypt_secret(), _get_fernet_instance(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Verify secrets are encrypted and decrypted accurately., test_crypto_encryption_roundtrip() (+8 more)

### Community 96 - "JobBase"
Cohesion: 0.50
Nodes (4): JobBase, JobCreate, JobUpdate, BaseModel

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (16): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start, 2. The 5-Phase Verification Loop (+8 more)

### Community 98 - "Account"
Cohesion: 0.13
Nodes (18): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, api_test_db(), client(), fixture, Session (+10 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "StudioDrafterWorkspace.jsx"
Cohesion: 0.24
Nodes (9): ProfileTemplatesTab(), CompilerDiagnosticsDrawer(), LatexCodeEditor, StudioFactAuditBadge(), StudioFormQADispatchHub(), StudioFormQAEditor(), analyzeLatexDiagnostics(), lintLatexSource() (+1 more)

### Community 102 - "GoogleIntegrationService"
Cohesion: 0.14
Nodes (11): get_google_auth_url(), GoogleAuthUrlResponse, get, Generate Google OAuth 2.0 consent URL for Gmail Draft composition. Scope is…, GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.… (+3 more)

### Community 103 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 104 - ".parse_from_db"
Cohesion: 0.19
Nodes (11): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Test that missing languages section defaults to ['english']. (+3 more)

### Community 105 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 108 - "AgentToolRegistry"
Cohesion: 0.20
Nodes (5): Session, AgentToolRegistry, Any, Central Registry for Autonomous Agent Tools. Enforces the Open-Closed…, Generates standard JSON schema definitions suitable for LLM function calling /…

### Community 109 - "MatchingService"
Cohesion: 0.19
Nodes (8): Session, MatchingService, Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…, Derive a deterministic UUID point ID for the account., Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…

### Community 110 - "ApplicationBase"
Cohesion: 0.22
Nodes (9): ApplicationBase, ApplicationCreate, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate (+1 more)

### Community 112 - "TargetDesignation"
Cohesion: 0.40
Nodes (6): add_designation(), Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, TargetDesignation, TargetDesignationBase, TargetDesignationCreate, TargetDesignationRead

### Community 113 - "session.py"
Cohesion: 0.15
Nodes (18): STAR Interview Coach API — CRUD for interview stories + tag-based querying. All…, decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+10 more)

### Community 115 - "TeXLiveCompilerService"
Cohesion: 0.32
Nodes (5): Any, Detect available TeX compiler binary on PATH., Return True if a TeX compiler is installed and executable., Compile LaTeX source into PDF using system TeX Live engine. Returns dict with…, TeXLiveCompilerService

### Community 116 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 118 - "_get_or_create_profile"
Cohesion: 0.18
Nodes (19): add_education(), add_language(), add_location(), add_skill(), add_work_experience(), apply_parsed_cv(), bulk_skills(), _get_or_create_profile() (+11 more)

### Community 119 - "plan_relevance_cuts"
Cohesion: 0.29
Nodes (7): extract_keywords_from_job(), plan_relevance_cuts(), any, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, Verify relevance scoring and trimming plan., test_relevance_scorer_and_cuts()

### Community 120 - "texlive_compiler.py"
Cohesion: 0.33
Nodes (5): TeX Live backend compiler service. Adapted from Overleaf CLSI (Common LaTeX…, shutil, subprocess, tempfile, time

### Community 121 - "set_compensation"
Cohesion: 0.50
Nodes (5): set_compensation(), CompensationBase, CompensationCreate, CompensationRead, put

### Community 122 - "test_profile_compile_texlive.py"
Cohesion: 0.29
Nodes (6): Tests for TeX Live compilation service and /compile-texlive endpoint., When TeX Live is not on PATH, the endpoint gracefully returns…, When TeX Live compiles successfully, returns PDF base64 and logs., test_compile_texlive_endpoint_mock_success(), test_compile_texlive_endpoint_when_compiler_unavailable(), unittest_mock

### Community 123 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 126 - "test_star_coach_tool"
Cohesion: 0.50
Nodes (4): BaseModel, StarCoachInput, Test STAR interview coach tool aligns story to competency., test_star_coach_tool()

## Knowledge Gaps
- **213 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+208 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 845 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobIngestionService`, `test_profile.py`, `models/__init__.py`, `test_interview.py`, `job.py`, `applications.py`, `test_matching.py`, `account.py`, `create_gmail_draft`, `api/profile.py`, `api/agent.py`, `Job`, `admin.py`, `test_auth.py`, `Architecture — Job Application Agent SaaS`, `trigger_ingestion`, `file_extractor.py`, `test_agent.py`, `Base`, `tasks.py`, `GoogleIntegrationService`, `test_matching_service_score_and_gate_clean_jobs`, `session.py`, `test_cv_tailor_service_with_structured_profile`, `test_star_coach_tool`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `JobBase`, `run_posting_guard`, `JobIngestionService`, `Job`, `models/__init__.py`, `test_pydantic_schemas`, `job.py`, `GreenhouseJobSource`, `test_freehire_bearer_auth`, `RemoteOKJobSource`, `LeverJobSource`, `RemotiveJobSource`, `.fetch`, `Base`, `JobSearchQuery`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobIngestionService`, `models/__init__.py`, `job.py`, `applications.py`, `test_matching.py`, `account.py`, `engine.py`, `admin.py`, `matching/service.py`, `trigger_ingestion`, `AgentEngine`, `test_agent.py`, `generate_interview_prep`, `Base`, `tasks.py`, `Account`, `test_matching_service_score_and_gate_clean_jobs`, `MatchingService`, `session.py`, `test_cv_tailor_service_with_structured_profile`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
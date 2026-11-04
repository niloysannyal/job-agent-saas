# Graph Report - job-agent-saas  (2026-11-04)

## Corpus Check
- 213 files · ~143,000 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2061 nodes · 5565 edges · 115 communities (100 shown, 15 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 730 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `37a5553a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- Job
- Account
- JobSearchQuery
- CVTemplateCompiler
- TestClient
- models/interview.py
- GreenhouseJobSource
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- sys
- tasks.py
- package.json
- LeverJobSource
- RemotiveJobSource
- UserProfile
- test_matching.py
- test_monitor_followups_task
- TestClient
- .score_and_gate_jobs
- What You Must Do When Invoked
- typing
- integrations.py
- Architecture — Job Application Agent SaaS
- models/__init__.py
- job.py
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- LinkedInJobSource
- stage_proposal_tool.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- crypto.py
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- Application
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- CVTailorService
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
- job_ingestion.py
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- Session
- React Frontend Development Standards (adapted from ECC)
- test_adzuna_fetch_with_mock_client
- theme.js
- devDependencies
- AgentToolRegistry
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- google_service.py
- ExperienceReflector
- MockEmbeddingClient
- Base
- Security & Tenancy Policy (adapted from ECC AgentShield)
- subscription.py
- test_agent.py
- get_current_account
- Product Development Environment Guide — Job Application Agent SaaS
- trigger_ingestion
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- LanguageGate
- api/auth.py
- db_session
- client
- client
- deploy.sh
- client
- FastAPI Backend Development Standards (adapted from ECC)
- parse_redis_settings
- client
- bug-workflow.md
- client
- get_me
- test_models.py

## God Nodes (most connected - your core abstractions)
1. `Account` - 179 edges
2. `Job` - 93 edges
3. `JobPosting` - 74 edges
4. `Base` - 73 edges
5. `UserProfile` - 64 edges
6. `JobSearchQuery` - 62 edges
7. `Application` - 58 edges
8. `LLMService` - 41 edges
9. `StarStory` - 37 edges
10. `JobSourceHTTPError` - 36 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `4. Pydantic Schemas & Security` --references--> `LLMProviderRead`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/models/llm_provider.py

## Import Cycles
- None detected.

## Communities (115 total, 15 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.12
Nodes (17): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+9 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.09
Nodes (34): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+26 more)

### Community 3 - "JobPosting"
Cohesion: 0.09
Nodes (39): Integration Checklist, Job Source Integrator, JobPosting, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any, Orchestrate fetching, integrity verification, and persistence of jobs. Args:… (+31 more)

### Community 4 - "Job"
Cohesion: 0.23
Nodes (14): Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application…, Test status progression: draft -> sent -> interview -> offer. (+6 more)

### Community 5 - "Account"
Cohesion: 0.08
Nodes (32): delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant(), delete, Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash. (+24 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.09
Nodes (22): IngestionRequest, Payload for triggering a job ingestion run., JobBase, JobCreate, JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources. (+14 more)

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
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (24): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (44): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+36 more)

### Community 14 - "sys"
Cohesion: 0.11
Nodes (16): os, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check(), Environment & Health Doctor — Job Application Agent SaaS Adapted from ECC's…, run_doctor() (+8 more)

### Community 15 - "tasks.py"
Cohesion: 0.13
Nodes (19): arq, arq_connections, Session, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task() (+11 more)

### Community 16 - "package.json"
Cohesion: 0.08
Nodes (23): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+15 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.07
Nodes (29): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+21 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "UserProfile"
Cohesion: 0.07
Nodes (54): generate_form_answers(), Harness² Recursive Form Q&A Generator. Applies Task-Level Recursion (Propose ->…, Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story… (+46 more)

### Community 20 - "test_matching.py"
Cohesion: 0.10
Nodes (23): Session, compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,… (+15 more)

### Community 21 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (31): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+23 more)

### Community 23 - ".score_and_gate_jobs"
Cohesion: 0.12
Nodes (15): ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models…, Extract readable text from LaTeX CV, stripping comments and common markup., Path, Score clean jobs with cosine similarity and apply language/dealbreaker gate.… (+7 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "typing"
Cohesion: 0.06
Nodes (19): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations. (+11 more)

### Community 26 - "integrations.py"
Cohesion: 0.16
Nodes (24): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+16 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.12
Nodes (16): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 1. Scope & rollout, 2. Priority build order (confirmed), 3. Human-in-the-loop (now a locked decision, not OPEN), 4. Module 1 — Find Job Opportunity (decision made) (+8 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.06
Nodes (118): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+110 more)

### Community 29 - "job.py"
Cohesion: 0.14
Nodes (24): AdzunaJobSource, AsyncClient, Adzuna API implementation of the JobSource interface (ARCHITECTURE.md §4).…, classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided… (+16 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.17
Nodes (25): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+17 more)

### Community 32 - "api/agent.py"
Cohesion: 0.13
Nodes (29): approve_proposal(), chat_with_agent(), get_conversation(), list_action_proposals(), list_conversations(), get, post, Session (+21 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.13
Nodes (24): create_app(), lifespan(), Create and configure FastAPI application., admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture (+16 more)

### Community 40 - "LinkedInJobSource"
Cohesion: 0.18
Nodes (9): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser() (+1 more)

### Community 41 - "stage_proposal_tool.py"
Cohesion: 0.14
Nodes (19): asyncio, AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+11 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.14
Nodes (40): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), dismiss_job_flag(), get_job_sources(), get_platform_metrics(), impersonate_tenant() (+32 more)

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
Cohesion: 0.24
Nodes (13): CareerAgentDock(), QUICK_CHIPS, FunnelInsight(), JobRadarCarousel(), SendApprovalGate(), STARStoryMatch(), TailorDiffReview(), RenderWidget() (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "crypto.py"
Cohesion: 0.14
Nodes (15): decrypt_secret(), encrypt_secret(), _get_fernet_instance(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Refresh an expired access token using the stored encrypted refresh token., Verify secrets are encrypted and decrypted accurately. (+7 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - "Application"
Cohesion: 0.12
Nodes (10): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, AccountCvVersion, Tailored CV version model matching ARCHITECTURE.md §7: (which tailored CV went…, Any, Alias for role to maintain consistency across frontend and APIs., CVTailorResult, 14. Decision log (+2 more)

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "CVTailorService"
Cohesion: 0.15
Nodes (14): CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, CVTailorService, Session, Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.…, Selects the best fact-verified Summary variant based on role keywords or…, Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7., test_cv_template_and_version_models() (+6 more)

### Community 60 - "dispatch_service.py"
Cohesion: 0.14
Nodes (18): EmailDispatchService, EmailDraftProvider, EmailDraftResult, Enum, str, Creates an email draft. If OAuth token is provided, creates a draft in user's…, Result of an email draft creation operation., Minimal-effort draft dispatch service. Enforces Strict Human-in-the-Loop on… (+10 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.27
Nodes (16): ApplicationStudio(), ProfileView(), WORKPLACE_LABELS, cleanLatexInline(), compactLatex(), compactLatexToTwoPages(), compileParsedLatexToPdf(), decodeHtmlEntities() (+8 more)

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

### Community 70 - "job_ingestion.py"
Cohesion: 0.26
Nodes (10): ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, MatchingResult, Summary of a match scoring run., collections, dataclasses, logging, pathlib (+2 more)

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
Nodes (20): LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can… (+12 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "Session"
Cohesion: 0.13
Nodes (15): Session, Test Application model matching ARCHITECTURE.md §3, §6 & §7., Test SubscriptionPlan and Entitlement models matching ARCHITECTURE.md §0 & §7., Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable…, Verify that deleting an account cascades to all tenant-scoped rows., Test StarStory model creation, tags, and account cascade., Test Account model defaults and multi-tenant fields., Test Job model matches ARCHITECTURE.md §7: (account_id, company, role, salary,… (+7 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "test_adzuna_fetch_with_mock_client"
Cohesion: 0.19
Nodes (10): asyncio, Test async fetch using string and dict queries., Test that HTTP errors from Adzuna raise JobSourceHTTPError., Test that an empty results array returns an empty list., Test async fetch parsing with an injected httpx.AsyncClient using MockTransport., test_adzuna_empty_results(), test_adzuna_fetch_query_variations(), test_adzuna_fetch_with_mock_client() (+2 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

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

### Community 88 - "google_service.py"
Cohesion: 0.20
Nodes (7): GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and…, Exchange an OAuth authorization code for access and refresh tokens. Fetches the…, email

### Community 90 - "ExperienceReflector"
Cohesion: 0.18
Nodes (9): ChannelStat, ExperienceInsights, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, Analyze all applications for an account and compute actionable insights,…, Session, test_experience_reflector_conversion_and_multipliers() (+1 more)

### Community 91 - "MockEmbeddingClient"
Cohesion: 0.08
Nodes (19): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text., db_session(), MockQdrantClient, Any, asyncio, fixture (+11 more)

### Community 92 - "Base"
Cohesion: 0.16
Nodes (26): Base, Base SQLAlchemy declarative model., get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db() (+18 more)

### Community 93 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 94 - "subscription.py"
Cohesion: 0.29
Nodes (10): EntitlementBase, EntitlementRead, EntitlementUpdate, BaseModel, Subscription plan catalog model matching ARCHITECTURE.md §0 & §7. Deferred…, SubscriptionPlan, SubscriptionPlanBase, SubscriptionPlanCreate (+2 more)

### Community 95 - "test_agent.py"
Cohesion: 0.15
Nodes (18): BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client(), fixture, Session (+10 more)

### Community 96 - "get_current_account"
Cohesion: 0.22
Nodes (10): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Ensure the caller has superadmin role privileges., Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates… (+2 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (16): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 1. Fast Start, 2. The 5-Phase Verification Loop (+8 more)

### Community 98 - "trigger_ingestion"
Cohesion: 0.20
Nodes (11): check_job_liveness(), IngestionResponse, list_jobs(), BaseModel, get, post, Session, Fetch jobs for an account ordered by match_score descending. Excludes vetoed… (+3 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "LanguageGate"
Cohesion: 0.15
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 102 - "api/auth.py"
Cohesion: 0.11
Nodes (33): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+25 more)

### Community 103 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 104 - "client"
Cohesion: 0.50
Nodes (3): api_test_db(), client(), fixture

### Community 105 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 107 - "client"
Cohesion: 0.38
Nodes (6): account_a(), account_b(), api_test_db(), client(), fixture, Session

### Community 108 - "FastAPI Backend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC)

### Community 109 - "parse_redis_settings"
Cohesion: 0.40
Nodes (5): parse_redis_settings(), Parse a redis connection URL into an arq RedisSettings instance., Verify URL parsing for Arq Redis connection settings., test_parse_redis_settings(), RedisSettings

### Community 110 - "client"
Cohesion: 0.40
Nodes (3): api_test_db(), client(), fixture

### Community 112 - "client"
Cohesion: 0.50
Nodes (3): api_test_db(), client(), fixture

### Community 113 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

### Community 116 - "test_models.py"
Cohesion: 0.08
Nodes (38): 4. Pydantic Schemas & Security, downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AccountBase, AccountCreate, AccountRead (+30 more)

## Knowledge Gaps
- **195 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+190 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 796 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobPosting`, `Job`, `TestClient`, `models/interview.py`, `applications.py`, `tasks.py`, `UserProfile`, `test_matching.py`, `test_monitor_followups_task`, `TestClient`, `integrations.py`, `models/__init__.py`, `job.py`, `engine.py`, `api/agent.py`, `test_admin.py`, `stage_proposal_tool.py`, `admin.py`, `test_auth.py`, `crypto.py`, `CVTailorService`, `Session`, `ExperienceReflector`, `MockEmbeddingClient`, `Base`, `subscription.py`, `test_agent.py`, `get_current_account`, `trigger_ingestion`, `api/auth.py`, `client`, `client`, `get_me`, `test_models.py`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `job_ingestion.py`, `JobSearchQuery`, `LinkedInJobSource`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `Base`, `LeverJobSource`, `RemotiveJobSource`, `test_adzuna_fetch_with_mock_client`, `test_models.py`, `models/__init__.py`, `job.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `Account`, `models/interview.py`, `applications.py`, `tasks.py`, `UserProfile`, `test_matching.py`, `test_monitor_followups_task`, `TestClient`, `.score_and_gate_jobs`, `models/__init__.py`, `job.py`, `engine.py`, `test_admin.py`, `stage_proposal_tool.py`, `admin.py`, `Application`, `CVTailorService`, `AgentEngine`, `job_ingestion.py`, `Session`, `ExperienceReflector`, `MockEmbeddingClient`, `Base`, `test_agent.py`, `trigger_ingestion`, `test_models.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 112 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
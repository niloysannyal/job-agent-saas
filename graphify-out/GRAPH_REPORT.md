# Graph Report - job-agent-saas  (2026-11-04)

## Corpus Check
- 189 files · ~133,765 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 1896 nodes · 4918 edges · 102 communities (83 shown, 19 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 643 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1e5bb335`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- test_cv_tailor.py
- JobPosting
- Job
- Account
- JobSearchQuery
- CVTemplateCompiler
- session.py
- StarStory
- greenhouse.py
- FreehireJobSource
- RemoteOKJobSource
- applications.py
- matching/service.py
- tasks.py
- package.json
- LeverJobSource
- JobSourceHTTPError
- FormQAGenerator
- test_matching.py
- test_monitor_followups_task
- TestClient
- .score_and_gate_jobs
- What You Must Do When Invoked
- alembic
- integrations.py
- Architecture — Job Application Agent SaaS
- models/__init__.py
- 7f7822f4eef9_add_github_url_to_projects_and_location_.py
- Settings
- a7c3e1f24b01_add_profile_and_interview_tables.py
- c4b1297e8df3_add_form_answers_and_oauth_connections.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- LinkedInJobSource
- check_migrations.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- admin.py
- b92e4d183f05_add_pgvector_embedding_to_jobs.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- decrypt_secret
- Project: Job Application Agent SaaS
- CVParserService
- Multi-Tenant SaaS Auditor
- posting_guard.py
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
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- SaaS Review Checklist
- Database Migrations Skill — Job Application Agent SaaS
- Hunt Targets
- typing
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- React Frontend Development Standards (adapted from ECC)
- theme.js
- devDependencies
- main.jsx
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- GoogleIntegrationService
- dispatch_service.py
- MockQdrantClient
- env.py
- encrypt_secret
- .generate
- f82a17d49b21_add_universal_career_tables_and_job_dates.py
- Product Development Environment Guide — Job Application Agent SaaS
- get_available_sources
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- LanguageGate
- test_auth.py
- db_session
- UserProfile
- deploy.sh
- bug-workflow.md
- Base

## God Nodes (most connected - your core abstractions)
1. `Account` - 163 edges
2. `Job` - 79 edges
3. `JobPosting` - 74 edges
4. `Base` - 67 edges
5. `JobSearchQuery` - 62 edges
6. `UserProfile` - 60 edges
7. `Application` - 50 edges
8. `JobSourceHTTPError` - 36 edges
9. `JobSource` - 35 edges
10. `LLMService` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `register()`  [INFERRED]
  docs/ROADMAP.md → backend/app/api/auth.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `get_current_account()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `2. Secrets & Encryption` --references--> `encrypt_secret()`  [INFERRED]
  .agents/rules/security-and-tenancy.md → backend/app/core/crypto.py

## Import Cycles
- None detected.

## Communities (102 total, 19 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.06
Nodes (24): FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction(), Enum, str, Return True if the line matches any instruction-injection pattern. (+16 more)

### Community 1 - "App.jsx"
Cohesion: 0.15
Nodes (18): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+10 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.08
Nodes (36): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+28 more)

### Community 3 - "JobPosting"
Cohesion: 0.07
Nodes (50): Integration Checklist, Job Source Integrator, JobBase, JobCreate, JobPosting, JobRead, JobUpdate, BaseModel (+42 more)

### Community 4 - "Job"
Cohesion: 0.10
Nodes (25): Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, api_test_db(), client(), fixture, Session (+17 more)

### Community 5 - "Account"
Cohesion: 0.08
Nodes (39): Account, Hash and set account password with bcrypt salt., Verify password against stored bcrypt hash., Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…, account_a(), account_b(), api_test_db(), client() (+31 more)

### Community 6 - "JobSearchQuery"
Cohesion: 0.08
Nodes (33): JobSearchQuery, Normalized query parameters for searching across job sources., AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any (+25 more)

### Community 7 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 8 - "session.py"
Cohesion: 0.10
Nodes (29): get_db(), get_engine(), get_session_factory(), FastAPI dependency that yields a SQLAlchemy database session., create_app(), lifespan(), Create and configure FastAPI application., account_a() (+21 more)

### Community 9 - "StarStory"
Cohesion: 0.14
Nodes (28): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+20 more)

### Community 10 - "greenhouse.py"
Cohesion: 0.07
Nodes (36): classify_location_type(), Robust location classifier prioritizing: 1. Explicit work mode if provided…, _clean_html(), _detect_location_type(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any (+28 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.10
Nodes (21): _clean_html(), _detect_location_type(), FreehireJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is…, Determine location type using centralized classifier. (+13 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.09
Nodes (23): _clean_html(), _format_salary(), Any, AsyncClient, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace., Format RemoteOK's numeric salary_min/salary_max into a display string., RemoteOK API implementation of the JobSource interface (ARCHITECTURE.md §4).… (+15 more)

### Community 13 - "applications.py"
Cohesion: 0.09
Nodes (47): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+39 more)

### Community 14 - "matching/service.py"
Cohesion: 0.08
Nodes (31): asyncio, compute_cosine_similarity(), Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, ExperienceInsights, ParsedProfile, ProfileParser, Structured representation of parsed user profile and CV., Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT… (+23 more)

### Community 15 - "tasks.py"
Cohesion: 0.08
Nodes (31): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), arq, arq_connections, Session (+23 more)

### Community 16 - "package.json"
Cohesion: 0.09
Nodes (21): dependencies, jspdf, lucide-react, react, react-dom, name, private, scripts (+13 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (29): _clean_html(), _detect_location_type(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime (+21 more)

### Community 18 - "JobSourceHTTPError"
Cohesion: 0.08
Nodes (34): JobSourceError, JobSourceHTTPError, Raised when an external job source HTTP request fails., Base exception for job source errors., _parse_iso_date(), datetime, Parse ISO 8601 date string with timezone., _parse_date() (+26 more)

### Community 19 - "FormQAGenerator"
Cohesion: 0.12
Nodes (24): ApplyChannelType, FormDetectiveService, FormFieldQuestion, FormInspectionResult, Enum, str, Represents a specific question field extracted from an application form or…, Extract valid recruiter or hiring email from apply URL or posting text. (+16 more)

### Community 20 - "test_matching.py"
Cohesion: 0.06
Nodes (40): Session, EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,… (+32 more)

### Community 21 - "test_monitor_followups_task"
Cohesion: 0.33
Nodes (6): asyncio, Verify monitor_followups_task finds applications older than 7 days., Verify reflect_experience_task executes cleanly in worker context., test_monitor_followups_task(), mock_session(), test_reflect_experience_task()

### Community 22 - "TestClient"
Cohesion: 0.07
Nodes (29): client(), fixture, Session, TestClient, In-memory SQLite database session with static pool for testing., Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged). (+21 more)

### Community 23 - ".score_and_gate_jobs"
Cohesion: 0.11
Nodes (13): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, ChannelStat, Analyze all applications for an account and compute actionable insights,…, Any, Path, Dynamically extracts candidate profile and CV data from database models… (+5 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 26 - "integrations.py"
Cohesion: 0.18
Nodes (21): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_status(), google_oauth_callback() (+13 more)

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.07
Nodes (24): Ensure the caller has superadmin role privileges., require_superadmin(), Any, Alias for role to maintain consistency across frontend and APIs., 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make) (+16 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.05
Nodes (124): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+116 more)

### Community 29 - "7f7822f4eef9_add_github_url_to_projects_and_location_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Upgrade schema: add github_url to projects and location to educations., Downgrade schema: drop github_url from projects and location from educations., upgrade()

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "a7c3e1f24b01_add_profile_and_interview_tables.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop Profile and Interview Coach tables., Create Profile and Interview Coach tables., upgrade()

### Community 32 - "c4b1297e8df3_add_form_answers_and_oauth_connections.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create application_form_answers and oauth_connections tables safely., Drop application_form_answers and oauth_connections tables safely., upgrade()

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.19
Nodes (19): admin_client(), override_current_account(), override_get_db(), admin_test_db(), fixture, Session, TestClient, regular_tenant_account() (+11 more)

### Community 40 - "LinkedInJobSource"
Cohesion: 0.20
Nodes (8): LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags(), asyncio, test_linkedin_job_source_parser()

### Community 41 - "check_migrations.py"
Cohesion: 0.60
Nodes (4): check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit()

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.11
Nodes (49): 4. Pydantic Schemas & Security, _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider() (+41 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

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

### Community 53 - "CVParserService"
Cohesion: 0.17
Nodes (9): CVParserService, Any, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON., Strip markdown fences (```json ... ```) from output. (+1 more)

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
Cohesion: 0.29
Nodes (15): ApplicationStudio(), ProfileView(), WORKPLACE_LABELS, cleanLatexInline(), compactLatex(), compactLatexToTwoPages(), compileParsedLatexToPdf(), decodeHtmlEntities() (+7 more)

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
Cohesion: 0.09
Nodes (28): Session, LLMProvider, ABC, Any, Generate text response given a prompt and optional context. Args: prompt: The…, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any (+20 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "devDependencies"
Cohesion: 0.29
Nodes (7): devDependencies, agentation, oxlint, @types/react, @types/react-dom, vite, @vitejs/plugin-react

### Community 84 - "main.jsx"
Cohesion: 0.50
Nodes (3): App(), frontend_src_index, react-dom

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

### Community 90 - "dispatch_service.py"
Cohesion: 0.20
Nodes (11): Enum, base64, cryptography_fernet, email, email_message, email_mime_application, email_mime_multipart, email_mime_text (+3 more)

### Community 91 - "MockQdrantClient"
Cohesion: 0.33
Nodes (3): MockQdrantClient, Any, In-memory mock of QdrantClient for testing without running Qdrant daemon.

### Community 92 - "env.py"
Cohesion: 0.28
Nodes (8): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), normalize_db_url(), Normalize database URL for driver compatibility., logging_config

### Community 93 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 94 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "f82a17d49b21_add_universal_career_tables_and_job_dates.py"
Cohesion: 0.33
Nodes (5): downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), json

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "get_available_sources"
Cohesion: 0.15
Nodes (17): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+9 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "LanguageGate"
Cohesion: 0.17
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 102 - "test_auth.py"
Cohesion: 0.06
Nodes (65): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+57 more)

### Community 103 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 104 - "UserProfile"
Cohesion: 0.10
Nodes (29): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, api_test_db(), client(), fixture, Session (+21 more)

### Community 116 - "Base"
Cohesion: 0.07
Nodes (69): Base, Base SQLAlchemy declarative model., Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), AccountBase, AccountCreate, AccountRead (+61 more)

## Knowledge Gaps
- **192 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+187 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 753 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `JobPosting`, `Job`, `session.py`, `StarStory`, `applications.py`, `tasks.py`, `test_matching.py`, `test_monitor_followups_task`, `TestClient`, `integrations.py`, `Architecture — Job Application Agent SaaS`, `models/__init__.py`, `test_admin.py`, `admin.py`, `decrypt_secret`, `GoogleIntegrationService`, `get_available_sources`, `test_auth.py`, `UserProfile`, `Base`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `Job`, `JobSearchQuery`, `LinkedInJobSource`, `greenhouse.py`, `FreehireJobSource`, `RemoteOKJobSource`, `LeverJobSource`, `JobSourceHTTPError`, `Base`, `posting_guard.py`, `models/__init__.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `test_cv_tailor.py`, `JobPosting`, `Account`, `StarStory`, `applications.py`, `matching/service.py`, `tasks.py`, `FormQAGenerator`, `test_matching.py`, `test_monitor_followups_task`, `TestClient`, `.score_and_gate_jobs`, `Architecture — Job Application Agent SaaS`, `models/__init__.py`, `test_admin.py`, `admin.py`, `get_available_sources`, `UserProfile`, `Base`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 99 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 16 INFERRED edges - model-reasoned connections that need verification._
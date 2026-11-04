# Graph Report - job-agent-saas  (2026-11-04)

## Corpus Check
- 232 files · ~147,434 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2100 nodes · 5657 edges · 115 communities (94 shown, 21 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 730 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ae70556`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- Job
- Application
- test_profile.py
- job.py
- CVTemplateCompiler
- test_interview.py
- models/interview.py
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
- test_matching.py
- react
- sqlalchemy
- detective.py
- What You Must Do When Invoked
- typing
- integrations.py
- Architecture — Job Application Agent SaaS
- models/__init__.py
- AdzunaJobSource
- Settings
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- tests/api/__init__.py
- get_available_sources
- event_bus.py
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- Account
- test_auth.py
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- lucide-react
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- cv_template.py
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- .sync_role_and_title
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- test_cv_tailor_service_with_structured_profile
- google_service.py
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
- LLMService
- Validation Scenarios
- rules/graphify.md
- extraction-spec.md
- workflows/graphify.md
- test_models.py
- React Frontend Development Standards (adapted from ECC)
- encrypt_secret
- theme.js
- plan_relevance_cuts
- AgentToolRegistry
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- email_service.py
- GoogleIntegrationService
- test_matching_service_score_and_gate_clean_jobs
- main.py
- .set_password
- .generate
- test_agent.py
- .verify_password
- Product Development Environment Guide — Job Application Agent SaaS
- trigger_ingestion
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- MatchingService
- account.py
- db_session
- test_form_qa_api.py
- deploy.sh
- llm_provider.py
- JobPosting
- bug-workflow.md
- test_integrations.py
- get_me
- .generate
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

## Communities (115 total, 21 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.12
Nodes (17): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+9 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.10
Nodes (28): ATSCheckResult, any, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance() (+20 more)

### Community 3 - "Job"
Cohesion: 0.11
Nodes (34): list_jobs(), get, Fetch jobs for an account ordered by match_score descending. Excludes vetoed…, Job, Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…, IngestionResult, JobIngestionService, Any (+26 more)

### Community 4 - "Application"
Cohesion: 0.07
Nodes (26): Integration Checklist, Job Source Integrator, Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, api_test_db() (+18 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "job.py"
Cohesion: 0.15
Nodes (24): _detect_location_type(), Infer location type (remote, hybrid, on-site) using centralized classifier., classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError (+16 more)

### Community 7 - "CVTemplateCompiler"
Cohesion: 0.23
Nodes (10): CVTemplateCompiler, escape_latex(), Any, CV Template Compiler. Replaces semantic template placeholders with cleanly…, Convert highlights string, JSON array, or newline list into a list of strings., Escape special LaTeX characters in a single pass to prevent double-escaping., Compiles structured profile data into a LaTeX document using curated templates., Compile complete CV LaTeX from structured profile data. (+2 more)

### Community 8 - "test_interview.py"
Cohesion: 0.14
Nodes (19): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, Test filtering STAR stories by tag and verified_only flag. (+11 more)

### Community 9 - "models/interview.py"
Cohesion: 0.14
Nodes (26): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+18 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.06
Nodes (33): _clean_html(), _detect_location_type(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime (+25 more)

### Community 11 - "FreehireJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), FreehireJobSource, _parse_iso_date(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace., Asynchronously fetch job postings from freehire.me matching the query. Query is… (+14 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.06
Nodes (62): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+54 more)

### Community 14 - "run_phase1_acceleration.py"
Cohesion: 0.09
Nodes (21): asyncio, os, pathlib, check_alembic_heads(), check_models_tenancy(), Database Migration & Schema Boundary Auditor — Job Application Agent SaaS…, run_migration_audit(), check() (+13 more)

### Community 15 - "tasks.py"
Cohesion: 0.11
Nodes (28): arq, arq_connections, Create a new database session instance outside of FastAPI request lifecycle…, SessionLocal(), embed_jobs_batch_task(), ingest_jobs_task(), monitor_followups_task(), Any (+20 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (30): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+22 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "UserProfile"
Cohesion: 0.22
Nodes (15): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+7 more)

### Community 20 - "test_matching.py"
Cohesion: 0.07
Nodes (37): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient, ABC, Deterministic mock embedding client for testing without network or GPU.…, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *… (+29 more)

### Community 21 - "react"
Cohesion: 0.13
Nodes (15): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+7 more)

### Community 22 - "sqlalchemy"
Cohesion: 0.06
Nodes (51): downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate (+43 more)

### Community 23 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

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
Cohesion: 0.10
Nodes (20): Ensure the caller has superadmin role privileges., require_superadmin(), 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log (+12 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.06
Nodes (121): add_certification(), add_designation(), add_education(), add_language(), add_location(), add_project(), add_skill(), add_work_experience() (+113 more)

### Community 29 - "AdzunaJobSource"
Cohesion: 0.09
Nodes (24): AdzunaJobSource, _clean_text(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime, Asynchronously fetch job postings matching the query from Adzuna. (+16 more)

### Community 30 - "Settings"
Cohesion: 0.33
Nodes (5): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings

### Community 31 - "engine.py"
Cohesion: 0.19
Nodes (24): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+16 more)

### Community 32 - "api/agent.py"
Cohesion: 0.12
Nodes (31): approve_proposal(), chat_with_agent(), get_conversation(), list_action_proposals(), list_conversations(), get, post, Session (+23 more)

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
Cohesion: 0.16
Nodes (10): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+2 more)

### Community 41 - "event_bus.py"
Cohesion: 0.17
Nodes (12): Executes human-in-the-loop approval of an action proposal. Enforces tenant…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent, ProposalCreatedEvent, BaseModel (+4 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "Account"
Cohesion: 0.14
Nodes (45): _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider(), delete_tenant() (+37 more)

### Community 45 - "test_auth.py"
Cohesion: 0.17
Nodes (23): auth_client(), auth_test_db(), fixture, Session, TestClient, seeded_user(), suspended_user(), test_get_me_with_invalid_jwt() (+15 more)

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

### Community 51 - "cv_template.py"
Cohesion: 0.24
Nodes (11): AccountCvVersion, AccountCvVersionBase, AccountCvVersionCreate, AccountCvVersionUpdate, CvTemplateBase, CvTemplateRead, CvTemplateUpdate, BaseModel (+3 more)

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "cv_parser.py"
Cohesion: 0.12
Nodes (14): CVParserService, Any, CV Auto-Parser Service. Extracts raw text from PDF, DOCX, TXT, or LaTeX files,…, Service to extract text from CV files and structure into profile models., Extract plain text from PDF, DOCX, or text files., Extract text from PDF pages using pypdf., Extract text from Word .docx file by inspecting word/document.xml., Send extracted CV text to LLM to parse into structured career JSON. (+6 more)

### Community 55 - ".sync_role_and_title"
Cohesion: 0.29
Nodes (4): Any, Alias for role to maintain consistency across frontend and APIs., field_validator, model_validator

### Community 58 - "Config & Assertion Protection Standard (adapted from ECC)"
Cohesion: 0.50
Nodes (3): Config & Assertion Protection Standard (adapted from ECC), Principle: Fix the Code, Never Weaken the Guardrail, Protected Targets & Non-Weakening Rules:

### Community 59 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 60 - "google_service.py"
Cohesion: 0.14
Nodes (14): decrypt_secret(), _get_fernet_instance(), Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, Refresh an expired access token using the stored encrypted refresh token., base64, cryptography_fernet, email (+6 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.18
Nodes (21): ApplicationStudio(), ProfileView(), StudioApprovalGate(), StudioDrafterWorkspace(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext() (+13 more)

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
Cohesion: 0.26
Nodes (6): AgentEngine, Any, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Fast-track common one-click prompt chips and unambiguous commands., Robustly extracts JSON payload from LLM responses even if wrapped in backticks., Core Autonomous Agent Orchestrator. Manages conversations, SSE streaming,…

### Community 70 - "session.py"
Cohesion: 0.13
Nodes (21): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, get_database_url() (+13 more)

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
Nodes (19): LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider, Any (+11 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "test_models.py"
Cohesion: 0.08
Nodes (42): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), ApplicationCreate, CvTemplate, CvTemplateCreate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Entitlement (+34 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "encrypt_secret"
Cohesion: 0.20
Nodes (9): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield), encrypt_secret(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Verify secrets are encrypted and decrypted accurately. (+1 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

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

### Community 88 - "email_service.py"
Cohesion: 0.29
Nodes (8): generate_otp(), is_smtp_configured(), Check if outbound SMTP server credentials are fully configured., Generate a cryptographically secure 6-digit numeric OTP code., Send 6-digit OTP verification email to user. Falls back gracefully to secure…, send_otp_email(), secrets, smtplib

### Community 90 - "GoogleIntegrationService"
Cohesion: 0.22
Nodes (6): GoogleIntegrationService, Any, Create a Gmail Draft (X-Unsent) via official Gmail API. Never sends the email —…, Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.…, Generate the Google OAuth 2.0 consent URL requesting offline access and…, Exchange an OAuth authorization code for access and refresh tokens. Fetches the…

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.09
Nodes (21): db_session(), MockQdrantClient, Any, asyncio, fixture, Path, Session, Test that missing languages section defaults to ['english']. (+13 more)

### Community 92 - "main.py"
Cohesion: 0.36
Nodes (6): create_app(), lifespan(), Create and configure FastAPI application., contextlib, FastAPI, fastapi_middleware_cors

### Community 94 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 95 - "test_agent.py"
Cohesion: 0.12
Nodes (24): BaseModel, SearchJobsInput, BaseModel, StageProposalInput, BaseModel, StarCoachInput, account_a(), account_b() (+16 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "trigger_ingestion"
Cohesion: 0.24
Nodes (10): check_job_liveness(), IngestionRequest, IngestionResponse, BaseModel, post, Session, Payload for triggering a job ingestion run., Summary metrics of an executed ingestion and matching run. (+2 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "MatchingService"
Cohesion: 0.08
Nodes (20): Session, LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., MatchingService, Any, Path (+12 more)

### Community 102 - "account.py"
Cohesion: 0.16
Nodes (27): login(), post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-…, Register a new tenant account with email and password. Returns authenticated…, register() (+19 more)

### Community 103 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

### Community 104 - "test_form_qa_api.py"
Cohesion: 0.33
Nodes (8): api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint(), test_draft_email_api_endpoint(), test_generate_form_answers_api_endpoint()

### Community 108 - "llm_provider.py"
Cohesion: 0.22
Nodes (11): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 4. Pydantic Schemas & Security, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), LLMProviderBase, LLMProviderCreate (+3 more)

### Community 109 - "JobPosting"
Cohesion: 0.12
Nodes (17): JobBase, JobCreate, JobPosting, JobSearchQuery, JobUpdate, BaseModel, Normalized query parameters for searching across job sources., Standardized JobPosting DTO returned by all JobSource.fetch implementations.… (+9 more)

### Community 112 - "test_integrations.py"
Cohesion: 0.18
Nodes (15): ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.…, api_test_db(), client(), fixture, Session, TestClient, Verify bookmarklet JS generation uses candidate profile facts. (+7 more)

### Community 117 - "get_me"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieve authenticated account profile and permissions from validated token.

## Knowledge Gaps
- **196 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+191 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 800 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `Job`, `Application`, `test_profile.py`, `job.py`, `test_interview.py`, `models/interview.py`, `applications.py`, `tasks.py`, `test_matching.py`, `sqlalchemy`, `integrations.py`, `Architecture — Job Application Agent SaaS`, `models/__init__.py`, `api/agent.py`, `test_admin.py`, `test_auth.py`, `cv_template.py`, `test_cv_tailor_service_with_structured_profile`, `session.py`, `test_models.py`, `test_matching_service_score_and_gate_clean_jobs`, `.set_password`, `test_agent.py`, `.verify_password`, `trigger_ingestion`, `account.py`, `test_form_qa_api.py`, `llm_provider.py`, `test_integrations.py`, `get_me`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `Job`, `Application`, `job.py`, `get_available_sources`, `GreenhouseJobSource`, `FreehireJobSource`, `RemoteOKJobSource`, `test_models.py`, `LeverJobSource`, `RemotiveJobSource`, `sqlalchemy`, `models/__init__.py`, `AdzunaJobSource`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `Application`, `job.py`, `models/interview.py`, `applications.py`, `run_phase1_acceleration.py`, `tasks.py`, `UserProfile`, `test_matching.py`, `sqlalchemy`, `models/__init__.py`, `engine.py`, `test_admin.py`, `Account`, `cv_template.py`, `.sync_role_and_title`, `test_cv_tailor_service_with_structured_profile`, `AgentEngine`, `test_models.py`, `test_matching_service_score_and_gate_clean_jobs`, `test_agent.py`, `trigger_ingestion`, `MatchingService`, `account.py`, `test_integrations.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 112 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
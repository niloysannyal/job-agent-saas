# Graph Report - job-agent-saas  (2026-11-09)

## Corpus Check
- 231 files · ~150,980 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 6, .tex 4, .css 2)

## Summary
- 2132 nodes · 5747 edges · 120 communities (100 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 744 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bbc61e7b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_posting_guard
- App.jsx
- tailor_service.py
- JobPosting
- test_applications.py
- test_profile.py
- JobSourceHTTPError
- models/profile.py
- test_interview.py
- integrations.py
- GreenhouseJobSource
- JobSearchQuery
- RemoteOKJobSource
- applications.py
- matching/service.py
- dispatch_service.py
- package.json
- LeverJobSource
- RemotiveJobSource
- test_jobs.py
- test_matching.py
- lucide-react
- TestClient
- api/interview.py
- What You Must Do When Invoked
- alembic
- create_gmail_draft
- models/__init__.py
- api/profile.py
- AdzunaJobSource
- config.py
- engine.py
- api/agent.py
- User Profile — Niloy Sannyal
- .oxlintrc.json
- Account
- tests/api/__init__.py
- get_available_sources
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
- .parse_from_db
- Project: Job Application Agent SaaS
- cv_parser.py
- Multi-Tenant SaaS Auditor
- CVTemplateCompiler
- attribution-and-scraping.md
- human-in-the-loop.md
- Config & Assertion Protection Standard (adapted from ECC)
- Architecture — Job Application Agent SaaS
- detective.py
- graphify reference: extra exports and benchmark
- ApplicationStudio.jsx
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- AgentEngine
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- get_monitor_summary
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
- MatchingService
- theme.js
- logging
- .get_tool_definitions
- Cycle: Red -> Green -> Refactor
- Verification Loop Skill — Job Application Agent SaaS
- Running Verification
- UserProfile
- .generate
- test_matching_service_score_and_gate_clean_jobs
- main.py
- session.py
- ProfileSkill
- test_agent.py
- SpokenLanguage
- Product Development Environment Guide — Job Application Agent SaaS
- create_app
- Roadmap — Job Application Agent SaaS
- JobsView.jsx
- LanguageGate
- subscription.py
- plan_relevance_cuts
- MockEmbeddingClient
- Security & Tenancy Policy (adapted from ECC AgentShield)
- deploy.sh
- .generate
- Base
- Certification
- Project
- bug-workflow.md
- test_cv_tailor_service_with_structured_profile
- verify.py
- UserProfileRead
- set_compensation
- prune_and_budget_latex
- db_session
- .to_dict
- .select_summary_variant

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
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `13. SaaS-only concerns still ahead (Phase 3+)` --references--> `get_current_account()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `3. Dependency Injection` --references--> `SessionLocal()`  [INFERRED]
  .agents/rules/fastapi-backend.md → backend/app/db/session.py

## Import Cycles
- None detected.

## Communities (120 total, 20 thin omitted)

### Community 0 - "run_posting_guard"
Cohesion: 0.05
Nodes (29): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+21 more)

### Community 1 - "App.jsx"
Cohesion: 0.11
Nodes (18): CareerAppInner(), AdminView(), CommandPalette(), DashboardView(), FollowUpModal(), InterviewCoachView(), LoginModal(), MaterialsModal() (+10 more)

### Community 2 - "tailor_service.py"
Cohesion: 0.14
Nodes (22): ATSCheckResult, Simulates ATS parser text-layer inspection: 1. Verifies contact header fields…, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, Audits tailored LaTeX text against the Verified Fact Ledger. Ensures no…, check_brace_balance(), escape_latex_special_chars() (+14 more)

### Community 3 - "JobPosting"
Cohesion: 0.08
Nodes (40): Integration Checklist, Job Source Integrator, JobPosting, BaseModel, Standardized JobPosting DTO returned by all JobSource.fetch implementations.…, IngestionResult, JobIngestionService, Any (+32 more)

### Community 4 - "test_applications.py"
Cohesion: 0.18
Nodes (15): api_test_db(), client(), fixture, Session, TestClient, Verify that Account B cannot read, tailor, or send Account A's applications., Test Module 3 (Monitor): Aggregated status summary view across all pipeline…, Test Module 3: Follow-up drafting and strict cap of 2 per application… (+7 more)

### Community 5 - "test_profile.py"
Cohesion: 0.10
Nodes (29): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, PATCH /api/v1/profile updates fields partially. (+21 more)

### Community 6 - "JobSourceHTTPError"
Cohesion: 0.14
Nodes (26): classify_location_type(), JobSource, ABC, Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:…, Robust location classifier prioritizing: 1. Explicit work mode if provided…, JobSourceConfigError, JobSourceError, JobSourceHTTPError (+18 more)

### Community 7 - "models/profile.py"
Cohesion: 0.16
Nodes (22): add_designation(), add_language(), add_location(), CertificationUpdate, EducationUpdate, ProfileSkillUpdate, ProjectUpdate, BaseModel (+14 more)

### Community 8 - "test_interview.py"
Cohesion: 0.14
Nodes (19): account_a(), account_b(), api_test_db(), client(), fixture, Session, TestClient, Test filtering STAR stories by tag and verified_only flag. (+11 more)

### Community 9 - "integrations.py"
Cohesion: 0.11
Nodes (27): decrypt_secret(), encrypt_secret(), _get_fernet_instance(), Encrypt a sensitive plaintext secret (OAuth token, API key) at rest. Returns…, Decrypt an encrypted secret at rest. If decryption fails (e.g. key mismatch or…, Derive a deterministic 32-byte URL-safe base64 Fernet key from the…, ApplicationFormAnswer, Stores structured questions and answers for a specific job application form.… (+19 more)

### Community 10 - "GreenhouseJobSource"
Cohesion: 0.07
Nodes (31): _clean_html(), GreenhouseJobSource, _do_fetch(), _parse_iso_date(), Any, AsyncClient, datetime, Extract the RFC 5988 'next' relation URL from the HTTP Link response header.… (+23 more)

### Community 11 - "JobSearchQuery"
Cohesion: 0.10
Nodes (24): JobSearchQuery, Normalized query parameters for searching across job sources., Any, Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…, Helper method to normalize search input into a JobSearchQuery instance., _clean_html(), FreehireJobSource, Any (+16 more)

### Community 12 - "RemoteOKJobSource"
Cohesion: 0.08
Nodes (26): _clean_html(), _format_salary(), _parse_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…, Strip HTML tags and normalize whitespace. (+18 more)

### Community 13 - "applications.py"
Cohesion: 0.10
Nodes (43): create_email_draft(), detect_apply_channel(), DetectChannelRequest, DetectChannelResponse, draft_follow_up(), DraftEmailRequest, DraftEmailResponse, evaluate_job_fit() (+35 more)

### Community 14 - "matching/service.py"
Cohesion: 0.12
Nodes (16): ProfileParser, Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…, dataclasses, os, pathlib, qdrant_client_models, check_alembic_heads(), check_models_tenancy() (+8 more)

### Community 15 - "dispatch_service.py"
Cohesion: 0.05
Nodes (48): 1. Architectural Structure, 2. Async Correctness, 3. Dependency Injection, 5. Testing, FastAPI Backend Development Standards (adapted from ECC), arq, arq_connections, Session (+40 more)

### Community 16 - "package.json"
Cohesion: 0.06
Nodes (31): dependencies, jspdf, lucide-react, react, react-dom, devDependencies, agentation, oxlint (+23 more)

### Community 17 - "LeverJobSource"
Cohesion: 0.08
Nodes (27): _clean_html(), LeverJobSource, _do_fetch(), _parse_created_at(), Any, AsyncClient, datetime, Strip HTML tags and normalize whitespace. (+19 more)

### Community 18 - "RemotiveJobSource"
Cohesion: 0.09
Nodes (22): _clean_html(), _parse_publication_date(), Any, AsyncClient, datetime, Asynchronously fetch remote job postings from Remotive matching the query. Maps…, Strip HTML tags and normalize whitespace., Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC). (+14 more)

### Community 19 - "test_jobs.py"
Cohesion: 0.16
Nodes (16): client(), fixture, Session, In-memory SQLite database session with static pool for testing., FastAPI TestClient with overridden get_db dependency., Explicit multi-tenant security test: Seeds jobs for two distinct accounts…, Seed test accounts for multi-tenant isolation tests., Seed a variety of jobs: - High match score, clean - Mid match score, clean -… (+8 more)

### Community 20 - "test_matching.py"
Cohesion: 0.13
Nodes (19): compute_cosine_similarity(), EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, ABC, Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…, Factory returning OpenAIEmbeddingClient if API key is provided and valid,…, Abstract interface for text embedding generation. (+11 more)

### Community 21 - "lucide-react"
Cohesion: 0.12
Nodes (16): ProfileEducationModal(), ProfileEducationTab(), ProfileExperienceModal(), ProfileExperienceTab(), ProfileIdentityTab(), ProfileProjectModal(), ProfileProjectsTab(), ProfileSkillsTab() (+8 more)

### Community 22 - "TestClient"
Cohesion: 0.12
Nodes (17): TestClient, Default request must exclude vetoed=True and integrity_status='flagged'…, Verify returned jobs are ordered by match_score descending, with unscored…, include_vetoed=True must include vetoed postings (unless also flagged)., include_flagged=True must include flagged postings (unless also vetoed)., show_all=True must include all jobs (both vetoed and flagged) for human review., Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…, Verify limit and offset pagination parameters work correctly. (+9 more)

### Community 23 - "api/interview.py"
Cohesion: 0.14
Nodes (25): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+17 more)

### Community 24 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 25 - "alembic"
Cohesion: 0.04
Nodes (22): alembic, downgrade(), Create agent action proposals, conversations, and messages tables., Drop agent tables in reverse order., upgrade(), downgrade(), Add is_pinned column to agent_conversations., Drop is_pinned column from agent_conversations. (+14 more)

### Community 26 - "create_gmail_draft"
Cohesion: 0.09
Nodes (29): BookmarkletResponse, create_gmail_draft(), CreateGmailDraftRequest, CreateGmailDraftResponse, disconnect_google(), get_autofill_bookmarklet(), get_google_auth_url(), get_google_status() (+21 more)

### Community 27 - "models/__init__.py"
Cohesion: 0.11
Nodes (26): add_education(), ApplicationBase, ApplicationCvVersionRead, ApplicationFormAnswerBase, ApplicationFormAnswerCreate, ApplicationFormAnswerRead, ApplicationJobRead, ApplicationUpdate (+18 more)

### Community 28 - "api/profile.py"
Cohesion: 0.12
Nodes (42): add_work_experience(), delete_certification(), delete_designation(), delete_education(), delete_language(), delete_location(), delete_project(), delete_skill() (+34 more)

### Community 29 - "AdzunaJobSource"
Cohesion: 0.08
Nodes (26): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), Any, AsyncClient, datetime (+18 more)

### Community 30 - "config.py"
Cohesion: 0.22
Nodes (6): Path, Resolve the Master CV path from explicit, local, or repository root paths., Resolve the User Profile path from explicit, local, or repository root paths., Settings, BaseSettings, pydantic_settings

### Community 31 - "engine.py"
Cohesion: 0.14
Nodes (27): BaseAgentTool, GenerativeUIWidget, ABC, BaseModel, Enum, str, Standardized Hexagonal Agent Tool Port. All external or internal autonomous…, Executes the autonomous tool action and returns structured data along with an… (+19 more)

### Community 32 - "api/agent.py"
Cohesion: 0.11
Nodes (34): approve_proposal(), chat_with_agent(), delete_conversation(), get_conversation(), list_action_proposals(), list_conversations(), delete, get (+26 more)

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "Account"
Cohesion: 0.11
Nodes (31): decode_access_token(), get_current_account(), get_optional_account(), Session, Optional authentication resolver for endpoints where account_id may be passed…, Decode and validate a JWT access token. Raises HTTPException(401) on expiration…, Resolve the current authenticated account context. 1. Primary: Validates…, Account (+23 more)

### Community 40 - "get_available_sources"
Cohesion: 0.15
Nodes (11): get_available_sources(), Return instantiated JobSource instances based on requested names or all…, LinkedInJobSource, Any, AsyncClient, Strip HTML tags and normalize whitespace., LinkedIn public guest API implementation of the JobSource interface…, _strip_tags() (+3 more)

### Community 41 - "stage_proposal_tool.py"
Cohesion: 0.17
Nodes (16): asyncio, AgentActionProposal, First-Class Action Proposal entity enforcing Human-in-the-Loop on Send. Every…, ApplicationTailoredEvent, DomainEvent, DomainEventBus, JobIngestedEvent, ProposalApprovedEvent (+8 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "admin.py"
Cohesion: 0.11
Nodes (50): 4. Pydantic Schemas & Security, _build_provider_read(), create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_job(), delete_llm_provider() (+42 more)

### Community 45 - "test_auth.py"
Cohesion: 0.07
Nodes (57): get_me(), login(), get, post, Session, Generate and dispatch a 6-digit OTP verification code to candidate's email.…, Verify 6-digit OTP code, create tenant account with full name and profile, and…, Authenticate user credentials and issue signed JWT bearer token. Supports auto-… (+49 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.22
Nodes (8): Agent Behavior Rules — Job Application Agent SaaS, Bug workflow, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "react"
Cohesion: 0.21
Nodes (13): CareerCopilotView(), FAST_CHIPS, STARTER_PROMPTS, FunnelInsight(), JobRadarCarousel(), SendApprovalGate(), STARStoryMatch(), TailorDiffReview() (+5 more)

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - ".parse_from_db"
Cohesion: 0.13
Nodes (14): ChannelStat, ExperienceInsights, Analyze all applications for an account and compute actionable insights,…, ParsedProfile, Any, Path, Structured representation of parsed user profile and CV., Dynamically extracts candidate profile and CV data from database models… (+6 more)

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
Cohesion: 0.05
Nodes (37): check_job_liveness(), IngestionRequest, IngestionResponse, list_jobs(), BaseModel, get, post, Session (+29 more)

### Community 60 - "detective.py"
Cohesion: 0.20
Nodes (15): ApplyChannelType, FormDetectiveService, FormInspectionResult, Enum, str, Extract valid recruiter or hiring email from apply URL or posting text., Identify ATS platform name from hostname or path., Extract explicit form questions found in the posting text, or synthesize the… (+7 more)

### Community 61 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 62 - "ApplicationStudio.jsx"
Cohesion: 0.20
Nodes (21): ApplicationStudio(), ProfileView(), StudioApprovalGate(), downloadLatexSource(), downloadPdfDocument(), sanitizeFileName(), StudioJobContext(), cleanLatexInline() (+13 more)

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
Cohesion: 0.15
Nodes (11): AgentMessage, Individual turn within an agent conversation, preserving thought traces, tool…, AgentEngine, Any, Session, Processes candidate prompt and yields typed SSE frames in real time: - {"type":…, Determines the conversation title per rules: - If a specific job is…, Fast-track common one-click prompt chips and unambiguous commands. (+3 more)

### Community 70 - "get_monitor_summary"
Cohesion: 0.29
Nodes (6): get_monitor_summary(), list_applications(), get, Module 3 (Monitor): Aggregated status summary view across all pipeline stages.…, List applications for a tenant account., StatusSummary

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
Nodes (19): Session, LLMProvider, ABC, Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md. Every…, MockLLMProvider, Any, Deterministic mock provider for unit testing and offline development. Can…, OpenAIProvider (+11 more)

### Community 75 - "Validation Scenarios"
Cohesion: 0.25
Nodes (7): 1. SuperAdmin Ops Center & Tenant Management, 2. Job Radar Ingestion & Integrity Shield, 3. Dynamic LLM Failover Engine & Priority Ordering, 4. Application Pipeline & Lifecycle Tracker, 5. CV Tailoring & Application Studio, QA & Validation Context — Job Application Agent SaaS, Validation Scenarios

### Community 79 - "Job"
Cohesion: 0.15
Nodes (28): downgrade(), Create universal career entities, add profile fields, and job date/status…, Revert universal career entities, profile fields, and job date columns., upgrade(), AccountBase, AccountCreate, AccountRead, ApplicationCreate (+20 more)

### Community 80 - "React Frontend Development Standards (adapted from ECC)"
Cohesion: 0.33
Nodes (5): 1. Anti-Template Quality & Design System, 2. Modal Backdrops & Glassmorphism, 3. Component Architecture & State, 4. Accessibility & Responsiveness, React Frontend Development Standards (adapted from ECC)

### Community 81 - "MatchingService"
Cohesion: 0.15
Nodes (10): Session, MatchingService, Any, Path, Session, Score clean jobs with cosine similarity and apply language/dealbreaker gate.…, Search for top jobs matching a vector embedding using Supabase pgvector cosine…, Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:… (+2 more)

### Community 82 - "theme.js"
Cohesion: 0.50
Nodes (6): LandingPageView(), applyTheme(), getInitialTheme(), getTheme, setTheme(), useTheme()

### Community 83 - "logging"
Cohesion: 0.17
Nodes (11): UploadFile, Accepts arbitrary user files (images, pdf, xlsx, txt, mp3, code, etc.),…, upload_files_for_agent(), extract_file_content(), Any, Extracts text, structured data, and metadata from arbitrary user-uploaded…, base64, csv (+3 more)

### Community 85 - "Cycle: Red -> Green -> Refactor"
Cohesion: 0.33
Nodes (5): Cycle: Red -> Green -> Refactor, Phase 1: RED (Write the Failing Test), Phase 2: GREEN (Implement the Minimal Working Solution), Phase 3: REFACTOR (Clean Code & Verify Boundaries), TDD Workflow Skill — Job Application Agent SaaS

### Community 86 - "Verification Loop Skill — Job Application Agent SaaS"
Cohesion: 0.40
Nodes (4): Execution, Phases Checked, Verification Loop Skill — Job Application Agent SaaS, When to Run

### Community 87 - "Running Verification"
Cohesion: 0.50
Nodes (3): Protocol Guidelines:, Running Verification, Verification Loop Standard (adapted from ECC)

### Community 88 - "UserProfile"
Cohesion: 0.23
Nodes (16): A single STAR-format interview story. Matches USER_PROFILE.md §"Interview story…, StarStory, Core profile for a user (one-to-one with Account). Stores identity, narrative,…, UserProfile, FormFieldQuestion, Represents a specific question field extracted from an application form or…, FormFieldAnswer, FormQAGenerator (+8 more)

### Community 90 - ".generate"
Cohesion: 0.22
Nodes (7): Any, Execute generation across the provider chain with automatic fallback., Core Behavioral Principles (from ECC), Development Context — Job Application Agent SaaS, Non-Negotiables & System Boundaries, Standard Verification Step, 5. Non-Negotiables

### Community 91 - "test_matching_service_score_and_gate_clean_jobs"
Cohesion: 0.10
Nodes (16): db_session(), MockQdrantClient, Any, asyncio, fixture, Session, Test embedding profile and upserting point into Qdrant., Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs… (+8 more)

### Community 92 - "main.py"
Cohesion: 0.09
Nodes (30): Session, Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…, seed_initial_data(), lifespan(), CvTemplate, LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…, Entitlement, Subscription plan catalog model matching ARCHITECTURE.md §0 & §7. Deferred… (+22 more)

### Community 93 - "session.py"
Cohesion: 0.24
Nodes (12): get_database_url(), Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory() (+4 more)

### Community 94 - "ProfileSkill"
Cohesion: 0.31
Nodes (11): add_skill(), apply_parsed_cv(), bulk_skills(), list_skills(), post, update_skill(), ProfileSkill, ProfileSkillBase (+3 more)

### Community 95 - "test_agent.py"
Cohesion: 0.10
Nodes (28): BaseModel, SearchJobsInput, BaseModel, StarCoachInput, account_a(), account_b(), api_test_db(), client() (+20 more)

### Community 96 - "SpokenLanguage"
Cohesion: 0.24
Nodes (11): CompensationExpectation, Target job titles / designations a user is searching for. Per ARCHITECTURE.md…, Target work locations / regions a user is willing to work in. Supports remote /…, Salary / compensation expectations (one per profile). Marked sensitive — never…, Languages the user speaks, with proficiency level. Used by the language gate in…, SpokenLanguage, TargetDesignation, TargetLocation (+3 more)

### Community 97 - "Product Development Environment Guide — Job Application Agent SaaS"
Cohesion: 0.20
Nodes (9): 1. Fast Start, 2. The 5-Phase Verification Loop, 3. Development Contexts (`contexts/`), 4. Agent Rules & Engineering Standards (`.agents/rules/`), 5. Automated Health & Quality Tooling (`scripts/`), Diagnose Environment Health, Install Automated Git Pre-Commit Hook, Launch Development Servers (+1 more)

### Community 98 - "create_app"
Cohesion: 0.22
Nodes (10): create_app(), Create and configure FastAPI application., api_test_db(), client(), fixture, Session, TestClient, test_detect_channel_api_endpoint() (+2 more)

### Community 99 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 100 - "JobsView.jsx"
Cohesion: 0.52
Nodes (5): JobDetailModal(), decodeHtmlEntities(), formatPostingDate(), formatSalary(), JobsView()

### Community 101 - "LanguageGate"
Cohesion: 0.15
Nodes (10): LanguageGate, Evaluate description against declared languages. Returns: (is_vetoed,…, Evaluates whether a job description requires a spoken language not declared in…, Detect any language explicitly marked as required or mandatory., English-only posting is not vetoed., Posting requiring German is vetoed if German is not declared., If user declared German, German requirement is not vetoed., test_language_gate_declared_language_allowed() (+2 more)

### Community 102 - "subscription.py"
Cohesion: 0.36
Nodes (9): EntitlementBase, EntitlementCreate, EntitlementRead, EntitlementUpdate, BaseModel, SubscriptionPlanBase, SubscriptionPlanCreate, SubscriptionPlanRead (+1 more)

### Community 103 - "plan_relevance_cuts"
Cohesion: 0.24
Nodes (9): extract_keywords_from_job(), plan_relevance_cuts(), any, Computes a relevance-weighted score for a single LaTeX bullet: score =…, Extracts non-stopword tokens from a job posting for relevance scoring., Applies relevance-weighted line scoring to trim bullets to fit within the…, score_bullet_relevance(), Verify relevance scoring and trimming plan. (+1 more)

### Community 104 - "MockEmbeddingClient"
Cohesion: 0.32
Nodes (3): MockEmbeddingClient, Deterministic mock embedding client for testing without network or GPU.…, Generate embedding for a single text.

### Community 105 - "Security & Tenancy Policy (adapted from ECC AgentShield)"
Cohesion: 0.33
Nodes (5): 1. Multi-Tenant Partitioning, 2. Secrets & Encryption, 3. Ingestion & Prompt Injection Defense, 4. Human-in-the-Loop on Send, Security & Tenancy Policy (adapted from ECC AgentShield)

### Community 108 - "Base"
Cohesion: 0.09
Nodes (23): Base, Base SQLAlchemy declarative model., Application, Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,…, ExperienceReflector, Session, Harness² Experiential Reflector: Analyzes historical application trajectories…, db_session() (+15 more)

### Community 109 - "Certification"
Cohesion: 0.40
Nodes (6): add_certification(), Certification, CertificationBase, CertificationCreate, CertificationRead, Professional certifications, licenses, and credentials.

### Community 110 - "Project"
Cohesion: 0.40
Nodes (6): add_project(), Project, ProjectBase, ProjectCreate, ProjectRead, Portfolio projects, open-source work, or major professional deliverables.

### Community 112 - "test_cv_tailor_service_with_structured_profile"
Cohesion: 0.40
Nodes (6): asyncio, Session, Verify complete Drafter + Reviewer pipeline, persistence, and strict human-in-…, Verify CVTailorService with structured career entities (universal profile) and…, test_cv_tailor_service_end_to_end(), test_cv_tailor_service_with_structured_profile()

### Community 113 - "verify.py"
Cohesion: 0.40
Nodes (5): main(), Path, Verification Loop — Job Application Agent SaaS Adapted from ECC's verification-…, run_step(), subprocess

### Community 114 - "UserProfileRead"
Cohesion: 0.50
Nodes (5): create_profile(), Create a user profile for an account (one per account)., UserProfileBase, UserProfileCreate, UserProfileRead

### Community 115 - "set_compensation"
Cohesion: 0.50
Nodes (5): set_compensation(), CompensationBase, CompensationCreate, CompensationRead, put

### Community 117 - "db_session"
Cohesion: 0.67
Nodes (3): db_session(), fixture, In-memory SQLite session with all multi-tenant tables.

## Knowledge Gaps
- **197 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 815 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Account` connect `Account` to `tailor_service.py`, `JobPosting`, `test_applications.py`, `test_profile.py`, `models/profile.py`, `test_interview.py`, `integrations.py`, `applications.py`, `test_jobs.py`, `test_matching.py`, `create_gmail_draft`, `models/__init__.py`, `api/profile.py`, `api/agent.py`, `admin.py`, `test_auth.py`, `Architecture — Job Application Agent SaaS`, `Job`, `logging`, `test_matching_service_score_and_gate_clean_jobs`, `main.py`, `test_agent.py`, `SpokenLanguage`, `create_app`, `subscription.py`, `Base`, `test_cv_tailor_service_with_structured_profile`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `JobPosting` connect `JobPosting` to `run_posting_guard`, `JobSourceHTTPError`, `get_available_sources`, `GreenhouseJobSource`, `JobSearchQuery`, `RemoteOKJobSource`, `Job`, `LeverJobSource`, `RemotiveJobSource`, `test_jobs.py`, `models/__init__.py`, `AdzunaJobSource`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `Job` connect `Job` to `tailor_service.py`, `JobPosting`, `test_applications.py`, `integrations.py`, `applications.py`, `matching/service.py`, `dispatch_service.py`, `test_jobs.py`, `test_matching.py`, `api/interview.py`, `models/__init__.py`, `engine.py`, `Account`, `stage_proposal_tool.py`, `admin.py`, `Architecture — Job Application Agent SaaS`, `AgentEngine`, `MatchingService`, `UserProfile`, `test_matching_service_score_and_gate_clean_jobs`, `main.py`, `test_agent.py`, `Base`, `test_cv_tailor_service_with_structured_profile`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `Job` (e.g. with `delete_job()` and `dismiss_job_flag()`) actually correct?**
  _`Job` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Base` (e.g. with `lifespan()` and `admin_test_db()`) actually correct?**
  _`Base` has 17 INFERRED edges - model-reasoned connections that need verification._
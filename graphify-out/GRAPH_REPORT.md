# Graph Report - job-agent-saas  (2026-10-28)

## Corpus Check
- 114 files · ~85,516 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 4, .css 2, .ini 1)

## Summary
- 1223 nodes · 3249 edges · 58 communities (47 shown, 11 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 438 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d16e6717`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/__init__.py
- typing
- test_cv_tailor.py
- App.jsx
- api/profile.py
- models/__init__.py
- applications.py
- JobSearchQuery
- env.py
- RemoteOKJobSource
- job.py
- Base
- AdzunaJobSource
- api/interview.py
- seed.py
- RemotiveJobSource
- LeverJobSource
- test_profile.py
- Account
- test_matching.py
- MatchingService
- typing
- job_ingestion.py
- job.py
- client
- test_applications.py
- test_matching.py
- Architecture — Job Application Agent SaaS
- test_multi_tenant_isolation_never_leaks_cross_account_data
- MatchingService
- Settings
- test_interview.py
- MockEmbeddingClient
- User Profile — Niloy Sannyal
- .oxlintrc.json
- test_admin.py
- Base
- OpenAIEmbeddingClient
- Research — Competitors, APIs, and Legal Notes
- Features & Views
- Account
- UserProfile
- Local setup
- Agent Behavior Rules — Job Application Agent SaaS
- test_multi_tenant_isolation_never_leaks_cross_account_data
- Job Application Agent — Original Idea (transcribed from notebook)
- Non-Negotiable Rules
- JobBase
- Project: Job Application Agent SaaS
- Roadmap — Job Application Agent SaaS
- Multi-Tenant SaaS Auditor
- test_models.py
- attribution-and-scraping.md
- human-in-the-loop.md

## God Nodes (most connected - your core abstractions)
1. `Account` - 100 edges
2. `JobPosting` - 74 edges
3. `JobSearchQuery` - 62 edges
4. `Job` - 61 edges
5. `Base` - 47 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 35 edges
8. `Application` - 32 edges
9. `run_posting_guard()` - 32 edges
10. `UserProfile` - 26 edges

## Surprising Connections (you probably didn't know these)
- `7.1 Superadmin Control Center & Impersonation Engine (built 2026-10-27)` --references--> `require_superadmin()`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/core/auth.py
- `Interfaces to honor, not bypass` --references--> `JobSource`  [INFERRED]
  AGENTS.md → backend/app/services/job_sources/base.py
- `Phase 0 — MVP build (target: 1 month, using Google Antigravity)` --references--> `UserProfile`  [INFERRED]
  docs/ROADMAP.md → backend/app/models/profile.py
- `4. Module 1 — Find Job Opportunity (decision made)` --references--> `SpokenLanguage`  [INFERRED]
  docs/ARCHITECTURE.md → backend/app/models/profile.py
- `Integration Checklist` --references--> `JobIngestionService`  [INFERRED]
  .agents/skills/job-source-integrator/SKILL.md → backend/app/services/job_ingestion.py

## Import Cycles
- None detected.

## Communities (58 total, 11 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.05
Nodes (16): Environment & Commands, Pipeline Verification Checklist, SaaS Pipeline Runner, FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction() (+8 more)

### Community 1 - "typing"
Cohesion: 0.06
Nodes (55): dependencies, jspdf@^4.2.1, lucide-react@^1.61.0, react@^19.3.1, react-dom@^19.3.1, devDependencies, oxlint@^1.88.0, @types/react@^19.3.0 (+47 more)

### Community 2 - "test_cv_tailor.py"
Cohesion: 0.07
Nodes (20): ATSCheckResult, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body(), strip_control_comments() (+12 more)

### Community 3 - "App.jsx"
Cohesion: 0.07
Nodes (17): IngestionRequest, IngestionResponse, list_jobs(), trigger_ingestion(), IngestionResult, JobIngestionService, db_session(), MockGeneralSource (+9 more)

### Community 4 - "api/profile.py"
Cohesion: 0.14
Nodes (23): add_designation(), add_language(), add_location(), create_profile(), _get_or_create_profile(), update_profile(), upsert_compensation(), CompensationBase (+15 more)

### Community 5 - "models/__init__.py"
Cohesion: 0.12
Nodes (22): AccountBase, AccountRead, AccountUpdate, ApplicationBase, ApplicationRead, ApplicationUpdate, AccountCvVersionBase, AccountCvVersionCreate (+14 more)

### Community 6 - "applications.py"
Cohesion: 0.09
Nodes (12): JobSearchQuery, AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), test_adzuna_empty_results(), test_adzuna_fetch_query_variations() (+4 more)

### Community 7 - "JobSearchQuery"
Cohesion: 0.12
Nodes (8): test_compensation_upsert(), test_create_and_get_profile(), test_get_profile_empty(), test_multi_tenant_isolation(), test_spoken_languages_crud(), test_target_designations_crud(), test_target_locations_crud(), test_update_profile()

### Community 8 - "env.py"
Cohesion: 0.20
Nodes (4): get_database_url(), run_migrations_offline(), run_migrations_online(), normalize_db_url()

### Community 9 - "RemoteOKJobSource"
Cohesion: 0.11
Nodes (8): LLMProvider, MockLLMProvider, OpenAIProvider, LLMService, test_llm_service_failover_chain(), test_llm_service_with_explicit_provider(), test_mock_llm_provider(), test_openai_provider_missing_key()

### Community 10 - "job.py"
Cohesion: 0.10
Nodes (8): _clean_html(), _detect_location_type(), _parse_iso_date(), _unescape_greenhouse_content(), test_greenhouse_fetch_string_slug(), test_greenhouse_fetch_with_mock_client(), handler(), test_greenhouse_http_error()

### Community 11 - "Base"
Cohesion: 0.09
Nodes (10): _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), test_freehire_bearer_auth(), test_freehire_fetch_data_normalization(), handler(), test_freehire_http_error() (+2 more)

### Community 12 - "AdzunaJobSource"
Cohesion: 0.09
Nodes (11): _clean_html(), _format_salary(), _parse_date(), RemoteOKJobSource, test_remoteok_empty_results(), test_remoteok_fetch_dict_query(), test_remoteok_fetch_string_query(), test_remoteok_fetch_with_mock_client() (+3 more)

### Community 13 - "api/interview.py"
Cohesion: 0.10
Nodes (19): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_llm_service(), get_monitor_summary() (+11 more)

### Community 14 - "seed.py"
Cohesion: 0.15
Nodes (11): seed_initial_data(), CvTemplate, CompensationExpectation, SpokenLanguage, TargetDesignation, TargetLocation, Entitlement, test_multi_tenant_cascade_deletes() (+3 more)

### Community 15 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (8): Integration Checklist, Job Source Integrator, JobPosting, LinkedInJobSource, _strip_tags(), test_trigger_ingestion_endpoint(), fetch(), test_linkedin_job_source_parser()

### Community 16 - "LeverJobSource"
Cohesion: 0.15
Nodes (8): Application, Job, test_application_status_update(), test_applications_multi_tenant_isolation(), test_follow_up_draft_and_cap_enforcement(), test_monitor_summary_view(), test_tailor_and_send_application_lifecycle(), test_application_model_and_human_in_the_loop_gate()

### Community 17 - "test_profile.py"
Cohesion: 0.11
Nodes (8): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), test_lever_fetch_string_slug(), test_lever_fetch_with_mock_client(), handler(), test_lever_http_error()

### Community 18 - "Account"
Cohesion: 0.11
Nodes (9): _clean_html(), _parse_publication_date(), RemotiveJobSource, test_remotive_empty_results(), test_remotive_fetch_dict_query(), test_remotive_fetch_string_query(), test_remotive_fetch_with_mock_client(), handler() (+1 more)

### Community 19 - "test_matching.py"
Cohesion: 0.11
Nodes (15): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+7 more)

### Community 20 - "MatchingService"
Cohesion: 0.14
Nodes (4): EmbeddingClient, get_embedding_client(), MockEmbeddingClient, OpenAIEmbeddingClient

### Community 22 - "job_ingestion.py"
Cohesion: 0.12
Nodes (8): test_default_exclusion_behavior(), test_override_include_flagged(), test_override_include_vetoed(), test_override_show_all(), test_pagination_limit_and_offset(), test_response_fields_contract(), test_sort_order_match_score_descending(), test_unversioned_root_jobs_route_is_not_exposed()

### Community 23 - "job.py"
Cohesion: 0.16
Nodes (6): JobSource, JobSourceConfigError, JobSourceError, JobSourceHTTPError, GreenhouseJobSource, get_available_sources()

### Community 24 - "client"
Cohesion: 0.47
Nodes (3): account_a(), account_b(), client()

### Community 25 - "test_applications.py"
Cohesion: 0.13
Nodes (5): upgrade(), upgrade(), downgrade(), upgrade(), upgrade()

### Community 26 - "test_matching.py"
Cohesion: 0.18
Nodes (5): compute_cosine_similarity(), db_session(), test_account(), test_compute_cosine_similarity(), test_get_embedding_client_factory()

### Community 27 - "Architecture — Job Application Agent SaaS"
Cohesion: 0.11
Nodes (18): 0. Design principle: "missing puzzle piece", 10. Hosting (OPEN — still genuinely undecided), 11. LLM provider strategy (confirmed), 12. Payments (research complete — decision still yours to make), 13. SaaS-only concerns still ahead (Phase 3+), 14. Decision log, 1. Scope & rollout, 2. Priority build order (confirmed) (+10 more)

### Community 28 - "test_multi_tenant_isolation_never_leaks_cross_account_data"
Cohesion: 0.21
Nodes (4): LanguageGate, test_language_gate_declared_language_allowed(), test_language_gate_english_clean(), test_language_gate_veto_undeclared_language()

### Community 29 - "MatchingService"
Cohesion: 0.12
Nodes (6): ProfileParser, MatchingService, test_matching_service_embed_and_upsert_qdrant(), test_matching_service_score_and_gate_clean_jobs(), test_profile_parser_cv_and_profile_extraction(), test_profile_parser_default_language_fallback()

### Community 31 - "test_interview.py"
Cohesion: 0.15
Nodes (6): test_create_and_get_story(), test_filter_stories_by_verification_and_tag(), test_interview_multi_tenant_isolation(), test_list_stories_empty(), test_list_tags(), test_update_and_delete_story()

### Community 33 - "User Profile — Niloy Sannyal"
Cohesion: 0.12
Nodes (16): Adaptability, Basic info, Facts that require confirmation before use (never invent these), Hobbies & personal interests, Interview story bank (STAR format), Job search logistics, Positioning & narrative, Reasons for leaving current role (+8 more)

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 35 - "test_admin.py"
Cohesion: 0.16
Nodes (15): get_current_account(), admin_client(), override_current_account(), override_get_db(), admin_test_db(), regular_tenant_account(), superadmin_account(), tenant_client() (+7 more)

### Community 40 - "Base"
Cohesion: 0.12
Nodes (13): Base, get_db(), get_engine(), get_session_factory(), create_app(), lifespan(), api_test_db(), client() (+5 more)

### Community 42 - "Research — Competitors, APIs, and Legal Notes"
Cohesion: 0.18
Nodes (10): Addendum (2026-10-04): Job sourcing & payments research, Addendum (2026-10-18): ai-job-search-dev/ai-job-search (MIT, 64k stars), Competitor landscape (auto-apply / job-search AI tools), Job data sourcing — legal layering (feeds ARCHITECTURE.md §4), Legal job-data API options to evaluate, Legal / ToS notes (OPEN — verify current terms before building), Open research tasks, Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12) (+2 more)

### Community 43 - "Features & Views"
Cohesion: 0.20
Nodes (9): 1. Dashboard (`DashboardView.jsx`), 2. Jobs Queue (`JobsView.jsx`), 3. Application Studio (`ApplicationStudio.jsx`), 4. Pipeline Application Monitor (`PipelineView.jsx`), 5. STAR Interview Coach (`InterviewCoachView.jsx`), 6. Profile & Dealbreakers (`ProfileView.jsx`), Development Setup, Features & Views (+1 more)

### Community 44 - "Account"
Cohesion: 0.14
Nodes (34): create_admin_template(), create_llm_provider(), create_tenant(), delete_admin_template(), delete_llm_provider(), delete_tenant(), get_job_sources(), get_platform_metrics() (+26 more)

### Community 45 - "UserProfile"
Cohesion: 0.20
Nodes (10): delete_designation(), delete_language(), delete_location(), get_compensation(), get_current_account(), get_profile(), list_designations(), list_languages() (+2 more)

### Community 46 - "Local setup"
Cohesion: 0.22
Nodes (8): 1. Backend Setup, 2. Frontend Setup, 3. Tests, 4. Codebase Knowledge Graph (Graphify), Current status, Docs index, Job Application Agent SaaS, Local setup

### Community 47 - "Agent Behavior Rules — Job Application Agent SaaS"
Cohesion: 0.25
Nodes (7): Agent Behavior Rules — Job Application Agent SaaS, Code conventions, Database & migrations, Folder structure — put new code in the right place, Interfaces to honor, not bypass, What NOT to build without being asked, When to stop and ask instead of proceeding

### Community 48 - "test_multi_tenant_isolation_never_leaks_cross_account_data"
Cohesion: 0.18
Nodes (5): client(), seeded_accounts(), seeded_jobs(), test_db(), test_multi_tenant_isolation_never_leaks_cross_account_data()

### Community 49 - "Job Application Agent — Original Idea (transcribed from notebook)"
Cohesion: 0.25
Nodes (7): General flow (manual, today), Job Application Agent — Original Idea (transcribed from notebook), Open questions from the original sketch (carried into ARCHITECTURE.md), Step 1 — Find Job Opportunity, Step 2 — Apply for the Job, Step 3 — Monitor Job Applications, The solution: 3 major tasks

### Community 50 - "Non-Negotiable Rules"
Cohesion: 0.29
Nodes (6): 1. Never Invent Facts, 2. LaTeX Syntax & Preamble Preservation, 3. Relevance-Weighted Trimming & Page Budget, 4. PDF Verification & ATS Text-Layer Check, CV Tailoring Guard, Non-Negotiable Rules

### Community 51 - "JobBase"
Cohesion: 0.50
Nodes (3): JobBase, JobCreate, JobUpdate

### Community 52 - "Project: Job Application Agent SaaS"
Cohesion: 0.29
Nodes (6): Current priority (per ROADMAP.md Phase 0 → 1), Non-negotiables (do not redesign these without being asked), Project: Job Application Agent SaaS, Read these before writing code, Tech stack (decided, don't re-propose alternatives), What this is

### Community 53 - "Roadmap — Job Application Agent SaaS"
Cohesion: 0.33
Nodes (5): Decision log, Phase 1 — Personal validation (the "1 month with my own data" period), Phase 2 — Expand job sourcing + add paying-user groundwork, Phase 3 — Open signups / SaaS launch, Roadmap — Job Application Agent SaaS

### Community 55 - "test_models.py"
Cohesion: 0.12
Nodes (12): AccountCreate, ApplicationCreate, CvTemplateCreate, LLMProviderCreate, db_session(), test_account_model(), test_cv_template_and_version_models(), test_job_model_matching_architecture_spec() (+4 more)

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `JobPosting` connect `RemotiveJobSource` to `models/__init__.py`, `App.jsx`, `models/__init__.py`, `applications.py`, `Base`, `job.py`, `Base`, `AdzunaJobSource`, `test_profile.py`, `Account`, `JobBase`, `typing`, `test_models.py`, `job.py`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `Account` (e.g. with `create_admin_template()` and `create_llm_provider()`) actually correct?**
  _`Account` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Should `models/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.053998632946001365 - nodes in this community are weakly interconnected._
- **Why does `Account` connect `Account` to `test_cv_tailor.py`, `App.jsx`, `api/profile.py`, `models/__init__.py`, `JobSearchQuery`, `api/interview.py`, `seed.py`, `LeverJobSource`, `test_matching.py`, `job.py`, `client`, `test_matching.py`, `MatchingService`, `test_interview.py`, `test_admin.py`, `Base`, `UserProfile`, `test_multi_tenant_isolation_never_leaks_cross_account_data`, `test_models.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `JobPosting` (e.g. with `Integration Checklist` and `JobIngestionService`) actually correct?**
  _`JobPosting` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Should `typing` be split into smaller, more focused modules?**
  _Cohesion score 0.061458718992965566 - nodes in this community are weakly interconnected._
- **Why does `Job` connect `LeverJobSource` to `test_cv_tailor.py`, `App.jsx`, `test_admin.py`, `models/__init__.py`, `Base`, `Account`, `api/interview.py`, `seed.py`, `test_multi_tenant_isolation_never_leaks_cross_account_data`, `test_matching.py`, `typing`, `test_models.py`, `job.py`, `test_matching.py`, `MatchingService`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
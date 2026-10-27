# Graph Report - job-agent-saas  (2026-10-27)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1037 nodes · 2831 edges · 40 communities (31 shown, 9 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 321 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d16e6717`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/__init__.py
- typing
- run_posting_guard
- App.jsx
- test_job_ingestion.py
- LLMService
- applications.py
- JobSearchQuery
- test_models.py
- RemoteOKJobSource
- job.py
- Base
- AdzunaJobSource
- api/interview.py
- JobPosting
- RemotiveJobSource
- LeverJobSource
- test_profile.py
- Account
- test_matching.py
- MatchingService
- TestClient
- job_ingestion.py
- jobs.py
- LinkedInJobSource
- test_applications.py
- config.py
- LanguageGate
- test_multi_tenant_isolation_never_leaks_cross_account_data
- OpenAIEmbeddingClient
- Settings
- MockQdrantClient
- MockEmbeddingClient
- .oxlintrc.json
- tests/api/__init__.py

## God Nodes (most connected - your core abstractions)
1. `JobPosting` - 73 edges
2. `Account` - 71 edges
3. `JobSearchQuery` - 62 edges
4. `Job` - 53 edges
5. `Base` - 45 edges
6. `JobSourceHTTPError` - 36 edges
7. `JobSource` - 31 edges
8. `run_posting_guard()` - 30 edges
9. `Application` - 28 edges
10. `TestInstructionDetection` - 23 edges

## Surprising Connections (you probably didn't know these)
- `JobIngestionService` --uses--> `GateResult`  [INFERRED]
  backend/app/services/job_ingestion.py → backend/app/services/posting_guard.py
- `GateResult` --uses--> `JobPosting`  [INFERRED]
  backend/app/services/posting_guard.py → backend/app/models/job.py
- `JobIngestionService` --uses--> `JobPosting`  [INFERRED]
  backend/app/services/job_ingestion.py → backend/app/models/job.py
- `AdzunaJobSource` --uses--> `JobPosting`  [INFERRED]
  backend/app/services/job_sources/adzuna.py → backend/app/models/job.py
- `JobSource` --uses--> `JobPosting`  [INFERRED]
  backend/app/services/job_sources/base.py → backend/app/models/job.py

## Import Cycles
- None detected.

## Communities (40 total, 9 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.06
Nodes (13): FlagKind, GateResult, IntegrityFlag, _is_invisible(), _line_looks_like_instruction(), run_posting_guard(), strip_invisible(), make_posting() (+5 more)

### Community 1 - "typing"
Cohesion: 0.06
Nodes (54): dependencies, jspdf@^4.2.1, lucide-react@^1.61.0, react@^19.3.1, react-dom@^19.3.1, devDependencies, oxlint@^1.88.0, @types/react@^19.3.0 (+46 more)

### Community 2 - "run_posting_guard"
Cohesion: 0.07
Nodes (21): AccountCvVersion, ATSCheckResult, run_ats_text_layer_check(), audit_fact_integrity(), FactAuditResult, check_brace_balance(), escape_latex_special_chars(), extract_preamble_and_body() (+13 more)

### Community 3 - "App.jsx"
Cohesion: 0.07
Nodes (17): IngestionRequest, IngestionResponse, list_jobs(), trigger_ingestion(), IngestionResult, JobIngestionService, db_session(), MockGeneralSource (+9 more)

### Community 4 - "test_job_ingestion.py"
Cohesion: 0.10
Nodes (32): add_designation(), add_language(), add_location(), create_profile(), delete_designation(), delete_language(), delete_location(), get_compensation() (+24 more)

### Community 5 - "LLMService"
Cohesion: 0.12
Nodes (30): AccountBase, AccountCreate, AccountRead, AccountUpdate, ApplicationBase, ApplicationCreate, ApplicationRead, ApplicationUpdate (+22 more)

### Community 6 - "applications.py"
Cohesion: 0.09
Nodes (14): AdzunaJobSource, _clean_text(), _detect_location_type(), _format_salary(), _parse_created_date(), JobSourceConfigError, JobSourceError, JobSourceHTTPError (+6 more)

### Community 7 - "JobSearchQuery"
Cohesion: 0.06
Nodes (20): Account, test_create_and_get_story(), test_filter_stories_by_verification_and_tag(), test_interview_multi_tenant_isolation(), test_list_stories_empty(), test_list_tags(), test_update_and_delete_story(), test_multi_tenant_isolation_never_leaks_cross_account_data() (+12 more)

### Community 8 - "test_models.py"
Cohesion: 0.12
Nodes (12): get_database_url(), run_migrations_offline(), run_migrations_online(), get_db(), get_engine(), get_session_factory(), create_app(), lifespan() (+4 more)

### Community 9 - "RemoteOKJobSource"
Cohesion: 0.10
Nodes (9): LLMProvider, MockLLMProvider, OpenAIProvider, LLMService, client(), test_llm_service_failover_chain(), test_llm_service_with_explicit_provider(), test_mock_llm_provider() (+1 more)

### Community 10 - "job.py"
Cohesion: 0.09
Nodes (12): JobPosting, _clean_html(), _detect_location_type(), GreenhouseJobSource, _parse_iso_date(), _unescape_greenhouse_content(), test_trigger_ingestion_endpoint(), fetch() (+4 more)

### Community 11 - "Base"
Cohesion: 0.11
Nodes (11): JobSearchQuery, _clean_html(), _detect_location_type(), FreehireJobSource, _parse_iso_date(), test_freehire_bearer_auth(), test_freehire_fetch_data_normalization(), handler() (+3 more)

### Community 12 - "AdzunaJobSource"
Cohesion: 0.10
Nodes (11): _clean_html(), _format_salary(), _parse_date(), RemoteOKJobSource, test_remoteok_empty_results(), test_remoteok_fetch_dict_query(), test_remoteok_fetch_string_query(), test_remoteok_fetch_with_mock_client() (+3 more)

### Community 13 - "api/interview.py"
Cohesion: 0.08
Nodes (13): draft_follow_up(), evaluate_job_fit(), FitDimension, FitEvaluationRequest, FitEvaluationResponse, FollowUpDraftResponse, get_monitor_summary(), list_applications() (+5 more)

### Community 14 - "JobPosting"
Cohesion: 0.12
Nodes (15): Base, seed_initial_data(), CvTemplate, StarStory, CompensationExpectation, SpokenLanguage, TargetDesignation, TargetLocation (+7 more)

### Community 15 - "RemotiveJobSource"
Cohesion: 0.10
Nodes (5): JobSource, get_available_sources(), LinkedInJobSource, _strip_tags(), test_linkedin_job_source_parser()

### Community 16 - "LeverJobSource"
Cohesion: 0.11
Nodes (14): get_llm_service(), tailor_application(), TailorRequest, TailorResponse, Application, AccountCvVersionRead, Job, test_application_status_update() (+6 more)

### Community 17 - "test_profile.py"
Cohesion: 0.11
Nodes (8): _clean_html(), _detect_location_type(), LeverJobSource, _parse_created_at(), test_lever_fetch_string_slug(), test_lever_fetch_with_mock_client(), handler(), test_lever_http_error()

### Community 18 - "Account"
Cohesion: 0.11
Nodes (9): _clean_html(), _parse_publication_date(), RemotiveJobSource, test_remotive_empty_results(), test_remotive_fetch_dict_query(), test_remotive_fetch_string_query(), test_remotive_fetch_with_mock_client(), handler() (+1 more)

### Community 19 - "test_matching.py"
Cohesion: 0.14
Nodes (14): create_story(), delete_story(), generate_interview_prep(), get_story(), InterviewPrepRequest, InterviewPrepResponse, list_stories(), list_tags() (+6 more)

### Community 20 - "MatchingService"
Cohesion: 0.11
Nodes (4): EmbeddingClient, get_embedding_client(), OpenAIEmbeddingClient, test_openai_embedding_client()

### Community 21 - "TestClient"
Cohesion: 0.19
Nodes (5): LanguageGate, ParsedProfile, ProfileParser, MatchingResult, MatchingService

### Community 22 - "job_ingestion.py"
Cohesion: 0.12
Nodes (8): test_default_exclusion_behavior(), test_override_include_flagged(), test_override_include_vetoed(), test_override_show_all(), test_pagination_limit_and_offset(), test_response_fields_contract(), test_sort_order_match_score_descending(), test_unversioned_root_jobs_route_is_not_exposed()

### Community 24 - "LinkedInJobSource"
Cohesion: 0.19
Nodes (4): MockEmbeddingClient, test_account(), test_matching_service_embed_and_upsert_qdrant(), test_matching_service_score_and_gate_clean_jobs()

### Community 25 - "test_applications.py"
Cohesion: 0.17
Nodes (4): upgrade(), downgrade(), upgrade(), upgrade()

### Community 26 - "config.py"
Cohesion: 0.22
Nodes (4): compute_cosine_similarity(), db_session(), test_compute_cosine_similarity(), test_get_embedding_client_factory()

### Community 27 - "LanguageGate"
Cohesion: 0.22
Nodes (4): client(), seeded_accounts(), seeded_jobs(), test_db()

### Community 28 - "test_multi_tenant_isolation_never_leaks_cross_account_data"
Cohesion: 0.20
Nodes (3): test_language_gate_declared_language_allowed(), test_language_gate_english_clean(), test_language_gate_veto_undeclared_language()

### Community 29 - "OpenAIEmbeddingClient"
Cohesion: 0.36
Nodes (4): JobBase, JobCreate, JobRead, JobUpdate

### Community 31 - "MockQdrantClient"
Cohesion: 0.38
Nodes (4): account_a(), account_b(), api_test_db(), client()

### Community 34 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `JobPosting` connect `job.py` to `models/__init__.py`, `App.jsx`, `LLMService`, `applications.py`, `test_models.py`, `Base`, `AdzunaJobSource`, `RemotiveJobSource`, `test_profile.py`, `Account`, `TestClient`, `OpenAIEmbeddingClient`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `JobPosting` (e.g. with `JobIngestionService` and `AdzunaJobSource`) actually correct?**
  _`JobPosting` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Should `models/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05859969558599695 - nodes in this community are weakly interconnected._
- **Why does `Account` connect `JobSearchQuery` to `run_posting_guard`, `App.jsx`, `test_job_ingestion.py`, `LLMService`, `test_models.py`, `JobPosting`, `LeverJobSource`, `LinkedInJobSource`, `config.py`, `LanguageGate`, `OpenAIEmbeddingClient`, `MockQdrantClient`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Account` (e.g. with `tailor_application()` and `account_a()`) actually correct?**
  _`Account` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Should `typing` be split into smaller, more focused modules?**
  _Cohesion score 0.05829420970266041 - nodes in this community are weakly interconnected._
- **Why does `Job` connect `LeverJobSource` to `run_posting_guard`, `App.jsx`, `LLMService`, `JobSearchQuery`, `test_models.py`, `api/interview.py`, `JobPosting`, `test_matching.py`, `TestClient`, `jobs.py`, `LinkedInJobSource`, `config.py`, `LanguageGate`, `OpenAIEmbeddingClient`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
# Account

> God node · 70 connections · `backend/app/models/account.py`

**Community:** [Account](Account.md)

## Connections by Relation

### calls
- seed_initial_data() `EXTRACTED`
- test_user_profile_and_relations() `EXTRACTED`
- test_multi_tenant_cascade_deletes() `EXTRACTED`
- test_application_status_update() `EXTRACTED`
- test_follow_up_draft_and_cap_enforcement() `EXTRACTED`
- test_monitor_summary_view() `EXTRACTED`
- test_cv_template_and_version_models() `EXTRACTED`
- test_applications_multi_tenant_isolation() `EXTRACTED`
- test_tailor_and_send_application_lifecycle() `EXTRACTED`
- test_multi_tenant_isolation_never_leaks_cross_account_data() `EXTRACTED`
- test_application_model_and_human_in_the_loop_gate() `EXTRACTED`
- test_subscription_plans_and_entitlements() `EXTRACTED`
- test_job_model_matching_architecture_spec() `EXTRACTED`
- test_star_story_model() `EXTRACTED`
- test_account_model() `EXTRACTED`

### contains
- account.py `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_models.py](test_models.py.md) `EXTRACTED`
- [job.py](job.py.md) `EXTRACTED`
- [applications.py](applications.py.md) `EXTRACTED`
- models/profile.py `EXTRACTED`
- [test_matching.py](test_matching.py.md) `EXTRACTED`
- test_cv_tailor.py `EXTRACTED`
- tailor_service.py `EXTRACTED`
- [test_profile.py](test_profile.py.md) `EXTRACTED`
- test_jobs.py `EXTRACTED`
- [test_applications.py](test_applications.py.md) `EXTRACTED`
- cv_template.py `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- test_interview.py `EXTRACTED`
- seed.py `EXTRACTED`
- application.py `EXTRACTED`
- subscription.py `EXTRACTED`
- models/interview.py `EXTRACTED`
- llm_provider.py `EXTRACTED`

### inherits
- [Base](Base.md) `EXTRACTED`

### rationale_for
- Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an… `EXTRACTED`

### uses
- tailor_application() `INFERRED`
- test_ingest_source_routing_and_persistence() `INFERRED`
- test_matching_service_embed_and_upsert_qdrant() `INFERRED`
- test_matching_service_score_and_gate_clean_jobs() `INFERRED`
- test_ingest_automatically_runs_matching_and_gating() `INFERRED`
- test_seed_initial_data() `INFERRED`
- test_ingest_deduplication() `INFERRED`
- test_ingest_resilience_to_source_errors() `INFERRED`
- test_ingest_runs_posting_integrity_gate() `INFERRED`
- test_ingest_target_company_exact_matching() `INFERRED`
- test_cv_tailor_service_end_to_end() `INFERRED`
- test_ingest_multi_tenant_isolation() `INFERRED`
- test_create_and_get_story() `INFERRED`
- test_account() `INFERRED`
- test_account() `INFERRED`
- seeded_accounts() `INFERRED`
- test_filter_stories_by_verification_and_tag() `INFERRED`
- test_interview_multi_tenant_isolation() `INFERRED`
- test_list_stories_empty() `INFERRED`
- test_list_tags() `INFERRED`
- *…and 13 more `uses` connection(s) not listed (lowest-degree first to go)*

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
# Job

> God node · 53 connections · `backend/app/models/job.py`

**Community:** [test_models.py](test_models.py.md)

## Connections by Relation

### calls
- .ingest() `EXTRACTED`
- test_multi_tenant_cascade_deletes() `EXTRACTED`
- test_application_status_update() `EXTRACTED`
- test_follow_up_draft_and_cap_enforcement() `EXTRACTED`
- test_monitor_summary_view() `EXTRACTED`
- test_cv_template_and_version_models() `EXTRACTED`
- test_applications_multi_tenant_isolation() `EXTRACTED`
- test_tailor_and_send_application_lifecycle() `EXTRACTED`
- test_multi_tenant_isolation_never_leaks_cross_account_data() `EXTRACTED`
- test_application_model_and_human_in_the_loop_gate() `EXTRACTED`
- test_job_model_matching_architecture_spec() `EXTRACTED`

### contains
- [job.py](job.py.md) `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_models.py](test_models.py.md) `EXTRACTED`
- [applications.py](applications.py.md) `EXTRACTED`
- account.py `EXTRACTED`
- [test_matching.py](test_matching.py.md) `EXTRACTED`
- test_cv_tailor.py `EXTRACTED`
- tailor_service.py `EXTRACTED`
- test_jobs.py `EXTRACTED`
- [test_applications.py](test_applications.py.md) `EXTRACTED`
- cv_template.py `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- [api/interview.py](api-interview.py.md) `EXTRACTED`
- application.py `EXTRACTED`
- [job_ingestion.py](job_ingestion.py.md) `EXTRACTED`
- matching/service.py `EXTRACTED`
- [jobs.py](jobs.py.md) `EXTRACTED`

### inherits
- [Base](Base.md) `EXTRACTED`

### method
- .title() `EXTRACTED`

### rationale_for
- Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,… `EXTRACTED`

### references
- .tailor_for_job() `EXTRACTED`
- .score_and_gate_jobs() `EXTRACTED`

### uses
- JobIngestionService `INFERRED`
- [MatchingService](MatchingService.md) `INFERRED`
- CVTailorService `INFERRED`
- tailor_application() `INFERRED`
- test_ingest_source_routing_and_persistence() `INFERRED`
- generate_interview_prep() `INFERRED`
- test_matching_service_score_and_gate_clean_jobs() `INFERRED`
- test_ingest_automatically_runs_matching_and_gating() `INFERRED`
- evaluate_job_fit() `INFERRED`
- test_cv_tailor_service_end_to_end() `INFERRED`
- test_ingest_deduplication() `INFERRED`
- test_ingest_multi_tenant_isolation() `INFERRED`
- test_ingest_runs_posting_integrity_gate() `INFERRED`
- test_ingest_target_company_exact_matching() `INFERRED`
- draft_follow_up() `INFERRED`
- update_application_status() `INFERRED`
- IngestionResult `INFERRED`
- mark_application_sent() `INFERRED`
- list_jobs() `INFERRED`
- seeded_jobs() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
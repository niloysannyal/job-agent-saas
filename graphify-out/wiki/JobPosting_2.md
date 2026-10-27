# JobPosting

> God node · 73 connections · `backend/app/models/job.py`

**Community:** [JobPosting](JobPosting.md)

## Connections by Relation

### calls
- make_posting() `EXTRACTED`
- test_pydantic_schemas() `EXTRACTED`
- test_trigger_ingestion_endpoint() `EXTRACTED`
- fetch() `EXTRACTED`

### contains
- [job.py](job.py.md) `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_models.py](test_models.py.md) `EXTRACTED`
- test_jobs.py `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- [job_ingestion.py](job_ingestion.py.md) `EXTRACTED`
- adzuna.py `EXTRACTED`
- greenhouse.py `EXTRACTED`
- linkedin.py `EXTRACTED`
- freehire.py `EXTRACTED`
- lever.py `EXTRACTED`
- remoteok.py `EXTRACTED`
- posting_guard.py `EXTRACTED`
- job_sources/base.py `EXTRACTED`
- remotive.py `EXTRACTED`
- test_adzuna.py `EXTRACTED`
- test_remoteok.py `EXTRACTED`
- test_posting_guard.py `EXTRACTED`
- test_freehire.py `EXTRACTED`
- test_remotive.py `EXTRACTED`
- test_greenhouse.py `EXTRACTED`
- *…and 1 more `imports` connection(s) not listed (lowest-degree first to go)*

### inherits
- BaseModel `EXTRACTED`

### rationale_for
- Standardized JobPosting DTO returned by all JobSource.fetch implementations.… `EXTRACTED`

### references
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- .fetch() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- .fetch() `EXTRACTED`
- ._parse_job_cards() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [JobSource](JobSource.md) `INFERRED`
- [run_posting_guard()](run_posting_guard_2.md) `INFERRED`
- JobIngestionService `INFERRED`
- [AdzunaJobSource](AdzunaJobSource.md) `INFERRED`
- FreehireJobSource `INFERRED`
- [RemoteOKJobSource](RemoteOKJobSource.md) `INFERRED`
- [RemotiveJobSource](RemotiveJobSource.md) `INFERRED`
- [LeverJobSource](LeverJobSource.md) `INFERRED`
- GreenhouseJobSource `INFERRED`
- MockGeneralSource `INFERRED`
- [LinkedInJobSource](LinkedInJobSource.md) `INFERRED`
- test_ingest_source_routing_and_persistence() `INFERRED`
- GateResult `INFERRED`
- test_ingest_automatically_runs_matching_and_gating() `INFERRED`
- test_ingest_deduplication() `INFERRED`
- test_ingest_multi_tenant_isolation() `INFERRED`
- test_ingest_resilience_to_source_errors() `INFERRED`
- test_ingest_runs_posting_integrity_gate() `INFERRED`
- test_ingest_target_company_exact_matching() `INFERRED`
- MockPerCompanySource `INFERRED`
- *…and 6 more `uses` connection(s) not listed (lowest-degree first to go)*

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
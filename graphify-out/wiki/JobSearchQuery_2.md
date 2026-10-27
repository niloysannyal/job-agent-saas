# JobSearchQuery

> God node · 62 connections · `backend/app/models/job.py`

**Community:** [JobSearchQuery](JobSearchQuery.md)

## Connections by Relation

### contains
- [job.py](job.py.md) `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- [job_ingestion.py](job_ingestion.py.md) `EXTRACTED`
- [jobs.py](jobs.py.md) `EXTRACTED`
- adzuna.py `EXTRACTED`
- greenhouse.py `EXTRACTED`
- linkedin.py `EXTRACTED`
- freehire.py `EXTRACTED`
- lever.py `EXTRACTED`
- remoteok.py `EXTRACTED`
- job_sources/base.py `EXTRACTED`
- remotive.py `EXTRACTED`
- test_adzuna.py `EXTRACTED`
- test_remoteok.py `EXTRACTED`
- test_freehire.py `EXTRACTED`
- test_remotive.py `EXTRACTED`
- test_greenhouse.py `EXTRACTED`
- test_lever.py `EXTRACTED`
- test_linkedin_source.py `EXTRACTED`

### inherits
- BaseModel `EXTRACTED`

### rationale_for
- Normalized query parameters for searching across job sources. `EXTRACTED`

### references
- .ingest() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .normalize_query() `EXTRACTED`
- ._parse_results() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- ._normalize_queries() `EXTRACTED`
- .fetch() `EXTRACTED`
- ._build_url_and_params() `EXTRACTED`
- ._build_params() `EXTRACTED`
- ._build_params() `EXTRACTED`
- ._build_params() `EXTRACTED`

### uses
- [JobSource](JobSource.md) `INFERRED`
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
- MockPerCompanySource `INFERRED`
- test_adzuna_fetch_with_mock_client() `INFERRED`
- test_freehire_bearer_auth() `INFERRED`
- test_freehire_fetch_data_normalization() `INFERRED`
- test_freehire_offset_from_page() `INFERRED`
- test_freehire_query_filters() `INFERRED`
- test_greenhouse_fetch_with_mock_client() `INFERRED`
- test_lever_fetch_with_mock_client() `INFERRED`
- test_remoteok_fetch_with_mock_client() `INFERRED`
- *…and 2 more `uses` connection(s) not listed (lowest-degree first to go)*

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
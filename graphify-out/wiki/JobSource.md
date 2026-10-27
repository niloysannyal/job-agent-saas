# JobSource

> God node · 31 connections · `backend/app/services/job_sources/base.py`

**Community:** [job.py](job.py.md)

## Connections by Relation

### contains
- job_sources/base.py `EXTRACTED`

### imports
- test_jobs.py `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- job_sources/__init__.py `EXTRACTED`
- [job_ingestion.py](job_ingestion.py.md) `EXTRACTED`
- adzuna.py `EXTRACTED`
- greenhouse.py `EXTRACTED`
- linkedin.py `EXTRACTED`
- freehire.py `EXTRACTED`
- lever.py `EXTRACTED`
- remoteok.py `EXTRACTED`
- remotive.py `EXTRACTED`

### inherits
- [AdzunaJobSource](AdzunaJobSource.md) `EXTRACTED`
- FreehireJobSource `EXTRACTED`
- [RemoteOKJobSource](RemoteOKJobSource.md) `EXTRACTED`
- [RemotiveJobSource](RemotiveJobSource.md) `EXTRACTED`
- [LeverJobSource](LeverJobSource.md) `EXTRACTED`
- GreenhouseJobSource `EXTRACTED`
- MockGeneralSource `EXTRACTED`
- [LinkedInJobSource](LinkedInJobSource.md) `EXTRACTED`
- MockPerCompanySource `EXTRACTED`
- ABC `EXTRACTED`

### method
- .normalize_query() `EXTRACTED`
- .fetch() `EXTRACTED`

### rationale_for
- Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:… `EXTRACTED`

### references
- .ingest() `EXTRACTED`

### uses
- [JobPosting](JobPosting.md) `INFERRED`
- [JobSearchQuery](JobSearchQuery.md) `INFERRED`
- JobIngestionService `INFERRED`
- get_available_sources() `INFERRED`
- test_trigger_ingestion_endpoint() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
# test_job_ingestion.py

> 51 nodes · cohesion 0.07

## Key Concepts

- **test_job_ingestion.py** (29 connections) — `backend/tests/services/test_job_ingestion.py`
- **JobIngestionService** (23 connections) — `backend/app/services/job_ingestion.py`
- **.ingest()** (19 connections) — `backend/app/services/job_ingestion.py`
- **MockGeneralSource** (14 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_source_routing_and_persistence()** (12 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_automatically_runs_matching_and_gating()** (11 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_deduplication()** (10 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_multi_tenant_isolation()** (10 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_resilience_to_source_errors()** (10 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_runs_posting_integrity_gate()** (10 connections) — `backend/tests/services/test_job_ingestion.py`
- **test_ingest_target_company_exact_matching()** (10 connections) — `backend/tests/services/test_job_ingestion.py`
- **trigger_ingestion()** (9 connections) — `backend/app/api/jobs.py`
- **MockPerCompanySource** (9 connections) — `backend/tests/services/test_job_ingestion.py`
- **Session** (8 connections)
- **asyncio** (7 connections)
- **list_jobs()** (6 connections) — `backend/app/api/jobs.py`
- **IngestionRequest** (5 connections) — `backend/app/api/jobs.py`
- **test_account()** (5 connections) — `backend/tests/services/test_job_ingestion.py`
- **IngestionResponse** (4 connections) — `backend/app/api/jobs.py`
- **._normalize_queries()** (4 connections) — `backend/app/services/job_ingestion.py`
- **db_session()** (4 connections) — `backend/tests/services/test_job_ingestion.py`
- **.fetch()** (4 connections) — `backend/tests/services/test_job_ingestion.py`
- **.__init__()** (3 connections) — `backend/app/services/job_ingestion.py`
- **BaseModel** (2 connections)
- **Session** (2 connections)
- *... and 26 more nodes in this community*

## Relationships

- [JobPosting](JobPosting.md) (14 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (11 shared connections)
- [test_models.py](test_models.py.md) (10 shared connections)
- [job.py](job.py.md) (9 shared connections)
- [Account](Account.md) (9 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (6 shared connections)
- [Base](Base.md) (6 shared connections)
- [jobs.py](jobs.py.md) (5 shared connections)
- [run_posting_guard](run_posting_guard.md) (3 shared connections)
- [MatchingService](MatchingService.md) (2 shared connections)
- [models/__init__.py](models-__init__.py.md) (1 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (1 shared connections)

## Source Files

- `backend/app/api/jobs.py`
- `backend/app/services/job_ingestion.py`
- `backend/tests/services/test_job_ingestion.py`

## Audit Trail

- EXTRACTED: 116 (68%)
- INFERRED: 54 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
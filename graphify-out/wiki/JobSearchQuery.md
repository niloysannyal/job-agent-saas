# JobSearchQuery

> 39 nodes · cohesion 0.10

## Key Concepts

- **JobSearchQuery** (62 connections) — `backend/app/models/job.py`
- **FreehireJobSource** (19 connections) — `backend/app/services/job_sources/freehire.py`
- **.fetch()** (15 connections) — `backend/app/services/job_sources/freehire.py`
- **test_freehire.py** (15 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **.normalize_query()** (12 connections) — `backend/app/services/job_sources/base.py`
- **test_freehire_bearer_auth()** (8 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **test_freehire_fetch_data_normalization()** (8 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **test_freehire_http_error()** (8 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **test_freehire_offset_from_page()** (8 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **test_freehire_query_filters()** (8 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **._parse_results()** (7 connections) — `backend/app/services/job_sources/freehire.py`
- **.fetch()** (5 connections) — `backend/app/services/job_sources/base.py`
- **asyncio** (5 connections)
- **handler()** (5 connections) — `backend/tests/services/job_sources/test_freehire.py`
- **.fetch()** (5 connections) — `backend/tests/services/test_job_ingestion.py`
- **_clean_html()** (4 connections) — `backend/app/services/job_sources/freehire.py`
- **._build_params()** (4 connections) — `backend/app/services/job_sources/freehire.py`
- **_detect_location_type()** (3 connections) — `backend/app/services/job_sources/freehire.py`
- **Any** (3 connections)
- **Any** (2 connections)
- **._build_headers()** (2 connections) — `backend/app/services/job_sources/freehire.py`
- **.__init__()** (2 connections) — `backend/app/services/job_sources/freehire.py`
- **Normalized query parameters for searching across job sources.** (1 connections) — `backend/app/models/job.py`
- **Asynchronously fetch job postings matching the query. IMPORTANT CALLER BEHAVIOR…** (1 connections) — `backend/app/services/job_sources/base.py`
- **Helper method to normalize search input into a JobSearchQuery instance.** (1 connections) — `backend/app/services/job_sources/base.py`
- *... and 14 more nodes in this community*

## Relationships

- [job.py](job.py.md) (32 shared connections)
- [JobPosting](JobPosting.md) (12 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (11 shared connections)
- [AdzunaJobSource](AdzunaJobSource.md) (6 shared connections)
- [RemoteOKJobSource](RemoteOKJobSource.md) (6 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (5 shared connections)
- [RemotiveJobSource](RemotiveJobSource.md) (5 shared connections)
- [LeverJobSource](LeverJobSource.md) (4 shared connections)
- [jobs.py](jobs.py.md) (1 shared connections)
- [models/__init__.py](models-__init__.py.md) (1 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (1 shared connections)
- [typing](typing.md) (1 shared connections)

## Source Files

- `backend/app/models/job.py`
- `backend/app/services/job_sources/base.py`
- `backend/app/services/job_sources/freehire.py`
- `backend/tests/services/job_sources/test_freehire.py`
- `backend/tests/services/test_job_ingestion.py`

## Audit Trail

- EXTRACTED: 115 (74%)
- INFERRED: 41 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
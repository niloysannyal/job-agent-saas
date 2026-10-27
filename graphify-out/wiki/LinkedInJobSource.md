# LinkedInJobSource

> 16 nodes · cohesion 0.16

## Key Concepts

- **LinkedInJobSource** (13 connections) — `backend/app/services/job_sources/linkedin.py`
- **get_available_sources()** (12 connections) — `backend/app/services/job_sources/__init__.py`
- **.fetch()** (7 connections) — `backend/app/services/job_sources/linkedin.py`
- **test_linkedin_source.py** (7 connections) — `backend/tests/services/test_linkedin_source.py`
- **._parse_job_cards()** (5 connections) — `backend/app/services/job_sources/linkedin.py`
- **_strip_tags()** (5 connections) — `backend/app/services/job_sources/linkedin.py`
- **test_linkedin_job_source_parser()** (4 connections) — `backend/tests/services/test_linkedin_source.py`
- **._fetch_html_with_backoff()** (2 connections) — `backend/app/services/job_sources/linkedin.py`
- **.__init__()** (2 connections) — `backend/app/services/job_sources/linkedin.py`
- **Return instantiated JobSource instances based on requested names or all…** (1 connections) — `backend/app/services/job_sources/__init__.py`
- **Any** (1 connections)
- **AsyncClient** (1 connections)
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/linkedin.py`
- **LinkedIn public guest API implementation of the JobSource interface…** (1 connections) — `backend/app/services/job_sources/linkedin.py`
- **asyncio** (1 connections)
- **unittest_mock** (1 connections)

## Relationships

- [job.py](job.py.md) (10 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (5 shared connections)
- [JobPosting](JobPosting.md) (4 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (1 shared connections)
- [AdzunaJobSource](AdzunaJobSource.md) (1 shared connections)
- [RemotiveJobSource](RemotiveJobSource.md) (1 shared connections)
- [RemoteOKJobSource](RemoteOKJobSource.md) (1 shared connections)
- [LeverJobSource](LeverJobSource.md) (1 shared connections)
- [jobs.py](jobs.py.md) (1 shared connections)
- [typing](typing.md) (1 shared connections)

## Source Files

- `backend/app/services/job_sources/__init__.py`
- `backend/app/services/job_sources/linkedin.py`
- `backend/tests/services/test_linkedin_source.py`

## Audit Trail

- EXTRACTED: 40 (89%)
- INFERRED: 5 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
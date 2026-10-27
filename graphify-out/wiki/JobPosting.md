# JobPosting

> 32 nodes · cohesion 0.09

## Key Concepts

- **JobPosting** (73 connections) — `backend/app/models/job.py`
- **GreenhouseJobSource** (16 connections) — `backend/app/services/job_sources/greenhouse.py`
- **.fetch()** (12 connections) — `backend/app/services/job_sources/greenhouse.py`
- **._parse_results()** (8 connections) — `backend/app/services/job_sources/greenhouse.py`
- **test_greenhouse_fetch_with_mock_client()** (8 connections) — `backend/tests/services/job_sources/test_greenhouse.py`
- **test_greenhouse_http_error()** (8 connections) — `backend/tests/services/job_sources/test_greenhouse.py`
- **test_greenhouse_fetch_string_slug()** (7 connections) — `backend/tests/services/job_sources/test_greenhouse.py`
- **BaseModel** (4 connections)
- **_clean_html()** (4 connections) — `backend/app/services/job_sources/greenhouse.py`
- **_parse_iso_date()** (4 connections) — `backend/app/services/job_sources/greenhouse.py`
- **JobUpdate** (3 connections) — `backend/app/models/job.py`
- **_detect_location_type()** (3 connections) — `backend/app/services/job_sources/greenhouse.py`
- **_unescape_greenhouse_content()** (3 connections) — `backend/app/services/job_sources/greenhouse.py`
- **asyncio** (3 connections)
- **handler()** (3 connections) — `backend/tests/services/job_sources/test_greenhouse.py`
- **._build_url()** (2 connections) — `backend/app/services/job_sources/greenhouse.py`
- **.__init__()** (2 connections) — `backend/app/services/job_sources/greenhouse.py`
- **Any** (2 connections)
- **datetime** (2 connections)
- **Standardized JobPosting DTO returned by all JobSource.fetch implementations.…** (1 connections) — `backend/app/models/job.py`
- **AsyncClient** (1 connections)
- **Asynchronously fetch all open job postings for a company from Greenhouse. Pass…** (1 connections) — `backend/app/services/job_sources/greenhouse.py`
- **Unescape Greenhouse's double-encoded HTML content field. The field is HTML-…** (1 connections) — `backend/app/services/job_sources/greenhouse.py`
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/greenhouse.py`
- **Parse ISO 8601 date string (with optional timezone offset).** (1 connections) — `backend/app/services/job_sources/greenhouse.py`
- *... and 7 more nodes in this community*

## Relationships

- [job.py](job.py.md) (30 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (14 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (12 shared connections)
- [run_posting_guard](run_posting_guard.md) (5 shared connections)
- [RemoteOKJobSource](RemoteOKJobSource.md) (5 shared connections)
- [AdzunaJobSource](AdzunaJobSource.md) (4 shared connections)
- [LeverJobSource](LeverJobSource.md) (4 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (4 shared connections)
- [RemotiveJobSource](RemotiveJobSource.md) (4 shared connections)
- [models/__init__.py](models-__init__.py.md) (3 shared connections)
- [TestClient](TestClient.md) (2 shared connections)
- [Base](Base.md) (2 shared connections)

## Source Files

- `backend/app/models/job.py`
- `backend/app/services/job_sources/greenhouse.py`
- `backend/tests/services/job_sources/test_greenhouse.py`

## Audit Trail

- EXTRACTED: 97 (71%)
- INFERRED: 39 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
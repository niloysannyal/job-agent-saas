# RemoteOKJobSource

> 36 nodes · cohesion 0.10

## Key Concepts

- **RemoteOKJobSource** (19 connections) — `backend/app/services/job_sources/remoteok.py`
- **test_remoteok.py** (16 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **.fetch()** (15 connections) — `backend/app/services/job_sources/remoteok.py`
- **test_remoteok_fetch_with_mock_client()** (8 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **test_remoteok_http_error()** (8 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **._parse_results()** (7 connections) — `backend/app/services/job_sources/remoteok.py`
- **test_remoteok_empty_results()** (7 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **test_remoteok_fetch_dict_query()** (7 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **test_remoteok_fetch_string_query()** (7 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **test_remoteok_legal_notice_only_response()** (7 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **asyncio** (6 connections)
- **handler()** (6 connections) — `backend/tests/services/job_sources/test_remoteok.py`
- **_clean_html()** (4 connections) — `backend/app/services/job_sources/remoteok.py`
- **_parse_date()** (4 connections) — `backend/app/services/job_sources/remoteok.py`
- **._build_params()** (4 connections) — `backend/app/services/job_sources/remoteok.py`
- **_format_salary()** (3 connections) — `backend/app/services/job_sources/remoteok.py`
- **Any** (3 connections)
- **datetime** (2 connections)
- **.__init__()** (2 connections) — `backend/app/services/job_sources/remoteok.py`
- **AsyncClient** (1 connections)
- **Asynchronously fetch remote job postings from RemoteOK matching the query. Maps…** (1 connections) — `backend/app/services/job_sources/remoteok.py`
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/remoteok.py`
- **Parse ISO 8601 date string from RemoteOK (e.g. '2026-10-24T00:00:02+00:00').** (1 connections) — `backend/app/services/job_sources/remoteok.py`
- **Format RemoteOK's numeric salary_min/salary_max into a display string.** (1 connections) — `backend/app/services/job_sources/remoteok.py`
- **RemoteOK API implementation of the JobSource interface (ARCHITECTURE.md §4).…** (1 connections) — `backend/app/services/job_sources/remoteok.py`
- *... and 11 more nodes in this community*

## Relationships

- [job.py](job.py.md) (17 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (6 shared connections)
- [JobPosting](JobPosting.md) (5 shared connections)
- [typing](typing.md) (1 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (1 shared connections)

## Source Files

- `backend/app/services/job_sources/remoteok.py`
- `backend/tests/services/job_sources/test_remoteok.py`

## Audit Trail

- EXTRACTED: 67 (74%)
- INFERRED: 24 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
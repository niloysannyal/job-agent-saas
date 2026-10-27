# RemotiveJobSource

> 30 nodes · cohesion 0.11

## Key Concepts

- **RemotiveJobSource** (18 connections) — `backend/app/services/job_sources/remotive.py`
- **.fetch()** (14 connections) — `backend/app/services/job_sources/remotive.py`
- **test_remotive_fetch_with_mock_client()** (8 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **test_remotive_http_error()** (8 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **test_remotive_empty_results()** (7 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **test_remotive_fetch_dict_query()** (7 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **test_remotive_fetch_string_query()** (7 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **._parse_results()** (6 connections) — `backend/app/services/job_sources/remotive.py`
- **asyncio** (5 connections)
- **handler()** (5 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **_clean_html()** (4 connections) — `backend/app/services/job_sources/remotive.py`
- **_parse_publication_date()** (4 connections) — `backend/app/services/job_sources/remotive.py`
- **._build_params()** (4 connections) — `backend/app/services/job_sources/remotive.py`
- **Any** (3 connections)
- **datetime** (2 connections)
- **.__init__()** (2 connections) — `backend/app/services/job_sources/remotive.py`
- **AsyncClient** (1 connections)
- **Asynchronously fetch remote job postings from Remotive matching the query. Maps…** (1 connections) — `backend/app/services/job_sources/remotive.py`
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/remotive.py`
- **Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC).** (1 connections) — `backend/app/services/job_sources/remotive.py`
- **Remotive API implementation of the JobSource interface (ARCHITECTURE.md §4).…** (1 connections) — `backend/app/services/job_sources/remotive.py`
- **String query is normalized and sent as 'search' param.** (1 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **Dict query is normalized; results_per_page is sent as 'limit'.** (1 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **Non-200 responses raise JobSourceHTTPError.** (1 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **Empty jobs array returns empty list.** (1 connections) — `backend/tests/services/job_sources/test_remotive.py`
- *... and 5 more nodes in this community*

## Relationships

- [job.py](job.py.md) (15 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (5 shared connections)
- [JobPosting](JobPosting.md) (4 shared connections)
- [typing](typing.md) (1 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (1 shared connections)

## Source Files

- `backend/app/services/job_sources/remotive.py`
- `backend/tests/services/job_sources/test_remotive.py`

## Audit Trail

- EXTRACTED: 51 (71%)
- INFERRED: 21 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
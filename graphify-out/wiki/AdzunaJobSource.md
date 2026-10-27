# AdzunaJobSource

> 34 nodes · cohesion 0.09

## Key Concepts

- **AdzunaJobSource** (20 connections) — `backend/app/services/job_sources/adzuna.py`
- **.fetch()** (15 connections) — `backend/app/services/job_sources/adzuna.py`
- **._parse_results()** (9 connections) — `backend/app/services/job_sources/adzuna.py`
- **test_adzuna_fetch_with_mock_client()** (8 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **test_adzuna_http_error()** (8 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **test_adzuna_empty_results()** (7 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **test_adzuna_fetch_query_variations()** (7 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **test_adzuna_missing_credentials()** (6 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **asyncio** (5 connections)
- **._build_url_and_params()** (4 connections) — `backend/app/services/job_sources/adzuna.py`
- **_clean_text()** (4 connections) — `backend/app/services/job_sources/adzuna.py`
- **_parse_created_date()** (4 connections) — `backend/app/services/job_sources/adzuna.py`
- **handler()** (4 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **._validate_credentials()** (3 connections) — `backend/app/services/job_sources/adzuna.py`
- **_detect_location_type()** (3 connections) — `backend/app/services/job_sources/adzuna.py`
- **_format_salary()** (3 connections) — `backend/app/services/job_sources/adzuna.py`
- **Any** (3 connections)
- **.__init__()** (2 connections) — `backend/app/services/job_sources/adzuna.py`
- **datetime** (2 connections)
- **AsyncClient** (1 connections)
- **Asynchronously fetch job postings matching the query from Adzuna.** (1 connections) — `backend/app/services/job_sources/adzuna.py`
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/adzuna.py`
- **Parse ISO formatted creation date from Adzuna response.** (1 connections) — `backend/app/services/job_sources/adzuna.py`
- **Format salary range into a human-readable display string.** (1 connections) — `backend/app/services/job_sources/adzuna.py`
- **Infer location type (remote, hybrid, on-site) from job fields.** (1 connections) — `backend/app/services/job_sources/adzuna.py`
- *... and 9 more nodes in this community*

## Relationships

- [job.py](job.py.md) (20 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (6 shared connections)
- [JobPosting](JobPosting.md) (4 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (1 shared connections)
- [typing](typing.md) (1 shared connections)

## Source Files

- `backend/app/services/job_sources/adzuna.py`
- `backend/tests/services/job_sources/test_adzuna.py`

## Audit Trail

- EXTRACTED: 60 (73%)
- INFERRED: 22 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
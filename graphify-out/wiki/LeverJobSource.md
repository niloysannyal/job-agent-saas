# LeverJobSource

> 27 nodes · cohesion 0.11

## Key Concepts

- **LeverJobSource** (17 connections) — `backend/app/services/job_sources/lever.py`
- **.fetch()** (12 connections) — `backend/app/services/job_sources/lever.py`
- **test_lever_fetch_with_mock_client()** (8 connections) — `backend/tests/services/job_sources/test_lever.py`
- **test_lever_http_error()** (8 connections) — `backend/tests/services/job_sources/test_lever.py`
- **._parse_results()** (7 connections) — `backend/app/services/job_sources/lever.py`
- **test_lever_fetch_string_slug()** (7 connections) — `backend/tests/services/job_sources/test_lever.py`
- **_parse_created_at()** (5 connections) — `backend/app/services/job_sources/lever.py`
- **_clean_html()** (4 connections) — `backend/app/services/job_sources/lever.py`
- **._extract_description()** (4 connections) — `backend/app/services/job_sources/lever.py`
- **Any** (4 connections)
- **_detect_location_type()** (3 connections) — `backend/app/services/job_sources/lever.py`
- **asyncio** (3 connections)
- **handler()** (3 connections) — `backend/tests/services/job_sources/test_lever.py`
- **._build_url()** (2 connections) — `backend/app/services/job_sources/lever.py`
- **.__init__()** (2 connections) — `backend/app/services/job_sources/lever.py`
- **datetime** (2 connections)
- **AsyncClient** (1 connections)
- **Strip HTML tags and normalize whitespace.** (1 connections) — `backend/app/services/job_sources/lever.py`
- **Asynchronously fetch all open job postings for a company from Lever. Pass the…** (1 connections) — `backend/app/services/job_sources/lever.py`
- **Parse createdAt which Lever provides as epoch milliseconds or ISO string.** (1 connections) — `backend/app/services/job_sources/lever.py`
- **Determine location type from Lever's workplaceType field, falling back to title…** (1 connections) — `backend/app/services/job_sources/lever.py`
- **Lever public Postings API implementation of the JobSource interface…** (1 connections) — `backend/app/services/job_sources/lever.py`
- **String company slug is normalized and targets the correct URL.** (1 connections) — `backend/tests/services/job_sources/test_lever.py`
- **Non-200 responses raise JobSourceHTTPError.** (1 connections) — `backend/tests/services/job_sources/test_lever.py`
- **Parse a realistic Lever response via injected MockTransport.** (1 connections) — `backend/tests/services/job_sources/test_lever.py`
- *... and 2 more nodes in this community*

## Relationships

- [job.py](job.py.md) (14 shared connections)
- [JobPosting](JobPosting.md) (4 shared connections)
- [JobSearchQuery](JobSearchQuery.md) (4 shared connections)
- [typing](typing.md) (1 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (1 shared connections)

## Source Files

- `backend/app/services/job_sources/lever.py`
- `backend/tests/services/job_sources/test_lever.py`

## Audit Trail

- EXTRACTED: 48 (76%)
- INFERRED: 15 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
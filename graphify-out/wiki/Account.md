# Account

> 23 nodes · cohesion 0.16

## Key Concepts

- **Account** (70 connections) — `backend/app/models/account.py`
- **test_interview.py** (26 connections) — `backend/tests/api/test_interview.py`
- **TestClient** (6 connections)
- **client()** (5 connections) — `backend/tests/api/test_interview.py`
- **test_create_and_get_story()** (5 connections) — `backend/tests/api/test_interview.py`
- **account_a()** (4 connections) — `backend/tests/api/test_interview.py`
- **account_b()** (4 connections) — `backend/tests/api/test_interview.py`
- **fixture** (4 connections)
- **test_filter_stories_by_verification_and_tag()** (4 connections) — `backend/tests/api/test_interview.py`
- **test_interview_multi_tenant_isolation()** (4 connections) — `backend/tests/api/test_interview.py`
- **test_list_stories_empty()** (4 connections) — `backend/tests/api/test_interview.py`
- **test_list_tags()** (4 connections) — `backend/tests/api/test_interview.py`
- **test_update_and_delete_story()** (4 connections) — `backend/tests/api/test_interview.py`
- **api_test_db()** (3 connections) — `backend/tests/api/test_interview.py`
- **Session** (3 connections)
- **Multi-tenant Account model matching ARCHITECTURE.md §7. Every tenant has an…** (1 connections) — `backend/app/models/account.py`
- **override_get_db()** (1 connections) — `backend/tests/api/test_interview.py`
- **Test filtering STAR stories by tag and verified_only flag.** (1 connections) — `backend/tests/api/test_interview.py`
- **GET /api/v1/interview/tags returns deduplicated sorted tags.** (1 connections) — `backend/tests/api/test_interview.py`
- **Verify tenant isolation on STAR stories.** (1 connections) — `backend/tests/api/test_interview.py`
- **GET /api/v1/interview/stories returns empty list when none exist.** (1 connections) — `backend/tests/api/test_interview.py`
- **POST /api/v1/interview/stories creates STAR story and GET retrieves it.** (1 connections) — `backend/tests/api/test_interview.py`
- **PATCH and DELETE endpoints for STAR stories.** (1 connections) — `backend/tests/api/test_interview.py`

## Relationships

- [Base](Base.md) (15 shared connections)
- [test_models.py](test_models.py.md) (11 shared connections)
- [test_profile.py](test_profile.py.md) (11 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (9 shared connections)
- [test_applications.py](test_applications.py.md) (8 shared connections)
- [jobs.py](jobs.py.md) (5 shared connections)
- [models/__init__.py](models-__init__.py.md) (3 shared connections)
- [api/interview.py](api-interview.py.md) (3 shared connections)
- [typing](typing.md) (3 shared connections)
- [test_multi_tenant_isolation_never_leaks_cross_account_data](test_multi_tenant_isolation_never_leaks_cross_account_data.md) (2 shared connections)
- [applications.py](applications.py.md) (2 shared connections)
- [job.py](job.py.md) (2 shared connections)

## Source Files

- `backend/app/models/account.py`
- `backend/tests/api/test_interview.py`

## Audit Trail

- EXTRACTED: 83 (70%)
- INFERRED: 35 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
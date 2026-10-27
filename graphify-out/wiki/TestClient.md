# TestClient

> 20 nodes · cohesion 0.10

## Key Concepts

- **TestClient** (10 connections)
- **test_trigger_ingestion_endpoint()** (6 connections) — `backend/tests/api/test_jobs.py`
- **test_default_exclusion_behavior()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_override_include_flagged()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_override_include_vetoed()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_override_show_all()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_pagination_limit_and_offset()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_response_fields_contract()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_sort_order_match_score_descending()** (3 connections) — `backend/tests/api/test_jobs.py`
- **test_unversioned_root_jobs_route_is_not_exposed()** (3 connections) — `backend/tests/api/test_jobs.py`
- **fetch()** (2 connections) — `backend/tests/api/test_jobs.py`
- **Default request must exclude vetoed=True and integrity_status='flagged'…** (1 connections) — `backend/tests/api/test_jobs.py`
- **Verify returned jobs are ordered by match_score descending, with unscored…** (1 connections) — `backend/tests/api/test_jobs.py`
- **include_vetoed=True must include vetoed postings (unless also flagged).** (1 connections) — `backend/tests/api/test_jobs.py`
- **include_flagged=True must include flagged postings (unless also vetoed).** (1 connections) — `backend/tests/api/test_jobs.py`
- **show_all=True must include all jobs (both vetoed and flagged) for human review.** (1 connections) — `backend/tests/api/test_jobs.py`
- **Verify company, role, match_score, vetoed, veto_reason, integrity_status, and…** (1 connections) — `backend/tests/api/test_jobs.py`
- **Verify limit and offset pagination parameters work correctly.** (1 connections) — `backend/tests/api/test_jobs.py`
- **Ensure API endpoints are strictly standardized under /api/v1 and unversioned…** (1 connections) — `backend/tests/api/test_jobs.py`
- **Test POST /api/v1/jobs/ingest triggers job sourcing, integrity guarding,…** (1 connections) — `backend/tests/api/test_jobs.py`

## Relationships

- [Base](Base.md) (9 shared connections)
- [JobPosting](JobPosting.md) (2 shared connections)
- [test_multi_tenant_isolation_never_leaks_cross_account_data](test_multi_tenant_isolation_never_leaks_cross_account_data.md) (1 shared connections)
- [job.py](job.py.md) (1 shared connections)

## Source Files

- `backend/tests/api/test_jobs.py`

## Audit Trail

- EXTRACTED: 31 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
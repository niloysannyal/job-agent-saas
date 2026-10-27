# test_multi_tenant_isolation_never_leaks_cross_account_data

> 13 nodes · cohesion 0.18

## Key Concepts

- **test_multi_tenant_isolation_never_leaks_cross_account_data()** (6 connections) — `backend/tests/api/test_jobs.py`
- **client()** (5 connections) — `backend/tests/api/test_jobs.py`
- **seeded_accounts()** (5 connections) — `backend/tests/api/test_jobs.py`
- **seeded_jobs()** (5 connections) — `backend/tests/api/test_jobs.py`
- **fixture** (4 connections)
- **Session** (4 connections)
- **test_db()** (4 connections) — `backend/tests/api/test_jobs.py`
- **override_get_db()** (1 connections) — `backend/tests/api/test_jobs.py`
- **In-memory SQLite database session with static pool for testing.** (1 connections) — `backend/tests/api/test_jobs.py`
- **FastAPI TestClient with overridden get_db dependency.** (1 connections) — `backend/tests/api/test_jobs.py`
- **Explicit multi-tenant security test: Seeds jobs for two distinct accounts…** (1 connections) — `backend/tests/api/test_jobs.py`
- **Seed test accounts for multi-tenant isolation tests.** (1 connections) — `backend/tests/api/test_jobs.py`
- **Seed a variety of jobs: - High match score, clean - Mid match score, clean -…** (1 connections) — `backend/tests/api/test_jobs.py`

## Relationships

- [Base](Base.md) (6 shared connections)
- [Account](Account.md) (2 shared connections)
- [test_models.py](test_models.py.md) (2 shared connections)
- [TestClient](TestClient.md) (1 shared connections)

## Source Files

- `backend/tests/api/test_jobs.py`

## Audit Trail

- EXTRACTED: 21 (84%)
- INFERRED: 4 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
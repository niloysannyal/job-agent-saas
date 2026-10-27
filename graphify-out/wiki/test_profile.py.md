# test_profile.py

> 25 nodes · cohesion 0.12

## Key Concepts

- **test_profile.py** (32 connections) — `backend/tests/api/test_profile.py`
- **TestClient** (8 connections)
- **client()** (5 connections) — `backend/tests/api/test_profile.py`
- **account_a()** (4 connections) — `backend/tests/api/test_profile.py`
- **account_b()** (4 connections) — `backend/tests/api/test_profile.py`
- **fixture** (4 connections)
- **test_compensation_upsert()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_create_and_get_profile()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_get_profile_empty()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_multi_tenant_isolation()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_spoken_languages_crud()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_target_designations_crud()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_target_locations_crud()** (4 connections) — `backend/tests/api/test_profile.py`
- **test_update_profile()** (4 connections) — `backend/tests/api/test_profile.py`
- **api_test_db()** (3 connections) — `backend/tests/api/test_profile.py`
- **Session** (3 connections)
- **override_get_db()** (1 connections) — `backend/tests/api/test_profile.py`
- **PATCH /api/v1/profile updates fields partially.** (1 connections) — `backend/tests/api/test_profile.py`
- **CRUD operations on target designations.** (1 connections) — `backend/tests/api/test_profile.py`
- **CRUD operations on target locations.** (1 connections) — `backend/tests/api/test_profile.py`
- **GET and PUT on compensation expectations.** (1 connections) — `backend/tests/api/test_profile.py`
- **CRUD operations on spoken languages.** (1 connections) — `backend/tests/api/test_profile.py`
- **Verify complete isolation between tenants A and B for profile and related…** (1 connections) — `backend/tests/api/test_profile.py`
- **GET /api/v1/profile returns null when account has no profile.** (1 connections) — `backend/tests/api/test_profile.py`
- **POST /api/v1/profile creates user profile and GET retrieves it.** (1 connections) — `backend/tests/api/test_profile.py`

## Relationships

- [Account](Account.md) (11 shared connections)
- [Base](Base.md) (7 shared connections)
- [models/__init__.py](models-__init__.py.md) (6 shared connections)
- [jobs.py](jobs.py.md) (5 shared connections)
- [test_applications.py](test_applications.py.md) (2 shared connections)
- [job.py](job.py.md) (1 shared connections)

## Source Files

- `backend/tests/api/test_profile.py`

## Audit Trail

- EXTRACTED: 56 (82%)
- INFERRED: 12 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
---
paths:
  - "backend/app/**/*.py"
  - "backend/tests/**/*.py"
---
# FastAPI Backend Development Standards (adapted from ECC)

## 1. Architectural Structure
- Keep FastAPI routers thin; delegate business logic to services (`backend/app/services/`).
- Put all data models in `backend/app/models/` (SQLAlchemy 2.0 ORM + Pydantic v2 schemas).
- Inject database sessions and authenticated user context via FastAPI `Depends()`.

## 2. Async Correctness
- Use `async def` for any router endpoint that performs I/O or network requests.
- Never use blocking `requests` inside async functions — use `httpx.AsyncClient`.
- For CPU-bound or sync operations, use thread-pool execution (`run_in_threadpool`).

## 3. Dependency Injection
```python
@router.get("/jobs")
async def list_jobs(
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_tenant),
):
    ...
```
- Never create `SessionLocal()` directly inside router endpoints.

## 4. Pydantic Schemas & Security
- Keep Create, Read, and Update schemas separate (e.g. `LLMProviderCreate`, `LLMProviderRead`, `LLMProviderUpdate`).
- Never expose password hashes, raw encryption keys, or tenant credentials in `Read` response models.
- Mask or encrypt secrets before storing in the database.

## 5. Testing
- Every new router endpoint or service gets an async or sync test in `backend/tests/`.
- Mock external APIs (OpenAI, Adzuna, Greenhouse) in unit tests using `unittest.mock` or pytest fixtures.


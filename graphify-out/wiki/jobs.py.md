# jobs.py

> 17 nodes · cohesion 0.21

## Key Concepts

- **jobs.py** (21 connections) — `backend/app/api/jobs.py`
- **session.py** (20 connections) — `backend/app/db/session.py`
- **main.py** (20 connections) — `backend/app/main.py`
- **get_db()** (13 connections) — `backend/app/db/session.py`
- **create_app()** (11 connections) — `backend/app/main.py`
- **get_session_factory()** (8 connections) — `backend/app/db/session.py`
- **get_engine()** (7 connections) — `backend/app/db/session.py`
- **FastAPI** (7 connections)
- **db/__init__.py** (6 connections) — `backend/app/db/__init__.py`
- **lifespan()** (6 connections) — `backend/app/main.py`
- **app/api/__init__.py** (1 connections) — `backend/app/api/__init__.py`
- **Session** (1 connections)
- **FastAPI dependency that yields a SQLAlchemy database session.** (1 connections) — `backend/app/db/session.py`
- **health_check()** (1 connections) — `backend/app/main.py`
- **Create and configure FastAPI application.** (1 connections) — `backend/app/main.py`
- **contextlib** (1 connections)
- **fastapi_middleware_cors** (1 connections)

## Relationships

- [Base](Base.md) (13 shared connections)
- [test_models.py](test_models.py.md) (7 shared connections)
- [models/__init__.py](models-__init__.py.md) (5 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (5 shared connections)
- [config.py](config.py.md) (5 shared connections)
- [Account](Account.md) (5 shared connections)
- [test_profile.py](test_profile.py.md) (5 shared connections)
- [applications.py](applications.py.md) (4 shared connections)
- [api/interview.py](api-interview.py.md) (4 shared connections)
- [LLMService](LLMService.md) (4 shared connections)
- [test_applications.py](test_applications.py.md) (4 shared connections)
- [typing](typing.md) (2 shared connections)

## Source Files

- `backend/app/api/__init__.py`
- `backend/app/api/jobs.py`
- `backend/app/db/__init__.py`
- `backend/app/db/session.py`
- `backend/app/main.py`

## Audit Trail

- EXTRACTED: 95 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
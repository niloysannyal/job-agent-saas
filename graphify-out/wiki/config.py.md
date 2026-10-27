# config.py

> 13 nodes · cohesion 0.17

## Key Concepts

- **config.py** (16 connections) — `backend/app/core/config.py`
- **env.py** (14 connections) — `backend/app/db/migrations/env.py`
- **run_migrations_offline()** (3 connections) — `backend/app/db/migrations/env.py`
- **run_migrations_online()** (3 connections) — `backend/app/db/migrations/env.py`
- **get_database_url()** (2 connections) — `backend/app/db/migrations/env.py`
- **conftest.py** (2 connections) — `backend/tests/conftest.py`
- **os** (2 connections)
- **sys** (2 connections)
- **core/__init__.py** (1 connections) — `backend/app/core/__init__.py`
- **Run migrations in 'offline' mode.** (1 connections) — `backend/app/db/migrations/env.py`
- **Run migrations in 'online' mode.** (1 connections) — `backend/app/db/migrations/env.py`
- **logging_config** (1 connections)
- **pydantic_settings** (1 connections)

## Relationships

- [jobs.py](jobs.py.md) (5 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (4 shared connections)
- [typing](typing.md) (3 shared connections)
- [Base](Base.md) (3 shared connections)
- [job.py](job.py.md) (2 shared connections)
- [LLMService](LLMService.md) (2 shared connections)
- [test_models.py](test_models.py.md) (1 shared connections)
- [test_matching.py](test_matching.py.md) (1 shared connections)
- [Settings](Settings.md) (1 shared connections)
- [models/__init__.py](models-__init__.py.md) (1 shared connections)

## Source Files

- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/db/migrations/env.py`
- `backend/tests/conftest.py`

## Audit Trail

- EXTRACTED: 36 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
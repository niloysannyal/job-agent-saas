# job.py

> 35 nodes · cohesion 0.18

## Key Concepts

- **job.py** (51 connections) — `backend/app/models/job.py`
- **JobSourceHTTPError** (36 connections) — `backend/app/services/job_sources/exceptions.py`
- **JobSource** (31 connections) — `backend/app/services/job_sources/base.py`
- **job_sources/__init__.py** (24 connections) — `backend/app/services/job_sources/__init__.py`
- **datetime** (22 connections)
- **adzuna.py** (20 connections) — `backend/app/services/job_sources/adzuna.py`
- **greenhouse.py** (19 connections) — `backend/app/services/job_sources/greenhouse.py`
- **linkedin.py** (19 connections) — `backend/app/services/job_sources/linkedin.py`
- **pytest** (18 connections)
- **exceptions.py** (17 connections) — `backend/app/services/job_sources/exceptions.py`
- **freehire.py** (17 connections) — `backend/app/services/job_sources/freehire.py`
- **lever.py** (17 connections) — `backend/app/services/job_sources/lever.py`
- **remoteok.py** (17 connections) — `backend/app/services/job_sources/remoteok.py`
- **job_sources/base.py** (16 connections) — `backend/app/services/job_sources/base.py`
- **remotive.py** (16 connections) — `backend/app/services/job_sources/remotive.py`
- **test_adzuna.py** (16 connections) — `backend/tests/services/job_sources/test_adzuna.py`
- **test_remotive.py** (15 connections) — `backend/tests/services/job_sources/test_remotive.py`
- **httpx** (15 connections)
- **test_greenhouse.py** (13 connections) — `backend/tests/services/job_sources/test_greenhouse.py`
- **test_lever.py** (13 connections) — `backend/tests/services/job_sources/test_lever.py`
- **JobSourceConfigError** (9 connections) — `backend/app/services/job_sources/exceptions.py`
- **JobSourceError** (6 connections) — `backend/app/services/job_sources/exceptions.py`
- **_parse_iso_date()** (4 connections) — `backend/app/services/job_sources/freehire.py`
- **html** (4 connections)
- **ABC** (2 connections)
- *... and 10 more nodes in this community*

## Relationships

- [JobSearchQuery](JobSearchQuery.md) (32 shared connections)
- [JobPosting](JobPosting.md) (30 shared connections)
- [typing](typing.md) (22 shared connections)
- [AdzunaJobSource](AdzunaJobSource.md) (20 shared connections)
- [Base](Base.md) (19 shared connections)
- [RemoteOKJobSource](RemoteOKJobSource.md) (17 shared connections)
- [RemotiveJobSource](RemotiveJobSource.md) (15 shared connections)
- [LeverJobSource](LeverJobSource.md) (14 shared connections)
- [LinkedInJobSource](LinkedInJobSource.md) (10 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (9 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (6 shared connections)
- [models/__init__.py](models-__init__.py.md) (5 shared connections)

## Source Files

- `backend/app/models/job.py`
- `backend/app/services/job_sources/__init__.py`
- `backend/app/services/job_sources/adzuna.py`
- `backend/app/services/job_sources/base.py`
- `backend/app/services/job_sources/exceptions.py`
- `backend/app/services/job_sources/freehire.py`
- `backend/app/services/job_sources/greenhouse.py`
- `backend/app/services/job_sources/lever.py`
- `backend/app/services/job_sources/linkedin.py`
- `backend/app/services/job_sources/remoteok.py`
- `backend/app/services/job_sources/remotive.py`
- `backend/tests/services/job_sources/test_adzuna.py`
- `backend/tests/services/job_sources/test_greenhouse.py`
- `backend/tests/services/job_sources/test_lever.py`
- `backend/tests/services/job_sources/test_remotive.py`

## Audit Trail

- EXTRACTED: 319 (94%)
- INFERRED: 19 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
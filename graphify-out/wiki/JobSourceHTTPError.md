# JobSourceHTTPError

> God node · 36 connections · `backend/app/services/job_sources/exceptions.py`

**Community:** [job.py](job.py.md)

## Connections by Relation

### calls
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`
- .fetch() `EXTRACTED`

### contains
- exceptions.py `EXTRACTED`

### imports
- job_sources/__init__.py `EXTRACTED`
- adzuna.py `EXTRACTED`
- greenhouse.py `EXTRACTED`
- linkedin.py `EXTRACTED`
- freehire.py `EXTRACTED`
- lever.py `EXTRACTED`
- remoteok.py `EXTRACTED`
- remotive.py `EXTRACTED`
- test_adzuna.py `EXTRACTED`
- test_remoteok.py `EXTRACTED`
- test_freehire.py `EXTRACTED`
- test_remotive.py `EXTRACTED`
- test_greenhouse.py `EXTRACTED`
- test_lever.py `EXTRACTED`

### inherits
- JobSourceError `EXTRACTED`

### method
- .__init__() `EXTRACTED`

### rationale_for
- Raised when an external job source HTTP request fails. `EXTRACTED`

### uses
- [AdzunaJobSource](AdzunaJobSource.md) `INFERRED`
- FreehireJobSource `INFERRED`
- [RemoteOKJobSource](RemoteOKJobSource.md) `INFERRED`
- [RemotiveJobSource](RemotiveJobSource.md) `INFERRED`
- [LeverJobSource](LeverJobSource.md) `INFERRED`
- GreenhouseJobSource `INFERRED`
- test_adzuna_http_error() `INFERRED`
- test_freehire_http_error() `INFERRED`
- test_greenhouse_http_error() `INFERRED`
- test_lever_http_error() `INFERRED`
- test_remoteok_http_error() `INFERRED`
- test_remotive_http_error() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
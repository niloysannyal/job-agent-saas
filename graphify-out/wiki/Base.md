# Base

> 34 nodes · cohesion 0.14

## Key Concepts

- **Base** (45 connections) — `backend/app/db/base.py`
- **account.py** (40 connections) — `backend/app/models/account.py`
- **test_jobs.py** (31 connections) — `backend/tests/api/test_jobs.py`
- **sqlalchemy** (30 connections)
- **cv_template.py** (29 connections) — `backend/app/models/cv_template.py`
- **sqlalchemy_orm** (27 connections)
- **application.py** (23 connections) — `backend/app/models/application.py`
- **subscription.py** (23 connections) — `backend/app/models/subscription.py`
- **db/base.py** (21 connections) — `backend/app/db/base.py`
- **llm_provider.py** (19 connections) — `backend/app/models/llm_provider.py`
- **uuid** (16 connections)
- **AccountCvVersion** (15 connections) — `backend/app/models/cv_template.py`
- **pydantic** (11 connections)
- **test_pydantic_schemas()** (10 connections) — `backend/tests/models/test_models.py`
- **AccountCreate** (5 connections) — `backend/app/models/account.py`
- **ApplicationBase** (5 connections) — `backend/app/models/application.py`
- **ApplicationCreate** (5 connections) — `backend/app/models/application.py`
- **AccountCvVersionBase** (5 connections) — `backend/app/models/cv_template.py`
- **CvTemplateBase** (5 connections) — `backend/app/models/cv_template.py`
- **CvTemplateCreate** (5 connections) — `backend/app/models/cv_template.py`
- **LLMProviderCreate** (5 connections) — `backend/app/models/llm_provider.py`
- **EntitlementCreate** (5 connections) — `backend/app/models/subscription.py`
- **SubscriptionPlanCreate** (5 connections) — `backend/app/models/subscription.py`
- **AccountCvVersionCreate** (4 connections) — `backend/app/models/cv_template.py`
- **BaseModel** (4 connections)
- *... and 9 more nodes in this community*

## Relationships

- [models/__init__.py](models-__init__.py.md) (51 shared connections)
- [test_models.py](test_models.py.md) (42 shared connections)
- [typing](typing.md) (26 shared connections)
- [job.py](job.py.md) (19 shared connections)
- [applications.py](applications.py.md) (16 shared connections)
- [Account](Account.md) (15 shared connections)
- [jobs.py](jobs.py.md) (13 shared connections)
- [api/interview.py](api-interview.py.md) (12 shared connections)
- [test_applications.py](test_applications.py.md) (9 shared connections)
- [TestClient](TestClient.md) (9 shared connections)
- [test_profile.py](test_profile.py.md) (7 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (6 shared connections)

## Source Files

- `backend/app/db/base.py`
- `backend/app/models/account.py`
- `backend/app/models/application.py`
- `backend/app/models/cv_template.py`
- `backend/app/models/llm_provider.py`
- `backend/app/models/subscription.py`
- `backend/tests/api/test_jobs.py`
- `backend/tests/models/test_models.py`

## Audit Trail

- EXTRACTED: 319 (97%)
- INFERRED: 11 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
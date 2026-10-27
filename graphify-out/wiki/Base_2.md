# Base

> God node · 45 connections · `backend/app/db/base.py`

**Community:** [Base](Base.md)

## Connections by Relation

### contains
- db/base.py `EXTRACTED`

### imports
- [test_models.py](test_models.py.md) `EXTRACTED`
- [job.py](job.py.md) `EXTRACTED`
- account.py `EXTRACTED`
- models/profile.py `EXTRACTED`
- [test_matching.py](test_matching.py.md) `EXTRACTED`
- test_cv_tailor.py `EXTRACTED`
- [test_profile.py](test_profile.py.md) `EXTRACTED`
- test_jobs.py `EXTRACTED`
- [test_applications.py](test_applications.py.md) `EXTRACTED`
- cv_template.py `EXTRACTED`
- [test_job_ingestion.py](test_job_ingestion.py.md) `EXTRACTED`
- test_interview.py `EXTRACTED`
- application.py `EXTRACTED`
- subscription.py `EXTRACTED`
- models/interview.py `EXTRACTED`
- main.py `EXTRACTED`
- llm_provider.py `EXTRACTED`
- env.py `EXTRACTED`
- db/__init__.py `EXTRACTED`

### inherits
- [Account](Account.md) `EXTRACTED`
- [Job](Job.md) `EXTRACTED`
- [Application](Application.md) `EXTRACTED`
- [UserProfile](UserProfile.md) `EXTRACTED`
- StarStory `EXTRACTED`
- AccountCvVersion `EXTRACTED`
- SpokenLanguage `EXTRACTED`
- TargetDesignation `EXTRACTED`
- TargetLocation `EXTRACTED`
- CvTemplate `EXTRACTED`
- LLMProviderConfig `EXTRACTED`
- CompensationExpectation `EXTRACTED`
- Entitlement `EXTRACTED`
- SubscriptionPlan `EXTRACTED`
- DeclarativeBase `EXTRACTED`

### rationale_for
- Base SQLAlchemy declarative model. `EXTRACTED`

### uses
- lifespan() `INFERRED`
- test_db() `INFERRED`
- db_session() `INFERRED`
- db_session() `INFERRED`
- db_session() `INFERRED`
- db_session() `INFERRED`
- api_test_db() `INFERRED`
- api_test_db() `INFERRED`
- api_test_db() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
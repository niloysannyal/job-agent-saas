# test_models.py

> 37 nodes · cohesion 0.10

## Key Concepts

- **test_models.py** (58 connections) — `backend/tests/models/test_models.py`
- **Job** (53 connections) — `backend/app/models/job.py`
- **seed.py** (25 connections) — `backend/app/db/seed.py`
- **seed_initial_data()** (19 connections) — `backend/app/db/seed.py`
- **CvTemplate** (12 connections) — `backend/app/models/cv_template.py`
- **LLMProviderConfig** (12 connections) — `backend/app/models/llm_provider.py`
- **Entitlement** (11 connections) — `backend/app/models/subscription.py`
- **test_seed_initial_data()** (11 connections) — `backend/tests/models/test_models.py`
- **Session** (10 connections)
- **SubscriptionPlan** (9 connections) — `backend/app/models/subscription.py`
- **test_multi_tenant_cascade_deletes()** (8 connections) — `backend/tests/models/test_models.py`
- **test_cv_template_and_version_models()** (7 connections) — `backend/tests/models/test_models.py`
- **test_application_model_and_human_in_the_loop_gate()** (6 connections) — `backend/tests/models/test_models.py`
- **test_subscription_plans_and_entitlements()** (6 connections) — `backend/tests/models/test_models.py`
- **test_job_model_matching_architecture_spec()** (5 connections) — `backend/tests/models/test_models.py`
- **test_star_story_model()** (5 connections) — `backend/tests/models/test_models.py`
- **db_session()** (4 connections) — `backend/tests/models/test_models.py`
- **test_account_model()** (4 connections) — `backend/tests/models/test_models.py`
- **test_llm_provider_config_model()** (4 connections) — `backend/tests/models/test_models.py`
- **Session** (1 connections)
- **Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11: 1.…** (1 connections) — `backend/app/db/seed.py`
- **LaTeX CV template model matching ARCHITECTURE.md §5 & §7. Admin-curated system…** (1 connections) — `backend/app/models/cv_template.py`
- **Multi-tenant Job model matching ARCHITECTURE.md §7: (account_id, company, role,…** (1 connections) — `backend/app/models/job.py`
- **LLM provider configuration table matching ARCHITECTURE.md §11. Allows…** (1 connections) — `backend/app/models/llm_provider.py`
- **Subscription plan catalog model matching ARCHITECTURE.md §0 & §7. Deferred…** (1 connections) — `backend/app/models/subscription.py`
- *... and 12 more nodes in this community*

## Relationships

- [Base](Base.md) (42 shared connections)
- [models/__init__.py](models-__init__.py.md) (30 shared connections)
- [api/interview.py](api-interview.py.md) (12 shared connections)
- [Account](Account.md) (11 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (10 shared connections)
- [applications.py](applications.py.md) (10 shared connections)
- [jobs.py](jobs.py.md) (7 shared connections)
- [typing](typing.md) (7 shared connections)
- [test_applications.py](test_applications.py.md) (6 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (4 shared connections)
- [job.py](job.py.md) (4 shared connections)
- [MatchingService](MatchingService.md) (3 shared connections)

## Source Files

- `backend/app/db/seed.py`
- `backend/app/models/cv_template.py`
- `backend/app/models/job.py`
- `backend/app/models/llm_provider.py`
- `backend/app/models/subscription.py`
- `backend/tests/models/test_models.py`

## Audit Trail

- EXTRACTED: 191 (87%)
- INFERRED: 29 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
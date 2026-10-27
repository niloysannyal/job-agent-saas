# LLMService

> 43 nodes · cohesion 0.10

## Key Concepts

- **LLMService** (23 connections) — `backend/app/services/llm/service.py`
- **llm/service.py** (19 connections) — `backend/app/services/llm/service.py`
- **LLMProvider** (15 connections) — `backend/app/services/llm/base.py`
- **MockLLMProvider** (14 connections) — `backend/app/services/llm/mock_provider.py`
- **test_llm.py** (13 connections) — `backend/tests/services/llm/test_llm.py`
- **OpenAIProvider** (11 connections) — `backend/app/services/llm/openai_provider.py`
- **openai_provider.py** (10 connections) — `backend/app/services/llm/openai_provider.py`
- **llm/base.py** (8 connections) — `backend/app/services/llm/base.py`
- **llm/__init__.py** (8 connections) — `backend/app/services/llm/__init__.py`
- **mock_provider.py** (8 connections) — `backend/app/services/llm/mock_provider.py`
- **client()** (8 connections) — `backend/tests/api/test_applications.py`
- **.generate()** (7 connections) — `backend/app/services/llm/service.py`
- **test_llm_service_failover_chain()** (7 connections) — `backend/tests/services/llm/test_llm.py`
- **._resolve_providers()** (6 connections) — `backend/app/services/llm/service.py`
- **test_llm_service_with_explicit_provider()** (5 connections) — `backend/tests/services/llm/test_llm.py`
- **test_openai_provider_missing_key()** (5 connections) — `backend/tests/services/llm/test_llm.py`
- **asyncio** (4 connections)
- **test_mock_llm_provider()** (4 connections) — `backend/tests/services/llm/test_llm.py`
- **.__init__()** (3 connections) — `backend/app/services/cv_tailor/tailor_service.py`
- **.generate()** (3 connections) — `backend/app/services/llm/base.py`
- **.generate()** (3 connections) — `backend/app/services/llm/mock_provider.py`
- **.generate()** (3 connections) — `backend/app/services/llm/openai_provider.py`
- **.__init__()** (3 connections) — `backend/app/services/llm/service.py`
- **ABC** (2 connections)
- **.__init__()** (2 connections) — `backend/app/services/llm/openai_provider.py`
- *... and 18 more nodes in this community*

## Relationships

- [typing](typing.md) (14 shared connections)
- [test_applications.py](test_applications.py.md) (7 shared connections)
- [applications.py](applications.py.md) (6 shared connections)
- [jobs.py](jobs.py.md) (4 shared connections)
- [job.py](job.py.md) (3 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (2 shared connections)
- [config.py](config.py.md) (2 shared connections)
- [test_models.py](test_models.py.md) (2 shared connections)
- [Base](Base.md) (2 shared connections)

## Source Files

- `backend/app/services/cv_tailor/tailor_service.py`
- `backend/app/services/llm/__init__.py`
- `backend/app/services/llm/base.py`
- `backend/app/services/llm/mock_provider.py`
- `backend/app/services/llm/openai_provider.py`
- `backend/app/services/llm/service.py`
- `backend/tests/api/test_applications.py`
- `backend/tests/services/llm/test_llm.py`

## Audit Trail

- EXTRACTED: 104 (81%)
- INFERRED: 24 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
# job_ingestion.py

> 19 nodes · cohesion 0.18

## Key Concepts

- **job_ingestion.py** (23 connections) — `backend/app/services/job_ingestion.py`
- **matching/service.py** (23 connections) — `backend/app/services/matching/service.py`
- **matching/__init__.py** (15 connections) — `backend/app/services/matching/__init__.py`
- **profile_parser.py** (11 connections) — `backend/app/services/matching/profile_parser.py`
- **logging** (9 connections)
- **IngestionResult** (8 connections) — `backend/app/services/job_ingestion.py`
- **ProfileParser** (8 connections) — `backend/app/services/matching/profile_parser.py`
- **MatchingResult** (7 connections) — `backend/app/services/matching/service.py`
- **pathlib** (5 connections)
- **ParsedProfile** (4 connections) — `backend/app/services/matching/profile_parser.py`
- **dataclasses** (4 connections)
- **app/services/__init__.py** (3 connections) — `backend/app/services/__init__.py`
- **.extract_clean_cv_text()** (3 connections) — `backend/app/services/matching/profile_parser.py`
- **Summary metrics of a job ingestion run.** (1 connections) — `backend/app/services/job_ingestion.py`
- **Structured representation of parsed user profile and CV.** (1 connections) — `backend/app/services/matching/profile_parser.py`
- **Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md. KNOWN FORMAT…** (1 connections) — `backend/app/services/matching/profile_parser.py`
- **Extract readable text from LaTeX CV, stripping comments and common markup.** (1 connections) — `backend/app/services/matching/profile_parser.py`
- **Summary of a match scoring run.** (1 connections) — `backend/app/services/matching/service.py`
- **qdrant_client_models** (1 connections)

## Relationships

- [test_matching.py](test_matching.py.md) (13 shared connections)
- [MatchingService](MatchingService.md) (8 shared connections)
- [typing](typing.md) (7 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (6 shared connections)
- [job.py](job.py.md) (6 shared connections)
- [Base](Base.md) (5 shared connections)
- [run_posting_guard](run_posting_guard.md) (4 shared connections)
- [test_models.py](test_models.py.md) (4 shared connections)
- [config.py](config.py.md) (4 shared connections)
- [LanguageGate](LanguageGate.md) (2 shared connections)
- [MockEmbeddingClient](MockEmbeddingClient.md) (2 shared connections)
- [LLMService](LLMService.md) (2 shared connections)

## Source Files

- `backend/app/services/__init__.py`
- `backend/app/services/job_ingestion.py`
- `backend/app/services/matching/__init__.py`
- `backend/app/services/matching/profile_parser.py`
- `backend/app/services/matching/service.py`

## Audit Trail

- EXTRACTED: 94 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
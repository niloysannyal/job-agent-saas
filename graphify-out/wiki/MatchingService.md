# MatchingService

> 21 nodes · cohesion 0.15

## Key Concepts

- **MatchingService** (17 connections) — `backend/app/services/matching/service.py`
- **.score_and_gate_jobs()** (11 connections) — `backend/app/services/matching/service.py`
- **test_matching_service_embed_and_upsert_qdrant()** (11 connections) — `backend/tests/services/matching/test_matching.py`
- **test_matching_service_score_and_gate_clean_jobs()** (11 connections) — `backend/tests/services/matching/test_matching.py`
- **.parse()** (8 connections) — `backend/app/services/matching/profile_parser.py`
- **.embed_and_upsert_profile()** (7 connections) — `backend/app/services/matching/service.py`
- **._get_qdrant_point_id()** (4 connections) — `backend/app/services/matching/service.py`
- **Path** (4 connections)
- **test_profile_parser_cv_and_profile_extraction()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **test_profile_parser_default_language_fallback()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **asyncio** (3 connections)
- **Path** (2 connections)
- **Path** (1 connections)
- **Score clean jobs with cosine similarity and apply language/dealbreaker gate.…** (1 connections) — `backend/app/services/matching/service.py`
- **Two-layer job match scoring service matching ARCHITECTURE.md §4: Layer 1:…** (1 connections) — `backend/app/services/matching/service.py`
- **Derive a deterministic UUID point ID for the account.** (1 connections) — `backend/app/services/matching/service.py`
- **Embed the Master CV and target-roles section of USER_PROFILE.md, upserting the…** (1 connections) — `backend/app/services/matching/service.py`
- **Test that missing languages section defaults to ['english'].** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Test embedding profile and upserting point into Qdrant.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Test that: 1. Clean jobs are embedded and scored. 2. Flagged jobs…** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Test extracting clean text from LaTeX CV and markdown profile.** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [job_ingestion.py](job_ingestion.py.md) (8 shared connections)
- [test_matching.py](test_matching.py.md) (8 shared connections)
- [test_models.py](test_models.py.md) (3 shared connections)
- [LanguageGate](LanguageGate.md) (3 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (2 shared connections)
- [MockQdrantClient](MockQdrantClient.md) (2 shared connections)
- [MockEmbeddingClient](MockEmbeddingClient.md) (2 shared connections)
- [test_account](test_account.md) (2 shared connections)
- [Account](Account.md) (2 shared connections)
- [OpenAIEmbeddingClient](OpenAIEmbeddingClient.md) (1 shared connections)

## Source Files

- `backend/app/services/matching/profile_parser.py`
- `backend/app/services/matching/service.py`
- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 52 (81%)
- INFERRED: 12 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
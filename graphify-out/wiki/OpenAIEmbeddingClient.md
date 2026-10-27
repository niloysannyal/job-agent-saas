# OpenAIEmbeddingClient

> 11 nodes · cohesion 0.24

## Key Concepts

- **OpenAIEmbeddingClient** (10 connections) — `backend/app/services/matching/embedding.py`
- **test_openai_embedding_client()** (8 connections) — `backend/tests/services/matching/test_matching.py`
- **.embed()** (4 connections) — `backend/app/services/matching/embedding.py`
- **.embed_batch()** (4 connections) — `backend/app/services/matching/embedding.py`
- **.__init__()** (1 connections) — `backend/app/services/matching/embedding.py`
- **Production embedding client backed by OpenAI's Embeddings API (text-…** (1 connections) — `backend/app/services/matching/embedding.py`
- **Generate embedding for a single text.** (1 connections) — `backend/app/services/matching/embedding.py`
- **Generate embeddings in batches of up to 100 items.** (1 connections) — `backend/app/services/matching/embedding.py`
- **Test OpenAIEmbeddingClient with mocked httpx response.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **json()** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **mock_post()** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [test_matching.py](test_matching.py.md) (5 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (1 shared connections)
- [MatchingService](MatchingService.md) (1 shared connections)

## Source Files

- `backend/app/services/matching/embedding.py`
- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 17 (85%)
- INFERRED: 3 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
# test_matching.py

> 21 nodes · cohesion 0.14

## Key Concepts

- **test_matching.py** (36 connections) — `backend/tests/services/matching/test_matching.py`
- **embedding.py** (13 connections) — `backend/app/services/matching/embedding.py`
- **EmbeddingClient** (13 connections) — `backend/app/services/matching/embedding.py`
- **get_embedding_client()** (10 connections) — `backend/app/services/matching/embedding.py`
- **compute_cosine_similarity()** (8 connections) — `backend/app/services/matching/embedding.py`
- **.__init__()** (5 connections) — `backend/app/services/matching/service.py`
- **test_compute_cosine_similarity()** (3 connections) — `backend/tests/services/matching/test_matching.py`
- **test_get_embedding_client_factory()** (3 connections) — `backend/tests/services/matching/test_matching.py`
- **math** (3 connections)
- **.embed()** (2 connections) — `backend/app/services/matching/embedding.py`
- **.embed_batch()** (2 connections) — `backend/app/services/matching/embedding.py`
- **ABC** (2 connections)
- **Compute cosine similarity between two numeric vectors: dot(a, b) / (norm(a) *…** (1 connections) — `backend/app/services/matching/embedding.py`
- **Factory returning OpenAIEmbeddingClient if API key is provided and valid,…** (1 connections) — `backend/app/services/matching/embedding.py`
- **Abstract interface for text embedding generation.** (1 connections) — `backend/app/services/matching/embedding.py`
- **Generate embedding vector for a single text string.** (1 connections) — `backend/app/services/matching/embedding.py`
- **Generate embeddings for a list of text strings.** (1 connections) — `backend/app/services/matching/embedding.py`
- **Any** (1 connections)
- **Session** (1 connections)
- **Verify cosine similarity calculation edge cases and bounds.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Test get_embedding_client factory switches between Mock and OpenAI based on key.** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [job_ingestion.py](job_ingestion.py.md) (13 shared connections)
- [MatchingService](MatchingService.md) (8 shared connections)
- [OpenAIEmbeddingClient](OpenAIEmbeddingClient.md) (5 shared connections)
- [Base](Base.md) (5 shared connections)
- [job.py](job.py.md) (4 shared connections)
- [MockEmbeddingClient](MockEmbeddingClient.md) (4 shared connections)
- [LanguageGate](LanguageGate.md) (4 shared connections)
- [typing](typing.md) (2 shared connections)
- [test_account](test_account.md) (2 shared connections)
- [config.py](config.py.md) (1 shared connections)
- [Account](Account.md) (1 shared connections)
- [test_models.py](test_models.py.md) (1 shared connections)

## Source Files

- `backend/app/services/matching/embedding.py`
- `backend/app/services/matching/service.py`
- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 79 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
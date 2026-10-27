# MockQdrantClient

> 7 nodes · cohesion 0.33

## Key Concepts

- **MockQdrantClient** (8 connections) — `backend/tests/services/matching/test_matching.py`
- **.create_collection()** (2 connections) — `backend/tests/services/matching/test_matching.py`
- **.upsert()** (2 connections) — `backend/tests/services/matching/test_matching.py`
- **Any** (2 connections)
- **.collection_exists()** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **.__init__()** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **In-memory mock of QdrantClient for testing without running Qdrant daemon.** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [MatchingService](MatchingService.md) (2 shared connections)
- [test_matching.py](test_matching.py.md) (1 shared connections)

## Source Files

- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 10 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
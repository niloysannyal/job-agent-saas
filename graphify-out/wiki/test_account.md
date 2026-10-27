# test_account

> 6 nodes · cohesion 0.33

## Key Concepts

- **test_account()** (5 connections) — `backend/tests/services/matching/test_matching.py`
- **db_session()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **Session** (3 connections)
- **fixture** (2 connections)
- **In-memory SQLite session for testing matching.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Create a test tenant account.** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [test_matching.py](test_matching.py.md) (2 shared connections)
- [MatchingService](MatchingService.md) (2 shared connections)
- [Base](Base.md) (1 shared connections)
- [Account](Account.md) (1 shared connections)

## Source Files

- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 9 (82%)
- INFERRED: 2 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
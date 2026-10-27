# LanguageGate

> 13 nodes · cohesion 0.21

## Key Concepts

- **LanguageGate** (13 connections) — `backend/app/services/matching/language_gate.py`
- **.check()** (7 connections) — `backend/app/services/matching/language_gate.py`
- **test_language_gate_declared_language_allowed()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **test_language_gate_english_clean()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **test_language_gate_veto_undeclared_language()** (4 connections) — `backend/tests/services/matching/test_matching.py`
- **._detect_required_languages()** (3 connections) — `backend/app/services/matching/language_gate.py`
- **.__init__()** (1 connections) — `backend/app/services/matching/language_gate.py`
- **Evaluate description against declared languages. Returns: (is_vetoed,…** (1 connections) — `backend/app/services/matching/language_gate.py`
- **Evaluates whether a job description requires a spoken language not declared in…** (1 connections) — `backend/app/services/matching/language_gate.py`
- **Detect any language explicitly marked as required or mandatory.** (1 connections) — `backend/app/services/matching/language_gate.py`
- **English-only posting is not vetoed.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **Posting requiring German is vetoed if German is not declared.** (1 connections) — `backend/tests/services/matching/test_matching.py`
- **If user declared German, German requirement is not vetoed.** (1 connections) — `backend/tests/services/matching/test_matching.py`

## Relationships

- [test_matching.py](test_matching.py.md) (4 shared connections)
- [MatchingService](MatchingService.md) (3 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (2 shared connections)
- [typing](typing.md) (1 shared connections)

## Source Files

- `backend/app/services/matching/language_gate.py`
- `backend/tests/services/matching/test_matching.py`

## Audit Trail

- EXTRACTED: 21 (81%)
- INFERRED: 5 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
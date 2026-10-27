# run_posting_guard

> 73 nodes · cohesion 0.06

## Key Concepts

- **run_posting_guard()** (30 connections) — `backend/app/services/posting_guard.py`
- **make_posting()** (23 connections) — `backend/tests/services/test_posting_guard.py`
- **TestInstructionDetection** (23 connections) — `backend/tests/services/test_posting_guard.py`
- **posting_guard.py** (17 connections) — `backend/app/services/posting_guard.py`
- **test_posting_guard.py** (16 connections) — `backend/tests/services/test_posting_guard.py`
- **._assert_flagged()** (16 connections) — `backend/tests/services/test_posting_guard.py`
- **strip_invisible()** (14 connections) — `backend/app/services/posting_guard.py`
- **GateResult** (11 connections) — `backend/app/services/posting_guard.py`
- **TestStripInvisible** (10 connections) — `backend/tests/services/test_posting_guard.py`
- **TestInvisibleCharacters** (9 connections) — `backend/tests/services/test_posting_guard.py`
- **FlagKind** (7 connections) — `backend/app/services/posting_guard.py`
- **TestCleanPosting** (7 connections) — `backend/tests/services/test_posting_guard.py`
- **._assert_not_flagged_as_instruction()** (6 connections) — `backend/tests/services/test_posting_guard.py`
- **TestCombinedIssues** (5 connections) — `backend/tests/services/test_posting_guard.py`
- **IntegrityFlag** (4 connections) — `backend/app/services/posting_guard.py`
- **_is_invisible()** (4 connections) — `backend/app/services/posting_guard.py`
- **.test_flagged_line_preserved_in_result()** (4 connections) — `backend/tests/services/test_posting_guard.py`
- **_line_looks_like_instruction()** (3 connections) — `backend/app/services/posting_guard.py`
- **.test_clean_posting_description_unchanged()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_clean_posting_passes()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_non_inspected_fields_carried_over()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_original_posting_not_mutated()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_result_posting_is_new_object()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_empty_description_passes()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- **.test_invisible_chars_and_instruction_both_flagged()** (3 connections) — `backend/tests/services/test_posting_guard.py`
- *... and 48 more nodes in this community*

## Relationships

- [JobPosting](JobPosting.md) (5 shared connections)
- [job_ingestion.py](job_ingestion.py.md) (4 shared connections)
- [job.py](job.py.md) (3 shared connections)
- [test_job_ingestion.py](test_job_ingestion.py.md) (3 shared connections)
- [typing](typing.md) (2 shared connections)

## Source Files

- `backend/app/services/posting_guard.py`
- `backend/tests/services/test_posting_guard.py`

## Audit Trail

- EXTRACTED: 162 (95%)
- INFERRED: 9 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
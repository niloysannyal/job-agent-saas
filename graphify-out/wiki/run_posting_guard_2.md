# run_posting_guard()

> God node · 30 connections · `backend/app/services/posting_guard.py`

**Community:** [run_posting_guard](run_posting_guard.md)

## Connections by Relation

### calls
- .ingest() `EXTRACTED`
- ._assert_flagged() `EXTRACTED`
- strip_invisible() `EXTRACTED`
- GateResult `EXTRACTED`
- ._assert_not_flagged_as_instruction() `EXTRACTED`
- IntegrityFlag `EXTRACTED`
- .test_flagged_line_preserved_in_result() `EXTRACTED`
- _line_looks_like_instruction() `EXTRACTED`
- .test_clean_posting_description_unchanged() `EXTRACTED`
- .test_clean_posting_passes() `EXTRACTED`
- .test_non_inspected_fields_carried_over() `EXTRACTED`
- .test_original_posting_not_mutated() `EXTRACTED`
- .test_result_posting_is_new_object() `EXTRACTED`
- .test_empty_description_passes() `EXTRACTED`
- .test_invisible_chars_and_instruction_both_flagged() `EXTRACTED`
- .test_none_description_treated_as_empty() `EXTRACTED`
- .test_flag_carries_line_text() `EXTRACTED`
- .test_multiple_injection_lines_produce_multiple_flags() `EXTRACTED`
- .test_bom_only_description() `EXTRACTED`
- .test_flag_detail_mentions_count() `EXTRACTED`
- *…and 5 more `calls` connection(s) not listed (lowest-degree first to go)*

### contains
- posting_guard.py `EXTRACTED`

### imports
- [job_ingestion.py](job_ingestion.py.md) `EXTRACTED`
- test_posting_guard.py `EXTRACTED`

### rationale_for
- Run the posting integrity gate on a JobPosting DTO. Steps: 1. Strip… `EXTRACTED`

### uses
- [JobPosting](JobPosting.md) `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
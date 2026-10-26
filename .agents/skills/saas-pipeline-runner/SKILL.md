---
name: saas-pipeline-runner
description: >-
  Run, test, and verify the FastAPI backend, job ingestion, matching pipeline,
  and full pytest test suite for the Job Application Agent SaaS using Python 3.14.
---

# SaaS Pipeline Runner

Use this skill when running tests, diagnosing test failures, validating API endpoints, or verifying the job ingestion and match scoring pipeline.

## Environment & Commands
- **Python Executable**: Python 3.14 is located at `C:\Python314\python.exe`. Always invoke pytest through this executable:
  ```powershell
  & "C:\Python314\python.exe" -m pytest backend/tests/
  ```
- **Single Module Testing**:
  ```powershell
  & "C:\Python314\python.exe" -m pytest backend/tests/api/test_jobs.py
  & "C:\Python314\python.exe" -m pytest backend/tests/services/test_job_ingestion.py
  & "C:\Python314\python.exe" -m pytest backend/tests/services/matching/test_matching.py
  ```
- **Local Dev Server**:
  ```powershell
  uvicorn app.main:app --reload
  ```
  API is served at `http://127.0.0.1:8000` with Swagger documentation at `http://127.0.0.1:8000/docs` and OpenAPI JSON at `/api/v1/openapi.json`.

## Pipeline Verification Checklist
1. **Posting Integrity**: Confirm all ingested postings run through `run_posting_guard()` before DB commitment.
2. **Matching & Gating**: Confirm `score_and_gate_jobs()` evaluates clean jobs, hard-vetoes undeclared languages, and strictly skips flagged postings.
3. **Queue Endpoint**: Verify `GET /api/v1/jobs?account_id=<id>` returns jobs sorted by `match_score` descending, with `vetoed=False` and `integrity_status='clean'` by default.
4. **Regression Count**: Verify that all 96 unit and integration tests continue to pass with zero failures.

---
name: tdd-workflow
description: Test-Driven Development (TDD) cycle for FastAPI backend services and React frontend components. Use when creating new API endpoints, job source adapters, or UI features.
---
# TDD Workflow Skill — Job Application Agent SaaS

Disciplined test-driven development cycle for backend endpoints, job adapters, and UI features.

## Cycle: Red -> Green -> Refactor

### Phase 1: RED (Write the Failing Test)
1. Identify the module being developed (e.g. `backend/app/services/job_sources/adzuna.py`).
2. Create or open the corresponding test file in `backend/tests/` (e.g. `backend/tests/services/job_sources/test_adzuna.py`).
3. Write the test specifying expected input, output, status codes, and error cases.
4. Run the test:
   ```bash
   cd backend; .\.venv\Scripts\python -m pytest tests/.../test_target.py
   ```
5. Confirm it fails for the expected reason (not an import typo).

### Phase 2: GREEN (Implement the Minimal Working Solution)
1. Write the minimal code in `backend/app/` to make the test pass.
2. Re-run pytest until it passes 100% green.

### Phase 3: REFACTOR (Clean Code & Verify Boundaries)
1. Remove duplication, improve variable names, ensure PEP 8 compliance and type hints.
2. Ensure multi-tenant isolation (`account_id` filtered).
3. Ensure no secrets are leaked or logged in plaintext.
4. Re-run tests to confirm zero regressions.


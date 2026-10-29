---
paths:
  - "**/*"
---
# Config & Assertion Protection Standard (adapted from ECC)

## Principle: Fix the Code, Never Weaken the Guardrail

Under pressure to make builds or tests pass, automated agents or developers may be tempted to edit test assertions, skip tests (`@pytest.mark.skip`), comment out auth checks, or weaken linter/security configs.

**This is strictly prohibited.**

### Protected Targets & Non-Weakening Rules:
1. **Never Weaken Test Assertions**:
   - If a test in `backend/tests/` fails, fix the underlying bug in `backend/app/` or `frontend/src/`.
   - Never change `assert response.status_code == 200` to `200 or 500`.
   - Never add `@pytest.mark.skip` or comment out assertions to bypass failing checks.

2. **Never Weaken Multi-Tenancy or Security Checks**:
   - Never remove `account_id` filtering from a query to make a query pass.
   - Never disable JWT expiry or algorithm checks.
   - Never allow unencrypted storage of API keys.

3. **Never Weaken the Human-in-the-Loop Send Gate**:
   - The application flow must always terminate at human review and manual approval before send.

4. **Preserve Database Migration History**:
   - Never edit an existing applied migration file. Always author a new forward migration.


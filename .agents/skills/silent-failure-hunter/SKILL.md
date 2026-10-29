---
name: silent-failure-hunter
description: Hunt and eliminate silent failures, swallowed exceptions, unlogged fallbacks, and missing error propagation across backend services and frontend components.
---
# Silent Failure Hunter Skill — Job Application Agent SaaS

Zero tolerance for silent failures, unhandled async promises, and swallowed errors.

## Hunt Targets

### 1. Bare `except:` or Empty Catch Blocks
- **Anti-Pattern**:
  ```python
  try:
      await fetch_from_api()
  except Exception:
      pass # Swallows critical errors silently!
  ```
- **Correction**: Log exception with full context and propagate or return explicit error object.

### 2. Dangerous Fallbacks in LLM & Ingestion
- Ensure LLM failover engine records fallback events and outputs structured logs.
- When an API key fails or errors out, raise `RuntimeError` or catch specifically to trigger the next priority node in the failover chain.

### 3. Missing Transaction Rollbacks
- In database writes, always wrap multi-step operations in try-except with `db.rollback()` before re-raising.

### 4. Frontend Unhandled Promise Rejections
- In React `fetch()` calls, always check `res.ok` before calling `res.json()`, and handle network disconnects with user-facing toasts or banner alerts.


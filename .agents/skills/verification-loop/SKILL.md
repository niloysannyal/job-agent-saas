---
name: verification-loop
description: Run the 5-phase product verification loop — frontend build, backend pytest suite, multi-tenant boundary audit, security scan, and AST knowledge graph update. Use when finishing a feature, before commits, or when verifying production readiness.
---
# Verification Loop Skill — Job Application Agent SaaS

Automated 5-phase verification protocol for reliable product development.

## When to Run
- After implementing a new endpoint, component, or data model
- Before declaring a feature complete
- Whenever refactoring code to ensure zero regressions

## Execution
Run the automated verification script:
```bash
python scripts/verify.py
```

## Phases Checked
1. **Frontend Build**: Runs `npm run build` in `frontend/` to ensure zero compilation or JSX errors.
2. **Backend Test Suite**: Runs pytest across `backend/tests/` (verifying all 151+ tests pass).
3. **Multi-Tenant Audit**: Checks SQLAlchemy models to verify `account_id` presence and cascade settings.
4. **Security Scan**: Checks for accidentally exposed plaintext API keys or passwords in modified files.
5. **AST Knowledge Graph**: Runs `graphify update .` to keep architecture navigation in sync.


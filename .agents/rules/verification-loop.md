---
paths:
  - "**/*"
---
# Verification Loop Standard (adapted from ECC)

Before completing any task, merge request, or refactoring turn, follow the **5-Phase Verification Protocol**:

```text
Phase 1: Build & Compile Check
Phase 2: Full Pytest Test Suite
Phase 3: Multi-Tenant Boundary Audit
Phase 4: Security & Secret Leakage Scan
Phase 5: Graphify Knowledge Graph Sync
```

## Running Verification
Execute the automated verification tool from the repository root:
```bash
python scripts/verify.py
```

### Protocol Guidelines:
1. **Never skip Phase 1**: If `npm run build` or Python syntax check fails, STOP immediately and fix syntax.
2. **Never commit failing tests**: All backend tests must be 100% green before pushing.
3. **Audit Tenancy**: Verify no newly added table is missing `account_id`.
4. **AST Synchronization**: Always run `graphify update .` after code file edits.


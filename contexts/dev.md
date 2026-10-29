# Development Context — Job Application Agent SaaS

Mode: Active Feature Implementation & Refactoring
Focus: High-reliability, test-driven product development for Job Application Agent SaaS.

## Core Behavioral Principles (from ECC)
1. **Plan & Test First**: Read requirements and existing tests before writing code.
2. **Priorities**:
   - 1. Get it working (functional correctness)
   - 2. Get it right (multi-tenant boundary, type-hinted, security-audited)
   - 3. Get it clean (refactor, eliminate technical debt, optimize performance)
3. **Commit Discipline**: Atomic, single-responsibility changes with imperative commit messages.
4. **Zero Regression**: Every new feature or fix must preserve existing 151+ tests.

## Non-Negotiables & System Boundaries
- **Human-in-the-Loop on Send**: Never implement an auto-send bypass.
- **Tenancy Isolation**: Every model and query includes `account_id`.
- **LLM Provider Abstraction**: LLM calls go through `LLMService.generate()`, never raw provider SDKs.
- **Master CV Integrity**: Source of truth is `cv_templates/01_MASTER_CV.tex`; never fabricate facts.

## Standard Verification Step
After modifying code, run:
```bash
python scripts/verify.py
```
This runs the 5-phase verification loop (backend pytest, frontend build, tenant audit, security check, graphify update).


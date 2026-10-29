# Product Development Environment Guide — Job Application Agent SaaS

This project incorporates the engineering operating system standards and developer harnesses adapted from [ECC (Everything Claude Code)](https://github.com/affaan-m/ECC).

---

## 1. Fast Start

### Diagnose Environment Health
Run the environment doctor to verify Python virtualenv, .env credentials, Node modules, and AST graph:
```bash
python scripts/doctor.py
```

### Launch Development Servers
```powershell
.\scripts\dev.ps1
```
- **Backend API**: http://127.0.0.1:8000
- **Interactive Swagger Docs**: http://127.0.0.1:8000/docs
- **Frontend SPA**: http://127.0.0.1:5173

### Install Automated Git Pre-Commit Hook
Enforce verification automatically before any `git commit`:
```bash
python scripts/install_hooks.py
```

---

## 2. The 5-Phase Verification Loop

Before committing code or completing any feature, always run the automated verification tool:
```bash
python scripts/verify.py
```
*(Use `--quick` or `-q` for rapid admin & auth checks during iteration)*

| Phase | Check | Purpose |
|:---:|:---|:---|
| **Phase 1** | Frontend Build | Ensures zero Vite/React JSX or build compilation failures (`npm run build`). |
| **Phase 2** | Pytest Suite | Runs backend tests to guarantee zero regressions. |
| **Phase 3** | Tenancy Audit | Verifies every model carries `account_id` foreign key with proper cascades. |
| **Phase 4** | Secret Leak Scan | Scans modified files for plaintext credentials or exposed API keys. |
| **Phase 5** | AST Graph Update | Updates Graphify knowledge graph (`graphify update .`) for architectural mapping. |

---

## 3. Development Contexts (`contexts/`)

Switch operational focus based on the task:
- [`contexts/dev.md`](file:///contexts/dev.md): Implementation & feature development rules.
- [`contexts/review.md`](file:///contexts/review.md): PR and code review checklist.
- [`contexts/qa.md`](file:///contexts/qa.md): Dogfooding & live tenant impersonation validation.

---

## 4. Agent Rules & Engineering Standards (`.agents/rules/`)

- [`fastapi-backend.md`](file:///.agents/rules/fastapi-backend.md): Async handlers, dependency injection, Pydantic v2 schemas.
- [`react-frontend.md`](file:///.agents/rules/react-frontend.md): Obsidian & Cyber Emerald design system, anti-template quality, glassmorphism modal backdrops.
- [`security-and-tenancy.md`](file:///.agents/rules/security-and-tenancy.md): Tenancy boundaries, AES-256 encryption at rest, prompt injection defenses.
- [`config-protection.md`](file:///.agents/rules/config-protection.md): Strictly prohibits weakening assertions or disabling security checks under pressure.
- [`verification-loop.md`](file:///.agents/rules/verification-loop.md): Mandatory 5-phase verification protocol.

## 5. Automated Health & Quality Tooling (`scripts/`)
- `python scripts/doctor.py`: System diagnostics for virtualenv, packages, `.env` keys, and AST graph.
- `python scripts/check_migrations.py`: Schema boundary and Alembic linear revision tree audit.
- `python scripts/review.py`: Automated code review scanner for bare excepts, debugger remnants, and secret leakage.
- `python scripts/verify.py`: Unified 5-phase verification loop runner.
- `python scripts/install_hooks.py`: Installs git pre-commit hook to automate verification.

---

## 5. Non-Negotiables

1. **Human-in-the-Loop on Send**: Every application ends at Draft; only the human clicks Send.
2. **Tenancy Isolation**: Every table carries `account_id` (except global master CV templates).
3. **Provider-Abstraction LLM Engine**: All model calls route through `LLMService.generate()` with priority failover and bedrock `.env` backup.
4. **Master CV Truth**: Experience facts originate solely from `cv_templates/01_MASTER_CV.tex`. Never fabricate facts.


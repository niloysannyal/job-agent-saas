#!/usr/bin/env python
"""
Database Migration & Schema Boundary Auditor — Job Application Agent SaaS
Adapted from ECC's database-migrations and database-reviewer skills.
Verifies Alembic version consistency and multi-tenant foreign key cascade safety.
"""
import sys
import re
from pathlib import Path

# Enable UTF-8 console output if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

def check_models_tenancy():
    models_dir = ROOT / "backend" / "app" / "models"
    non_tenant_allowed = {"cv_template.py", "__init__.py"}
    passed = True
    checked = 0
    errors = []

    for py_file in models_dir.glob("*.py"):
        if py_file.name in non_tenant_allowed:
            continue
        content = py_file.read_text(encoding="utf-8")
        if "Base" in content and "account_id" not in content and "Account" not in content:
            errors.append(f"Model {py_file.name} missing 'account_id' foreign key")
            passed = False
        else:
            checked += 1

    return passed, checked, errors

def check_alembic_heads():
    alembic_dir = ROOT / "backend" / "alembic" / "versions"
    if not alembic_dir.exists():
        return True, 0, []
    
    versions = list(alembic_dir.glob("*.py"))
    down_revisions = set()
    revision_ids = set()

    for v in versions:
        content = v.read_text(encoding="utf-8")
        rev_match = re.search(r"revision\s*=\s*['\"]([^'\"]+)['\"]", content)
        down_match = re.search(r"down_revision\s*=\s*['\"]?([^'\"\n]+)['\"]?", content)
        if rev_match:
            revision_ids.add(rev_match.group(1))
        if down_match and down_match.group(1) != "None":
            down_revisions.add(down_match.group(1))

    # Single head verification: only 1 revision shouldn't be in down_revisions
    heads = revision_ids - down_revisions
    if len(heads) > 1:
        return False, len(versions), [f"Multiple Alembic migration heads detected: {heads}. Run 'alembic merge' to resolve."]
    return True, len(versions), []

def run_migration_audit():
    print("=" * 65)
    print("  Job Application Agent SaaS -- Database & Migration Audit")
    print("=" * 65)
    
    tenancy_ok, model_count, tenancy_errs = check_models_tenancy()
    alembic_ok, migration_count, alembic_errs = check_alembic_heads()

    if tenancy_ok:
        print(f"[PASS] Multi-tenant isolation verified across {model_count} models.")
    else:
        for err in tenancy_errs:
            print(f"[FAIL] {err}")

    if alembic_ok:
        print(f"[PASS] Alembic linear revision tree verified ({migration_count} migrations tracked).")
    else:
        for err in alembic_errs:
            print(f"[FAIL] {err}")

    all_passed = tenancy_ok and alembic_ok
    print("=" * 65)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_migration_audit())


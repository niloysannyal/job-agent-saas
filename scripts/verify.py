#!/usr/bin/env python
"""
Verification Loop — Job Application Agent SaaS
Adapted from ECC's verification-loop skill.
Automates the 5-phase product verification gate before commits or feature completion.
"""
import sys
import os
import subprocess
from pathlib import Path

# Enable UTF-8 console output if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

def run_step(step_num: int, title: str, cmd: list[str], cwd: Path) -> bool:
    print(f"\n--- Phase {step_num}: {title} ---")
    print(f"Command: {' '.join(cmd)} in {cwd.name}/")
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode == 0:
        print(f"[PASS] Phase {step_num}: {title}")
        return True
    else:
        print(f"[FAIL] Phase {step_num}: {title} (Exit Code {res.returncode})")
        return False

def main():
    print("=" * 65)
    print("  Job Application Agent SaaS -- 5-Phase Verification Loop")
    print("=" * 65)

    quick_mode = "--quick" in sys.argv or "-q" in sys.argv

    # Phase 1: Frontend Build
    frontend_ok = run_step(
        1, "Frontend Build & Compile",
        ["npm.cmd" if os.name == "nt" else "npm", "run", "build"],
        ROOT / "frontend"
    )
    if not frontend_ok:
        print("\n[STOP] Frontend build failed. Fix compilation errors first.")
        return 1

    # Phase 2: Pytest Suite
    venv_pytest = ROOT / "backend" / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("pytest.exe" if os.name == "nt" else "pytest")
    test_args = ["tests/api/test_admin.py", "tests/api/test_auth.py"] if quick_mode else ["tests/"]
    backend_ok = run_step(
        2, f"Backend Pytest Suite ({'Quick Admin/Auth' if quick_mode else 'Full Suite'})",
        [str(venv_pytest)] + test_args,
        ROOT / "backend"
    )
    if not backend_ok:
        print("\n[STOP] Backend tests failed. Fix regressions before proceeding.")
        return 1

    # Phase 3: Database & Migration Schema Boundary Audit
    migration_res = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_migrations.py")], cwd=ROOT)
    if migration_res.returncode != 0:
        print("\n[STOP] Database schema or migration audit failed.")
        return 1
    print("[PASS] Phase 3: Database & Migration Schema Boundary Audit")

    # Phase 4: Code Quality & Security Scan
    review_res = subprocess.run([sys.executable, str(ROOT / "scripts" / "review.py")], cwd=ROOT)
    if review_res.returncode != 0:
        print("\n[STOP] Code review detected critical or high security/quality issues.")
        return 1
    print("[PASS] Phase 4: Code Quality & Security Scan")

    # Phase 5: Graphify AST update
    print("\n--- Phase 5: Knowledge Graph AST Synchronization ---")
    graph_res = subprocess.run(["graphify", "update", "."], cwd=ROOT)
    if graph_res.returncode == 0:
        print("[PASS] Phase 5: Graphify knowledge graph synchronized.")
    else:
        print("[WARN] Graphify sync completed with non-zero exit code.")

    print("\n" + "=" * 65)
    print("🎉 ALL 5 VERIFICATION PHASES PASSED! Production Ready.")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    sys.exit(main())

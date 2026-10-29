#!/usr/bin/env python
"""
Automated Code Quality & Hygiene Reviewer — Job Application Agent SaaS
Adapted from ECC's code-reviewer, fastapi-reviewer, and silent-failure-hunter.
Scans for debug remnants, bare exceptions, secret leaks, and maintainability ceilings.
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

def review_codebase():
    print("=" * 65)
    print("  Job Application Agent SaaS -- Automated Code Quality Review")
    print("=" * 65)

    findings = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}

    # Directories to inspect
    scan_dirs = [
        ROOT / "backend" / "app",
        ROOT / "frontend" / "src"
    ]

    secret_patterns = [r"sk-proj-[a-zA-Z0-9_\-]{20,}", r"ghp_[a-zA-Z0-9]{36}", r"xoxb-[a-zA-Z0-9_\-]+"]
    bare_except_pattern = re.compile(r"except\s*:\s*(#.*)?$")

    for sdir in scan_dirs:
        for f in sdir.rglob("*.*"):
            if f.suffix not in [".py", ".jsx", ".js", ".ts", ".tsx", ".css"]:
                continue
            if "node_modules" in str(f) or ".venv" in str(f) or "dist" in str(f):
                continue

            rel_path = f.relative_to(ROOT)
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()

            # 1. Maintainability ceiling check (soft 800 lines)
            if len(lines) > 800 and f.suffix != ".css":
                findings["MEDIUM"].append(f"{rel_path}: Large source file ({len(lines)} lines, soft ceiling is 800)")

            for idx, line in enumerate(lines, 1):
                # 2. Secret Check (CRITICAL)
                for sp in secret_patterns:
                    if re.search(sp, line):
                        findings["CRITICAL"].append(f"{rel_path}:{idx}: Potential exposed API secret")

                # 3. Bare except check in Python (HIGH)
                if f.suffix == ".py" and bare_except_pattern.search(line.strip()):
                    findings["HIGH"].append(f"{rel_path}:{idx}: Bare except clause without exception type")

                # 4. Debugger in JS/React (HIGH)
                if f.suffix in [".jsx", ".js", ".tsx", ".ts"]:
                    if "debugger;" in line:
                        findings["HIGH"].append(f"{rel_path}:{idx}: Leftover 'debugger;' statement")

    # Output findings
    total_findings = sum(len(v) for v in findings.values())
    
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        items = findings[sev]
        if items:
            print(f"\n[{sev}] ({len(items)} finding(s)):")
            for item in items[:10]:  # limit to top 10 per severity
                print(f"  - {item}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more.")

    print("\n" + "=" * 65)
    if findings["CRITICAL"] or findings["HIGH"]:
        print("  FAIL: Critical or High quality issues must be resolved.")
        print("=" * 65)
        return 1
    elif findings["MEDIUM"]:
        print("  PASS WITH ADVISORIES: All critical checks clean. Maintainability advisories noted.")
        print("=" * 65)
        return 0
    else:
        print("  PASS: Codebase is 100% clean and meets all ECC quality gates.")
        print("=" * 65)
        return 0

if __name__ == "__main__":
    sys.exit(review_codebase())


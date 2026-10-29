#!/usr/bin/env python
"""
Environment & Health Doctor — Job Application Agent SaaS
Adapted from ECC's doctor diagnostic pattern.
Verifies Python version, virtualenv, dependencies, database, and frontend health.
"""
import sys
import os
from pathlib import Path

# Enable UTF-8 console output if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

def check(name: str, passed: bool, detail: str = ""):
    symbol = "+" if passed else "x"
    status = "PASS" if passed else "FAIL"
    print(f"[{symbol}] {name:<35} : {status} {detail}")
    return passed

def run_doctor():
    print("=" * 65)
    print("  Job Application Agent SaaS -- Development Environment Doctor")
    print("=" * 65)
    all_ok = True

    # 1. Python Check
    py_ver = sys.version.split()[0]
    all_ok &= check("Python Version (>=3.11)", sys.version_info >= (3, 11), f"({py_ver})")

    # 2. Virtualenv Check
    venv_python = ROOT / "backend" / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    has_venv = venv_python.exists()
    all_ok &= check("Backend Virtualenv (.venv)", has_venv, str(venv_python))

    # 3. Environment Variables (.env)
    env_file = ROOT / "backend" / ".env"
    has_env = env_file.exists()
    env_keys = []
    if has_env:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    env_keys.append(line.split("=")[0].strip())
    has_openai = "OPENAI_API_KEY" in env_keys
    has_db = "DATABASE_URL" in env_keys
    all_ok &= check("Backend .env File", has_env)
    all_ok &= check("  -> DATABASE_URL present", has_db)
    all_ok &= check("  -> OPENAI_API_KEY present", has_openai)

    # 4. Node & Frontend Check
    package_json = ROOT / "frontend" / "package.json"
    node_modules = ROOT / "frontend" / "node_modules"
    all_ok &= check("Frontend package.json", package_json.exists())
    all_ok &= check("Frontend node_modules", node_modules.exists())

    # 5. Core Rules & Contexts
    contexts = (ROOT / "contexts" / "dev.md").exists() and (ROOT / "contexts" / "review.md").exists()
    all_ok &= check("ECC Dev & Review Contexts", contexts)

    # 6. Graphify Knowledge Graph
    graph_json = ROOT / "graphify-out" / "graph.json"
    all_ok &= check("Graphify AST Knowledge Graph", graph_json.exists())

    print("=" * 65)
    if all_ok:
        print("  All environment health checks PASSED! Ready for development.")
    else:
        print("  Some checks failed. Please resolve the items above before proceeding.")
    print("=" * 65)
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(run_doctor())


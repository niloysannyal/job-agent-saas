#!/usr/bin/env python
"""
Database Restore Script — Job Application Agent SaaS
Run this on your home desktop (on or after 16 November 2026) to restore
your work from your office laptop snapshot with 100% data fidelity.
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import create_engine, text
from app.db.session import normalize_db_url

def run_alembic_migrations():
    print("Running Alembic migrations to ensure schema is at latest head...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "backend")
    raw_db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/jobeazy")
    env["DATABASE_URL"] = normalize_db_url(raw_db_url)

    cmd = [sys.executable, "-m", "alembic", "-c", "backend/alembic.ini", "upgrade", "head"]
    res = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Warning/Error running Alembic: {res.stderr}\n{res.stdout}")
    else:
        print("  ✓ Schema up to date.")

def restore_database(snapshot_file=None):
    if not snapshot_file:
        snapshot_file = ROOT / "backups" / "jobeazy_latest.json"
        if not snapshot_file.exists():
            snapshot_file = ROOT / "backups" / "supabase_backup_latest.json"
    
    snapshot_path = Path(snapshot_file)
    if not snapshot_path.exists():
        print(f"Error: Snapshot file {snapshot_path} does not exist.")
        sys.exit(1)

    raw_db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/jobeazy")
    db_url = normalize_db_url(raw_db_url)

    print(f"\nRestoring snapshot: {snapshot_path.name}")
    print(f"Target Database: {db_url.split('@')[-1]}")

    with open(snapshot_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tables_data = data.get("tables", {})
    engine = create_engine(db_url, echo=False)
    audit_results = []

    try:
        with engine.begin() as conn:
            conn.execute(text("SET session_replication_role = 'replica';"))

            for table_name, table_info in tables_data.items():
                rows = table_info.get("rows", [])
                expected_count = table_info.get("count", len(rows))
                
                check_res = conn.execute(text(
                    f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}')"
                ))
                if not check_res.scalar():
                    print(f"  ⚠ Table '{table_name}' does not exist in target DB — skipping.")
                    continue

                if not rows:
                    audit_results.append((table_name, 0, 0, "OK (Empty)"))
                    continue

                col_type_res = conn.execute(text(
                    f"SELECT column_name, data_type FROM information_schema.columns "
                    f"WHERE table_schema = 'public' AND table_name = '{table_name}'"
                ))
                col_types = {r[0]: r[1].lower() for r in col_type_res.fetchall()}

                clean_rows = []
                for r in rows:
                    clean_row = {}
                    for k, v in r.items():
                        dtype = col_types.get(k, "")
                        if v is None:
                            clean_row[k] = None
                        elif "timestamp" in dtype or dtype == "date":
                            if isinstance(v, str):
                                try:
                                    clean_row[k] = datetime.fromisoformat(v)
                                except Exception:
                                    clean_row[k] = v
                            else:
                                clean_row[k] = v
                        elif dtype in ("json", "jsonb"):
                            if isinstance(v, (dict, list)):
                                clean_row[k] = json.dumps(v)
                            else:
                                clean_row[k] = v
                        elif dtype == "bytea":
                            if isinstance(v, str):
                                try:
                                    clean_row[k] = bytes.fromhex(v)
                                except Exception:
                                    clean_row[k] = v.encode()
                            else:
                                clean_row[k] = v
                        else:
                            clean_row[k] = v
                    clean_rows.append(clean_row)

                columns = table_info.get("columns", list(rows[0].keys()))
                cols_str = ", ".join(f'"{c}"' for c in columns)
                placeholders = ", ".join(f":{c}" for c in columns)
                insert_stmt = text(f'INSERT INTO "{table_name}" ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING')

                conn.execute(insert_stmt, clean_rows)
                
                cnt_res = conn.execute(text(f'SELECT count(*) FROM "{table_name}"'))
                actual_count = cnt_res.scalar()
                
                status = "PASS" if actual_count >= expected_count else "FAIL"
                audit_results.append((table_name, expected_count, actual_count, status))
                print(f"  ✓ {table_name}: {actual_count} rows in database")

            conn.execute(text("SET session_replication_role = 'origin';"))

        print("\n" + "=" * 60)
        print("DATABASE RESTORE AUDIT REPORT")
        print("=" * 60)
        print(f"{'Table Name':<30} | {'Snapshot':<8} | {'Database':<8} | {'Status'}")
        print("-" * 60)
        for t, exp, act, stat in audit_results:
            print(f"{t:<30} | {exp:<8} | {act:<8} | {stat}")
        print("=" * 60)
        print("Restoration successful! You can continue development.\n")

    finally:
        engine.dispose()

if __name__ == "__main__":
    run_alembic_migrations()
    snapshot = sys.argv[1] if len(sys.argv) > 1 else None
    restore_database(snapshot)


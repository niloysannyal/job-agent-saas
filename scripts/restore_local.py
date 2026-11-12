#!/usr/bin/env python
"""
Restore Data to Local PostgreSQL — Job Application Agent SaaS
Restores a JSON snapshot exported from Supabase into the local PostgreSQL instance.
Uses PostgreSQL's session_replication_role='replica' for fast, deadlock-free restoration,
and type-casts ISO strings to datetime and dicts to JSON according to column metadata.
"""
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure backend is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def restore_data(snapshot_file=None, target_db_url=None):
    if not snapshot_file:
        snapshot_file = ROOT / "backups" / "supabase_backup_latest.json"
    snapshot_path = Path(snapshot_file)
    if not snapshot_path.exists():
        print(f"Error: Snapshot file {snapshot_path} does not exist.")
        sys.exit(1)

    if not target_db_url:
        target_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/jobeazy")
    
    if target_db_url.startswith("postgres://"):
        target_db_url = target_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif target_db_url.startswith("postgresql://") and not target_db_url.startswith("postgresql+"):
        target_db_url = target_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif target_db_url.startswith("postgresql+psycopg://"):
        target_db_url = target_db_url.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
    elif target_db_url.startswith("postgresql+psycopg2://"):
        target_db_url = target_db_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

    print(f"Reading snapshot: {snapshot_path.name}")
    with open(snapshot_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tables_data = data.get("tables", {})
    print(f"Snapshot contains {len(tables_data)} tables from {data.get('timestamp')}.")
    print(f"Target Database: {target_db_url.split('@')[-1]}")

    engine = create_async_engine(target_db_url, echo=False)
    audit_results = []

    try:
        async with engine.begin() as conn:
            # Disable triggers & FK constraints for bulk replica restoration
            await conn.execute(text("SET session_replication_role = 'replica';"))

            for table_name, table_info in tables_data.items():
                rows = table_info.get("rows", [])
                expected_count = table_info.get("count", len(rows))
                
                # Check if table exists in target DB
                check_res = await conn.execute(text(
                    f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}')"
                ))
                if not check_res.scalar():
                    print(f"  ⚠ Table '{table_name}' does not exist in target DB — skipping.")
                    continue

                if not rows:
                    audit_results.append((table_name, 0, 0, "OK (Empty)"))
                    continue

                # Query column data types to cast cleanly
                col_type_res = await conn.execute(text(
                    f"SELECT column_name, data_type FROM information_schema.columns "
                    f"WHERE table_schema = 'public' AND table_name = '{table_name}'"
                ))
                col_types = {r[0]: r[1].lower() for r in col_type_res.fetchall()}

                # Type-cast rows according to target schema
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

                # Execute batch insert
                await conn.execute(insert_stmt, clean_rows)
                
                # Verify actual row count
                cnt_res = await conn.execute(text(f'SELECT count(*) FROM "{table_name}"'))
                actual_count = cnt_res.scalar()
                
                status = "PASS" if actual_count >= expected_count else "FAIL"
                audit_results.append((table_name, expected_count, actual_count, status))
                print(f"  ✓ {table_name}: restored {len(rows)} rows (Target count: {actual_count})")

            # Re-enable triggers & FK constraints
            await conn.execute(text("SET session_replication_role = 'origin';"))

        print("\n" + "=" * 60)
        print("TABLE RESTORATION AUDIT REPORT")
        print("=" * 60)
        print(f"{'Table Name':<30} | {'Backup':<8} | {'Target':<8} | {'Status'}")
        print("-" * 60)
        for t, exp, act, stat in audit_results:
            print(f"{t:<30} | {exp:<8} | {act:<8} | {stat}")
        print("=" * 60)
        print("Restoration complete!\n")

    finally:
        await engine.dispose()

if __name__ == "__main__":
    snapshot = sys.argv[1] if len(sys.argv) > 1 else None
    target = sys.argv[2] if len(sys.argv) > 2 else None
    asyncio.run(restore_data(snapshot, target))

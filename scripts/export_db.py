#!/usr/bin/env python
"""
Database Export Script — Job Application Agent SaaS
Exports all tables from the local PostgreSQL database into a portable JSON snapshot.
Run this before switching machines (e.g. on 15 November 2026).
"""
import json
import os
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import create_engine, text
from app.db.session import normalize_db_url

def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, bytes):
        return obj.hex()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_database():
    backups_dir = ROOT / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    json_path = backups_dir / f"jobeazy_backup_{timestamp}.json"
    latest_json_path = backups_dir / "jobeazy_latest.json"

    raw_db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/jobeazy")
    db_url = normalize_db_url(raw_db_url)

    print(f"Exporting local database from: {db_url.split('@')[-1]}...")
    engine = create_engine(db_url, echo=False)

    payload = {
        "timestamp": timestamp,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "tables": {}
    }

    try:
        with engine.connect() as conn:
            res = conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
            ))
            tables = [r[0] for r in res.fetchall()]
            total_rows = 0

            for table in tables:
                col_res = conn.execute(text(
                    f"SELECT column_name, data_type FROM information_schema.columns "
                    f"WHERE table_schema = 'public' AND table_name = '{table}' ORDER BY ordinal_position"
                ))
                columns = [c[0] for c in col_res.fetchall()]

                row_res = conn.execute(text(f'SELECT * FROM "{table}"'))
                rows = row_res.mappings().all()
                row_dicts = [dict(r) for r in rows]
                payload["tables"][table] = {
                    "columns": columns,
                    "count": len(row_dicts),
                    "rows": row_dicts
                }
                total_rows += len(row_dicts)
                print(f"  ✓ {table}: {len(row_dicts)} rows")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, default=json_serializer, indent=2)
        with open(latest_json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, default=json_serializer, indent=2)

        print(f"\nExport successful! {total_rows} rows saved to:")
        print(f"  - {json_path}")
        print(f"  - {latest_json_path}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    export_database()


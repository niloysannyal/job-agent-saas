#!/usr/bin/env python
"""
Backup Supabase Data — Job Application Agent SaaS
Extracts all public tables and rows into a structured JSON snapshot using asyncpg.
"""
import asyncio
import json
import os
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
import uuid

# Ensure backend is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

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

TABLES_IN_DEPENDENCY_ORDER = [
    "alembic_version",
    "subscription_plans",
    "accounts",
    "users",
    "profiles",
    "experience_entries",
    "education_entries",
    "project_entries",
    "skill_entries",
    "jobs",
    "cv_templates",
    "account_cv_versions",
    "applications",
    "interviews",
    "interview_turns",
    "agent_conversations",
    "agent_messages",
    "oauth_accounts",
    "llm_providers",
    "entitlements",
]

async def backup_data():
    backups_dir = ROOT / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    json_path = backups_dir / f"supabase_backup_{timestamp}.json"
    latest_json_path = backups_dir / "supabase_backup_latest.json"

    raw_url = settings.DATABASE_URL
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+"):
        raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif raw_url.startswith("postgresql+psycopg2://"):
        raw_url = raw_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

    print(f"Connecting to database via asyncpg...")
    engine = create_async_engine(raw_url, echo=False)

    backup_payload = {
        "timestamp": timestamp,
        "source": raw_url.split("@")[-1] if "@" in raw_url else "unknown",
        "tables": {}
    }

    try:
        async with engine.connect() as conn:
            res = await conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            existing_tables = set(r[0] for r in res.fetchall())
            print(f"Found {len(existing_tables)} existing tables in public schema.")

            ordered_tables = [t for t in TABLES_IN_DEPENDENCY_ORDER if t in existing_tables]
            for t in sorted(existing_tables):
                if t not in ordered_tables:
                    ordered_tables.append(t)

            total_rows = 0
            for table in ordered_tables:
                col_res = await conn.execute(text(
                    f"SELECT column_name, data_type FROM information_schema.columns "
                    f"WHERE table_schema = 'public' AND table_name = '{table}' ORDER BY ordinal_position"
                ))
                columns = [c[0] for c in col_res.fetchall()]

                row_res = await conn.execute(text(f'SELECT * FROM "{table}"'))
                rows = row_res.mappings().all()
                row_dicts = [dict(r) for r in rows]
                backup_payload["tables"][table] = {
                    "columns": columns,
                    "count": len(row_dicts),
                    "rows": row_dicts
                }
                total_rows += len(row_dicts)
                print(f"  ✓ {table}: {len(row_dicts)} rows backed up")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(backup_payload, f, default=json_serializer, indent=2)
        with open(latest_json_path, "w", encoding="utf-8") as f:
            json.dump(backup_payload, f, default=json_serializer, indent=2)

        print(f"\nSuccessfully backed up {total_rows} total rows across {len(ordered_tables)} tables.")
        print(f"Snapshot written to:")
        print(f"  - {json_path}")
        print(f"  - {latest_json_path}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(backup_data())

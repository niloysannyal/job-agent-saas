"""
scripts/setup_checkpointer.py

One-time / startup script to initialize LangGraph checkpointer tables
and apply Row Level Security in PostgreSQL.
"""

import asyncio
import os
import sys

# Ensure backend is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.config import settings
from app.services.agent.checkpointer import (
    create_checkpointer_pool,
    init_tenant_checkpointer,
)


async def main():
    print(f"Connecting to database: {settings.DATABASE_URL.split('@')[-1]}")
    pool = create_checkpointer_pool(settings.DATABASE_URL)
    async with pool:
        checkpointer = await init_tenant_checkpointer(pool)
        print("TenantScopedAsyncPostgresSaver setup completed successfully!")

        async with checkpointer._cursor() as cur:
            await cur.execute(
                """
                SELECT tablename, rowsecurity
                FROM pg_tables
                WHERE tablename IN ('checkpoints', 'checkpoint_blobs', 'checkpoint_writes', 'checkpoint_migrations', 'thread_accounts')
                ORDER BY tablename;
                """
            )
            rows = await cur.fetchall()
            print("\nTable status:")
            for row in rows:
                print(f"  - {row['tablename']}: RLS enabled = {row['rowsecurity']}")


if __name__ == "__main__":
    asyncio.run(main())


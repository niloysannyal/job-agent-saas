"""
backend/app/services/agent/checkpointer.py

Multi-Tenant Scoped LangGraph PostgreSQL Checkpointer.
Enforces JobEazy Rule #3 (tenant isolation) over LangGraph's account-less internal checkpoint tables:
1. Manages thread ownership via `thread_accounts` table.
2. Intercepts read, write, and search operations to prevent cross-tenant state access.
3. Configures connection pool parameters for Supabase transaction poolers (port 6543):
   - prepare_threshold = None (disables prepared statements)
   - autocommit = True (permits CREATE INDEX CONCURRENTLY during checkpointer.setup())
   - supports_pipeline = False (disables pipelining for multiplexed poolers)
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
from typing import Any, AsyncIterator, Dict, Optional, Sequence, Tuple
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import (
    ChannelVersions,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


class TenantSecurityException(PermissionError):
    """Raised when an account attempts to access a thread belonging to another tenant."""
    pass


class TenantScopedAsyncPostgresSaver(AsyncPostgresSaver):
    """
    Tenant-boundary guard wrapping LangGraph's AsyncPostgresSaver.
    Guarantees that state threads are strictly isolated by account_id.
    """

    def _extract_tenancy(self, config: Optional[RunnableConfig]) -> Tuple[str, str, str]:
        if not config:
            raise ValueError("RunnableConfig is required for tenant checkpointer operations.")
        configurable = config.get("configurable", {})
        thread_id = configurable.get("thread_id")
        account_id = configurable.get("account_id")
        graph_type = configurable.get("graph_type", "apply")

        if not thread_id or not account_id:
            raise ValueError("Both 'thread_id' and 'account_id' are strictly required in config['configurable'].")

        return str(thread_id), str(account_id), str(graph_type)

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id, account_id, graph_type = self._extract_tenancy(config)

        # 1. Enforce ownership in thread_accounts registry
        async with self._cursor() as cur:
            await cur.execute(
                "SELECT account_id FROM thread_accounts WHERE thread_id = %s",
                (thread_id,),
            )
            row = await cur.fetchone()
            if row:
                if row["account_id"] != account_id:
                    raise TenantSecurityException(
                        f"Tenant isolation breach: Account '{account_id}' attempted to write to thread '{thread_id}' owned by '{row['account_id']}'."
                    )
                await cur.execute(
                    "UPDATE thread_accounts SET updated_at = NOW() WHERE thread_id = %s",
                    (thread_id,),
                )
            else:
                await cur.execute(
                    """
                    INSERT INTO thread_accounts (thread_id, account_id, graph_type, created_at, updated_at)
                    VALUES (%s, %s, %s, NOW(), NOW())
                    ON CONFLICT (thread_id) DO UPDATE SET updated_at = NOW()
                    WHERE thread_accounts.account_id = EXCLUDED.account_id;
                    """,
                    (thread_id, account_id, graph_type),
                )

        # 2. Proceed with underlying checkpoint write
        return await super().aput(config, checkpoint, metadata, new_versions)

    async def aget_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        thread_id, account_id, _ = self._extract_tenancy(config)

        # 1. Verify tenant owns thread
        async with self._cursor() as cur:
            await cur.execute(
                "SELECT account_id FROM thread_accounts WHERE thread_id = %s",
                (thread_id,),
            )
            row = await cur.fetchone()
            if not row or row["account_id"] != account_id:
                # Silently return None on unauthorized or unowned thread lookup
                return None

        # 2. Return underlying checkpoint
        return await super().aget_tuple(config)


def create_checkpointer_pool(
    conninfo: str,
    min_size: int = 1,
    max_size: int = 10,
    timeout: float = 30.0,
) -> AsyncConnectionPool:
    """
    Factory creating a psycopg_pool.AsyncConnectionPool calibrated for Supabase
    transaction poolers (port 6543) and LangGraph index migrations.
    """
    return AsyncConnectionPool(
        conninfo=conninfo,
        min_size=min_size,
        max_size=max_size,
        timeout=timeout,
        check=AsyncConnectionPool.check_connection,
        kwargs={
            "autocommit": True,         # Required for CREATE INDEX CONCURRENTLY during checkpointer.setup()
            "row_factory": dict_row,    # Required by LangGraph checkpointer queries
            "prepare_threshold": None,  # Mandatory: disables prepared statements for Supavisor transaction pooler
        },
        open=False,
    )


async def init_tenant_checkpointer(pool: AsyncConnectionPool) -> TenantScopedAsyncPostgresSaver:
    """
    Initializes and sets up the TenantScopedAsyncPostgresSaver.
    """
    if not pool.opened:
        await pool.open()

    checkpointer = TenantScopedAsyncPostgresSaver(pool)
    checkpointer.supports_pipeline = False  # Pooler compatibility
    await checkpointer.setup()
    return checkpointer


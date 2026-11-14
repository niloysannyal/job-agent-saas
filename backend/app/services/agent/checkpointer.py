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

        # G6 Prefix Enforcement: Thread IDs must be securely scoped to the account with trailing hyphens
        valid_prefixes = (
            f"apply-{account_id}-",
            f"copilot-{account_id}-",
            f"{account_id}-",
        )
        if not str(thread_id).startswith(valid_prefixes):
            raise TenantSecurityException(
                f"Thread ID '{thread_id}' violates multi-tenant prefix constraint for account '{account_id}'."
            )

        return str(thread_id), str(account_id), str(graph_type)

    async def _ensure_thread_ownership(
        self,
        cur: Any,
        thread_id: str,
        account_id: str,
        graph_type: str = "apply",
    ) -> None:
        """
        Atomically registers or verifies thread ownership in the thread_accounts table.
        Prevents race conditions and ensures aput_writes (which fires before aput on step 1)
        can safely register the thread.
        """
        await cur.execute(
            """
            INSERT INTO thread_accounts (thread_id, account_id, graph_type, created_at, updated_at)
            VALUES (%s, %s, %s, NOW(), NOW())
            ON CONFLICT (thread_id) DO NOTHING;
            """,
            (thread_id, account_id, graph_type),
        )
        await cur.execute(
            "SELECT account_id FROM thread_accounts WHERE thread_id = %s",
            (thread_id,),
        )
        row = await cur.fetchone()
        if not row or row["account_id"] != account_id:
            owner = row["account_id"] if row else "unknown"
            raise TenantSecurityException(
                f"Tenant isolation breach: Account '{account_id}' attempted to access thread '{thread_id}' owned by '{owner}'."
            )
        await cur.execute(
            "UPDATE thread_accounts SET updated_at = NOW() WHERE thread_id = %s",
            (thread_id,),
        )

    # -----------------------------------------------------------------------
    # Prohibit Sync Checkpointer Methods (G6)
    # -----------------------------------------------------------------------
    def put(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def put_writes(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def get_tuple(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def list(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def delete_thread(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def delete_for_runs(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def copy_thread(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def prune(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    def get_delta_channel_history(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Sync checkpointer methods are prohibited; use async equivalents.")

    # -----------------------------------------------------------------------
    # Async Methods with Strict Tenancy & Atomic Registration (G6 Anti-Race)
    # -----------------------------------------------------------------------
    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id, account_id, graph_type = self._extract_tenancy(config)

        # 1. Atomic registration & verification in thread_accounts registry
        async with self._cursor() as cur:
            await self._ensure_thread_ownership(cur, thread_id, account_id, graph_type)

        # 2. Proceed with underlying checkpoint write
        return await super().aput(config, checkpoint, metadata, new_versions)

    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[Tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        thread_id, account_id, graph_type = self._extract_tenancy(config)
        async with self._cursor() as cur:
            # Bug 1 Fix: aput_writes fires before aput on step 1 of new workflows; ensure ownership atomically
            await self._ensure_thread_ownership(cur, thread_id, account_id, graph_type)
        return await super().aput_writes(config, writes, task_id, task_path=task_path)

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

    async def alist(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[CheckpointTuple]:
        if not config:
            raise ValueError("RunnableConfig with 'account_id' is strictly required for tenant alist.")

        configurable = config.get("configurable", {})
        account_id = configurable.get("account_id")
        if not account_id:
            raise ValueError("Missing 'account_id' in config['configurable'] for alist.")

        thread_id = configurable.get("thread_id")
        if thread_id:
            async with self._cursor() as cur:
                await cur.execute(
                    "SELECT account_id FROM thread_accounts WHERE thread_id = %s",
                    (thread_id,),
                )
                row = await cur.fetchone()
                if not row or row["account_id"] != account_id:
                    return

            async for item in super().alist(config, filter=filter, before=before, limit=limit):
                yield item
        else:
            async with self._cursor() as cur:
                await cur.execute(
                    "SELECT thread_id FROM thread_accounts WHERE account_id = %s",
                    (account_id,),
                )
                rows = await cur.fetchall()
                allowed_thread_ids = {r["thread_id"] for r in rows}

            async for item in super().alist(config, filter=filter, before=before, limit=limit):
                cfg = getattr(item, "config", {}) or {}
                if cfg.get("configurable", {}).get("thread_id") in allowed_thread_ids:
                    yield item

    async def adelete_thread(self, thread_id: str, account_id: Optional[str] = None) -> None:
        """
        Deletes thread checkpoints and cleans up thread_accounts registry.
        Requires account_id validation to prevent unauthenticated or cross-tenant deletion.
        """
        if not account_id:
            raise TenantSecurityException(
                f"Deletion rejected: 'account_id' is mandatory to delete thread '{thread_id}'."
            )

        async with self._cursor() as cur:
            await cur.execute(
                "SELECT account_id FROM thread_accounts WHERE thread_id = %s",
                (thread_id,),
            )
            row = await cur.fetchone()
            if row:
                if row["account_id"] != account_id:
                    raise TenantSecurityException(
                        f"Tenant isolation breach: Account '{account_id}' attempted to delete thread '{thread_id}' owned by '{row['account_id']}'."
                    )
                await cur.execute(
                    "DELETE FROM thread_accounts WHERE thread_id = %s AND account_id = %s",
                    (thread_id, account_id),
                )

        if hasattr(super(), "adelete_thread"):
            await super().adelete_thread(thread_id)

    async def setup(self) -> None:
        """Run underlying setup and enforce Row Level Security on checkpointer tables in Supabase Postgres."""
        await super().setup()
        async with self._cursor() as cur:
            for tbl in ["checkpoints", "checkpoint_blobs", "checkpoint_writes", "checkpoint_migrations", "thread_accounts"]:
                try:
                    await cur.execute(f"ALTER TABLE IF EXISTS {tbl} ENABLE ROW LEVEL SECURITY;")
                except Exception as e:
                    logger.warning(f"Could not enable RLS on {tbl}: {e}")


def normalize_libpq_url(conninfo: str) -> str:
    """Normalize SQLAlchemy or psycopg URL schemes to standard libpq connection URI."""
    if not conninfo:
        return conninfo
    for prefix in ("postgresql+psycopg://", "postgres+psycopg://", "postgresql+psycopg2://"):
        if conninfo.startswith(prefix):
            return "postgresql://" + conninfo[len(prefix):]
    return conninfo


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
    conninfo = normalize_libpq_url(conninfo)
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
    if pool.closed:
        await pool.open()

    checkpointer = TenantScopedAsyncPostgresSaver(pool)
    checkpointer.supports_pipeline = False  # Pooler compatibility
    await checkpointer.setup()
    return checkpointer


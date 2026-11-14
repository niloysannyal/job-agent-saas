"""
backend/tests/agent/test_multi_tenant_checkpointer.py

Unit tests for TenantScopedAsyncPostgresSaver (G6 Hardening):
1. Validates that thread_id and account_id are strictly enforced.
2. Validates prefix enforcement (thread_id must be scoped to account_id).
3. Prohibits all synchronous checkpointer methods (raises NotImplementedError).
4. Asserts tenant isolation on aput, aput_writes, aget_tuple, alist, adelete_thread.
5. Verifies atomic thread registration anti-race behavior.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.agent.checkpointer import (
    TenantScopedAsyncPostgresSaver,
    TenantSecurityException,
    create_checkpointer_pool,
)


@pytest.mark.asyncio
async def test_tenancy_extraction_enforcement():
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    # Missing config
    with pytest.raises(ValueError, match="RunnableConfig is required"):
        saver._extract_tenancy(None)

    # Missing account_id
    with pytest.raises(ValueError, match="Both 'thread_id' and 'account_id' are strictly required"):
        saver._extract_tenancy({"configurable": {"thread_id": "apply-acc-abc-123"}})

    # Prefix mismatch: thread_id does not contain account_id
    with pytest.raises(TenantSecurityException, match="violates multi-tenant prefix constraint"):
        saver._extract_tenancy({
            "configurable": {"thread_id": "apply-acc-victim-123", "account_id": "acc-attacker"}
        })

    # Valid config
    thread_id, account_id, graph_type = saver._extract_tenancy({
        "configurable": {"thread_id": "apply-acc-abc-123", "account_id": "acc-abc", "graph_type": "apply"}
    })
    assert thread_id == "apply-acc-abc-123"
    assert account_id == "acc-abc"
    assert graph_type == "apply"


@pytest.mark.asyncio
async def test_sync_methods_strictly_prohibited():
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.put(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.get(MagicMock())

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.get_tuple(MagicMock())

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.put_writes(MagicMock(), MagicMock(), "task_1")

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.list(MagicMock())

    with pytest.raises(NotImplementedError, match="Sync checkpointer methods are prohibited"):
        saver.delete_thread("thread-1")


@pytest.mark.asyncio
async def test_tenant_cross_access_blocking():
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    mock_cur = AsyncMock()
    # Thread owned by 'account-owner'
    mock_cur.fetchone = AsyncMock(return_value={"account_id": "account-owner"})

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)
    saver._cursor = MagicMock(return_value=mock_ctx)

    # 1. Cross-tenant READ attempt
    read_config = {
        "configurable": {"thread_id": "apply-account-intruder-123", "account_id": "account-intruder"}
    }
    result = await saver.aget_tuple(read_config)
    assert result is None

    # 2. Cross-tenant WRITE attempt
    write_config = {
        "configurable": {"thread_id": "apply-account-intruder-123", "account_id": "account-intruder"}
    }
    with pytest.raises(TenantSecurityException, match="Tenant isolation breach"):
        await saver.aput(write_config, checkpoint=MagicMock(), metadata=MagicMock(), new_versions=MagicMock())

    # 3. Cross-tenant aput_writes attempt
    with pytest.raises(TenantSecurityException, match="Tenant isolation breach"):
        await saver.aput_writes(write_config, writes=[("channel", "data")], task_id="task-1")

    # 4. Cross-tenant adelete_thread attempt
    with pytest.raises(TenantSecurityException, match="Tenant isolation breach"):
        await saver.adelete_thread("apply-account-intruder-123", account_id="account-intruder")

    # 5. Missing account_id in adelete_thread rejected
    with pytest.raises(TenantSecurityException, match="account_id' is mandatory"):
        await saver.adelete_thread("apply-account-intruder-123", account_id=None)


@pytest.mark.asyncio
async def test_prefix_trailing_hyphen_bypass_prevented():
    """Bug 2 Verification: account_id 'acc_1' must not match 'apply-acc_10-xyz'."""
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    # Attacker owns acc_1, tries to access acc_10's thread
    with pytest.raises(TenantSecurityException, match="violates multi-tenant prefix constraint"):
        saver._extract_tenancy({
            "configurable": {"thread_id": "apply-acc_10-thread_uuid", "account_id": "acc_1"}
        })

    # Substring in middle of UUID also rejected
    with pytest.raises(TenantSecurityException, match="violates multi-tenant prefix constraint"):
        saver._extract_tenancy({
            "configurable": {"thread_id": "apply-victim-acc_1-uuid", "account_id": "acc_1"}
        })

    # Exact scoped prefix succeeds
    thread_id, account_id, _ = saver._extract_tenancy({
        "configurable": {"thread_id": "apply-acc_1-thread_uuid", "account_id": "acc_1"}
    })
    assert thread_id == "apply-acc_1-thread_uuid"
    assert account_id == "acc_1"


@pytest.mark.asyncio
async def test_aput_writes_fires_first_and_registers_thread():
    """Bug 1 Verification: aput_writes on step 1 of new workflow registers ownership atomically."""
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    mock_cur = AsyncMock()
    # On first write, insert happens, then fetchone returns the newly registered owner
    mock_cur.fetchone = AsyncMock(return_value={"account_id": "acc-new"})

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)
    saver._cursor = MagicMock(return_value=mock_ctx)

    with patch("langgraph.checkpoint.postgres.aio.AsyncPostgresSaver.aput_writes", new_callable=AsyncMock) as mock_super_writes:
        config = {
            "configurable": {"thread_id": "apply-acc-new-run1", "account_id": "acc-new"}
        }
        await saver.aput_writes(config, writes=[("channel", "data")], task_id="task-0")
        assert mock_super_writes.called

        # Verify atomic registration was attempted
        executed_sqls = [call[0][0] for call in mock_cur.execute.call_args_list]
        assert any("INSERT INTO thread_accounts" in sql for sql in executed_sqls)
        assert any("SELECT account_id FROM thread_accounts" in sql for sql in executed_sqls)


def test_pool_configuration():
    pool = create_checkpointer_pool("postgresql://test:test@localhost:5432/test_db")
    assert pool.kwargs.get("autocommit") is True
    assert pool.kwargs.get("prepare_threshold") is None

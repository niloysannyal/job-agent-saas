"""
backend/tests/agent/test_multi_tenant_checkpointer.py

Unit tests for TenantScopedAsyncPostgresSaver:
1. Validates that thread_id and account_id are strictly enforced.
2. Asserts tenant isolation (Account B cannot read or overwrite Account A's state thread).
3. Verifies TenantSecurityException is raised on cross-tenant write attempts.
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
        saver._extract_tenancy({"configurable": {"thread_id": "thread-123"}})

    # Valid config
    thread_id, account_id, graph_type = saver._extract_tenancy({
        "configurable": {"thread_id": "apply-123", "account_id": "acc-abc", "graph_type": "apply"}
    })
    assert thread_id == "apply-123"
    assert account_id == "acc-abc"
    assert graph_type == "apply"


@pytest.mark.asyncio
async def test_tenant_cross_access_blocking():
    saver = TenantScopedAsyncPostgresSaver(conn=MagicMock())

    # Mock cursor context manager
    mock_cur = AsyncMock()
    # Thread owned by 'account-owner'
    mock_cur.fetchone = AsyncMock(return_value={"account_id": "account-owner"})
    
    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)
    saver._cursor = MagicMock(return_value=mock_ctx)

    # 1. Cross-tenant READ attempt by 'account-intruder'
    read_config = {
        "configurable": {"thread_id": "thread-123", "account_id": "account-intruder"}
    }
    result = await saver.aget_tuple(read_config)
    assert result is None  # Silently returns None for unauthorized lookup

    # 2. Cross-tenant WRITE attempt by 'account-intruder'
    write_config = {
        "configurable": {"thread_id": "thread-123", "account_id": "account-intruder"}
    }
    with pytest.raises(TenantSecurityException, match="Tenant isolation breach"):
        await saver.aput(write_config, checkpoint=MagicMock(), metadata=MagicMock(), new_versions=MagicMock())


def test_pool_configuration():
    pool = create_checkpointer_pool("postgresql://test:test@localhost:5432/test_db")
    assert pool.kwargs.get("autocommit") is True
    assert pool.kwargs.get("prepare_threshold") is None

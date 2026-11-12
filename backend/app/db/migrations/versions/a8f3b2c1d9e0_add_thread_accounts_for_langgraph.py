"""add thread_accounts table for langgraph multi-tenant checkpointer

Revision ID: a8f3b2c1d9e0
Revises: 7f2a94915bf7
Create Date: 2026-11-12 17:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a8f3b2c1d9e0"
down_revision: Union[str, None] = "7f2a94915bf7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "thread_accounts",
        sa.Column("thread_id", sa.String(length=128), primary_key=True, nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("graph_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE", name="fk_thread_accounts_account_id"),
    )
    op.create_index("ix_thread_accounts_account_id", "thread_accounts", ["account_id"], unique=False)
    op.create_index("ix_thread_accounts_account_thread", "thread_accounts", ["account_id", "thread_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_thread_accounts_account_thread", table_name="thread_accounts")
    op.drop_index("ix_thread_accounts_account_id", table_name="thread_accounts")
    op.drop_table("thread_accounts")


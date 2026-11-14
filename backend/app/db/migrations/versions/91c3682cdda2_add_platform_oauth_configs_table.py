"""add platform_oauth_configs table

Revision ID: 91c3682cdda2
Revises: a8f3b2c1d9e0
Create Date: 2026-11-14 15:29:15.260462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91c3682cdda2'
down_revision: Union[str, Sequence[str], None] = 'a8f3b2c1d9e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to include platform_oauth_configs table."""
    op.create_table(
        "platform_oauth_configs",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=True),
        sa.Column("provider", sa.String(length=50), nullable=False, server_default="google"),
        sa.Column("client_id", sa.String(length=255), nullable=False),
        sa.Column("encrypted_client_secret", sa.Text(), nullable=True),
        sa.Column("redirect_uri", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
            ondelete="CASCADE",
            name="fk_platform_oauth_configs_account_id",
        ),
    )
    op.create_index("ix_platform_oauth_configs_account_id", "platform_oauth_configs", ["account_id"], unique=False)
    op.create_index("ix_platform_oauth_configs_provider", "platform_oauth_configs", ["provider"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_platform_oauth_configs_provider", table_name="platform_oauth_configs")
    op.drop_index("ix_platform_oauth_configs_account_id", table_name="platform_oauth_configs")
    op.drop_table("platform_oauth_configs")

"""add_role_and_status_to_accounts

Revision ID: 7b8e2b6659a9
Revises: a7c3e1f24b01
Create Date: 2026-10-28 00:18:58.955930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8e2b6659a9'
down_revision: Union[str, Sequence[str], None] = 'a7c3e1f24b01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'accounts',
        sa.Column('role', sa.String(length=50), nullable=False, server_default='tenant')
    )
    op.add_column(
        'accounts',
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('accounts', 'status')
    op.drop_column('accounts', 'role')


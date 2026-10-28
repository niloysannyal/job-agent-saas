"""add_hashed_password_to_accounts

Revision ID: e57e51d71b2e
Revises: 7b8e2b6659a9
Create Date: 2026-10-28 15:29:00.798651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e57e51d71b2e'
down_revision: Union[str, Sequence[str], None] = '7b8e2b6659a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'accounts',
        sa.Column('hashed_password', sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('accounts', 'hashed_password')

"""add_is_pinned_to_agent_conversations

Revision ID: 74cebd545352
Revises: 3257c49a645d
Create Date: 2026-11-05 11:08:33.434481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74cebd545352'
down_revision: Union[str, Sequence[str], None] = '3257c49a645d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_pinned column to agent_conversations."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'agent_conversations' in existing_tables:
        columns = [c['name'] for c in inspector.get_columns('agent_conversations')]
        if 'is_pinned' not in columns:
            op.add_column(
                'agent_conversations',
                sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default=sa.text('false')),
            )


def downgrade() -> None:
    """Drop is_pinned column from agent_conversations."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'agent_conversations' in existing_tables:
        columns = [c['name'] for c in inspector.get_columns('agent_conversations')]
        if 'is_pinned' in columns:
            op.drop_column('agent_conversations', 'is_pinned')

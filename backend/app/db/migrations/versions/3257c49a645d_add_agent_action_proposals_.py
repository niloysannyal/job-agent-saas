"""add_agent_action_proposals_conversations_messages

Revision ID: 3257c49a645d
Revises: 7f7822f4eef9
Create Date: 2026-11-04 12:49:02.025293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3257c49a645d'
down_revision: Union[str, Sequence[str], None] = '7f7822f4eef9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create agent action proposals, conversations, and messages tables."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    # 1. agent_action_proposals
    if 'agent_action_proposals' not in existing_tables:
        op.create_table(
            'agent_action_proposals',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('action_type', sa.String(length=100), nullable=False),
            sa.Column('target_id', sa.String(length=36), nullable=True),
            sa.Column('title', sa.String(length=255), nullable=False, server_default='Proposed Agent Action'),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('payload_snapshot', sa.JSON(), nullable=False),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
            sa.Column('idempotency_key', sa.String(length=128), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True),
        )
        op.create_index('ix_agent_action_proposals_account_id', 'agent_action_proposals', ['account_id'])
        op.create_index('ix_agent_action_proposals_status', 'agent_action_proposals', ['status'])
        op.create_index('ix_agent_action_proposals_idempotency_key', 'agent_action_proposals', ['idempotency_key'])

    # 2. agent_conversations
    if 'agent_conversations' not in existing_tables:
        op.create_table(
            'agent_conversations',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False, server_default='Agent Session'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_agent_conversations_account_id', 'agent_conversations', ['account_id'])

    # 3. agent_messages
    if 'agent_messages' not in existing_tables:
        op.create_table(
            'agent_messages',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('conversation_id', sa.String(length=36), sa.ForeignKey('agent_conversations.id', ondelete='CASCADE'), nullable=False),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('role', sa.String(length=50), nullable=False),
            sa.Column('content', sa.Text(), nullable=False, server_default=''),
            sa.Column('thought', sa.Text(), nullable=True),
            sa.Column('tool_calls', sa.JSON(), nullable=True),
            sa.Column('tool_result', sa.JSON(), nullable=True),
            sa.Column('ui_widget', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_agent_messages_conversation_id', 'agent_messages', ['conversation_id'])
        op.create_index('ix_agent_messages_account_id', 'agent_messages', ['account_id'])


def downgrade() -> None:
    """Drop agent tables in reverse order."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'agent_messages' in existing_tables:
        op.drop_table('agent_messages')
    if 'agent_conversations' in existing_tables:
        op.drop_table('agent_conversations')
    if 'agent_action_proposals' in existing_tables:
        op.drop_table('agent_action_proposals')

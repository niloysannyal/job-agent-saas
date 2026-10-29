"""add application_form_answers and oauth_connections tables

Revision ID: c4b1297e8df3
Revises: e57e51d71b2e
Create Date: 2026-10-29 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4b1297e8df3'
down_revision: Union[str, Sequence[str], None] = 'e57e51d71b2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create application_form_answers and oauth_connections tables safely."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    # application_form_answers
    if 'application_form_answers' not in tables:
        op.create_table(
            'application_form_answers',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('application_id', sa.String(length=36), sa.ForeignKey('applications.id', ondelete='CASCADE'), nullable=False),
            sa.Column('question_id', sa.String(length=100), nullable=False),
            sa.Column('question_prompt', sa.Text(), nullable=False),
            sa.Column('field_type', sa.String(length=50), nullable=False, server_default='paragraph'),
            sa.Column('tailored_answer', sa.Text(), nullable=False),
            sa.Column('candidate_angles', sa.Text(), nullable=True),
            sa.Column('verified_facts_used', sa.Text(), nullable=True),
            sa.Column('char_count', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_application_form_answers_account_id', 'application_form_answers', ['account_id'])
        op.create_index('ix_application_form_answers_application_id', 'application_form_answers', ['application_id'])

    # oauth_connections
    if 'oauth_connections' not in tables:
        op.create_table(
            'oauth_connections',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('provider', sa.String(length=50), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=True),
            sa.Column('encrypted_access_token', sa.Text(), nullable=True),
            sa.Column('encrypted_refresh_token', sa.Text(), nullable=True),
            sa.Column('token_expires_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('scope', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_oauth_connections_account_id', 'oauth_connections', ['account_id'])


def downgrade() -> None:
    """Drop application_form_answers and oauth_connections tables safely."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if 'oauth_connections' in tables:
        indexes = [idx['name'] for idx in inspector.get_indexes('oauth_connections')]
        if 'ix_oauth_connections_account_id' in indexes:
            op.drop_index('ix_oauth_connections_account_id', table_name='oauth_connections')
        op.drop_table('oauth_connections')

    if 'application_form_answers' in tables:
        indexes = [idx['name'] for idx in inspector.get_indexes('application_form_answers')]
        if 'ix_application_form_answers_application_id' in indexes:
            op.drop_index('ix_application_form_answers_application_id', table_name='application_form_answers')
        if 'ix_application_form_answers_account_id' in indexes:
            op.drop_index('ix_application_form_answers_account_id', table_name='application_form_answers')
        op.drop_table('application_form_answers')

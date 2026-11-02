"""add email verifications table

Revision ID: a81f3d820c74
Revises: f82a17d49b21
Create Date: 2026-11-02 11:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a81f3d820c74'
down_revision: Union[str, Sequence[str], None] = 'f82a17d49b21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'email_verifications' not in existing_tables:
        op.create_table(
            'email_verifications',
            sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('otp_code', sa.String(length=6), nullable=False),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_email_verifications_email', 'email_verifications', ['email'])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'email_verifications' in existing_tables:
        op.drop_index('ix_email_verifications_email', table_name='email_verifications')
        op.drop_table('email_verifications')


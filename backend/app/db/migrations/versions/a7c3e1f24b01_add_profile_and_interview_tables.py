"""add user_profiles target_designations target_locations compensation_expectations spoken_languages star_stories tables

Revision ID: a7c3e1f24b01
Revises: 9fa848922c02
Create Date: 2026-10-26 17:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c3e1f24b01'
down_revision: Union[str, Sequence[str], None] = '9fa848922c02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create Profile and Interview Coach tables."""

    # user_profiles (one-to-one with accounts)
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('current_role', sa.String(255), nullable=True),
        sa.Column('current_company', sa.String(255), nullable=True),
        sa.Column('education', sa.Text(), nullable=True),
        sa.Column('location_city', sa.String(100), nullable=True),
        sa.Column('location_country', sa.String(100), nullable=True),
        sa.Column('portfolio_url', sa.String(500), nullable=True),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('github_url', sa.String(500), nullable=True),
        sa.Column('core_narrative', sa.Text(), nullable=True),
        sa.Column('primary_identity', sa.Text(), nullable=True),
        sa.Column('one_liner', sa.Text(), nullable=True),
        sa.Column('engineering_principle', sa.Text(), nullable=True),
        sa.Column('avoid_phrases', sa.Text(), nullable=True),
        sa.Column('working_style', sa.Text(), nullable=True),
        sa.Column('leadership_example', sa.Text(), nullable=True),
        sa.Column('dealbreakers', sa.Text(), nullable=True),
        sa.Column('notice_period', sa.String(100), nullable=True),
        sa.Column('visa_needs', sa.String(255), nullable=True),
        sa.Column('reason_for_leaving', sa.Text(), nullable=True),
        sa.Column('tone_preferences', sa.Text(), nullable=True),
        sa.Column('master_cv_latex', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_user_profiles_account_id', 'user_profiles', ['account_id'])

    # target_designations
    op.create_table(
        'target_designations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
    )
    op.create_index('ix_target_designations_account_id', 'target_designations', ['account_id'])
    op.create_index('ix_target_designations_profile_id', 'target_designations', ['profile_id'])

    # target_locations
    op.create_table(
        'target_locations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('location_name', sa.String(255), nullable=False),
        sa.Column('location_type', sa.String(50), nullable=False, server_default='any'),
        sa.Column('relocation_willing', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
    )
    op.create_index('ix_target_locations_account_id', 'target_locations', ['account_id'])
    op.create_index('ix_target_locations_profile_id', 'target_locations', ['profile_id'])

    # compensation_expectations (one-to-one with user_profiles)
    op.create_table(
        'compensation_expectations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('min_salary', sa.Float(), nullable=True),
        sa.Column('max_salary', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(10), nullable=False, server_default='USD'),
        sa.Column('period', sa.String(20), nullable=False, server_default='yearly'),
        sa.Column('is_negotiable', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('is_sensitive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
    )
    op.create_index('ix_compensation_expectations_account_id', 'compensation_expectations', ['account_id'])
    op.create_index('ix_compensation_expectations_profile_id', 'compensation_expectations', ['profile_id'])

    # spoken_languages
    op.create_table(
        'spoken_languages',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('language', sa.String(50), nullable=False),
        sa.Column('proficiency', sa.String(50), nullable=False, server_default='fluent'),
    )
    op.create_index('ix_spoken_languages_account_id', 'spoken_languages', ['account_id'])
    op.create_index('ix_spoken_languages_profile_id', 'spoken_languages', ['profile_id'])

    # star_stories
    op.create_table(
        'star_stories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('account_id', sa.String(36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('situation', sa.Text(), nullable=False),
        sa.Column('action', sa.Text(), nullable=False),
        sa.Column('result', sa.Text(), nullable=False),
        sa.Column('good_for_tags', sa.Text(), nullable=False, server_default=''),
        sa.Column('company', sa.String(255), nullable=True),
        sa.Column('role', sa.String(255), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_star_stories_account_id', 'star_stories', ['account_id'])


def downgrade() -> None:
    """Drop Profile and Interview Coach tables."""
    op.drop_table('star_stories')
    op.drop_table('spoken_languages')
    op.drop_table('compensation_expectations')
    op.drop_table('target_locations')
    op.drop_table('target_designations')
    op.drop_table('user_profiles')

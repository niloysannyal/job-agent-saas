"""add universal career tables, profile fields, and job dates

Revision ID: f82a17d49b21
Revises: c4b1297e8df3
Create Date: 2026-10-31 14:30:00.000000

"""
import json
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f82a17d49b21'
down_revision: Union[str, Sequence[str], None] = 'c4b1297e8df3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create universal career entities, add profile fields, and job date/status columns."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    # 1. Update jobs table: is_active and posted_at
    if 'jobs' in existing_tables:
        job_cols = [c['name'] for c in inspector.get_columns('jobs')]
        if 'is_active' not in job_cols:
            op.add_column('jobs', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
            op.create_index('ix_jobs_is_active', 'jobs', ['is_active'])
        if 'posted_at' not in job_cols:
            op.add_column('jobs', sa.Column('posted_at', sa.DateTime(timezone=True), nullable=True))
            op.create_index('ix_jobs_posted_at', 'jobs', ['posted_at'])

    # 2. Update user_profiles table: headline, phone, summary, active_template_id
    if 'user_profiles' in existing_tables:
        prof_cols = [c['name'] for c in inspector.get_columns('user_profiles')]
        if 'headline' not in prof_cols:
            op.add_column('user_profiles', sa.Column('headline', sa.String(length=255), nullable=True))
        if 'phone' not in prof_cols:
            op.add_column('user_profiles', sa.Column('phone', sa.String(length=50), nullable=True))
        if 'summary' not in prof_cols:
            op.add_column('user_profiles', sa.Column('summary', sa.Text(), nullable=True))
        if 'active_template_id' not in prof_cols:
            op.add_column('user_profiles', sa.Column('active_template_id', sa.String(length=36), sa.ForeignKey('cv_templates.id', ondelete='SET NULL'), nullable=True))

    # 3. Create work_experiences table
    if 'work_experiences' not in existing_tables:
        op.create_table(
            'work_experiences',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('profile_id', sa.String(length=36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
            sa.Column('company', sa.String(length=255), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('location', sa.String(length=255), nullable=True),
            sa.Column('location_type', sa.String(length=50), nullable=False, server_default='onsite'),
            sa.Column('start_date', sa.String(length=50), nullable=False),
            sa.Column('end_date', sa.String(length=50), nullable=True),
            sa.Column('is_current', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('highlights', sa.Text(), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_work_experiences_account_id', 'work_experiences', ['account_id'])
        op.create_index('ix_work_experiences_profile_id', 'work_experiences', ['profile_id'])

    # 4. Create educations table
    if 'educations' not in existing_tables:
        op.create_table(
            'educations',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('profile_id', sa.String(length=36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
            sa.Column('institution', sa.String(length=255), nullable=False),
            sa.Column('degree', sa.String(length=255), nullable=False),
            sa.Column('field_of_study', sa.String(length=255), nullable=True),
            sa.Column('start_date', sa.String(length=50), nullable=True),
            sa.Column('end_date', sa.String(length=50), nullable=True),
            sa.Column('grade', sa.String(length=50), nullable=True),
            sa.Column('activities', sa.Text(), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_educations_account_id', 'educations', ['account_id'])
        op.create_index('ix_educations_profile_id', 'educations', ['profile_id'])

    # 5. Create profile_skills table
    if 'profile_skills' not in existing_tables:
        op.create_table(
            'profile_skills',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('profile_id', sa.String(length=36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('category', sa.String(length=50), nullable=False, server_default='Technical'),
            sa.Column('proficiency', sa.String(length=50), nullable=False, server_default='Intermediate'),
            sa.Column('years_of_experience', sa.Float(), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_profile_skills_account_id', 'profile_skills', ['account_id'])
        op.create_index('ix_profile_skills_profile_id', 'profile_skills', ['profile_id'])

    # 6. Create projects table
    if 'projects' not in existing_tables:
        op.create_table(
            'projects',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('profile_id', sa.String(length=36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('role', sa.String(length=255), nullable=True),
            sa.Column('url', sa.String(length=500), nullable=True),
            sa.Column('start_date', sa.String(length=50), nullable=True),
            sa.Column('end_date', sa.String(length=50), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('highlights', sa.Text(), nullable=True),
            sa.Column('technologies', sa.Text(), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_projects_account_id', 'projects', ['account_id'])
        op.create_index('ix_projects_profile_id', 'projects', ['profile_id'])

    # 7. Create certifications table
    if 'certifications' not in existing_tables:
        op.create_table(
            'certifications',
            sa.Column('id', sa.String(length=36), primary_key=True),
            sa.Column('account_id', sa.String(length=36), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('profile_id', sa.String(length=36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('issuing_organization', sa.String(length=255), nullable=False),
            sa.Column('issue_date', sa.String(length=50), nullable=True),
            sa.Column('expiration_date', sa.String(length=50), nullable=True),
            sa.Column('credential_id', sa.String(length=255), nullable=True),
            sa.Column('credential_url', sa.String(length=500), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index('ix_certifications_account_id', 'certifications', ['account_id'])
        op.create_index('ix_certifications_profile_id', 'certifications', ['profile_id'])

    # 8. Data backfill for existing accounts (e.g. Niloy's profile)
    now = datetime.now(timezone.utc)
    res = bind.execute(sa.text('SELECT id, account_id, current_company, "current_role", education FROM user_profiles')).fetchall()
    for row in res:
        p_id, a_id, curr_comp, curr_role, edu_text = row[0], row[1], row[2], row[3], row[4]
        # Backfill headline & summary
        bind.execute(
            sa.text("""
                UPDATE user_profiles 
                SET headline = COALESCE(headline, :headline),
                    summary = COALESCE(summary, :summary)
                WHERE id = :p_id
            """),
            {
                "headline": f"{curr_role or 'Software Engineer'} | Building Scalable Systems",
                "summary": "Experienced professional dedicated to building reliable, high-performance systems and delivering business impact.",
                "p_id": p_id,
            }
        )
        # Check if work experience exists
        exp_count = bind.execute(sa.text("SELECT count(*) FROM work_experiences WHERE profile_id = :p_id"), {"p_id": p_id}).scalar()
        if exp_count == 0 and curr_comp and curr_role:
            betopia_bullets = json.dumps([
                "Led design and engineering of multi-agent and LLM workflow pipelines.",
                "Built production integrations with backend business systems and APIs.",
                "Maintained 99.9% uptime and streamlined deployment monitoring.",
            ])
            bind.execute(
                sa.text("""
                    INSERT INTO work_experiences (id, account_id, profile_id, company, title, location, location_type, start_date, end_date, is_current, description, highlights, order_index, created_at, updated_at)
                    VALUES (:id, :a_id, :p_id, :company, :title, :location, 'onsite', '2023-08', NULL, true, :desc, :highlights, 0, :now, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "a_id": a_id,
                    "p_id": p_id,
                    "company": curr_comp,
                    "title": curr_role,
                    "location": "Dhaka, Bangladesh",
                    "desc": "Core engineering and system architecture.",
                    "highlights": betopia_bullets,
                    "now": now,
                }
            )

        # Check if education exists
        edu_count = bind.execute(sa.text("SELECT count(*) FROM educations WHERE profile_id = :p_id"), {"p_id": p_id}).scalar()
        if edu_count == 0 and edu_text:
            bind.execute(
                sa.text("""
                    INSERT INTO educations (id, account_id, profile_id, institution, degree, field_of_study, start_date, end_date, grade, activities, order_index, created_at, updated_at)
                    VALUES (:id, :a_id, :p_id, :inst, :degree, :field, '2018', '2022', 'First Class', NULL, 0, :now, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "a_id": a_id,
                    "p_id": p_id,
                    "inst": "University of Rajshahi",
                    "degree": "B.Sc.",
                    "field": "Information and Communication Engineering",
                    "now": now,
                }
            )

        # Check if skills exist
        skill_count = bind.execute(sa.text("SELECT count(*) FROM profile_skills WHERE profile_id = :p_id"), {"p_id": p_id}).scalar()
        if skill_count == 0:
            core_skills = [
                ("Python", "Languages", "Expert", 3.0),
                ("FastAPI", "Frameworks", "Expert", 2.5),
                ("PostgreSQL", "Databases", "Advanced", 3.0),
                ("Docker", "Cloud & DevOps", "Advanced", 2.0),
                ("React", "Frontend", "Intermediate", 2.0),
                ("Git & CI/CD", "Tools", "Advanced", 3.0),
            ]
            for idx, (s_name, s_cat, s_prof, s_yrs) in enumerate(core_skills):
                bind.execute(
                    sa.text("""
                        INSERT INTO profile_skills (id, account_id, profile_id, name, category, proficiency, years_of_experience, order_index, created_at)
                        VALUES (:id, :a_id, :p_id, :name, :category, :proficiency, :yrs, :idx, :now)
                    """),
                    {
                        "id": str(uuid.uuid4()),
                        "a_id": a_id,
                        "p_id": p_id,
                        "name": s_name,
                        "category": s_cat,
                        "proficiency": s_prof,
                        "yrs": s_yrs,
                        "idx": idx,
                        "now": now,
                    }
                )


def downgrade() -> None:
    """Revert universal career entities, profile fields, and job date columns."""
    op.drop_table('certifications')
    op.drop_table('projects')
    op.drop_table('profile_skills')
    op.drop_table('educations')
    op.drop_table('work_experiences')

    op.drop_column('user_profiles', 'active_template_id')
    op.drop_column('user_profiles', 'summary')
    op.drop_column('user_profiles', 'phone')
    op.drop_column('user_profiles', 'headline')

    op.drop_index('ix_jobs_posted_at', table_name='jobs')
    op.drop_column('jobs', 'posted_at')
    op.drop_index('ix_jobs_is_active', table_name='jobs')
    op.drop_column('jobs', 'is_active')

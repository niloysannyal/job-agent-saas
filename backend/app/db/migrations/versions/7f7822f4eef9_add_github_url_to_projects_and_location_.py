"""add_github_url_to_projects_and_location_to_educations

Revision ID: 7f7822f4eef9
Revises: b92e4d183f05
Create Date: 2026-11-04 10:35:27.861364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f7822f4eef9'
down_revision: Union[str, Sequence[str], None] = 'b92e4d183f05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add github_url to projects and location to educations."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # 1. Add github_url to projects table
    project_cols = [c["name"] for c in inspector.get_columns("projects")]
    if "github_url" not in project_cols:
        op.add_column("projects", sa.Column("github_url", sa.String(500), nullable=True))

    # 2. Add location to educations table
    edu_cols = [c["name"] for c in inspector.get_columns("educations")]
    if "location" not in edu_cols:
        op.add_column("educations", sa.Column("location", sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema: drop github_url from projects and location from educations."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    project_cols = [c["name"] for c in inspector.get_columns("projects")]
    if "github_url" in project_cols:
        op.drop_column("projects", "github_url")

    edu_cols = [c["name"] for c in inspector.get_columns("educations")]
    if "location" in edu_cols:
        op.drop_column("educations", "location")

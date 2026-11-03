"""add pgvector embedding to jobs

Revision ID: b92e4d183f05
Revises: a81f3d820c74
Create Date: 2026-11-02 16:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'b92e4d183f05'
down_revision: Union[str, Sequence[str], None] = 'a81f3d820c74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    is_postgres = bind.dialect.name == "postgresql"

    # 1. On PostgreSQL, ensure the pgvector extension is activated
    if is_postgres:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. Add embedding column to jobs table if not present
    existing_columns = [c["name"] for c in inspector.get_columns("jobs")]
    if "embedding" not in existing_columns:
        op.add_column(
            "jobs",
            sa.Column("embedding", Vector(1536), nullable=True),
        )

    # 3. Create HNSW index for fast sub-millisecond cosine distance searches
    if is_postgres:
        op.execute(
            "CREATE INDEX IF NOT EXISTS ix_jobs_embedding_hnsw ON jobs USING hnsw (embedding vector_cosine_ops);"
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        op.execute("DROP INDEX IF EXISTS ix_jobs_embedding_hnsw;")

    existing_columns = [c["name"] for c in inspector.get_columns("jobs")]
    if "embedding" in existing_columns:
        op.drop_column("jobs", "embedding")


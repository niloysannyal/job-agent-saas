import os
import sys
from logging.config import fileConfig
from urllib.parse import urlparse

from sqlalchemy import pool
from alembic import context

# Ensure backend root is on Python sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_engine, normalize_db_url
import app.models  # Ensure all SQLAlchemy models are registered on Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def assert_safe_database_url(url: str) -> None:
    """
    Enforces local development boundary per Advisor Review 9.
    Blocks remote host execution (e.g. Supabase, poolers) and requires database name
    ending in _test or _dev unless explicitly bypassed via ALLOW_UNSAFE_DB_OPERATION=true.
    """
    if os.getenv("ALLOW_UNSAFE_DB_OPERATION", "").lower() in ("true", "1", "yes"):
        return

    parsed = urlparse(url)
    host = parsed.hostname or ""
    db_name = (parsed.path or "").lstrip("/")

    if "supabase" in host.lower() or "pooler" in host.lower():
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Migration blocked against remote host: {host}"
        )
    if host not in ("localhost", "127.0.0.1", "db"):
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Migrations must run against local database (localhost/127.0.0.1), got: {host}"
        )
    if not (db_name.endswith(("_test", "_dev")) or db_name in ("jobeazy_dev", "jobeazy_test", "jobeazy")):
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Database name must end in _test or _dev, got: {db_name}"
        )


def get_database_url() -> str:
    url = normalize_db_url(settings.DATABASE_URL)
    assert_safe_database_url(url)
    return url


def include_object(object, name, type_, reflected, compare_to):
    # Filter out preexisting raw-SQL indexes or duplicate unique constraints
    if type_ == "index" and name in (
        "ix_jobs_embedding_hnsw",
        "ix_agent_action_proposals_status",
        "ix_compensation_expectations_account_id",
        "ix_compensation_expectations_profile_id",
        "ix_user_profiles_account_id",
    ):
        return False
    if type_ == "unique_constraint" and name in (
        "user_profiles_account_id_key",
        "compensation_expectations_account_id_key",
        "compensation_expectations_profile_id_key",
    ):
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = get_database_url()
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

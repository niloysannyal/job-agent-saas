import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import pytest

# Ensure safe test database URL is used during test execution
if "DATABASE_URL" not in os.environ or not (os.environ["DATABASE_URL"].endswith(("_test", "_dev")) or "jobeazy_test" in os.environ["DATABASE_URL"]):
    os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5433/jobeazy_test"

# Add backend directory to sys.path so app can be imported
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.core.config import settings
from app.db.session import normalize_db_url


def assert_safe_test_database_url(url: str) -> None:
    """
    Enforces local development and test boundary per Advisor Review 9.
    Blocks test suite execution against remote hosts and requires database name
    ending in _test or _dev unless explicitly bypassed via ALLOW_UNSAFE_DB_OPERATION=true.
    """
    if os.getenv("ALLOW_UNSAFE_DB_OPERATION", "").lower() in ("true", "1", "yes"):
        return

    parsed = urlparse(url)
    host = parsed.hostname or ""
    db_name = (parsed.path or "").lstrip("/")

    if "supabase" in host.lower() or "pooler" in host.lower():
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Test suite refused against remote host: {host}"
        )
    if host not in ("localhost", "127.0.0.1", "db"):
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Tests must run against localhost/127.0.0.1, got: {host}"
        )
    if not (db_name.endswith(("_test", "_dev")) or db_name in ("jobeazy_dev", "jobeazy_test")):
        raise RuntimeError(
            f"SECURITY TRIPWIRE TRIGGERED: Database name must end in _test or _dev, got: {db_name}"
        )


@pytest.fixture(scope="session", autouse=True)
def verify_test_db_safety():
    """Verify database safety before running any tests."""
    url = normalize_db_url(settings.DATABASE_URL)
    assert_safe_test_database_url(url)


@pytest.fixture
def test_db_session():
    """Provides a transactional database session against the safe local test database."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5433/jobeazy_test")
    if "jobeazy_test" not in db_url and "_test" not in db_url:
        db_url = "postgresql+psycopg://postgres:postgres@localhost:5433/jobeazy_test"

    assert_safe_test_database_url(db_url)
    engine = create_engine(db_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        engine.dispose()

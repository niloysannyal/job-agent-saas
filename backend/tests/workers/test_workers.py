from datetime import datetime, timezone, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import SessionLocal
from app.models.account import Account
from app.models.application import Application
from app.models.job import Job
from app.workers.worker import parse_redis_settings, WorkerSettings
from app.workers.tasks import monitor_followups_task, reflect_experience_task


def test_parse_redis_settings():
    """Verify URL parsing for Arq Redis connection settings."""
    settings = parse_redis_settings("redis://:secretpass@redis.example.com:6380/2")
    assert settings.host == "redis.example.com"
    assert settings.port == 6380
    assert settings.password == "secretpass"
    assert settings.database == 2


def test_worker_settings_configuration():
    """Verify Arq WorkerSettings has expected functions, crons, and timeouts."""
    assert len(WorkerSettings.functions) == 4
    assert len(WorkerSettings.cron_jobs) >= 1
    assert WorkerSettings.job_timeout == 300


@pytest.mark.asyncio
async def test_monitor_followups_task(monkeypatch):
    """Verify monitor_followups_task finds applications older than 7 days."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def mock_session():
        return Session(engine)

    monkeypatch.setattr("app.workers.tasks.SessionLocal", mock_session)

    with Session(engine) as session:
        acc = Account(id="acc-worker-1", email="worker@example.com")
        session.add(acc)
        job = Job(
            account_id="acc-worker-1",
            role="AI Engineer",
            company="OpenAI",
            source="remotive",
            apply_link="https://openai.com/apply",
            integrity_status="clean",
        )
        session.add(job)
        session.commit()

        # Recent application (2 days ago)
        app_recent = Application(
            account_id="acc-worker-1",
            job_id=job.id,
            status="applied",
            created_at=datetime.now(timezone.utc) - timedelta(days=2),
        )
        # Stale application (10 days ago)
        app_stale = Application(
            account_id="acc-worker-1",
            job_id=job.id,
            status="applied",
            created_at=datetime.now(timezone.utc) - timedelta(days=10),
        )
        session.add_all([app_recent, app_stale])
        session.commit()

    res = await monitor_followups_task(ctx={}, account_id="acc-worker-1")
    assert res["status"] == "success"
    assert res["followup_due_count"] == 1


@pytest.mark.asyncio
async def test_reflect_experience_task(monkeypatch):
    """Verify reflect_experience_task executes cleanly in worker context."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def mock_session():
        return Session(engine)

    monkeypatch.setattr("app.workers.tasks.SessionLocal", mock_session)

    with Session(engine) as session:
        acc = Account(id="acc-worker-2", email="worker2@example.com")
        session.add(acc)
        session.commit()

    res = await reflect_experience_task(ctx={}, account_id="acc-worker-2")
    assert res["status"] == "success"
    assert "conversion_rate" in res


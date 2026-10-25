from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.account import Account, AccountCreate
from app.models.job import Job, JobPosting


@pytest.fixture
def db_session():
    """In-memory SQLite session for testing models."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_account_model(db_session: Session):
    """Test Account model defaults and multi-tenant fields."""
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    assert account.id is not None
    assert len(account.id) == 36  # UUID string
    assert account.email == "niloy@example.com"
    assert account.plan_tier == "free"
    assert account.account_template_limit is None
    assert account.created_at is not None


def test_job_model_matching_architecture_spec(db_session: Session):
    """
    Test Job model matches ARCHITECTURE.md §7:
    (account_id, company, role, salary, deadline, location_type, country,
     visa_required, target_company, match_score, status, source, apply_link, found_at)
    """
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()

    now = datetime.now(timezone.utc)
    job = Job(
        account_id=account.id,
        company="Optimizely",
        role="AI/ML Engineer",
        description="Build LLM and agentic AI systems.",
        salary="£65,000 - £75,000",
        salary_min=65000.0,
        salary_max=75000.0,
        currency="£",
        deadline=now,
        location_type="hybrid",
        country="UK",
        city="London",
        visa_required=True,
        target_company=True,
        match_score=0.92,
        status="new",
        integrity_status="clean",
        source="adzuna",
        source_job_id="12345",
        apply_link="https://jobs.optimizely.com/12345",
        found_at=now,
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    assert job.id is not None
    assert job.account_id == account.id
    assert job.company == "Optimizely"
    assert job.role == "AI/ML Engineer"
    assert job.visa_required is True
    assert job.target_company is True
    assert job.match_score == 0.92
    assert job.status == "new"
    assert job.integrity_status == "clean"
    assert job.source == "adzuna"
    assert job.apply_link == "https://jobs.optimizely.com/12345"
    assert job.location_type == "hybrid"
    assert job.country == "UK"

    # Verify relationship
    assert job.account.email == "niloy@example.com"
    assert len(account.jobs) == 1
    assert account.jobs[0].id == job.id


def test_pydantic_schemas():
    """Verify Pydantic schemas serialize and validate correctly."""
    acc_in = AccountCreate(email="test@user.com", plan_tier="free")
    assert acc_in.email == "test@user.com"
    assert acc_in.plan_tier == "free"

    posting = JobPosting(
        id="adzuna:999",
        source="adzuna",
        company="DeepMind",
        role="Research Engineer",
        apply_link="https://deepmind.google/careers",
        location_type="on-site",
    )
    assert posting.id == "adzuna:999"
    assert posting.source == "adzuna"
    assert posting.company == "DeepMind"

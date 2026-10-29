import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.application import Application
from app.models.job import Job
from app.models.profile import UserProfile
from app.services.matching.experience_reflector import ExperienceReflector


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_experience_reflector_empty(db_session: Session):
    account_id = "test-empty-acc"
    acc = Account(id=account_id, email="empty@example.com")
    db_session.add(acc)
    db_session.commit()

    reflector = ExperienceReflector(db=db_session)
    insights = reflector.reflect_for_account(account_id)

    assert insights.account_id == account_id
    assert insights.total_applications == 0
    assert insights.interviews_count == 0
    assert insights.overall_conversion_rate == 0.0
    assert len(insights.strategic_recommendations) > 0


def test_experience_reflector_conversion_and_multipliers(db_session: Session):
    account_id = "test-learning-acc"
    acc = Account(id=account_id, email="learner@example.com")
    db_session.add(acc)

    prof = UserProfile(account_id=account_id, full_name="Niloy Sannyal")
    db_session.add(prof)

    job1 = Job(
        account_id=account_id,
        role="Senior AI Engineer",
        company="Anthropic",
        source="remotive",
        apply_link="https://jobs.example.com/apply/1",
        description="Build high-performance systems with FastAPI and Qdrant vector databases.",
        integrity_status="clean",
    )
    job2 = Job(
        account_id=account_id,
        role="Web Developer",
        company="LegacyCorp",
        source="remotive",
        apply_link="https://jobs.example.com/apply/2",
        description="Maintain WordPress sites and legacy PHP backends.",
        integrity_status="clean",
    )
    job3 = Job(
        account_id=account_id,
        role="ML Engineer",
        company="Mistral",
        source="remoteok",
        apply_link="https://jobs.example.com/apply/3",
        description="Train and evaluate open models using PyTorch.",
        integrity_status="clean",
    )
    db_session.add_all([job1, job2, job3])
    db_session.commit()

    app1 = Application(
        account_id=account_id,
        job_id=job1.id,
        channel="email",
        status="interview",
        draft_content="Architected FastAPI microservices with sub-100ms response.",
    )
    app2 = Application(
        account_id=account_id,
        job_id=job2.id,
        channel="email",
        status="rejected",
        draft_content="Experience maintaining WordPress blogs.",
    )
    app3 = Application(
        account_id=account_id,
        job_id=job3.id,
        channel="form",
        status="applied",
    )
    db_session.add_all([app1, app2, app3])
    db_session.commit()

    reflector = ExperienceReflector(db=db_session)
    insights = reflector.reflect_for_account(account_id)

    assert insights.total_applications == 3
    assert insights.interviews_count == 1
    assert insights.rejections_count == 1
    assert insights.overall_conversion_rate == 33.3

    # FastAPI should have a boost multiplier (> 1.0)
    assert "FastAPI" in insights.skill_weight_multipliers
    assert insights.skill_weight_multipliers["FastAPI"] > 1.0

    # Channel stats check
    assert insights.channel_performance["email"].total_applied == 2
    assert insights.channel_performance["email"].interviews == 1
    assert insights.channel_performance["form"].total_applied == 1


def test_experience_insights_api_endpoint(db_session: Session):
    account_id = "test-api-exp-acc"
    acc = Account(id=account_id, email="api-exp@example.com")
    db_session.add(acc)
    db_session.commit()

    app = create_app()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        resp = client.get(
            f"/api/v1/profile/experience-insights?account_id={account_id}",
            headers={"X-Account-ID": account_id},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["account_id"] == account_id
        assert "overall_conversion_rate" in data
        assert "channel_performance" in data
        assert "strategic_recommendations" in data

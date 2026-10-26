import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.job import Job
from app.services.llm.mock_provider import MockLLMProvider
from app.services.llm.service import LLMService


@pytest.fixture
def api_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


from app.api.applications import get_llm_service


@pytest.fixture
def client(api_test_db: Session):
    app = create_app()

    def override_get_db():
        yield api_test_db

    mock_llm = MockLLMProvider(
        default_response="""---COVER_NOTE---
Dear Hiring Team,

I am excited to apply. Having built the Betopia Sales Agent for 600+ salespersons with sub-100ms latency, I look forward to contributing.
---GAPS---
None
---FINAL_COVER---
Dear Hiring Team,

I am excited to apply. Having built the Betopia Sales Agent for 600+ salespersons with sub-100ms latency, I look forward to contributing.
---CONFIRMED_GAPS---
None
"""
    )
    mock_service = LLMService(provider=mock_llm)

    def override_get_llm_service():
        return mock_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_llm_service] = override_get_llm_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_tailor_and_send_application_lifecycle(client: TestClient, api_test_db: Session):
    """
    Test Module 2 (Apply) application tailoring and strict human-in-the-loop Send gate.
    """
    # Create tenant
    account = Account(email="niloy@example.com")
    api_test_db.add(account)
    api_test_db.commit()

    # Create job
    job = Job(
        account_id=account.id,
        company="Anthropic",
        role="AI Research Engineer",
        description="Build LLM evaluations and Python pipelines.",
        apply_link="https://anthropic.com/careers/1",
        source="direct",
    )
    api_test_db.add(job)
    api_test_db.commit()

    # 1. Trigger Tailoring
    tailor_payload = {
        "account_id": account.id,
        "job_id": job.id,
        "channel": "email",
    }
    res = client.post("/api/v1/applications/tailor", json=tailor_payload)
    assert res.status_code == 201
    data = res.json()

    assert data["cv_version"]["id"] is not None
    assert data["application"]["id"] is not None
    assert data["application"]["status"] == "draft"
    # STRICT HUMAN-IN-THE-LOOP: sent_at MUST be null at generation time
    assert data["application"]["sent_at"] is None
    assert "Betopia Sales Agent" in data["application"]["draft_content"]

    app_id = data["application"]["id"]

    # 2. List applications
    list_res = client.get(f"/api/v1/applications?account_id={account.id}")
    assert list_res.status_code == 200
    apps_list = list_res.json()
    assert len(apps_list) == 1
    assert apps_list[0]["id"] == app_id

    # 3. Human Reviews and confirms Send gate
    send_res = client.post(f"/api/v1/applications/{app_id}/send?account_id={account.id}")
    assert send_res.status_code == 200
    sent_app = send_res.json()
    assert sent_app["status"] == "sent"
    assert sent_app["sent_at"] is not None


def test_applications_multi_tenant_isolation(client: TestClient, api_test_db: Session):
    """
    Verify that Account B cannot read, tailor, or send Account A's applications.
    """
    acc_a = Account(email="tenant_a@example.com")
    acc_b = Account(email="tenant_b@example.com")
    api_test_db.add_all([acc_a, acc_b])
    api_test_db.commit()

    job_a = Job(account_id=acc_a.id, company="Corp A", role="Dev", apply_link="http://a.com", source="direct")
    api_test_db.add(job_a)
    api_test_db.commit()

    # Tailor for A
    tailor_res = client.post("/api/v1/applications/tailor", json={
        "account_id": acc_a.id,
        "job_id": job_a.id,
        "channel": "email",
    })
    assert tailor_res.status_code == 201
    app_id_a = tailor_res.json()["application"]["id"]

    # Account B tries to view Account A's applications
    b_list = client.get(f"/api/v1/applications?account_id={acc_b.id}")
    assert b_list.status_code == 200
    assert len(b_list.json()) == 0

    # Account B tries to trigger Send on Account A's application
    b_send = client.post(f"/api/v1/applications/{app_id_a}/send?account_id={acc_b.id}")
    assert b_send.status_code == 404

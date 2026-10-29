import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.interview import StarStory
from app.models.profile import UserProfile


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


@pytest.fixture
def client(api_test_db: Session):
    app = create_app()

    def override_get_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_detect_channel_api_endpoint(client: TestClient, api_test_db: Session):
    account = Account(email="niloy@example.com")
    api_test_db.add(account)
    api_test_db.commit()

    payload = {
        "apply_link": "https://forms.gle/testApplicantForm123",
        "description": "Please fill out our Google Form: https://forms.gle/testApplicantForm123 to apply. Questions include: Why do you want to join? What is your notice period?",
        "company": "DeepMind",
        "role": "Research Engineer",
    }
    response = client.post(f"/api/v1/applications/detect-channel?account_id={account.id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["channel_type"] == "google_form"
    assert data["form_url"] == "https://forms.gle/testApplicantForm123"
    assert len(data["detected_questions"]) >= 2
    prompts = [q["prompt"] for q in data["detected_questions"]]
    assert any("Why do you want to join?" in p for p in prompts)


def test_generate_form_answers_api_endpoint(client: TestClient, api_test_db: Session):
    account = Account(email="niloy@example.com")
    api_test_db.add(account)
    api_test_db.commit()

    # Seed User Profile
    profile = UserProfile(
        account_id=account.id,
        full_name="Niloy Sannyal",
        one_liner="AI Engineer building production agentic and RAG systems",
        portfolio_url="https://niloysannyal.dev",
        github_url="https://github.com/niloysannyal",
        notice_period="2 weeks",
    )
    api_test_db.add(profile)

    # Seed verified STAR story
    story = StarStory(
        account_id=account.id,
        title="Betopia Odoo CRM AI Agent",
        situation="600+ salespersons struggled with manual inquiry turnaround in Odoo CRM. Required an autonomous AI agent operating under sub-100ms latency.",
        action="Engineered FastAPI microservice with Qdrant vector search and dynamic LLM priority failover.",
        result="Cut response turnaround by 65% with zero unplanned downtime for 600+ enterprise users.",
        is_verified=True,
    )
    api_test_db.add(story)
    api_test_db.commit()

    payload = {
        "company_name": "Scale AI",
        "role_title": "Senior AI Systems Engineer",
        "job_description": "We are looking for an engineer to architect high-throughput LLM pipelines.",
        "questions": [
            {
                "id": "why_company",
                "prompt": "Why do you want to join Scale AI as Senior AI Systems Engineer?",
                "field_type": "paragraph",
                "char_limit": 1500,
            },
            {
                "id": "technical_challenge",
                "prompt": "Describe a production system or technical architecture you owned.",
                "field_type": "paragraph",
                "char_limit": 2000,
            },
            {
                "id": "portfolio_links",
                "prompt": "Links to your portfolio or GitHub repositories.",
                "field_type": "url",
            },
        ],
    }

    response = client.post(f"/api/v1/applications/generate-form-answers?account_id={account.id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["company_name"] == "Scale AI"
    assert data["role_title"] == "Senior AI Systems Engineer"
    assert data["total_questions"] == 3
    assert len(data["answers"]) == 3
    assert data["all_facts_verified"] is True

    # Check that answers contain candidate facts
    answers_map = {a["question_id"]: a for a in data["answers"]}
    
    assert "Scale AI" in answers_map["why_company"]["answer"]
    assert len(answers_map["why_company"]["candidate_angles"]) == 2

    assert "Betopia Odoo CRM AI Agent" in answers_map["technical_challenge"]["verified_facts_used"]
    assert "Situation:" in answers_map["technical_challenge"]["answer"]
    assert "600+" in answers_map["technical_challenge"]["answer"]

    assert "github.com/niloysannyal" in answers_map["portfolio_links"]["answer"]


def test_draft_email_api_endpoint(client: TestClient, api_test_db: Session):
    account = Account(email="niloy@example.com")
    api_test_db.add(account)
    api_test_db.commit()

    payload = {
        "account_id": account.id,
        "to_email": "jobs@anthropic.com",
        "subject": "Application: AI Systems Engineer - Niloy Sannyal",
        "body_text": "Hi Anthropic Team, please find my tailored application attached.",
        "from_email": "niloy@example.com",
        "attachment_pdf_base64": "JVBERi0xLjQKJWR1bW15IHBkZiBjb250ZW50Cg==",
        "attachment_filename": "Niloy_Sannyal_Tailored_CV.pdf",
    }

    response = client.post(f"/api/v1/applications/draft-email?account_id={account.id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["to_email"] == "jobs@anthropic.com"
    assert data["subject"] == "Application: AI Systems Engineer - Niloy Sannyal"
    assert "mailto:jobs@anthropic.com" in data["mailto_url"]
    assert data["has_attachment"] is True
    assert "X-Unsent: 1" in data["eml_content"]
    assert "Niloy_Sannyal_Tailored_CV.pdf" in data["eml_content"]


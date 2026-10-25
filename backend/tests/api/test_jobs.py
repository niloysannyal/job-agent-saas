from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.account import Account
from app.models.job import Job


@pytest.fixture
def test_db():
    """In-memory SQLite database session with static pool for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(test_db: Session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_accounts(test_db: Session):
    """Seed test accounts for multi-tenant isolation tests."""
    account_1 = Account(email="niloy@example.com")
    account_2 = Account(email="other@example.com")
    test_db.add_all([account_1, account_2])
    test_db.commit()
    test_db.refresh(account_1)
    test_db.refresh(account_2)
    return account_1, account_2


@pytest.fixture
def seeded_jobs(test_db: Session, seeded_accounts):
    """
    Seed a variety of jobs:
    - High match score, clean
    - Mid match score, clean
    - Low match score, clean
    - Unscored (None), clean
    - Vetoed job (vetoed=True, clean integrity)
    - Flagged job (integrity_status='flagged', vetoed=False)
    - Both vetoed and flagged
    - Job belonging to another account
    """
    account_1, account_2 = seeded_accounts
    now = datetime.now(timezone.utc)

    jobs = [
        Job(
            account_id=account_1.id,
            company="Anthropic",
            role="AI Alignment Engineer",
            match_score=0.95,
            target_company=True,
            vetoed=False,
            veto_reason=None,
            integrity_status="clean",
            source="greenhouse",
            apply_link="https://boards.greenhouse.io/anthropic/jobs/1",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="OpenAI",
            role="ML Systems Engineer",
            match_score=0.80,
            target_company=False,
            vetoed=False,
            veto_reason=None,
            integrity_status="clean",
            source="adzuna",
            apply_link="https://adzuna.com/jobs/2",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="DeepMind",
            role="Research Engineer",
            match_score=0.60,
            target_company=True,
            vetoed=False,
            veto_reason=None,
            integrity_status="clean",
            source="remotive",
            apply_link="https://remotive.com/jobs/3",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="Startup Labs",
            role="Python Developer",
            match_score=None,
            target_company=False,
            vetoed=False,
            veto_reason=None,
            integrity_status="clean",
            source="remoteok",
            apply_link="https://remoteok.com/jobs/4",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="Berlin AI",
            role="Senior ML Engineer",
            match_score=0.98,
            target_company=False,
            vetoed=True,
            veto_reason="Requires undeclared language: german",
            integrity_status="clean",
            source="adzuna",
            apply_link="https://adzuna.com/jobs/5",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="Spam Promotions",
            role="Telegram Promoter",
            match_score=0.92,
            target_company=False,
            vetoed=False,
            veto_reason=None,
            integrity_status="flagged",
            source="adzuna",
            apply_link="https://adzuna.com/jobs/6",
            found_at=now,
        ),
        Job(
            account_id=account_1.id,
            company="Shady Enterprise",
            role="Lead Operator",
            match_score=0.85,
            target_company=False,
            vetoed=True,
            veto_reason="Requires undeclared language: french",
            integrity_status="flagged",
            source="remoteok",
            apply_link="https://remoteok.com/jobs/7",
            found_at=now,
        ),
        # Job belonging to account_2
        Job(
            account_id=account_2.id,
            company="Other Corp",
            role="VP of AI",
            match_score=1.00,
            target_company=True,
            vetoed=False,
            veto_reason=None,
            integrity_status="clean",
            source="greenhouse",
            apply_link="https://boards.greenhouse.io/other/jobs/8",
            found_at=now,
        ),
    ]
    test_db.add_all(jobs)
    test_db.commit()
    return jobs


def test_default_exclusion_behavior(client: TestClient, seeded_accounts, seeded_jobs):
    """
    Default request must exclude vetoed=True and integrity_status='flagged' postings.
    Must also isolate by account_id.
    """
    account_1, _ = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}")
    assert response.status_code == 200
    data = response.json()

    # Total 7 jobs for account_1: 4 clean & non-vetoed, 1 vetoed, 1 flagged, 1 both.
    # Default must return only the 4 clean, non-vetoed jobs.
    assert len(data) == 4

    roles = [j["role"] for j in data]
    assert "AI Alignment Engineer" in roles
    assert "ML Systems Engineer" in roles
    assert "Research Engineer" in roles
    assert "Python Developer" in roles

    # Ensure excluded jobs are NOT present
    assert "Senior ML Engineer" not in roles   # vetoed
    assert "Telegram Promoter" not in roles    # flagged
    assert "Lead Operator" not in roles        # both
    assert "VP of AI" not in roles             # other account


def test_sort_order_match_score_descending(client: TestClient, seeded_accounts, seeded_jobs):
    """
    Verify returned jobs are ordered by match_score descending, with unscored (None) last.
    """
    account_1, _ = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}")
    assert response.status_code == 200
    data = response.json()

    # Scores: 0.95 -> 0.80 -> 0.60 -> None
    scores = [j["match_score"] for j in data]
    assert scores == [0.95, 0.80, 0.60, None]
    assert data[0]["company"] == "Anthropic"
    assert data[1]["company"] == "OpenAI"
    assert data[2]["company"] == "DeepMind"
    assert data[3]["company"] == "Startup Labs"


def test_override_include_vetoed(client: TestClient, seeded_accounts, seeded_jobs):
    """
    include_vetoed=True must include vetoed postings (unless also flagged).
    """
    account_1, _ = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}&include_vetoed=true")
    assert response.status_code == 200
    data = response.json()

    # 4 clean jobs + 1 clean-vetoed job = 5 jobs
    assert len(data) == 5
    roles = [j["role"] for j in data]
    assert "Senior ML Engineer" in roles       # clean & vetoed included
    assert "Telegram Promoter" not in roles    # flagged still excluded
    assert "Lead Operator" not in roles        # both still excluded


def test_override_include_flagged(client: TestClient, seeded_accounts, seeded_jobs):
    """
    include_flagged=True must include flagged postings (unless also vetoed).
    """
    account_1, _ = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}&include_flagged=true")
    assert response.status_code == 200
    data = response.json()

    # 4 clean jobs + 1 flagged-nonvetoed job = 5 jobs
    assert len(data) == 5
    roles = [j["role"] for j in data]
    assert "Telegram Promoter" in roles       # flagged included
    assert "Senior ML Engineer" not in roles   # vetoed still excluded
    assert "Lead Operator" not in roles        # both still excluded


def test_override_show_all(client: TestClient, seeded_accounts, seeded_jobs):
    """
    show_all=True must include all jobs (both vetoed and flagged) for human review.
    """
    account_1, account_2 = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}&show_all=true")
    assert response.status_code == 200
    data = response.json()

    # All 7 jobs for account_1 returned
    assert len(data) == 7
    roles = [j["role"] for j in data]
    assert "Senior ML Engineer" in roles
    assert "Telegram Promoter" in roles
    assert "Lead Operator" in roles

    # Account 2 job must still be excluded (multi-tenant boundary)
    assert "VP of AI" not in roles


def test_response_fields_contract(client: TestClient, seeded_accounts, seeded_jobs):
    """
    Verify company, role, match_score, vetoed, veto_reason, integrity_status,
    and target_company are all present in the response payloads.
    """
    account_1, _ = seeded_accounts

    response = client.get(f"/api/v1/jobs?account_id={account_1.id}&show_all=true")
    assert response.status_code == 200
    data = response.json()

    # Check top job (Anthropic)
    top_job = next(j for j in data if j["company"] == "Anthropic")
    assert top_job["role"] == "AI Alignment Engineer"
    assert top_job["match_score"] == 0.95
    assert top_job["vetoed"] is False
    assert top_job["veto_reason"] is None
    assert top_job["integrity_status"] == "clean"
    assert top_job["target_company"] is True

    # Check vetoed job (Berlin AI)
    vetoed_job = next(j for j in data if j["company"] == "Berlin AI")
    assert vetoed_job["vetoed"] is True
    assert vetoed_job["veto_reason"] == "Requires undeclared language: german"
    assert vetoed_job["integrity_status"] == "clean"

    # Check flagged job (Spam Promotions)
    flagged_job = next(j for j in data if j["company"] == "Spam Promotions")
    assert flagged_job["integrity_status"] == "flagged"
    assert flagged_job["vetoed"] is False


def test_pagination_limit_and_offset(client: TestClient, seeded_accounts, seeded_jobs):
    """
    Verify limit and offset pagination parameters work correctly.
    """
    account_1, _ = seeded_accounts

    # Fetch first 2
    res_page_1 = client.get(f"/api/v1/jobs?account_id={account_1.id}&limit=2&offset=0")
    assert res_page_1.status_code == 200
    page_1 = res_page_1.json()
    assert len(page_1) == 2
    assert page_1[0]["company"] == "Anthropic"
    assert page_1[1]["company"] == "OpenAI"

    # Fetch next 2
    res_page_2 = client.get(f"/api/v1/jobs?account_id={account_1.id}&limit=2&offset=2")
    assert res_page_2.status_code == 200
    page_2 = res_page_2.json()
    assert len(page_2) == 2
    assert page_2[0]["company"] == "DeepMind"
    assert page_2[1]["company"] == "Startup Labs"


def test_root_and_apiv1_routes_both_accessible(client: TestClient, seeded_accounts, seeded_jobs):
    """
    Ensure endpoint is accessible both at /api/v1/jobs and /jobs.
    """
    account_1, _ = seeded_accounts

    res_v1 = client.get(f"/api/v1/jobs?account_id={account_1.id}")
    res_root = client.get(f"/jobs?account_id={account_1.id}")

    assert res_v1.status_code == 200
    assert res_root.status_code == 200
    assert res_v1.json() == res_root.json()

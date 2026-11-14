"""
backend/tests/api/test_tools_api.py

Unit and integration tests for Decoupled Tools API (/api/v1/tools/):
- POST /api/v1/tools/analyze-fit
- POST /api/v1/tools/detect-method
- POST /api/v1/tools/draft-cv
- POST /api/v1/tools/review-cv
- POST /api/v1/tools/draft-outreach
- POST /api/v1/tools/apply-workflow/start
- POST /api/v1/tools/apply-workflow/resume
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.auth import get_current_account
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.job import Job
from app.models.profile import UserProfile, ProfileSkill, WorkExperience


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
def account_a(api_test_db: Session):
    acc = Account(email="niloy@example.com")
    api_test_db.add(acc)
    api_test_db.commit()
    api_test_db.refresh(acc)
    return acc


from contextlib import asynccontextmanager

@pytest.fixture
def client(api_test_db: Session, account_a: Account):
    @asynccontextmanager
    async def dummy_lifespan(app):
        yield

    app = create_app()
    app.router.lifespan_context = dummy_lifespan
    app.dependency_overrides[get_db] = lambda: api_test_db
    app.dependency_overrides[get_current_account] = lambda: account_a
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_job(api_test_db: Session, account_a: Account):
    job = Job(
        account_id=account_a.id,
        role="Lead AI Systems Engineer",
        company="DeepMind",
        description="We are seeking a Lead AI Engineer with Python, FastAPI, Docker, and LLM experience. Send CV to jobs@deepmind.com",
        apply_link="https://deepmind.google/careers",
        source="adzuna",
    )
    api_test_db.add(job)
    api_test_db.commit()
    api_test_db.refresh(job)
    return job


def test_tools_analyze_fit_endpoint(client: TestClient, sample_job: Job):
    """Test POST /api/v1/tools/analyze-fit returns 4-dimension diagnostic."""
    res = client.post(
        "/api/v1/tools/analyze-fit",
        json={"job_id": sample_job.id},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["company"] == "DeepMind"
    assert data["role"] == "Lead AI Systems Engineer"
    assert data["overall_score"] >= 60
    assert "skills" in data["dimensions"]
    assert "experience" in data["dimensions"]
    assert "trajectory" in data["dimensions"]
    assert "seniority" in data["dimensions"]
    assert data["language_gate_passed"] is True


def test_tools_detect_method_endpoint(client: TestClient, sample_job: Job):
    """Test POST /api/v1/tools/detect-method discovers email application."""
    res = client.post(
        "/api/v1/tools/detect-method",
        json={"job_id": sample_job.id},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["channel_type"] == "direct_email"
    assert data["recruiter_email"] == "jobs@deepmind.com"


def test_tools_draft_cv_endpoint(client: TestClient):
    """Test POST /api/v1/tools/draft-cv produces tailored LaTeX without mutation."""
    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = """---TAILORED_SUMMARY---
\\resumeItem{AI Engineer building production agentic AI systems for DeepMind.}
---COVER_NOTE---
Dear Hiring Team at DeepMind, I am excited to apply.
---GAPS---
- None
"""
        res = client.post(
            "/api/v1/tools/draft-cv",
            json={
                "job_role": "Lead AI Engineer",
                "job_company": "DeepMind",
                "job_description": "Python, FastAPI, Docker, and LLMs",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "DeepMind" in data["draft_summary_bullet"]
        assert "DeepMind" in data["draft_cover_letter"]
        assert len(data["draft_assembled_latex"]) > 0


def test_tools_review_cv_endpoint(client: TestClient):
    """Test POST /api/v1/tools/review-cv audits fact integrity and ATS score."""
    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = """---FINAL_SUMMARY---
\\resumeItem{AI Engineer specialized in agentic AI and LLM systems for 600+ salespersons.}
---FINAL_COVER---
Dear DeepMind Team, I am writing to apply.
---CONFIRMED_GAPS---
- None
"""
        res = client.post(
            "/api/v1/tools/review-cv",
            json={
                "draft_latex": "\\documentclass{article}\n\\begin{document}\n\\section{SUMMARY}\n\\resumeItemListStart\n\\resumeItem{AI Engineer}\n\\resumeItemListEnd\n\\end{document}",
                "draft_summary_bullet": "\\resumeItem{AI Engineer}",
                "draft_cover_letter": "Cover note",
                "job_role": "Lead AI Engineer",
                "job_company": "DeepMind",
                "job_description": "Python, FastAPI, Docker, and LLMs",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "ats_score" in data
        assert "fact_audit_passed" in data
        assert "computed_page_count" in data


def test_tools_draft_outreach_endpoint(client: TestClient):
    """Test POST /api/v1/tools/draft-outreach synthesizes tailored copy."""
    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = """SUBJECT: Lead AI Engineer Application - Niloy Sannyal
BODY:
Dear DeepMind Team, I am writing to express my strong enthusiasm for the Lead AI Engineer role.

In my recent experience as an AI Engineer, I built production agentic AI systems embedded in Odoo CRM for 600+ salespersons, with a multi-provider LLM chain and Qdrant RAG.
"""
        res = client.post(
            "/api/v1/tools/draft-outreach",
            json={
                "company_name": "DeepMind",
                "role_title": "Lead AI Engineer",
                "job_description": "Python, FastAPI, Docker, and LLMs",
                "channel_type": "email",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert data["channel_type"] == "email"
        assert "DeepMind" in data["body_content"]
        assert data["facts_verified"] is True


def test_tools_apply_workflow_start_sse_stream(client: TestClient, sample_job: Job):
    """Test POST /api/v1/tools/apply-workflow/start emits SSE stream with thoughts and tools."""
    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = """---TAILORED_SUMMARY---
\\resumeItem{AI Engineer specializing in Agentic AI and FastAPI systems for DeepMind.}
---COVER_NOTE---
Dear Hiring Team at DeepMind, I am thrilled to apply.
---GAPS---
- None
"""
        res = client.post(
            "/api/v1/tools/apply-workflow/start",
            json={
                "job_id": sample_job.id,
                "autonomy_mode": "supervised",
            },
        )
        assert res.status_code == 200
        assert "text/event-stream" in res.headers["content-type"]
        body_text = res.text
        assert "data: " in body_text
        assert "thought" in body_text
        assert "analyze_fit" in body_text


def test_tools_apply_workflow_concurrency_and_stale_lock(client: TestClient, sample_job: Job, api_test_db: Session, account_a: Account):
    """Test Contract 4 / S8 / G7: 409 Conflict on active concurrent run, and stale lock reclamation (>10 min)."""
    from datetime import datetime, timedelta, timezone
    from app.models.agent import ThreadAccount

    now = datetime.now(timezone.utc)
    thread_id = f"apply-{account_a.id}-{sample_job.id[:8]}-active"

    # 1. Active thread (<10 min old) blocks new concurrent run
    active_thread = ThreadAccount(
        thread_id=thread_id,
        account_id=account_a.id,
        graph_type="apply",
        created_at=now - timedelta(minutes=2),
        updated_at=now - timedelta(minutes=2),
    )
    api_test_db.add(active_thread)
    api_test_db.commit()

    res_conflict = client.post(
        "/api/v1/tools/apply-workflow/start",
        json={"job_id": sample_job.id, "autonomy_mode": "supervised"},
    )
    assert res_conflict.status_code == 409
    assert "currently in progress" in res_conflict.json()["detail"]

    # 2. Make thread stale (>10 min old)
    active_thread.updated_at = now - timedelta(minutes=15)
    api_test_db.commit()

    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "---TAILORED_SUMMARY---\n\\resumeItem{AI Engineer}\n---COVER_NOTE---\nCover\n---GAPS---\n- None\n"
        res_reclaimed = client.post(
            "/api/v1/tools/apply-workflow/start",
            json={"job_id": sample_job.id, "autonomy_mode": "supervised"},
        )
        assert res_reclaimed.status_code == 200
        assert "text/event-stream" in res_reclaimed.headers["content-type"]

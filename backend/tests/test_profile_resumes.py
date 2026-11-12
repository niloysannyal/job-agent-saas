import io
import pytest
from datetime import datetime, timezone
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import pypdf

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.profile import (
    UserProfile,
    ProfileSkill,
    WorkExperience,
    Project,
    Education,
    TargetDesignation,
    UserResume,
)
from app.services.matching.profile_parser import ProfileParser


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
def test_account(api_test_db: Session) -> Account:
    account = Account(id="tenant-resume-test-1", email="resume-test@example.com", plan_tier="free")
    api_test_db.add(account)
    api_test_db.commit()
    api_test_db.refresh(account)
    return account


@pytest.fixture
def client(api_test_db: Session):
    app = create_app()

    def override_get_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_minimal_pdf_bytes(text: str = "Test Candidate Resume") -> bytes:
    """Generate a minimal valid 1-page PDF file in memory using pypdf."""
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=595, height=842)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_list_resumes_empty(client: TestClient, test_account: Account):
    res = client.get(f"/api/v1/profile/resumes?account_id={test_account.id}")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["count"] == 0
    assert data["max_limit"] == 5
    assert data["resumes"] == []


def test_upload_resume_pdf_and_default_flag(client: TestClient, test_account: Account):
    pdf_bytes = create_minimal_pdf_bytes("Senior AI Engineer Resume Content")
    files = {"file": ("senior_ai_engineer.pdf", pdf_bytes, "application/pdf")}
    data = {"name": "AI Engineering Resume", "account_id": test_account.id}

    res = client.post("/api/v1/profile/resumes/upload", files=files, data=data)
    assert res.status_code == status.HTTP_200_OK
    body = res.json()
    assert body["name"] == "AI Engineering Resume"
    assert body["filename"] == "senior_ai_engineer.pdf"
    assert body["source_type"] == "uploaded"
    assert body["is_default"] is True  # First resume is automatically default
    assert body["page_count"] >= 1
    assert body["file_size_bytes"] == len(pdf_bytes)

    # Verify listed in GET /resumes
    list_res = client.get(f"/api/v1/profile/resumes?account_id={test_account.id}")
    assert list_res.status_code == 200
    resumes = list_res.json()["resumes"]
    assert len(resumes) == 1
    assert resumes[0]["id"] == body["id"]
    assert resumes[0]["is_default"] is True


def test_save_builder_resume(client: TestClient, test_account: Account):
    latex_code = r"""
    \documentclass{article}
    \begin{document}
    \textbf{Niloy Sannyal} - Principal AI Systems Architect
    \section{Experience}
    Built Betopia Sales Agent and LLM RAG pipelines.
    \end{document}
    """
    payload = {
        "account_id": test_account.id,
        "name": "LaTeX Custom Built Resume",
        "latex_source": latex_code,
        "is_default": False,
    }
    res = client.post("/api/v1/profile/resumes/save-builder", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["name"] == "LaTeX Custom Built Resume"
    assert data["source_type"] == "builder"
    assert data["has_latex"] is True


def test_set_default_resume_toggle(client: TestClient, test_account: Account):
    # Upload resume 1 (becomes default)
    pdf_bytes = create_minimal_pdf_bytes()
    res1 = client.post(
        "/api/v1/profile/resumes/upload",
        files={"file": ("r1.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Resume 1", "account_id": test_account.id},
    ).json()

    # Upload resume 2
    res2 = client.post(
        "/api/v1/profile/resumes/upload",
        files={"file": ("r2.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Resume 2", "account_id": test_account.id},
    ).json()

    assert res1["is_default"] is True

    # Set resume 2 as default
    toggle_res = client.put(f"/api/v1/profile/resumes/{res2['id']}/default?account_id={test_account.id}")
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_default"] is True

    # Check list - resume 2 is default, resume 1 is not
    list_res = client.get(f"/api/v1/profile/resumes?account_id={test_account.id}").json()["resumes"]
    r2_item = next(r for r in list_res if r["id"] == res2["id"])
    r1_item = next(r for r in list_res if r["id"] == res1["id"])
    assert r2_item["is_default"] is True
    assert r1_item["is_default"] is False


def test_max_five_resumes_cap(client: TestClient, test_account: Account):
    pdf_bytes = create_minimal_pdf_bytes()
    # Add 5 resumes
    for i in range(1, 6):
        resp = client.post(
            "/api/v1/profile/resumes/upload",
            files={"file": (f"res_{i}.pdf", pdf_bytes, "application/pdf")},
            data={"name": f"Resume {i}", "account_id": test_account.id},
        )
        assert resp.status_code == 200

    # 6th resume must be rejected with 400
    resp_overflow = client.post(
        "/api/v1/profile/resumes/upload",
        files={"file": ("res_6.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Resume 6", "account_id": test_account.id},
    )
    assert resp_overflow.status_code == 400
    assert "Maximum limit of 5 saved resumes reached" in resp_overflow.json()["detail"]


def test_delete_resume_and_auto_promote_default(client: TestClient, test_account: Account):
    pdf_bytes = create_minimal_pdf_bytes()
    r1 = client.post(
        "/api/v1/profile/resumes/upload",
        files={"file": ("r1.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Resume 1", "account_id": test_account.id},
    ).json()
    r2 = client.post(
        "/api/v1/profile/resumes/upload",
        files={"file": ("r2.pdf", pdf_bytes, "application/pdf")},
        data={"name": "Resume 2", "account_id": test_account.id},
    ).json()

    # R1 is default. Delete R1.
    del_res = client.delete(f"/api/v1/profile/resumes/{r1['id']}?account_id={test_account.id}")
    assert del_res.status_code == 200

    # R2 should now be auto-promoted to default
    list_res = client.get(f"/api/v1/profile/resumes?account_id={test_account.id}").json()["resumes"]
    assert len(list_res) == 1
    assert list_res[0]["id"] == r2["id"]
    assert list_res[0]["is_default"] is True


def test_profile_parser_from_db_structured(api_test_db: Session, test_account: Account):
    """Test that ProfileParser.parse_from_db synthesizes structured profile data + default resume."""
    profile = UserProfile(
        account_id=test_account.id,
        full_name="Niloy Sannyal",
        headline="Senior AI Systems Engineer",
        summary="Specialist in high-throughput agentic workflows, FastAPI, and Qdrant RAG.",
        current_role="Staff AI Engineer",
        current_company="Betopia Global",
        dealbreakers="Non-technical management, unpaid equity only",
    )
    api_test_db.add(profile)
    api_test_db.flush()

    # Add Target Designation
    td = TargetDesignation(account_id=test_account.id, profile_id=profile.id, title="Lead Agentic AI Architect")
    api_test_db.add(td)

    # Add Skill
    skill1 = ProfileSkill(account_id=test_account.id, profile_id=profile.id, name="Qdrant Vector DB", category="AI & MLOps", proficiency="Expert")
    skill2 = ProfileSkill(account_id=test_account.id, profile_id=profile.id, name="FastAPI", category="Backend", proficiency="Expert")
    api_test_db.add_all([skill1, skill2])

    # Add Work Experience
    exp = WorkExperience(
        account_id=test_account.id,
        profile_id=profile.id,
        company="Betopia Global",
        title="Staff AI Engineer",
        start_date="2023",
        end_date="Present",
        is_current=True,
        description="Architected multi-agent dispatch system with sub-100ms latency.",
        highlights="Processed 10M+ daily vector searches.",
    )
    api_test_db.add(exp)

    # Add Default Resume
    resume = UserResume(
        account_id=test_account.id,
        profile_id=profile.id,
        name="Production Resume 2026",
        filename="niloy_prod_2026.pdf",
        source_type="uploaded",
        extracted_text="Production Experience: Designed enterprise sales agent with Odoo and Qdrant integration.",
        is_default=True,
    )
    api_test_db.add(resume)
    api_test_db.commit()

    # Parse profile from DB
    parsed = ProfileParser.parse_from_db(db=api_test_db, account_id=test_account.id)

    assert "Lead Agentic AI Architect" in parsed.target_roles_text
    assert "Non-technical management" in parsed.dealbreakers_text
    assert "Senior AI Systems Engineer" in parsed.combined_embedding_text
    assert "Qdrant Vector DB" in parsed.combined_embedding_text
    assert "FastAPI" in parsed.combined_embedding_text
    assert "Betopia Global" in parsed.combined_embedding_text
    assert "Production Experience: Designed enterprise sales agent" in parsed.combined_embedding_text
    assert "TARGET ROLES:" in parsed.combined_embedding_text
    assert "EXPERIENCE AND SKILLS:" in parsed.combined_embedding_text

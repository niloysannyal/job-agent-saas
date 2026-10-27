import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.auth import get_current_account
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.cv_template import CvTemplate
from app.models.job import Job
from app.models.llm_provider import LLMProviderConfig


@pytest.fixture
def admin_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def superadmin_account(admin_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="superadmin@example.com",
        plan_tier="unlimited",
        role="superadmin",
        status="active",
    )
    admin_test_db.add(acc)
    admin_test_db.commit()
    admin_test_db.refresh(acc)
    return acc


@pytest.fixture
def regular_tenant_account(admin_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="tenant@example.com",
        plan_tier="free",
        role="tenant",
        status="active",
    )
    admin_test_db.add(acc)
    admin_test_db.commit()
    admin_test_db.refresh(acc)
    return acc


@pytest.fixture
def admin_client(admin_test_db: Session, superadmin_account: Account):
    app = create_app()

    def override_get_db():
        yield admin_test_db

    def override_current_account():
        return superadmin_account

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_account] = override_current_account

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def tenant_client(admin_test_db: Session, regular_tenant_account: Account):
    app = create_app()

    def override_get_db():
        yield admin_test_db

    def override_current_account():
        return regular_tenant_account

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_account] = override_current_account

    with TestClient(app) as test_client:
        yield test_client


def test_get_metrics(admin_client: TestClient, admin_test_db: Session, superadmin_account: Account):
    # Add a sample job
    job = Job(
        account_id=superadmin_account.id,
        company="TechCorp",
        role="AI Engineer",
        apply_link="https://techcorp.com/apply",
        source="adzuna",
        integrity_status="clean",
        vetoed=False,
    )
    admin_test_db.add(job)
    admin_test_db.commit()

    resp = admin_client.get("/api/v1/admin/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_tenants"] >= 1
    assert data["total_jobs"] >= 1
    assert data["clean_jobs"] >= 1


def test_tenants_lifecycle(admin_client: TestClient):
    # 1. Create tenant
    create_resp = admin_client.post(
        "/api/v1/admin/tenants",
        json={"email": "newtenant@example.com", "plan_tier": "free", "role": "tenant"},
    )
    assert create_resp.status_code == 200
    tenant_data = create_resp.json()
    tenant_id = tenant_data["id"]
    assert tenant_data["email"] == "newtenant@example.com"
    assert tenant_data["role"] == "tenant"

    # 2. List tenants
    list_resp = admin_client.get("/api/v1/admin/tenants")
    assert list_resp.status_code == 200
    emails = [t["email"] for t in list_resp.json()]
    assert "newtenant@example.com" in emails

    # 3. Update tenant
    update_resp = admin_client.patch(
        f"/api/v1/admin/tenants/{tenant_id}",
        json={"plan_tier": "pro", "status": "suspended"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["plan_tier"] == "pro"
    assert update_resp.json()["status"] == "suspended"

    # 4. Impersonate tenant
    imp_resp = admin_client.post(f"/api/v1/admin/tenants/{tenant_id}/impersonate")
    assert imp_resp.status_code == 200
    assert imp_resp.json()["impersonating"] is True
    assert imp_resp.json()["tenant_id"] == tenant_id

    # 5. Delete tenant
    del_resp = admin_client.delete(f"/api/v1/admin/tenants/{tenant_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "deleted"


def test_llm_providers_lifecycle(admin_client: TestClient):
    # 1. Register provider
    create_resp = admin_client.post(
        "/api/v1/admin/llm-providers",
        json={
            "provider": "anthropic",
            "model_name": "claude-3-5-sonnet",
            "api_key": "test-key-123",
            "is_active": True,
            "priority": 2,
        },
    )
    assert create_resp.status_code == 200
    provider_data = create_resp.json()
    provider_id = provider_data["id"]
    assert provider_data["provider"] == "anthropic"
    assert provider_data["has_api_key"] is True

    # 2. List providers
    list_resp = admin_client.get("/api/v1/admin/llm-providers")
    assert list_resp.status_code == 200
    providers = list_resp.json()
    assert any(p["id"] == provider_id for p in providers)

    # 3. Update provider
    patch_resp = admin_client.patch(
        f"/api/v1/admin/llm-providers/{provider_id}",
        json={"priority": 1, "is_active": False},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["priority"] == 1
    assert patch_resp.json()["is_active"] is False

    # 4. Delete provider
    del_resp = admin_client.delete(f"/api/v1/admin/llm-providers/{provider_id}")
    assert del_resp.status_code == 200


def test_job_sources_list(admin_client: TestClient):
    resp = admin_client.get("/api/v1/admin/jobs/sources")
    assert resp.status_code == 200
    sources = resp.json()
    assert len(sources) >= 5
    source_names = [s["name"] for s in sources]
    assert "adzuna" in source_names
    assert "remotive" in source_names
    assert "remoteok" in source_names


def test_admin_templates_lifecycle(admin_client: TestClient):
    create_resp = admin_client.post(
        "/api/v1/admin/templates",
        json={
            "name": "Modern_Executive_CV",
            "description": "Executive 1-page template",
            "latex_source": "\\documentclass{article}\\begin{document}Executive\\end{document}",
            "is_admin_default": False,
        },
    )
    assert create_resp.status_code == 200
    tmpl_id = create_resp.json()["id"]

    list_resp = admin_client.get("/api/v1/admin/templates")
    assert list_resp.status_code == 200
    assert any(t["id"] == tmpl_id for t in list_resp.json())

    del_resp = admin_client.delete(f"/api/v1/admin/templates/{tmpl_id}")
    assert del_resp.status_code == 200


def test_require_superadmin_forbidden(tenant_client: TestClient):
    # A regular tenant attempting to access admin endpoints should receive 403 Forbidden
    resp = tenant_client.get("/api/v1/admin/metrics")
    assert resp.status_code == 403
    assert "Superadmin privileges required" in resp.json()["detail"]

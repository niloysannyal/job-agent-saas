import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.auth import create_access_token
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account


@pytest.fixture
def auth_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def auth_client(auth_test_db: Session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: auth_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_user(auth_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="testuser@example.com",
        plan_tier="free",
        role="tenant",
        status="active",
    )
    acc.set_password("MySecurePass123!")
    auth_test_db.add(acc)
    auth_test_db.commit()
    auth_test_db.refresh(acc)
    return acc


@pytest.fixture
def suspended_user(auth_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="suspended@example.com",
        plan_tier="free",
        role="tenant",
        status="suspended",
    )
    acc.set_password("Pass1234!")
    auth_test_db.add(acc)
    auth_test_db.commit()
    auth_test_db.refresh(acc)
    return acc


def test_login_success(auth_client: TestClient, seeded_user: Account):
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "MySecurePass123!"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["account_id"] == seeded_user.id
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "tenant"


def test_login_invalid_password(auth_client: TestClient, seeded_user: Account):
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "WrongPassword!"},
    )
    assert resp.status_code == 401
    assert "Invalid email or password" in resp.json()["detail"]


def test_login_nonexistent_email(auth_client: TestClient):
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.com", "password": "AnyPassword!"},
    )
    assert resp.status_code == 401
    assert "Invalid email or password" in resp.json()["detail"]


def test_login_suspended_account(auth_client: TestClient, suspended_user: Account):
    resp = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "suspended@example.com", "password": "Pass1234!"},
    )
    assert resp.status_code == 403
    assert "suspended" in resp.json()["detail"]


def test_get_me_with_valid_jwt(auth_client: TestClient, seeded_user: Account):
    token = create_access_token(
        data={
            "sub": seeded_user.id,
            "email": seeded_user.email,
            "role": seeded_user.role,
            "plan_tier": seeded_user.plan_tier,
        }
    )
    resp = auth_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == seeded_user.id
    assert data["email"] == seeded_user.email
    assert data["role"] == "tenant"


def test_get_me_with_invalid_jwt(auth_client: TestClient):
    resp = auth_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert resp.status_code == 401


def test_register_new_tenant(auth_client: TestClient):
    resp = auth_client.post(
        "/api/v1/auth/register",
        json={"email": "newcandidate@example.com", "password": "StrongPassword123!"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["email"] == "newcandidate@example.com"
    assert data["role"] == "tenant"


def test_register_duplicate_email(auth_client: TestClient, seeded_user: Account):
    resp = auth_client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "AnotherPassword!"},
    )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["detail"]


def test_jwt_bearer_token_enforces_superadmin_guard(
    auth_client: TestClient, seeded_user: Account, auth_test_db: Session
):
    # Regular tenant token attempting to access superadmin endpoints
    tenant_token = create_access_token(
        data={"sub": seeded_user.id, "email": seeded_user.email, "role": "tenant"}
    )
    resp = auth_client.get(
        "/api/v1/admin/tenants",
        headers={"Authorization": f"Bearer {tenant_token}"},
    )
    assert resp.status_code == 403

    # Superadmin token accessing superadmin endpoint
    admin_acc = Account(
        id=str(uuid.uuid4()),
        email="super@example.com",
        plan_tier="unlimited",
        role="superadmin",
        status="active",
    )
    auth_test_db.add(admin_acc)
    auth_test_db.commit()

    admin_token = create_access_token(
        data={"sub": admin_acc.id, "email": admin_acc.email, "role": "superadmin"}
    )
    resp_admin = auth_client.get(
        "/api/v1/admin/tenants",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp_admin.status_code == 200


def test_send_otp_success(auth_client: TestClient):
    resp = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": "newcandidate@example.com"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["email"] == "newcandidate@example.com"
    assert "dev_otp" in data
    assert len(data["dev_otp"]) == 6


def test_send_otp_invalid_email(auth_client: TestClient):
    resp = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": "not-an-email"},
    )
    assert resp.status_code == 422


def test_send_otp_duplicate_email(auth_client: TestClient, seeded_user: Account):
    resp = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": seeded_user.email},
    )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["detail"]


def test_send_otp_rate_limiting(auth_client: TestClient):
    email = "ratelimit@example.com"
    resp1 = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": email},
    )
    assert resp1.status_code == 200

    # Second immediate attempt must trigger 429 cooldown
    resp2 = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": email},
    )
    assert resp2.status_code == 429
    assert "wait 60 seconds" in resp2.json()["detail"]


def test_verify_otp_success_creates_account_and_profile(auth_client: TestClient, auth_test_db: Session):
    email = "verifiedcandidate@example.com"
    otp_resp = auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": email},
    )
    assert otp_resp.status_code == 200
    code = otp_resp.json()["dev_otp"]

    verify_resp = auth_client.post(
        "/api/v1/auth/signup/verify-otp",
        json={
            "email": email,
            "otp_code": code,
            "password": "SecurePassword123!",
            "full_name": "Verified Candidate",
            "headline": "Lead Systems Architect",
        },
    )
    assert verify_resp.status_code == 201
    auth_data = verify_resp.json()
    assert auth_data["email"] == email
    assert auth_data["is_new_user"] is True
    assert "access_token" in auth_data

    # Verify database state
    from app.models.profile import UserProfile
    from app.models.subscription import Entitlement

    acc = auth_test_db.query(Account).filter_by(email=email).first()
    assert acc is not None
    assert acc.verify_password("SecurePassword123!") is True

    prof = auth_test_db.query(UserProfile).filter_by(account_id=acc.id).first()
    assert prof is not None
    assert prof.full_name == "Verified Candidate"
    assert prof.headline == "Lead Systems Architect"

    ent = auth_test_db.query(Entitlement).filter_by(account_id=acc.id).first()
    assert ent is not None
    assert ent.all_access is True


def test_verify_otp_wrong_code(auth_client: TestClient):
    email = "wrongcode@example.com"
    auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": email},
    )

    verify_resp = auth_client.post(
        "/api/v1/auth/signup/verify-otp",
        json={
            "email": email,
            "otp_code": "000000",
            "password": "SecurePassword123!",
            "full_name": "Test Candidate",
        },
    )
    assert verify_resp.status_code == 400
    assert "Invalid verification code" in verify_resp.json()["detail"]


def test_verify_otp_expired_code(auth_client: TestClient, auth_test_db: Session):
    from datetime import datetime, timedelta, timezone
    from app.models.account import EmailVerification

    email = "expired@example.com"
    auth_client.post(
        "/api/v1/auth/signup/send-otp",
        json={"email": email},
    )

    # Force expiration in DB
    ver = auth_test_db.query(EmailVerification).filter_by(email=email).first()
    ver.expires_at = datetime.now(timezone.utc) - timedelta(minutes=15)
    auth_test_db.commit()

    verify_resp = auth_client.post(
        "/api/v1/auth/signup/verify-otp",
        json={
            "email": email,
            "otp_code": ver.otp_code,
            "password": "SecurePassword123!",
            "full_name": "Expired Candidate",
        },
    )
    assert verify_resp.status_code == 400
    assert "expired" in verify_resp.json()["detail"]



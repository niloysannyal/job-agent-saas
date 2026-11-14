import uuid
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.auth import get_current_account
from app.core.crypto import encrypt_secret, decrypt_secret
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.oauth import OAuthConnection, PlatformOAuthAppConfig
from app.services.integrations.google_service import GoogleIntegrationService


@pytest.fixture
def oauth_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def superadmin_account(oauth_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="superadmin@example.com",
        plan_tier="unlimited",
        role="superadmin",
        status="active",
    )
    oauth_test_db.add(acc)
    oauth_test_db.commit()
    oauth_test_db.refresh(acc)
    return acc


@pytest.fixture
def tenant_account(oauth_test_db: Session) -> Account:
    acc = Account(
        id=str(uuid.uuid4()),
        email="tenant@example.com",
        plan_tier="free",
        role="tenant",
        status="active",
    )
    oauth_test_db.add(acc)
    oauth_test_db.commit()
    oauth_test_db.refresh(acc)
    return acc


@pytest.fixture
def admin_client(oauth_test_db: Session, superadmin_account: Account) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: oauth_test_db
    app.dependency_overrides[get_current_account] = lambda: superadmin_account
    return TestClient(app)


@pytest.fixture
def tenant_client(oauth_test_db: Session, tenant_account: Account) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: oauth_test_db
    app.dependency_overrides[get_current_account] = lambda: tenant_account
    return TestClient(app)


def test_admin_google_oauth_crud(admin_client: TestClient, oauth_test_db: Session):
    """Verify SuperAdmin can view, configure, and reset platform Google OAuth app credentials."""
    # 1. Initial check (falls back to env or empty)
    res = admin_client.get("/api/v1/admin/integrations/google")
    assert res.status_code == 200
    data = res.json()
    assert "configured" in data
    assert "source" in data

    # 2. Save custom credentials via UI
    payload = {
        "client_id": "test-gcp-12345.apps.googleusercontent.com",
        "client_secret": "super-secret-gcp-secret-xyz",
        "redirect_uri": "http://localhost:5173/auth/google/callback",
        "is_active": True,
    }
    save_res = admin_client.post("/api/v1/admin/integrations/google", json=payload)
    assert save_res.status_code == 200
    saved = save_res.json()
    assert saved["configured"] is True
    assert saved["source"] == "db"
    assert saved["client_id"] == "test-gcp-12345.apps.googleusercontent.com"
    assert saved["has_secret"] is True
    # Secret must never be leaked plaintext in response
    assert "super-secret-gcp-secret-xyz" not in str(saved)

    # 3. Verify in DB encrypted
    row = oauth_test_db.query(PlatformOAuthAppConfig).filter_by(provider="google").first()
    assert row is not None
    assert row.client_id == "test-gcp-12345.apps.googleusercontent.com"
    assert decrypt_secret(row.encrypted_client_secret) == "super-secret-gcp-secret-xyz"

    # 4. Dynamic resolution by GoogleIntegrationService
    creds = GoogleIntegrationService.resolve_platform_credentials(db=oauth_test_db)
    assert creds["client_id"] == "test-gcp-12345.apps.googleusercontent.com"
    assert creds["client_secret"] == "super-secret-gcp-secret-xyz"
    assert creds["source"] == "db"

    # 5. Delete/Revert
    del_res = admin_client.delete("/api/v1/admin/integrations/google")
    assert del_res.status_code == 200
    assert oauth_test_db.query(PlatformOAuthAppConfig).filter_by(provider="google").count() == 0


def test_tenant_cannot_access_admin_oauth(tenant_client: TestClient):
    """Regular candidates cannot view or edit platform Google OAuth credentials."""
    res = tenant_client.get("/api/v1/admin/integrations/google")
    assert res.status_code == 403


def test_unified_email_status_empty(tenant_client: TestClient):
    """When no connection exists, unified status returns connected=False."""
    res = tenant_client.get("/api/v1/integrations/email/status")
    assert res.status_code == 200
    data = res.json()
    assert data["connected"] is False
    assert data["provider"] is None
    assert data["email"] is None


def test_smtp_connect_and_disconnect(tenant_client: TestClient, oauth_test_db: Session, tenant_account: Account):
    """Verify candidate can connect and disconnect email via SMTP / Gmail App Password."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_instance = MagicMock()
        mock_smtp.return_value = mock_instance

        # 1. Connect
        payload = {
            "email": "candidate@gmail.com",
            "app_password": "abcd efgh ijkl mnop",
            "host": "smtp.gmail.com",
            "port": 587,
        }
        res = tenant_client.post("/api/v1/integrations/smtp/connect", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["email"] == "candidate@gmail.com"
        assert data["provider"] == "smtp"

        # Verify SMTP connection test was performed
        mock_instance.starttls.assert_called_once()
        mock_instance.login.assert_called_once_with("candidate@gmail.com", "abcdefghijklmnop")

        # 2. Check unified status
        status_res = tenant_client.get("/api/v1/integrations/email/status")
        assert status_res.status_code == 200
        status_data = status_res.json()
        assert status_data["connected"] is True
        assert status_data["provider"] == "smtp"
        assert status_data["email"] == "candidate@gmail.com"

        # 3. Disconnect
        disc_res = tenant_client.post("/api/v1/integrations/smtp/disconnect")
        assert disc_res.status_code == 200

        # 4. Status should be disconnected
        status_after = tenant_client.get("/api/v1/integrations/email/status").json()
        assert status_after["connected"] is False


def test_google_oauth_callback_flow(tenant_client: TestClient, oauth_test_db: Session, tenant_account: Account):
    """Verify code exchange and callback upsert into oauth_connections."""
    from app.api.integrations import generate_oauth_state
    signed_state = generate_oauth_state(tenant_account.id)
    res = tenant_client.post(
        "/api/v1/integrations/google/callback",
        json={"code": "4/0AfDfakecode12345", "state": signed_state},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["connected"] is True
    assert data["provider"] == "google"
    assert data["email"] == "user@gmail.com"

    # Verify unified status reflects Google
    status_res = tenant_client.get("/api/v1/integrations/email/status").json()
    assert status_res["connected"] is True
    assert status_res["provider"] == "google"
    assert status_res["email"] == "user@gmail.com"

    # Disconnect
    disc = tenant_client.post("/api/v1/integrations/google/disconnect")
    assert disc.status_code == 200
    assert tenant_client.get("/api/v1/integrations/email/status").json()["connected"] is False


def test_google_oauth_state_csrf_and_tenant_verification(tenant_client: TestClient, tenant_account: Account, oauth_test_db: Session):
    """Verify state parameter is cryptographically signed and rejects tampering/spoofing."""
    from urllib.parse import urlparse, parse_qs
    from app.api.integrations import generate_oauth_state, verify_oauth_state

    # 1. Generate auth URL
    res = tenant_client.get("/api/v1/integrations/google/auth-url")
    assert res.status_code == 200
    auth_url = res.json()["auth_url"]

    # 2. Extract state parameter
    parsed = urlparse(auth_url)
    qs = parse_qs(parsed.query)
    assert "state" in qs
    state_token = qs["state"][0]

    # 3. Verify state resolves to the correct account_id
    verified_id = verify_oauth_state(state_token)
    assert verified_id == tenant_account.id

    # 4. Tampered state must be rejected
    with pytest.raises(Exception):
        verify_oauth_state(state_token + "tampered")

    # 5. GET callback with valid signed state executes redirect
    with patch("app.services.integrations.google_service.GoogleIntegrationService.exchange_code_for_tokens") as mock_exchange:
        mock_exchange.return_value = {
            "access_token": "ya29.test_token",
            "refresh_token": "1//test_refresh",
            "email": "verified.user@gmail.com",
            "expires_in": 3600,
            "scope": "https://www.googleapis.com/auth/gmail.send",
        }
        cb_res = tenant_client.get(
            f"/api/v1/integrations/google/callback?code=mock_code&state={state_token}",
            follow_redirects=False,
        )
        assert cb_res.status_code == 307
        assert "google_connected=true" in cb_res.headers["location"]

        # Verify DB connection record
        conn = oauth_test_db.query(OAuthConnection).filter_by(account_id=tenant_account.id).first()
        assert conn is not None
        assert conn.email == "verified.user@gmail.com"

    # 6. GET callback with spoofed/tampered state fails with 400
    forged_res = tenant_client.get(
        "/api/v1/integrations/google/callback?code=mock_code&state=forged_state_token",
        follow_redirects=False,
    )
    assert forged_res.status_code == 400



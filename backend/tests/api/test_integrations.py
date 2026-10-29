import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.crypto import encrypt_secret, decrypt_secret
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.oauth import OAuthConnection
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


def test_crypto_encryption_roundtrip():
    """Verify secrets are encrypted and decrypted accurately."""
    secret = "ya29.a0AfH6SMAmock-secret-oauth-token-12345"
    encrypted = encrypt_secret(secret)
    assert encrypted != secret
    assert isinstance(encrypted, str)
    decrypted = decrypt_secret(encrypted)
    assert decrypted == secret


def test_google_auth_url_endpoint(client: TestClient):
    """Verify GET /api/v1/integrations/google/auth-url returns a valid Google consent URL."""
    headers = {"X-Account-ID": "test-tenant-oauth-1"}
    resp = client.get("/api/v1/integrations/google/auth-url", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "accounts.google.com/o/oauth2/v2/auth" in data["auth_url"]
    assert "gmail.compose" in data["auth_url"]


def test_google_callback_and_status(client: TestClient, api_test_db: Session):
    """Verify code exchange, DB persistence with encryption, status check, and disconnect."""
    account_id = "test-tenant-oauth-2"
    # Ensure account exists
    acc = api_test_db.query(Account).filter_by(id=account_id).first()
    if not acc:
        acc = Account(id=account_id, email="tenant-oauth2@example.com", role="tenant")
        api_test_db.add(acc)
        api_test_db.commit()

    headers = {"X-Account-ID": account_id}

    # Initially status should be connected=False
    status_resp = client.get("/api/v1/integrations/google/status", headers=headers)
    assert status_resp.status_code == 200
    assert status_resp.json()["connected"] is False

    # Simulate OAuth callback with authorization code
    cb_resp = client.post(
        "/api/v1/integrations/google/callback",
        headers=headers,
        json={"code": "4/0AeanS0TESTING_AUTH_CODE", "state": "test_state"},
    )
    assert cb_resp.status_code == 200
    cb_data = cb_resp.json()
    assert cb_data["connected"] is True
    assert cb_data["provider"] == "google"
    assert cb_data["email"] == "user@gmail.com"

    # Verify encrypted in DB
    conn = api_test_db.query(OAuthConnection).filter_by(account_id=account_id, provider="google").first()
    assert conn is not None
    assert conn.encrypted_access_token is not None
    assert decrypt_secret(conn.encrypted_access_token).startswith("mock_access_token")

    # Status should now be connected=True
    status_resp2 = client.get("/api/v1/integrations/google/status", headers=headers)
    assert status_resp2.status_code == 200
    assert status_resp2.json()["connected"] is True

    # Test creating Gmail draft
    draft_resp = client.post(
        "/api/v1/integrations/google/create-draft",
        headers=headers,
        json={
            "recipient_email": "recruiter@techcorp.io",
            "subject": "Senior AI Engineer Application - Alex Mercer",
            "body_text": "Hi Jane, I am reaching out regarding the Senior AI Engineer role.",
            "attach_cv": False,
        },
    )
    assert draft_resp.status_code == 200
    draft_data = draft_resp.json()
    assert draft_data["success"] is True
    assert "draft_id" in draft_data
    assert "mail.google.com" in draft_data["web_link"]

    # Disconnect
    disc_resp = client.post("/api/v1/integrations/google/disconnect", headers=headers)
    assert disc_resp.status_code == 200
    assert disc_resp.json()["success"] is True

    # Confirm disconnected
    status_resp3 = client.get("/api/v1/integrations/google/status", headers=headers)
    assert status_resp3.status_code == 200
    assert status_resp3.json()["connected"] is False


def test_bookmarklet_generation(client: TestClient, api_test_db: Session):
    """Verify bookmarklet JS generation uses candidate profile facts."""
    account_id = "test-tenant-bm-1"
    acc = api_test_db.query(Account).filter_by(id=account_id).first()
    if not acc:
        acc = Account(id=account_id, email="alex.m@example.com", role="tenant")
        api_test_db.add(acc)

    prof = api_test_db.query(UserProfile).filter_by(account_id=account_id).first()
    if not prof:
        prof = UserProfile(
            account_id=account_id,
            full_name="Alex Mercer",
            github_url="https://github.com/alexmercer",
            linkedin_url="https://linkedin.com/in/alexmercer",
            portfolio_url="https://alexmercer.dev",
        )
        api_test_db.add(prof)
    api_test_db.commit()

    headers = {"X-Account-ID": account_id}
    resp = client.get("/api/v1/integrations/autofill/bookmarklet", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "bookmarklet_js" in data
    assert "javascript:(function()" in data["bookmarklet_js"]
    assert "Alex Mercer" in data["bookmarklet_js"]
    assert "alex.m@example.com" in data["bookmarklet_js"]

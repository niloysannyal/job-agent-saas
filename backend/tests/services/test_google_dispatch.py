import os
import sys
from pathlib import Path
import uuid
from unittest.mock import AsyncMock, patch
import pytest
from cryptography.fernet import Fernet
import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.core.config import settings
from app.core.crypto import (
    encrypt_oauth_token,
    decrypt_oauth_token,
    get_oauth_fernet,
    _derive_legacy_key,
)
from app.models.account import Account
from app.models.oauth import OAuthConnection
from app.services.integrations.mime_builder import (
    MimeBuilder,
    InvalidEmailRecipientException,
    InvalidPdfPayloadException,
    MessageSizeExceededException,
    GMAIL_MAX_MESSAGE_BYTES,
)
from app.services.integrations.google_service import (
    GoogleIntegrationService,
    GmailApiException,
    GmailApiNotConfiguredException,
    GmailRateLimitException,
    GmailInsufficientPermissionsException,
    GmailServerErrorException,
    GmailNetworkTimeoutException,
    GMAIL_FULL_OAUTH_SCOPES,
    GMAIL_SEND_URL,
)
from scripts.migrate_oauth_encryption import migrate_oauth_tokens


# --- 1. MimeBuilder Tests ---

def test_mime_builder_plain_message():
    """Verify basic plaintext MIME message construction."""
    import email
    raw = MimeBuilder.build_message(
        to="recruiter@example.com",
        subject="Senior Systems Engineer",
        body_text="Hello, please consider my application.",
        send_id="test-send-uuid-1234",
    )
    parsed = email.message_from_bytes(raw)
    assert parsed["To"] == "recruiter@example.com"
    assert parsed["Subject"] == "Senior Systems Engineer"
    assert parsed["X-JobEazy-Send-ID"] == "test-send-uuid-1234"
    body_payload = parsed.get_payload(decode=True).decode("utf-8")
    assert "Hello, please consider my application." in body_payload

    # Verify base64url encoding
    b64 = MimeBuilder.to_base64url(raw)
    assert isinstance(b64, str)
    assert len(b64) > 0


def test_mime_builder_with_valid_pdf():
    """Verify multipart MIME message with valid PDF magic bytes."""
    import email
    valid_pdf = b"%PDF-1.7\nSample binary content for testing\n%%EOF"
    raw = MimeBuilder.build_message(
        to="hiring@techcorp.com",
        subject="Platform Lead Application",
        body_text="Attached is my tailored CV.",
        pdf_bytes=valid_pdf,
        pdf_filename="Niloy_Sannyal_CV.pdf",
        extra_headers={"In-Reply-To": "<msg123@techcorp.com>"},
    )
    parsed = email.message_from_bytes(raw)
    assert parsed.is_multipart()
    assert parsed["To"] == "hiring@techcorp.com"
    assert parsed["Subject"] == "Platform Lead Application"
    assert parsed["In-Reply-To"] == "<msg123@techcorp.com>"

    parts = parsed.get_payload()
    assert len(parts) == 2

    # Plaintext part
    text_part = parts[0]
    assert text_part.get_content_type() == "text/plain"
    assert "Attached is my tailored CV." in text_part.get_payload(decode=True).decode("utf-8")

    # PDF attachment part
    pdf_part = parts[1]
    assert pdf_part.get_content_type() == "application/pdf"
    assert pdf_part.get_filename() == "Niloy_Sannyal_CV.pdf"
    assert pdf_part.get_payload(decode=True) == valid_pdf


def test_mime_builder_invalid_recipient():
    """Verify RFC 5322 invalid recipient emails are rejected."""
    with pytest.raises(InvalidEmailRecipientException):
        MimeBuilder.build_message(
            to="not-an-email",
            subject="Subj",
            body_text="Body",
        )

    with pytest.raises(InvalidEmailRecipientException):
        MimeBuilder.build_message(
            to="@missinguser.com",
            subject="Subj",
            body_text="Body",
        )


def test_mime_builder_invalid_pdf_bytes():
    """Verify non-PDF bytes (missing %PDF-1. magic header) are rejected."""
    invalid_pdf = b"NOT_A_PDF_HEADER but something else"
    with pytest.raises(InvalidPdfPayloadException):
        MimeBuilder.build_message(
            to="recruiter@example.com",
            subject="Subj",
            body_text="Body",
            pdf_bytes=invalid_pdf,
        )


def test_mime_builder_exceeds_size_ceiling():
    """Verify payloads exceeding Gmail 25 MB ceiling are blocked."""
    # Create oversized payload using mock
    with patch("app.services.integrations.mime_builder.GMAIL_MAX_MESSAGE_BYTES", 100):
        with pytest.raises(MessageSizeExceededException):
            MimeBuilder.build_message(
                to="recruiter@example.com",
                subject="Subj",
                body_text="A" * 200,
            )


# --- 2. MultiFernet Key Rotation & Isolation Tests ---

def test_multifernet_single_key_roundtrip():
    """Verify OAuth token encryption and decryption roundtrip."""
    raw_token = "ya29.a0AfH6SMA-test-access-token-12345"
    encrypted = encrypt_oauth_token(raw_token)
    assert encrypted != raw_token
    decrypted = decrypt_oauth_token(encrypted)
    assert decrypted == raw_token


def test_multifernet_key_rotation():
    """
    Advisor Review 10 Requirement:
    Encrypt with K_old, configure MultiFernet with [K_new, K_old],
    verify decryption succeeds with fallback, and new encryption uses K_new.
    """
    key_old = Fernet.generate_key().decode("ascii")
    key_new = Fernet.generate_key().decode("ascii")

    # 1. Encrypt with old key
    mf_old = get_oauth_fernet(keys_override=[key_old])
    raw_secret = "refresh_token_secret_xyz_98765"
    encrypted_with_old = mf_old.encrypt(raw_secret.encode("utf-8")).decode("ascii")

    # 2. Configure rotated MultiFernet with [key_new, key_old]
    mf_rotated = get_oauth_fernet(keys_override=[key_new, key_old])

    # 3. Decrypt ciphertext encrypted with old key -> MUST succeed via fallback
    decrypted = mf_rotated.decrypt(encrypted_with_old.encode("ascii")).decode("utf-8")
    assert decrypted == raw_secret

    # 4. Encrypt new secret with rotated MultiFernet -> uses key_new
    new_secret = "new_access_token_11111"
    encrypted_new = mf_rotated.encrypt(new_secret.encode("utf-8")).decode("ascii")

    # Verify key_new decrypts it directly
    fernet_new = Fernet(key_new.encode("ascii"))
    assert fernet_new.decrypt(encrypted_new.encode("ascii")).decode("utf-8") == new_secret


def test_worker_isolation_without_jwt_secret():
    """
    Advisor Review 10 Requirement:
    Worker process with only OAUTH_ENCRYPTION_KEY can decrypt without JWT_SECRET_KEY.
    """
    key = Fernet.generate_key().decode("ascii")
    token = "secret_oauth_token_val_456"

    # Simulate environment with explicit OAUTH_ENCRYPTION_KEY
    with patch.object(settings, "OAUTH_ENCRYPTION_KEY", key):
        with patch.object(settings, "JWT_SECRET_KEY", "completely-different-jwt-key"):
            encrypted = encrypt_oauth_token(token)
            decrypted = decrypt_oauth_token(encrypted)
            assert decrypted == token


# --- 3. GoogleIntegrationService Tests ---

def test_google_auth_url_scope():
    """Verify authorization URL includes gmail.send, gmail.compose, and userinfo.email."""
    url = GoogleIntegrationService.get_authorization_url(state="test_state_123")
    assert "gmail.send" in url
    assert "gmail.compose" in url
    assert "userinfo.email" in url
    assert "state=test_state_123" in url


@pytest.mark.asyncio
async def test_mock_send_gmail_message():
    """Verify mock send dispatch returns id, threadId, and SENT label."""
    raw_mime = MimeBuilder.build_message(
        to="recruiter@target.com",
        subject="Engineering Role",
        body_text="Hi team",
    )
    result = await GoogleIntegrationService.send_gmail_message(
        access_token="mock_access_token_xyz",
        raw_mime_bytes=raw_mime,
    )
    assert "id" in result
    assert "threadId" in result
    assert result["labelIds"] == ["SENT"]
    assert result["id"].startswith("mock_sent_msg_")


@pytest.mark.asyncio
async def test_send_gmail_error_mapping():
    """Verify mapping of Google HTTP error codes to specification exception classes."""
    raw_mime = MimeBuilder.build_message(
        to="recruiter@target.com",
        subject="Subj",
        body_text="Body",
    )

    # Test 403 accessNotConfigured -> GmailApiNotConfiguredException
    mock_resp_403_cfg = httpx.Response(
        status_code=403,
        json={"error": {"errors": [{"reason": "accessNotConfigured"}], "message": "API disabled"}},
    )
    with patch("httpx.AsyncClient.post", return_value=mock_resp_403_cfg):
        with pytest.raises(GmailApiNotConfiguredException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)

    # Test 403 rateLimitExceeded -> GmailRateLimitException
    mock_resp_403_rate = httpx.Response(
        status_code=403,
        json={"error": {"errors": [{"reason": "rateLimitExceeded"}], "message": "Limit hit"}},
    )
    with patch("httpx.AsyncClient.post", return_value=mock_resp_403_rate):
        with pytest.raises(GmailRateLimitException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)

    # Test 403 insufficientPermissions -> GmailInsufficientPermissionsException
    mock_resp_403_perm = httpx.Response(
        status_code=403,
        json={"error": {"errors": [{"reason": "insufficientPermissions"}], "message": "Missing send scope"}},
    )
    with patch("httpx.AsyncClient.post", return_value=mock_resp_403_perm):
        with pytest.raises(GmailInsufficientPermissionsException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)

    # Test 429 Too Many Requests -> GmailRateLimitException
    mock_resp_429 = httpx.Response(
        status_code=429,
        json={"error": {"message": "Too many requests"}},
    )
    with patch("httpx.AsyncClient.post", return_value=mock_resp_429):
        with pytest.raises(GmailRateLimitException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)

    # Test 503 Service Unavailable -> GmailServerErrorException
    mock_resp_503 = httpx.Response(
        status_code=503,
        json={"error": {"message": "Service unavailable"}},
    )
    with patch("httpx.AsyncClient.post", return_value=mock_resp_503):
        with pytest.raises(GmailServerErrorException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)

    # Test Timeout -> GmailNetworkTimeoutException
    with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timed out")):
        with pytest.raises(GmailNetworkTimeoutException):
            await GoogleIntegrationService.send_gmail_message("real_live_token", raw_mime)


# --- 4. Migration Script Verification Test ---

def test_migrate_oauth_encryption_script(test_db_session):
    """
    Verify migrate_oauth_tokens re-encrypts rows from legacy Fernet to MultiFernet cleanly.
    """
    account_id = str(uuid.uuid4())
    account = Account(id=account_id, email=f"mig_{uuid.uuid4().hex[:6]}@example.com")

    # Create legacy-encrypted token
    legacy_fernet = _derive_legacy_key(settings.JWT_SECRET_KEY)
    legacy_f = Fernet(legacy_fernet)
    old_access_token = "ya29.legacy_token_12345"
    old_refresh_token = "refresh_legacy_67890"

    legacy_enc_access = legacy_f.encrypt(old_access_token.encode("utf-8")).decode("ascii")
    legacy_enc_refresh = legacy_f.encrypt(old_refresh_token.encode("utf-8")).decode("ascii")

    conn = OAuthConnection(
        id=str(uuid.uuid4()),
        account_id=account_id,
        provider="google",
        email="migrated_user@gmail.com",
        encrypted_access_token=legacy_enc_access,
        encrypted_refresh_token=legacy_enc_refresh,
    )
    test_db_session.add_all([account, conn])
    test_db_session.commit()

    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5433/jobeazy_test")

    # Run migration with dry-run first
    migrated_dry = migrate_oauth_tokens(db_url, dry_run=True)
    assert migrated_dry >= 1

    # Run migration live
    migrated_live = migrate_oauth_tokens(db_url, dry_run=False)
    assert migrated_live >= 1

    # Reload connection and verify it decrypts with decrypt_oauth_token
    reloaded = test_db_session.query(OAuthConnection).filter_by(id=conn.id).one()
    assert decrypt_oauth_token(reloaded.encrypted_access_token) == old_access_token
    assert decrypt_oauth_token(reloaded.encrypted_refresh_token) == old_refresh_token

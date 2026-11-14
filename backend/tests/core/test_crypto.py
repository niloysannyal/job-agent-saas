import pytest
from app.core.config import settings
from app.core.crypto import (
    get_oauth_fernet,
    encrypt_oauth_token,
    decrypt_oauth_token,
)


def test_get_oauth_fernet_dev_fallback(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    monkeypatch.setattr(settings, "OAUTH_ENCRYPTION_KEY", None)

    fernet = get_oauth_fernet()
    assert fernet is not None

    token = "secret_token_123"
    encrypted = encrypt_oauth_token(token)
    assert encrypted != token
    assert decrypt_oauth_token(encrypted) == token


def test_get_oauth_fernet_production_strict_error(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    monkeypatch.setattr(settings, "OAUTH_ENCRYPTION_KEY", None)

    with pytest.raises(RuntimeError) as exc_info:
        get_oauth_fernet()

    assert "OAUTH_ENCRYPTION_KEY must be set in production" in str(exc_info.value)


def test_get_oauth_fernet_with_dedicated_key(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    # Valid 32 url-safe base64 encoded key
    key1 = "k_u6YQdC4J5eK0P8wZ2V1xL9oR3tU7sA5mB7cD9eF1g="
    monkeypatch.setattr(settings, "OAUTH_ENCRYPTION_KEY", key1)

    fernet = get_oauth_fernet()
    assert fernet is not None

    token = "prod_secret_token_999"
    encrypted = encrypt_oauth_token(token)
    assert decrypt_oauth_token(encrypted) == token

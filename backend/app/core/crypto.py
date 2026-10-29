import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet
from app.core.config import settings


def _get_fernet_instance() -> Fernet:
    """
    Derive a deterministic 32-byte URL-safe base64 Fernet key
    from the application's JWT_SECRET_KEY.
    """
    key_bytes = hashlib.sha256(settings.JWT_SECRET_KEY.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    return Fernet(fernet_key)


def encrypt_secret(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypt a sensitive plaintext secret (OAuth token, API key) at rest.
    Returns URL-safe ciphertext string, or None if input is empty.
    """
    if not plaintext:
        return None
    f = _get_fernet_instance()
    return f.encrypt(plaintext.encode()).decode()


def decrypt_secret(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypt an encrypted secret at rest.
    If decryption fails (e.g. key mismatch or raw unencrypted legacy value),
    returns the original string.
    """
    if not ciphertext:
        return None
    try:
        f = _get_fernet_instance()
        return f.decrypt(ciphertext.encode()).decode()
    except Exception:
        # Backward compatibility for plain strings in testing or before encryption
        return ciphertext


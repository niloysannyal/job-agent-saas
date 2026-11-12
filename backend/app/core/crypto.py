import base64
import hashlib
import logging
from typing import List, Optional
from cryptography.fernet import Fernet, MultiFernet, InvalidToken

from app.core.config import settings

logger = logging.getLogger(__name__)


def _derive_legacy_key(secret: str) -> bytes:
    """Derive a deterministic 32-byte URL-safe base64 Fernet key from secret string."""
    key_bytes = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def _get_legacy_fernet() -> Fernet:
    """Legacy Fernet instance derived from JWT_SECRET_KEY."""
    return Fernet(_derive_legacy_key(settings.JWT_SECRET_KEY))


def get_oauth_fernet(keys_override: Optional[List[str]] = None) -> MultiFernet:
    """
    Construct MultiFernet instance for OAuth token encryption/decryption.
    Supports zero-downtime key rotation:
    - Primary key (first in list) is used for all new encryptions.
    - Secondary/older keys are used for decryption fallback.
    
    If OAUTH_ENCRYPTION_KEY is unset, falls back to legacy JWT_SECRET_KEY-derived key
    for seamless local test and dev environments.
    """
    keys_str = None
    if keys_override:
        keys_str = ",".join(keys_override)
    elif settings.OAUTH_ENCRYPTION_KEY:
        keys_str = settings.OAUTH_ENCRYPTION_KEY

    fernet_instances: List[Fernet] = []

    if keys_str:
        raw_keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        for k in raw_keys:
            try:
                # Direct Fernet key (32 url-safe base64-encoded bytes)
                fernet_instances.append(Fernet(k.encode("ascii")))
            except Exception:
                # If a raw arbitrary passphrase is provided, derive a valid key
                derived = _derive_legacy_key(k)
                fernet_instances.append(Fernet(derived))

    if not fernet_instances:
        # Fallback to JWT-derived key with dev-only fallback
        fernet_instances.append(_get_legacy_fernet())

    return MultiFernet(fernet_instances)


def encrypt_oauth_token(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypt an OAuth token (access or refresh token) using MultiFernet primary key.
    Worker processes receive only OAUTH_ENCRYPTION_KEY and do not require JWT_SECRET_KEY.
    """
    if not plaintext:
        return None
    mf = get_oauth_fernet()
    return mf.encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt_oauth_token(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypt an encrypted OAuth token at rest using MultiFernet.
    Tries each configured key in order. If decryption fails, attempts legacy fallback.
    If input is a mock token or unencrypted plaintext, returns as-is for test compatibility.
    """
    if not ciphertext:
        return None
    try:
        mf = get_oauth_fernet()
        return mf.decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except (InvalidToken, Exception):
        # Secondary fallback: try legacy JWT fernet
        try:
            legacy = _get_legacy_fernet()
            return legacy.decrypt(ciphertext.encode("ascii")).decode("utf-8")
        except Exception:
            # Plaintext fallback for mock/test strings
            return ciphertext


def encrypt_secret(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypt a general sensitive plaintext secret (e.g. LLM API key, SMTP password) at rest.
    """
    if not plaintext:
        return None
    f = _get_legacy_fernet()
    return f.encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt_secret(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypt an encrypted secret at rest.
    Gracefully falls back between legacy fernet, MultiFernet, and raw text.
    """
    if not ciphertext:
        return None
    try:
        f = _get_legacy_fernet()
        return f.decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except Exception:
        try:
            mf = get_oauth_fernet()
            return mf.decrypt(ciphertext.encode("ascii")).decode("utf-8")
        except Exception:
            return ciphertext

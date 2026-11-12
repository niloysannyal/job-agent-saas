"""
backend/app/services/dispatch/hash_utils.py

Canonical length-prefixed content hashing for SendAuthorizations and SendEvidence.
Prevents whitespace/delimiter tampering across pipeline boundaries.
"""

import hashlib
from typing import Optional


def compute_content_hash(
    cv_version_id: Optional[str],
    subject: Optional[str],
    body: Optional[str],
    recipient: Optional[str],
    answers_json: Optional[str],
    attachment_sha256: Optional[str],
) -> str:
    """
    Computes deterministic SHA-256 over length-prefixed fields:
    len(val):val|len(val):val|...

    Canonical empty values:
    - cv_version_id: "" if None
    - subject: "" if None
    - body: "" if None
    - recipient: "" if None
    - answers_json: "[]" for email applications
    - attachment_sha256: "" if None
    """
    fields = [
        cv_version_id or "",
        subject or "",
        body or "",
        recipient or "",
        answers_json or "[]",
        attachment_sha256 or "",
    ]
    encoded_parts = [f"{len(f)}:{f}" for f in fields]
    canonical_payload = "|".join(encoded_parts)
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()


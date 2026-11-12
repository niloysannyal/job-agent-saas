#!/usr/bin/env python3
"""
scripts/migrate_oauth_encryption.py

One-time migration script to re-encrypt stored OAuth tokens from legacy JWT_SECRET_KEY Fernet
to dedicated OAUTH_ENCRYPTION_KEY MultiFernet.

Usage:
  python scripts/migrate_oauth_encryption.py [--dry-run] [--db-url URL]
"""

import argparse
import logging
import os
import sys

# Ensure repository root and backend directory are on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import (
    _get_legacy_fernet,
    encrypt_oauth_token,
    decrypt_oauth_token,
    get_oauth_fernet,
)
from app.models.oauth import OAuthConnection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("migrate_oauth_encryption")


def migrate_oauth_tokens(db_url: str, dry_run: bool = False) -> int:
    """
    Migrate OAuth tokens from legacy Fernet to dedicated MultiFernet.
    Returns number of migrated connections.
    """
    # Safety tripwire: refuse remote hosts
    if "supabase" in db_url.lower() or "pooler" in db_url.lower():
        raise RuntimeError("BLOCKED: Migration refused against remote host!")

    logger.info("Connecting to database: %s", db_url.split("@")[-1] if "@" in db_url else db_url)
    engine = create_engine(db_url)
    legacy_fernet = _get_legacy_fernet()

    with Session(engine) as session:
        connections = session.query(OAuthConnection).all()
        logger.info("Found %d OAuthConnection rows to inspect.", len(connections))

        migrated_count = 0
        for conn in connections:
            modified = False

            # Migrate access token
            if conn.encrypted_access_token:
                try:
                    # Attempt legacy decrypt
                    plain_access = legacy_fernet.decrypt(conn.encrypted_access_token.encode("ascii")).decode("utf-8")
                except Exception:
                    # Might already be decrypted or unencrypted mock token
                    plain_access = decrypt_oauth_token(conn.encrypted_access_token)

                new_enc_access = encrypt_oauth_token(plain_access)
                # Verify roundtrip
                assert decrypt_oauth_token(new_enc_access) == plain_access, "Access token roundtrip verification failed!"
                conn.encrypted_access_token = new_enc_access
                modified = True

            # Migrate refresh token
            if conn.encrypted_refresh_token:
                try:
                    plain_refresh = legacy_fernet.decrypt(conn.encrypted_refresh_token.encode("ascii")).decode("utf-8")
                except Exception:
                    plain_refresh = decrypt_oauth_token(conn.encrypted_refresh_token)

                new_enc_refresh = encrypt_oauth_token(plain_refresh)
                # Verify roundtrip
                assert decrypt_oauth_token(new_enc_refresh) == plain_refresh, "Refresh token roundtrip verification failed!"
                conn.encrypted_refresh_token = new_enc_refresh
                modified = True

            if modified:
                migrated_count += 1
                logger.info("Migrated OAuth tokens for account_id=%s, provider=%s", conn.account_id, conn.provider)

        if dry_run:
            logger.info("[DRY RUN] Rolled back %d updated rows. Zero database changes committed.", migrated_count)
            session.rollback()
        else:
            session.commit()
            logger.info("Successfully committed %d migrated OAuth records.", migrated_count)

    engine.dispose()
    return migrated_count


def main():
    parser = argparse.ArgumentParser(description="Migrate OAuthConnection tokens to OAUTH_ENCRYPTION_KEY MultiFernet")
    parser.add_argument("--dry-run", action="store_true", help="Inspect and test migration without committing changes")
    parser.add_argument("--db-url", type=str, default=None, help="Database URL (defaults to settings.DATABASE_URL)")

    args = parser.parse_args()
    db_url = args.db_url or settings.DATABASE_URL

    try:
        migrate_oauth_tokens(db_url, dry_run=args.dry_run)
    except Exception as e:
        logger.error("Migration failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()


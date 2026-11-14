"""
scripts/preflight_check.py
Inspect the local PostgreSQL environment state prior to live dogfooding.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.db.session import get_session_factory
from app.models.account import Account
from app.models.oauth import OAuthConnection
from app.models.dispatch import AccountDispatchSettings, TrustedRecipient
from app.models.llm_provider import LLMProviderConfig


def main():
    session = get_session_factory()()
    try:
        print("=== PRE-FLIGHT DB CHECK (localhost:5433/jobeazy) ===\n")
        
        accounts = session.query(Account).all()
        print(f"Accounts ({len(accounts)}):")
        for a in accounts:
            print(f"  - id={a.id}, email={a.email}, role={a.role}, plan={a.plan_tier}")

        oauths = session.query(OAuthConnection).all()
        print(f"\nOAuth Connections ({len(oauths)}):")
        for o in oauths:
            has_token = bool(o.encrypted_access_token)
            print(f"  - account_id={o.account_id}, provider={o.provider}, email={o.email}, has_token={has_token}, expires={o.token_expires_at}")

        settings = session.query(AccountDispatchSettings).all()
        print(f"\nDispatch Settings ({len(settings)}):")
        for d in settings:
            print(f"  - account_id={d.account_id}, autonomy_mode={d.autonomy_mode}, kill_switch={d.kill_switch}, auto_daily_cap={d.autonomous_daily_cap}")

        trusted = session.query(TrustedRecipient).all()
        print(f"\nTrusted Recipients ({len(trusted)}):")
        for t in trusted:
            print(f"  - account_id={t.account_id}, email={t.recipient_email}, domain={t.recipient_domain}")

        llms = session.query(LLMProviderConfig).order_by(LLMProviderConfig.priority.asc()).all()
        print(f"\nLLM Providers in DB ({len(llms)}):")
        for l in llms:
            print(f"  - provider={l.provider}, model={l.model_name}, priority={l.priority}, active={l.is_active}, has_key={bool(l.encrypted_api_key)}")

    finally:
        session.close()


if __name__ == "__main__":
    main()

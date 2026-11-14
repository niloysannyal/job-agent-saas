"""
scripts/cleanup_synthetic_tests.py
Purge synthetic live dogfooding test accounts and evidence from local PostgreSQL.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.db.session import get_session_factory
from app.models.account import Account
from app.models.application import Application
from app.models.dispatch import (
    AccountDispatchSettings,
    ApplicationPdfPayload,
    DispatchedAction,
    HoldQueueItem,
    SendAuthorization,
    SendEvidence,
    TrustedRecipient,
)
from app.models.job import Job
from app.models.metering import QuotaReservation
from app.models.oauth import OAuthConnection


def cleanup():
    session = get_session_factory()()
    try:
        synthetic_accounts = session.query(Account).filter(Account.id.like("acc-live-%")).all()
        print(f"Found {len(synthetic_accounts)} synthetic accounts to clean up.")

        for acc in synthetic_accounts:
            acc_id = acc.id
            print(f"Purging account: {acc_id} ({acc.email})...")

            # 1. SendEvidence
            ev_count = session.query(SendEvidence).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 2. DispatchedAction
            act_count = session.query(DispatchedAction).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 3. HoldQueueItem
            hold_count = session.query(HoldQueueItem).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 4. QuotaReservation
            qr_count = session.query(QuotaReservation).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 5. SendAuthorization
            auth_count = session.query(SendAuthorization).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 6. ApplicationPdfPayload
            apps = session.query(Application).filter_by(account_id=acc_id).all()
            for app in apps:
                session.query(ApplicationPdfPayload).filter_by(application_id=app.id).delete(synchronize_session=False)
            # 7. Application
            app_count = session.query(Application).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 8. TrustedRecipient
            tr_count = session.query(TrustedRecipient).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 9. Jobs
            job_count = session.query(Job).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 10. OAuthConnection
            oauth_count = session.query(OAuthConnection).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 11. AccountDispatchSettings
            set_count = session.query(AccountDispatchSettings).filter_by(account_id=acc_id).delete(synchronize_session=False)
            # 12. Account
            session.delete(acc)

            print(f"  -> Deleted: {app_count} apps, {auth_count} auths, {hold_count} holds, {act_count} actions, {ev_count} evidence, {tr_count} trusted, {job_count} jobs.")

        session.commit()
        print("\nCleanup completed successfully! All synthetic test accounts purged.")

        remaining = session.query(Account).all()
        print(f"\nRemaining legitimate accounts in DB ({len(remaining)}):")
        for r in remaining:
            print(f"  - {r.id}: {r.email} ({r.role})")

    finally:
        session.close()


if __name__ == "__main__":
    cleanup()

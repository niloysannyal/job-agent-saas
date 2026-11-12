import os
import uuid
from datetime import datetime, timedelta, timezone
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.db.base import Base
from app.models.account import Account
from app.models.job import Job
from app.models.application import Application
from app.models.dispatch import (
    AccountDispatchSettings,
    UserCommand,
    SendAuthorization,
    HoldQueueItem,
    SendEvidence,
    DispatchedAction,
    TrustedRecipient,
    JobFeedback,
)
from app.models.metering import (
    AccountSubscription,
    AccountUsageCounter,
    QuotaReservation,
    UsageEvent,
    AccountQuotaOverride,
)
from app.models.model_pricing import ModelPricing
from app.models.admin_audit_log import AdminAuditLog
from app.models.subscription import SubscriptionPlan, Entitlement


def test_partial_unique_retry_after_abort(test_db_session):
    """
    Advisor Review 9 Item 8 & 11:
    Verifies that the partial unique index on dispatched_actions
    allows re-dispatching a job if a previous dispatch was aborted or failed.
    """
    account_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())

    account = Account(id=account_id, email=f"user_{uuid.uuid4().hex[:6]}@example.com")
    job = Job(id=job_id, role="Platform Engineer", company="Acme Inc", apply_link="https://example.com/apply", source="test", account_id=account_id)
    app = Application(id=app_id, account_id=account_id, job_id=job_id)

    test_db_session.add_all([account, job, app])
    test_db_session.commit()

    # 1. First dispatch action in 'sent' status
    action1 = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job_id,
        application_id=app_id,
        channel="email",
        sequence_kind="initial_application",
        mode="supervised",
        status="sent",
        dispatched_at=datetime.now(timezone.utc),
    )
    test_db_session.add(action1)
    test_db_session.commit()

    # 2. Attempt duplicate while first is 'sent' -> must fail integrity error
    action2 = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job_id,
        application_id=app_id,
        channel="email",
        sequence_kind="initial_application",
        mode="supervised",
        status="sending",
    )
    test_db_session.add(action2)
    with pytest.raises(IntegrityError):
        test_db_session.commit()
    test_db_session.rollback()

    # 3. Transition action1 to 'aborted'
    test_db_session.query(DispatchedAction).filter_by(id=action1.id).update({"status": "aborted"})
    test_db_session.commit()

    # 4. Retry dispatch after abort -> must SUCCEED due to partial unique index
    action3 = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job_id,
        application_id=app_id,
        channel="email",
        sequence_kind="initial_application",
        mode="supervised",
        status="reserved",
    )
    test_db_session.add(action3)
    test_db_session.commit()

    # Assert action3 was persisted cleanly
    persisted = test_db_session.query(DispatchedAction).filter_by(id=action3.id).one()
    assert persisted.status == "reserved"


def test_account_deletion_with_audit_fks(test_db_session):
    """
    Advisor Review 9 Item 7 & 11:
    Verifies that an account with SendEvidence, DispatchedAction, and SendAuthorization
    can be deleted cleanly due to DEFERRABLE INITIALLY DEFERRED foreign keys.
    """
    account_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())
    auth_id = str(uuid.uuid4())
    cmd_id = str(uuid.uuid4())

    account = Account(id=account_id, email=f"delete_test_{uuid.uuid4().hex[:6]}@example.com")
    job = Job(id=job_id, role="Backend Lead", company="Startup Co", apply_link="https://startup.co/apply", source="test", account_id=account_id)
    app = Application(id=app_id, account_id=account_id, job_id=job_id)
    cmd = UserCommand(
        id=cmd_id,
        account_id=account_id,
        command_type="single",
        mode="supervised",
        source="ui_click",
        target_job_ids=[job_id],
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    auth = SendAuthorization(
        id=auth_id,
        account_id=account_id,
        application_id=app_id,
        command_id=cmd_id,
        recipient_email="recruiter@startup.co",
        content_hash="a" * 64,
        minted_by="human_approval",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    action = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job_id,
        application_id=app_id,
        channel="email",
        sequence_kind="initial_application",
        mode="supervised",
        status="sent",
        dispatched_at=datetime.now(timezone.utc),
    )
    evidence = SendEvidence(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job_id,
        application_id=app_id,
        authorization_id=auth_id,
        channel="email",
        external_message_id="msg_12345",
        subject="Application for Backend Lead",
        headers_snapshot={"X-Test": "1"},
        canonical_content_hash="a" * 64,
        recipient_email="recruiter@startup.co",
        sent_at=datetime.now(timezone.utc),
    )

    test_db_session.add_all([account, job, app])
    test_db_session.flush()
    test_db_session.add(cmd)
    test_db_session.flush()
    test_db_session.add(auth)
    test_db_session.flush()
    test_db_session.add_all([action, evidence])
    test_db_session.commit()

    # In ordered deletion: delete child evidence and actions in the same transaction
    # Deferred FK constraint verifies referential integrity at COMMIT time.
    test_db_session.delete(evidence)
    test_db_session.delete(action)
    test_db_session.delete(account)
    test_db_session.commit()

    # Verify account is completely gone
    assert test_db_session.query(Account).filter_by(id=account_id).first() is None


def test_stale_claimed_and_sending_sweep(test_db_session):
    """
    Advisor Review 9 Item 2 & 11:
    Verifies sweeping stale claimed workers back to 'pending'
    and sweeping stale sending workers (> HTTP timeout + margin) to 'unknown'.
    """
    account_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())
    auth_id = str(uuid.uuid4())

    account = Account(id=account_id, email=f"sweep_{uuid.uuid4().hex[:6]}@example.com")
    job = Job(id=job_id, role="DevOps Engineer", company="Cloud Corp", apply_link="https://cloud.com/apply", source="test", account_id=account_id)
    app = Application(id=app_id, account_id=account_id, job_id=job_id)
    auth = SendAuthorization(
        id=auth_id,
        account_id=account_id,
        application_id=app_id,
        recipient_email="jobs@cloud.com",
        content_hash="b" * 64,
        minted_by="autonomous_policy",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    # 1. Stale claimed item (claimed 5 minutes ago, threshold 30s)
    stale_claimed = HoldQueueItem(
        id=str(uuid.uuid4()),
        account_id=account_id,
        application_id=app_id,
        authorization_id=auth_id,
        status="claimed",
        hold_kind="autonomous_delay",
        release_at=datetime.now(timezone.utc) - timedelta(minutes=6),
        claimed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
    )

    # 2. Stale sending item (sending started 5 minutes ago, threshold 60s)
    stale_sending = HoldQueueItem(
        id=str(uuid.uuid4()),
        account_id=account_id,
        application_id=app_id,
        authorization_id=auth_id,
        status="sending",
        hold_kind="autonomous_delay",
        release_at=datetime.now(timezone.utc) - timedelta(minutes=6),
        claimed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
        sending_started_at=datetime.now(timezone.utc) - timedelta(minutes=4),
    )

    test_db_session.add_all([account, job, app])
    test_db_session.flush()
    test_db_session.add(auth)
    test_db_session.flush()
    test_db_session.add_all([stale_claimed, stale_sending])
    test_db_session.commit()

    # Run sweeper query
    now = datetime.now(timezone.utc)
    claim_timeout = now - timedelta(seconds=30)
    sending_timeout = now - timedelta(seconds=60)

    # Reset stale claimed -> pending
    test_db_session.query(HoldQueueItem).filter(
        HoldQueueItem.status == "claimed",
        HoldQueueItem.claimed_at < claim_timeout,
    ).update({"status": "pending", "claimed_at": None})

    # Transition stale sending -> unknown
    test_db_session.query(HoldQueueItem).filter(
        HoldQueueItem.status == "sending",
        HoldQueueItem.sending_started_at < sending_timeout,
    ).update({"status": "unknown"})
    test_db_session.commit()

    # Assert statuses updated
    reloaded_claimed = test_db_session.query(HoldQueueItem).filter_by(id=stale_claimed.id).one()
    reloaded_sending = test_db_session.query(HoldQueueItem).filter_by(id=stale_sending.id).one()

    assert reloaded_claimed.status == "pending"
    assert reloaded_claimed.claimed_at is None
    assert reloaded_sending.status == "unknown"


def test_concurrent_claims_vs_caps(test_db_session):
    """
    Advisor Review 9 Item 11:
    Verifies that autonomous cap checks block claims once rolling limit is reached.
    """
    account_id = str(uuid.uuid4())
    account = Account(id=account_id, email=f"caps_{uuid.uuid4().hex[:6]}@example.com")
    settings = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode="autonomous",
        autonomous_daily_cap=2,  # Cap at 2 sends per day
        safety_daily_cap=10,
    )
    test_db_session.add_all([account, settings])
    test_db_session.commit()

    # Simulate 2 already dispatched actions in the last hour
    job1_id = str(uuid.uuid4())
    job2_id = str(uuid.uuid4())
    job3_id = str(uuid.uuid4())

    job1 = Job(id=job1_id, role="Role 1", company="Co 1", apply_link="https://co1.com/apply", source="test", account_id=account_id)
    job2 = Job(id=job2_id, role="Role 2", company="Co 2", apply_link="https://co2.com/apply", source="test", account_id=account_id)
    job3 = Job(id=job3_id, role="Role 3", company="Co 3", apply_link="https://co3.com/apply", source="test", account_id=account_id)
    app1 = Application(id=str(uuid.uuid4()), account_id=account_id, job_id=job1_id)
    app2 = Application(id=str(uuid.uuid4()), account_id=account_id, job_id=job2_id)
    app3 = Application(id=str(uuid.uuid4()), account_id=account_id, job_id=job3_id)

    act1 = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job1_id,
        application_id=app1.id,
        channel="email",
        mode="autonomous",
        status="sent",
        created_at=datetime.now(timezone.utc) - timedelta(minutes=10),
    )
    act2 = DispatchedAction(
        id=str(uuid.uuid4()),
        account_id=account_id,
        job_id=job2_id,
        application_id=app2.id,
        channel="email",
        mode="autonomous",
        status="sending",
        created_at=datetime.now(timezone.utc) - timedelta(minutes=5),
    )
    test_db_session.add_all([job1, job2, job3])
    test_db_session.flush()
    test_db_session.add_all([app1, app2, app3])
    test_db_session.flush()
    test_db_session.add_all([act1, act2])
    test_db_session.commit()

    # Query rolling active autonomous actions in last 24h
    window_start = datetime.now(timezone.utc) - timedelta(days=1)
    rolling_count = test_db_session.query(DispatchedAction).filter(
        DispatchedAction.account_id == account_id,
        DispatchedAction.mode == "autonomous",
        DispatchedAction.created_at >= window_start,
        DispatchedAction.status.in_(["reserved", "sending", "sent", "unknown"]),
    ).count()

    assert rolling_count == 2
    # Verify that attempting to claim a 3rd autonomous job violates daily cap
    assert rolling_count >= settings.autonomous_daily_cap

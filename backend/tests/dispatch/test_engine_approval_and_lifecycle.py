import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.crypto import encrypt_oauth_token
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.agent import AgentActionProposal
from app.models.application import Application
from app.models.dispatch import (
    AccountDispatchSettings,
    ApplicationPdfPayload,
    DispatchedAction,
    HoldQueueItem,
    SendAuthorization,
    SendEvidence,
    UserCommand,
)
from app.models.job import Job
from app.models.metering import (
    AccountUsageCounter,
    QuotaReservation,
    UsageEvent,
    AccountQuotaOverride,
)
from app.models.oauth import OAuthConnection
from app.models.subscription import Entitlement
from app.services.agent.engine import AgentEngine
from app.services.dispatch.gateway import SendGateway
from app.services.dispatch.hash_utils import compute_content_hash
from app.services.metering.quota_service import QuotaService
from app.workers.dispatch_poller import claim_pending_batch


def create_approval_fixture(test_db_session: Session, quota_limit: int = 10):
    account_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())
    proposal_id = str(uuid.uuid4())

    account = Account(id=account_id, email=f"candidate_{uuid.uuid4().hex[:6]}@example.com")
    entitlement = Entitlement(
        account_id=account_id,
        all_access=False,
        max_active_applications=quota_limit,
    )
    job = Job(
        id=job_id,
        role="Senior Distributed Systems Engineer",
        company="TechCorp Cloud",
        apply_link="https://techcorp.cloud/careers/apply",
        source="test",
        account_id=account_id,
        is_active=True,
        vetoed=False,
    )
    app = Application(
        id=app_id,
        account_id=account_id,
        job_id=job_id,
        status="draft",
        subject="Application: Senior Distributed Systems Engineer - Niloy",
        draft_content="Dear TechCorp Hiring Team, I am thrilled to apply...",
        recipient_email="hiring@techcorp.cloud",
        channel="email",
    )
    valid_pdf = b"%PDF-1.4\nTest dummy CV PDF bytes\n%%EOF"
    pdf_payload = ApplicationPdfPayload(
        application_id=app_id,
        account_id=account_id,
        sha256="dummy_pdf_sha256_techcorp",
        payload_bytes=valid_pdf,
        size_bytes=len(valid_pdf),
    )
    app.pdf_sha256 = pdf_payload.sha256

    proposal = AgentActionProposal(
        id=proposal_id,
        account_id=account_id,
        action_type="SEND_APPLICATION_EMAIL",
        target_id=app_id,
        title="Send Application to TechCorp Cloud",
        payload_snapshot={
            "job_role": "Senior Distributed Systems Engineer",
            "company": "TechCorp Cloud",
            "recipient": "hiring@techcorp.cloud",
        },
        status="pending",
    )
    settings_row = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode="supervised",
        autonomous_daily_cap=10,
        autonomous_hourly_cap=5,
        safety_daily_cap=50,
        safety_hourly_cap=20,
    )
    oauth = OAuthConnection(
        id=str(uuid.uuid4()),
        account_id=account_id,
        provider="google",
        email="candidate_google@gmail.com",
        encrypted_access_token=encrypt_oauth_token("mock_token_abc"),
    )

    test_db_session.add_all([account, entitlement, job, app, settings_row, oauth])
    test_db_session.flush()
    test_db_session.add_all([pdf_payload, proposal])
    test_db_session.commit()

    return {
        "account": account,
        "job": job,
        "app": app,
        "proposal": proposal,
        "settings": settings_row,
        "oauth": oauth,
        "pdf_bytes": valid_pdf,
    }


@pytest.mark.asyncio
async def test_approve_proposal_queues_application_and_mints_records(test_db_session: Session):
    """
    Verify Task 4 Human-in-the-Loop on Send:
    1. Proposal approved.
    2. Application status becomes 'queued' (NOT 'applied'!).
    3. sent_at remains None until external send occurs.
    4. UserCommand, SendAuthorization, and HoldQueueItem are minted.
    5. Quota is reserved.
    """
    data = create_approval_fixture(test_db_session)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)

    res = await engine.approve_proposal(data["proposal"].id)
    assert res["success"] is True
    assert res["status"] == "queued"
    assert "undo_expires_at" in res
    assert "hold_queue_item_id" in res

    # 1. Assert Application status
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "queued"
    assert reloaded_app.sent_at is None  # CRITICAL INVARIANT: NOT marked sent yet!

    # 2. Assert UserCommand created
    cmd = test_db_session.query(UserCommand).filter_by(account_id=data["account"].id).one()
    assert cmd.mode == "supervised"
    assert cmd.source == "ui_click"
    assert data["job"].id in cmd.target_job_ids

    # 3. Assert SendAuthorization minted
    auth = test_db_session.query(SendAuthorization).filter_by(id=res["authorization_id"]).one()
    assert auth.minted_by == "human_approval"
    assert auth.status == "pending"
    assert auth.recipient_email == "hiring@techcorp.cloud"

    # Verify content hash matches canonical calculation
    expected_hash = compute_content_hash(
        cv_version_id="",
        subject=data["app"].subject,
        body=data["app"].draft_content,
        recipient="hiring@techcorp.cloud",
        answers_json="[]",
        attachment_sha256="dummy_pdf_sha256_techcorp",
    )
    assert auth.content_hash == expected_hash

    # 4. Assert HoldQueueItem created
    hold = test_db_session.query(HoldQueueItem).filter_by(id=res["hold_queue_item_id"]).one()
    assert hold.status == "pending"
    assert hold.hold_kind == "review_required"
    assert hold.release_at > datetime.now(timezone.utc)

    # 5. Assert Quota reservation created
    quota_res = test_db_session.query(QuotaReservation).filter_by(id=hold.reservation_id).one()
    assert quota_res.status == "reserved"
    assert quota_res.units == 1

    # Assert usage counter has reserved = 1
    counter = (
        test_db_session.query(AccountUsageCounter)
        .filter_by(account_id=data["account"].id)
        .one()
    )
    assert counter.applications_reserved_count == 1
    assert counter.applications_sent_count == 0


@pytest.mark.asyncio
async def test_mid_hold_cancel_reverts_to_draft_and_releases_resources(test_db_session: Session):
    """
    Verify Candidate Undo Window:
    When a user cancels within the 30s countdown:
    1. HoldQueueItem status becomes 'aborted' with abort_reason='user_cancelled'.
    2. SendAuthorization is voided.
    3. Application reverts to 'draft'.
    4. Quota reservation is released and reserved counter decremented.
    """
    data = create_approval_fixture(test_db_session)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)

    # Approve to queue
    approve_res = await engine.approve_proposal(data["proposal"].id)
    assert approve_res["status"] == "queued"

    # User immediately hits Undo / Cancel
    cancel_res = await engine.cancel_hold_dispatch(application_id=data["app"].id)
    assert cancel_res["success"] is True
    assert cancel_res["status"] == "aborted"
    assert cancel_res["abort_reason"] == "user_cancelled"
    assert cancel_res["application_status"] == "draft"

    # 1. Assert Application reverted to draft
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "draft"
    assert reloaded_app.sent_at is None

    # 2. Assert Hold item aborted
    hold = test_db_session.query(HoldQueueItem).filter_by(id=approve_res["hold_queue_item_id"]).one()
    assert hold.status == "aborted"
    assert hold.abort_reason == "user_cancelled"

    # 3. Assert Authorization voided
    auth = test_db_session.query(SendAuthorization).filter_by(id=approve_res["authorization_id"]).one()
    assert auth.status == "voided"
    assert auth.voided_at is not None

    # 4. Assert Quota reservation released
    quota_res = test_db_session.query(QuotaReservation).filter_by(id=hold.reservation_id).one()
    assert quota_res.status == "released"

    counter = test_db_session.query(AccountUsageCounter).filter_by(account_id=data["account"].id).one()
    assert counter.applications_reserved_count == 0


@pytest.mark.asyncio
async def test_cancel_fails_if_dispatch_already_active(test_db_session: Session):
    """
    Verify cancel is rejected if dispatch has already been claimed or is sending.
    """
    data = create_approval_fixture(test_db_session)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)

    approve_res = await engine.approve_proposal(data["proposal"].id)
    hold = test_db_session.query(HoldQueueItem).filter_by(id=approve_res["hold_queue_item_id"]).one()

    # Worker has claimed or is sending
    hold.status = "sending"
    test_db_session.commit()

    cancel_res = await engine.cancel_hold_dispatch(hold_item_id=hold.id)
    assert cancel_res["success"] is False
    assert "already in 'sending' state" in cancel_res["message"]

    # Application remains queued
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "queued"


@pytest.mark.asyncio
async def test_poller_and_gateway_complete_queued_dispatch(test_db_session: Session):
    """
    End-to-End Task 4 Verification:
    Proposal approved -> queued in hold -> timer expires -> claimed by poller ->
    dispatched by gateway -> status becomes 'applied', sent_at recorded, quota settled.
    """
    data = create_approval_fixture(test_db_session)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)

    # 1. Human approves proposal
    approve_res = await engine.approve_proposal(data["proposal"].id)
    hold_id = approve_res["hold_queue_item_id"]

    # 2. Advance time past undo countdown
    hold = test_db_session.query(HoldQueueItem).filter_by(id=hold_id).one()
    hold.release_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    # Clean up lingering pending items from prior tests so our item is at top of queue
    test_db_session.query(HoldQueueItem).filter(HoldQueueItem.id != hold_id, HoldQueueItem.status == "pending").delete(synchronize_session=False)
    test_db_session.commit()

    # 3. Poller claims batch with SKIP LOCKED
    claimed = claim_pending_batch(test_db_session, batch_size=10)
    assert hold_id in claimed

    # 4. Gateway executes two-phase dispatch
    success = await SendGateway.dispatch_hold_item(test_db_session, hold_id)
    assert success is True

    # 5. Verify final states
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "applied"
    assert reloaded_app.sent_at is not None

    reloaded_auth = test_db_session.query(SendAuthorization).filter_by(id=approve_res["authorization_id"]).one()
    assert reloaded_auth.status == "consumed"
    assert reloaded_auth.consumed_at is not None

    reloaded_hold = test_db_session.query(HoldQueueItem).filter_by(id=hold_id).one()
    assert reloaded_hold.status == "sent"

    action = (
        test_db_session.query(DispatchedAction)
        .filter_by(account_id=data["account"].id, job_id=data["job"].id)
        .one()
    )
    assert action.status == "sent"
    assert action.dispatched_at is not None

    # Quota reservation is settled
    quota_res = test_db_session.query(QuotaReservation).filter_by(id=hold.reservation_id).one()
    assert quota_res.status == "settled"

    # Counter has permanent sent = 1, reserved = 0
    counter = test_db_session.query(AccountUsageCounter).filter_by(account_id=data["account"].id).one()
    assert counter.applications_sent_count == 1
    assert counter.applications_reserved_count == 0

    # Immutable UsageEvent recorded
    usage_event = test_db_session.query(UsageEvent).filter_by(account_id=data["account"].id).one()
    assert usage_event.event_type == "email_dispatch"
    assert usage_event.status == "succeeded"
    assert usage_event.units == 1


@pytest.mark.asyncio
async def test_quota_exceeded_blocks_proposal_approval(test_db_session: Session):
    """
    Verify quota barrier:
    When an account has consumed its monthly application limit,
    approve_proposal fails closed with QUOTA_EXCEEDED error.
    """
    data = create_approval_fixture(test_db_session, quota_limit=1)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)

    # Pre-consume quota limit of 1
    period_start, period_end = QuotaService.get_period_boundaries(test_db_session, data["account"].id)
    counter = QuotaService.ensure_counter_exists(test_db_session, data["account"].id, period_start, period_end)
    counter.applications_sent_count = 1
    test_db_session.commit()

    # Attempt to approve proposal
    res = await engine.approve_proposal(data["proposal"].id)
    assert res["success"] is False
    assert res["error_code"] == "QUOTA_EXCEEDED"
    assert "Quota exceeded" in res["message"]

    # Application remains draft
    reloaded_app = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded_app.status == "draft"
    assert reloaded_app.sent_at is None

    # No hold queue items created
    holds = test_db_session.query(HoldQueueItem).filter_by(account_id=data["account"].id).all()
    assert len(holds) == 0


@pytest.fixture
def client(test_db_session: Session):
    app = create_app()

    def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.mark.asyncio
async def test_api_cancel_application_send_endpoint(client: TestClient, test_db_session: Session):
    """
    Verify REST API endpoint POST /api/v1/applications/{application_id}/cancel-send.
    """
    data = create_approval_fixture(test_db_session)
    engine = AgentEngine(account_id=data["account"].id, db_session=test_db_session)
    approve_res = await engine.approve_proposal(data["proposal"].id)
    assert approve_res["status"] == "queued"

    response = client.post(
        f"/api/v1/applications/{data['app'].id}/cancel-send?account_id={data['account'].id}"
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert res_data["status"] == "aborted"
    assert res_data["application_status"] == "draft"

    # Reload application
    reloaded = test_db_session.query(Application).filter_by(id=data["app"].id).one()
    assert reloaded.status == "draft"

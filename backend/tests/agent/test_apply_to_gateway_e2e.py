"""
backend/tests/agent/test_apply_to_gateway_e2e.py

End-to-End Verification of ApplyGraph to SendGateway Outbox Handoff.
Verifies:
1. ApplyGraph executes through assemble_package_node and dispatch_node.
2. Relational persistence of Application, ApplicationPdfPayload, SendAuthorization, and HoldQueueItem.
3. Strict Content Hash synchronization between assemble_package_node and SendGateway._run_precheck_and_reserve.
4. Precheck succeeds with proceed == True, reserving idempotency and transitioning status to 'sending'.
"""

import hashlib
import pytest
from unittest.mock import AsyncMock, patch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from app.models.account import Account
from app.models.job import Job
from app.models.dispatch import (
    AccountDispatchSettings,
    ApplicationPdfPayload,
    DispatchedAction,
    HoldQueueItem,
    SendAuthorization,
    TrustedRecipient,
)
from app.models.application import Application
from app.models.metering import QuotaReservation
from app.services.agent.workflows.apply_graph import build_apply_graph
from app.services.cv_tailor.reviewer import CVReviewOutput
from app.services.dispatch.gateway import SendGateway
from app.services.dispatch.hash_utils import compute_content_hash


@pytest.fixture
def e2e_account_and_job(test_db_session):
    """Seed real Account, Job, AccountDispatchSettings, and TrustedRecipient in test database."""
    import uuid
    account_id = f"acc-e2e-{uuid.uuid4().hex[:8]}"
    job_id = f"job-e2e-{uuid.uuid4().hex[:8]}"

    # 1. Account
    acc = Account(id=account_id, email=f"{account_id}@example.com")
    test_db_session.add(acc)

    # 2. Job
    job = Job(
        id=job_id,
        account_id=account_id,
        company="Google DeepMind",
        role="Staff Research Engineer",
        source="greenhouse",
        apply_link="https://deepmind.google/careers",
        is_active=True,
        vetoed=False,
    )
    test_db_session.add(job)

    # 3. AccountDispatchSettings
    settings_row = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode="autonomous",
        safety_daily_cap=50,
        safety_hourly_cap=10,
        autonomous_daily_cap=10,
        autonomous_hourly_cap=5,
        kill_switch=False,
        is_suspended_by_admin=False,
    )
    test_db_session.add(settings_row)

    # 4. TrustedRecipient
    tr = TrustedRecipient(
        account_id=account_id,
        email="careers@deepmind.com",
        source="manual_approval",
    )
    test_db_session.add(tr)

    test_db_session.commit()
    return {"account_id": account_id, "job_id": job_id}


@pytest.mark.asyncio
async def test_apply_graph_to_sendgateway_precheck_e2e(e2e_account_and_job, test_db_session):
    """
    Executes full ApplyGraph pipeline to dispatch, then feeds the generated HoldQueueItem
    directly to SendGateway._run_precheck_and_reserve to prove:
    - Zero hash formula mismatch.
    - Zero ForeignKey violation.
    - Zero missing PDF payload or Application record.
    - 100% successful proceed == True.
    """
    account_id = e2e_account_and_job["account_id"]
    job_id = e2e_account_and_job["job_id"]

    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": f"thread-e2e-{job_id}"}}
    initial_state = {
        "account_id": account_id,
        "job_id": job_id,
        "user_email": "candidate-e2e@example.com",
        "company_name": "Google DeepMind",
        "role_title": "Staff Research Engineer",
        "job_description": "Building next-generation autonomous AI agents with Python, PyTorch, and distributed systems. Send CV to careers@deepmind.com",
        "autonomy_mode": "autonomous",
    }

    tailored_latex = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\resumeItem{Staff Research Engineer specializing in Agent State Machines.}\n"
        "\\end{document}"
    )

    with patch("app.services.cv_tailor.reviewer.CVReviewerService.review_cv", new_callable=AsyncMock) as mock_review, \
         patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = (
            "---TAILORED_SUMMARY---\n"
            "\\resumeItem{Staff Research Engineer specializing in Agent State Machines.}\n"
            "---COVER_NOTE---\n"
            "Dear DeepMind Hiring Team, I am eager to apply for the Staff Research Engineer role.\n"
            "---GAPS---\n- None\n"
        )
        mock_review.return_value = CVReviewOutput(
            is_valid=True,
            final_tailored_latex=tailored_latex,
            final_summary_bullet="\\resumeItem{Staff Research Engineer specializing in Agent State Machines.}",
            final_cover_letter="Cover letter",
            confirmed_gaps=[],
            ats_score=92.0,
            fact_audit_passed=True,
            hallucination_detected=False,
            line_count=45,
            computed_page_count=1,
            reviewer_notes="Pristine fact check and page budget.",
        )

        # 1. Execute ApplyGraph
        await graph.ainvoke(initial_state, config=thread_config)

    # 2. Inspect final graph state
    state = await graph.aget_state(thread_config)
    assert state.next == ()
    assert state.values["status"] == "queued_in_hold"
    assert state.values["downgrade_reason"] is None
    hold_item_id = state.values["hold_queue_item_id"]
    assert hold_item_id is not None
    assert not hold_item_id.startswith("hold-") or len(hold_item_id) == 36  # Real UUID

    # 3. Verify Database Records persisted by ApplyGraph
    app_record = test_db_session.query(Application).filter_by(account_id=account_id, job_id=job_id).first()
    assert app_record is not None
    assert app_record.status == "draft"
    assert app_record.pdf_sha256 is not None
    assert app_record.recipient_email == "careers@deepmind.com"

    pdf_payload = test_db_session.query(ApplicationPdfPayload).filter_by(application_id=app_record.id).first()
    assert pdf_payload is not None
    assert pdf_payload.sha256 == app_record.pdf_sha256
    assert pdf_payload.payload_bytes is not None
    assert len(pdf_payload.payload_bytes) > 0

    send_auth = test_db_session.query(SendAuthorization).filter_by(application_id=app_record.id).first()
    assert send_auth is not None
    assert send_auth.status == "pending"
    assert send_auth.attachment_sha256 == pdf_payload.sha256

    hold_item = test_db_session.query(HoldQueueItem).filter_by(id=hold_item_id).first()
    assert hold_item is not None
    assert hold_item.account_id == account_id
    assert hold_item.application_id == app_record.id
    assert hold_item.authorization_id == send_auth.id
    assert hold_item.status == "pending"
    assert hold_item.hold_kind == "autonomous_delay"

    # 4. Execute SendGateway Phase 1 Pre-Check
    precheck_result = SendGateway._run_precheck_and_reserve(test_db_session, hold_item)

    # Assert pre-check passes cleanly
    assert precheck_result.get("proceed") is True, f"Precheck failed: {hold_item.abort_reason} - {hold_item.error_message}"
    assert precheck_result["app_id"] == app_record.id
    assert precheck_result["auth_id"] == send_auth.id
    assert precheck_result["pdf_sha256"] == pdf_payload.sha256
    assert precheck_result["pdf_bytes"] == pdf_payload.payload_bytes
    assert precheck_result["recipient_email"] == "careers@deepmind.com"

    # Assert idempotency reservation and status transition
    action = test_db_session.query(DispatchedAction).filter_by(id=precheck_result["action_id"]).first()
    assert action is not None
    assert action.status == "reserved"
    assert action.application_id == app_record.id
    assert action.mode == "autonomous"

    # Assert HoldQueueItem transitioned to sending
    assert hold_item.status == "sending"
    assert hold_item.sending_started_at is not None

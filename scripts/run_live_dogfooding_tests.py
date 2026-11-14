"""
scripts/run_live_dogfooding_tests.py

Phase 0 Live Dogfooding Verification Script.
Executes:
1. Live Test #1: Supervised Mode End-to-End Dispatch
   (ApplyGraph -> HITL Gate -> Human Approval -> HoldQueueItem -> Poller Release -> Gmail Settlement)
2. Live Test #2: TOFU Autonomous Downgrade -> Human Approval -> trusted_recipients Upsert -> Poller Release

Queries and prints the exact PostgreSQL rows written across all M1 dispatch tables.
"""

import asyncio
from datetime import datetime, timedelta, timezone
import os
import sys
import uuid
from unittest.mock import AsyncMock, patch

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from sqlalchemy import text

from app.core.crypto import encrypt_oauth_token
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
from app.models.oauth import OAuthConnection
from app.models.profile import UserProfile
from app.services.agent.workflows.apply_graph import build_apply_graph
from app.services.dispatch.gateway import SendGateway
from app.workers.dispatch_poller import poll_and_dispatch_batch


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_db_rows(session, account_id: str, tag: str):
    print(f"\n--- [POSTGRESQL STATE FOR {tag} (account_id={account_id})] ---")

    # 1. Applications
    apps = session.query(Application).filter_by(account_id=account_id).all()
    print(f"\n[applications] ({len(apps)} rows):")
    for a in apps:
        print(f"  - id={a.id} | status={a.status} | subject={a.subject} | recipient={a.recipient_email} | sent_at={a.sent_at}")

    # 2. Send Authorizations
    auths = session.query(SendAuthorization).filter_by(account_id=account_id).all()
    print(f"\n[send_authorizations] ({len(auths)} rows):")
    for s in auths:
        print(f"  - id={s.id} | status={s.status} | minted_by={s.minted_by} | hash={s.content_hash[:16]}... | recipient={s.recipient_email} | consumed_at={s.consumed_at}")

    # 3. Hold Queue Items
    holds = session.query(HoldQueueItem).filter_by(account_id=account_id).all()
    print(f"\n[hold_queue_items] ({len(holds)} rows):")
    for h in holds:
        print(f"  - id={h.id} | status={h.status} | release_at={h.release_at} | sending_started={h.sending_started_at} | channel={h.channel}")

    # 4. Trusted Recipients
    trusted = session.query(TrustedRecipient).filter_by(account_id=account_id).all()
    print(f"\n[trusted_recipients] ({len(trusted)} rows):")
    for t in trusted:
        print(f"  - id={t.id} | email={t.email} | source={t.source} | confirmed_at={t.confirmed_at}")

    # 5. Dispatched Actions
    actions = session.query(DispatchedAction).filter_by(account_id=account_id).all()
    print(f"\n[dispatched_actions] ({len(actions)} rows):")
    for act in actions:
        print(f"  - id={act.id} | status={act.status} | mode={act.mode} | channel={act.channel} | dispatched_at={act.dispatched_at}")

    # 6. Send Evidence
    evidences = session.query(SendEvidence).filter_by(account_id=account_id).all()
    print(f"\n[send_evidence] ({len(evidences)} rows):")
    for ev in evidences:
        print(f"  - id={ev.id} | external_msg_id={ev.external_message_id} | subject={ev.subject} | recipient={ev.recipient_email} | sent_at={ev.sent_at}")


async def run_supervised_test(session):
    print_section("LIVE TEST #1: SUPERVISED MODE DISPATCH (FULL END-TO-END)")
    account_id = f"acc-live-sup-{uuid.uuid4().hex[:8]}"
    job_id = f"job-live-sup-{uuid.uuid4().hex[:8]}"

    # 1. Seed Account
    acc = Account(id=account_id, email=f"{account_id}@jobeazy.com", role="tenant", plan_tier="free")
    session.add(acc)

    # 2. Seed Job
    job = Job(
        id=job_id,
        account_id=account_id,
        company="Stripe Payments",
        role="Senior Backend Infrastructure Engineer",
        source="greenhouse",
        apply_link="mailto:hiring@stripe.com",
        is_active=True,
        vetoed=False,
    )
    session.add(job)

    # 3. Seed Dispatch Settings (Supervised Mode)
    settings = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode="supervised",
        autonomous_daily_cap=5,
        autonomous_hourly_cap=2,
        safety_daily_cap=50,
        safety_hourly_cap=10,
        kill_switch=False,
        is_suspended_by_admin=False,
    )
    session.add(settings)

    # 4. Seed Google OAuth Connection
    oauth_conn = OAuthConnection(
        id=f"oauth-{account_id}",
        account_id=account_id,
        provider="google",
        email=f"{account_id}@gmail.com",
        encrypted_access_token=encrypt_oauth_token("mock_google_access_token_phase0"),
        token_expires_at=datetime.now(timezone.utc) + timedelta(hours=2),
    )
    session.add(oauth_conn)
    session.commit()

    print(f"1. Seeded Account ({account_id}) and Job ({job_id}) in supervised mode.")

    # 5. Build and invoke ApplyGraph in supervised mode
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)
    thread_config = {"configurable": {"thread_id": f"apply-{account_id}-run1", "account_id": account_id}}

    initial_state = {
        "account_id": account_id,
        "job_id": job_id,
        "apply_url": job.apply_link,
        "user_email": f"{account_id}@jobeazy.com",
        "company_name": "Stripe Payments",
        "role_title": "Senior Backend Infrastructure Engineer",
        "job_description": "We are seeking a Senior Backend Engineer proficient in Python, PostgreSQL, and distributed message queues.",
        "autonomy_mode": "supervised",
        "target_email": "hiring@stripe.com",
    }

    print("2. Invoking ApplyGraph until HITL gate...")
    await graph.ainvoke(initial_state, config=thread_config)

    state_before = await graph.aget_state(thread_config)
    print(f"   -> Graph halted at: {state_before.next}")
    assert state_before.next == ("hitl_gate",), f"Expected ('hitl_gate',), got {state_before.next}"
    print(f"   -> Application package assembled and waiting at SendApprovalGate.")

    # 6. Resume with Human Approval
    print("3. Human submits APPROVE at SendApprovalGate...")
    resume_command = Command(resume={"action": "approve"})
    await graph.ainvoke(resume_command, config=thread_config)

    state_after = await graph.aget_state(thread_config)
    print(f"   -> Graph state after approval: {state_after.values.get('status')}")
    assert state_after.values.get("status") == "queued_in_hold"
    hold_id = state_after.values.get("hold_queue_item_id")
    print(f"   -> Successfully queued in hold outbox! hold_queue_item_id={hold_id}")

    # 7. Make hold item immediately eligible for poller release (simulate 30s elapsed)
    hold_row = session.query(HoldQueueItem).filter_by(id=hold_id).first()
    hold_row.release_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    session.commit()
    print("4. Advanced hold item release_at to simulate 30s delay elapsed.")

    # 8. Run dispatch poller to claim and dispatch
    print("5. Executing dispatch_poller release via SendGateway...")
    mock_send_result = {
        "id": "msg_gmail_supervised_9a8b7c6d5e",
        "threadId": "thread_stripe_9a8b7c6d5e",
        "labelIds": ["SENT"],
    }

    with patch("app.services.integrations.google_service.GoogleIntegrationService.send_gmail_message", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = mock_send_result
        dispatched_count = await poll_and_dispatch_batch(session, batch_size=10)
        print(f"   -> Poller dispatched {dispatched_count} item(s).")
        assert dispatched_count == 1, f"Expected 1 dispatched item, got {dispatched_count}"

    # 9. Print Postgres State
    print_db_rows(session, account_id, "TEST #1 (SUPERVISED MODE)")
    return account_id


async def run_tofu_test(session):
    print_section("LIVE TEST #2: TOFU AUTONOMOUS DOWNGRADE -> HUMAN APPROVAL -> TRUSTED RECIPIENTS")
    account_id = f"acc-live-tofu-{uuid.uuid4().hex[:8]}"
    job_id = f"job-live-tofu-{uuid.uuid4().hex[:8]}"
    untrusted_email = "lead-recruiter@anthropic.com"

    # 1. Seed Account
    acc = Account(id=account_id, email=f"{account_id}@jobeazy.com", role="tenant", plan_tier="free")
    session.add(acc)

    # 2. Seed Job with UNTRUSTED recipient email
    job = Job(
        id=job_id,
        account_id=account_id,
        company="Anthropic Safety",
        role="Staff AI Safety Engineer",
        source="greenhouse",
        apply_link=f"mailto:{untrusted_email}",
        is_active=True,
        vetoed=False,
    )
    session.add(job)

    # 3. Seed Dispatch Settings (Autonomous Mode)
    settings = AccountDispatchSettings(
        account_id=account_id,
        autonomy_mode="autonomous",
        autonomous_daily_cap=5,
        autonomous_hourly_cap=2,
        safety_daily_cap=50,
        safety_hourly_cap=10,
        kill_switch=False,
        is_suspended_by_admin=False,
    )
    session.add(settings)

    # 4. Seed Google OAuth Connection
    oauth_conn = OAuthConnection(
        id=f"oauth-{account_id}",
        account_id=account_id,
        provider="google",
        email=f"{account_id}@gmail.com",
        encrypted_access_token=encrypt_oauth_token("mock_google_access_token_tofu"),
        token_expires_at=datetime.now(timezone.utc) + timedelta(hours=2),
    )
    session.add(oauth_conn)
    session.commit()

    print(f"1. Seeded Account ({account_id}) in AUTONOMOUS mode targeting unverified '{untrusted_email}'.")

    # Verify recipient is NOT currently trusted
    existing_tr = session.query(TrustedRecipient).filter_by(account_id=account_id, email=untrusted_email).first()
    assert existing_tr is None, "Precondition violated: recipient should not be trusted yet."
    print("   -> Precondition verified: recipient is NOT in trusted_recipients table.")

    # 5. Build and invoke ApplyGraph in AUTONOMOUS mode
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)
    thread_config = {"configurable": {"thread_id": f"apply-{account_id}-tofu1", "account_id": account_id}}

    initial_state = {
        "account_id": account_id,
        "job_id": job_id,
        "apply_url": job.apply_link,
        "user_email": f"{account_id}@jobeazy.com",
        "company_name": "Anthropic Safety",
        "role_title": "Staff AI Safety Engineer",
        "job_description": "We are seeking a Staff AI Safety Engineer to conduct rigorous empirical model evaluations.",
        "autonomy_mode": "autonomous",  # Requested autonomous
        "target_email": untrusted_email,
    }

    print("2. Invoking ApplyGraph in AUTONOMOUS mode...")
    await graph.ainvoke(initial_state, config=thread_config)

    state_before = await graph.aget_state(thread_config)
    print(f"   -> Graph halted at: {state_before.next}")
    downgrade_reason = state_before.values.get("downgrade_reason")
    print(f"   -> Decision D1 downgrade_reason: '{downgrade_reason}'")

    assert state_before.next == ("hitl_gate",), f"Expected TOFU downgrade to hitl_gate, got {state_before.next}"
    assert downgrade_reason is not None and "trusted_recipients" in downgrade_reason, f"Expected TOFU reason, got {downgrade_reason}"
    print("   -> TOFU Barrier Confirmed: Autonomous run successfully downgraded to HITL Gate!")

    # 6. Candidate inspects TOFU banner and approves at Gate
    print(f"3. Human reviews package, acknowledges TOFU recipient '{untrusted_email}', and clicks APPROVE...")
    resume_command = Command(resume={"action": "approve"})
    await graph.ainvoke(resume_command, config=thread_config)

    state_after = await graph.aget_state(thread_config)
    assert state_after.values.get("status") == "queued_in_hold"
    hold_id = state_after.values.get("hold_queue_item_id")
    print(f"   -> Workflow completed to outbox: hold_queue_item_id={hold_id}")

    # 7. Verify TOFU Upsert into trusted_recipients table!
    tr_row = session.query(TrustedRecipient).filter_by(account_id=account_id, email=untrusted_email).first()
    assert tr_row is not None, f"Expected {untrusted_email} to be upserted into trusted_recipients, but not found!"
    assert tr_row.source == "manual_approval"
    print(f"   -> TOFU Registration Verified: '{tr_row.email}' registered with source='{tr_row.source}' at {tr_row.confirmed_at}!")

    # 8. Advance hold time and run poller
    hold_row = session.query(HoldQueueItem).filter_by(id=hold_id).first()
    hold_row.release_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    session.commit()

    print("4. Executing dispatch_poller release via SendGateway...")
    mock_send_result = {
        "id": "msg_gmail_tofu_4f5e6d7c8b",
        "threadId": "thread_anthropic_4f5e6d7c8b",
        "labelIds": ["SENT"],
    }

    with patch("app.services.integrations.google_service.GoogleIntegrationService.send_gmail_message", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = mock_send_result
        dispatched_count = await poll_and_dispatch_batch(session, batch_size=10)
        print(f"   -> Poller dispatched {dispatched_count} item(s).")
        assert dispatched_count == 1

    # 9. Print Postgres State
    print_db_rows(session, account_id, "TEST #2 (TOFU AUTONOMOUS DOWNGRADE)")
    return account_id


async def main():
    session = get_session_factory()()
    try:
        await run_supervised_test(session)
        await run_tofu_test(session)
        print_section("ALL LIVE DOGFOODING TESTS COMPLETED WITH 100% SUCCESS!")
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())


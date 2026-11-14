"""
backend/tests/agent/test_apply_graph.py

Unit tests for Modular LangGraph ApplyGraph pipeline:
1. Supervised flow: stops at hitl_gate with interrupt() and SendApprovalGate payload.
2. Resume with approval: Command(resume={"action": "approve"}) executes dispatch.
3. Resume with reject: Command(resume={"action": "reject"}) exits at failed.
4. Autonomous flow: passes pre-send verification barrier and routes directly to dispatch.
5. Autonomous downgrade: catches public webmail (@gmail.com) and downgrades to hitl_gate.
6. Drop edge: low fit score (<60) routes to skip_job (END).
"""

import pytest
from unittest.mock import AsyncMock, patch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from app.models.account import Account
from app.models.job import Job
from app.models.dispatch import HoldQueueItem, SendAuthorization, TrustedRecipient
from app.models.metering import QuotaReservation
from app.services.agent.workflows.state import ApplyState
from app.services.agent.workflows.apply_graph import build_apply_graph
from app.services.matching.fit_analyzer import FitAnalyzerOutput, DimensionDiagnostic
from app.services.cv_tailor.reviewer import CVReviewOutput
from app.services.outreach.drafter_service import OutreachDrafterOutput, FormAnswerPair


@pytest.fixture(autouse=True)
def seed_test_apply_graph_fixtures(test_db_session):
    """Seeds test account and jobs in PostgreSQL to satisfy relational foreign key constraints."""
    acc = test_db_session.query(Account).filter_by(id="acc-tenant-1").first()
    if not acc:
        acc = Account(id="acc-tenant-1", email="candidate@example.com")
        test_db_session.add(acc)
        test_db_session.commit()

    jobs = [
        ("job-101", "Lead AI Engineer", "DeepMind"),
        ("job-102", "Lead AI Engineer", "DeepMind"),
        ("job-103", "Lead AI Engineer", "DeepMind"),
        ("job-201", "Lead AI Engineer", "DeepMind"),
        ("job-202", "Lead AI Engineer", "StartupLab"),
        ("job-203", "Lead AI Engineer", "DeepMind"),
        ("job-301", "Senior Clinical Nurse", "BioPharma"),
        ("job-401", "Lead AI Engineer", "DeepMind"),
        ("job-501", "Research Scientist", "OpenAI"),
        ("job-601", "Safety Engineer", "Anthropic"),
        ("job-701", "AI Systems Engineer", "Microsoft"),
    ]
    for jid, role, company in jobs:
        j = test_db_session.query(Job).filter_by(id=jid).first()
        if not j:
            j = Job(
                id=jid,
                account_id="acc-tenant-1",
                role=role,
                company=company,
                source="test",
                apply_link=f"https://{company.lower().replace(' ', '')}.com/apply",
                is_active=True,
            )
            test_db_session.add(j)
    test_db_session.commit()
    yield


@pytest.fixture
def mock_llm_responses():
    """Mock LLMService.generate to return valid structured responses."""
    with patch("app.services.llm.service.LLMService.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = """---TAILORED_SUMMARY---
\\resumeItem{AI Engineer specializing in Agentic AI and FastAPI systems for DeepMind.}
---COVER_NOTE---
Dear Hiring Team at DeepMind, I am thrilled to apply for the Lead AI Engineer position.
---GAPS---
- None
"""
        yield mock_gen


@pytest.mark.asyncio
async def test_apply_graph_supervised_reaches_interrupt(mock_llm_responses):
    """Verifies supervised execution halts cleanly at hitl_gate with interrupt()."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-sup-1"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-101",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "We are seeking a Lead AI Engineer with Python, FastAPI, Docker, and LLM experience.",
        "autonomy_mode": "supervised",
    }

    # Execute graph until interrupt
    result = await graph.ainvoke(initial_state, config=thread_config)

    # Verify graph state is paused at hitl_gate
    state = await graph.aget_state(thread_config)
    assert state.next == ("hitl_gate",)
    assert len(state.tasks) > 0
    assert len(state.tasks[0].interrupts) > 0

    interrupt_payload = state.tasks[0].interrupts[0].value
    assert "widget" in interrupt_payload
    widget = interrupt_payload["widget"]
    assert widget["type"] == "SendApprovalGate"
    assert widget["props"]["company"] == "DeepMind"
    assert widget["props"]["role"] == "Lead AI Engineer"
    assert widget["props"]["content_hash"] is not None


@pytest.mark.asyncio
async def test_apply_graph_resume_with_approval(mock_llm_responses):
    """Verifies resuming an interrupted graph with Command(resume=approve) runs dispatch."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-sup-2"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-102",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "Python, FastAPI, Docker, and LLM experience.",
        "autonomy_mode": "supervised",
    }

    # 1. Run until hitl_gate interrupt
    await graph.ainvoke(initial_state, config=thread_config)
    state_before = await graph.aget_state(thread_config)
    assert state_before.next == ("hitl_gate",)

    # 2. Resume with user approval Command
    resume_command = Command(resume={"action": "approve"})
    resumed_result = await graph.ainvoke(resume_command, config=thread_config)

    # 3. Verify workflow completed to dispatch
    state_after = await graph.aget_state(thread_config)
    assert state_after.next == ()  # Reached END
    assert state_after.values["status"] == "queued_in_hold"
    assert state_after.values["package_ref"] is not None


@pytest.mark.asyncio
async def test_apply_graph_resume_with_reject(mock_llm_responses):
    """Verifies resuming an interrupted graph with Command(resume=reject) terminates at failed."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-sup-3"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-103",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "Python, FastAPI, Docker, and LLM experience.",
        "autonomy_mode": "supervised",
    }

    await graph.ainvoke(initial_state, config=thread_config)
    resume_command = Command(resume={"action": "reject"})
    await graph.ainvoke(resume_command, config=thread_config)

    state_after = await graph.aget_state(thread_config)
    assert state_after.next == ()
    assert state_after.values["status"] == "waiting_approval"  # rejected before dispatch


@pytest.mark.asyncio
async def test_apply_graph_autonomous_flow_passes_gates(mock_llm_responses, test_db_session):
    """Verifies legitimate corporate email with trusted recipient executes autonomously without interrupt."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    # Seed trusted recipient for jobs@deepmind.com
    tr = test_db_session.query(TrustedRecipient).filter_by(account_id="acc-tenant-1", email="jobs@deepmind.com").first()
    if not tr:
        tr = TrustedRecipient(account_id="acc-tenant-1", email="jobs@deepmind.com", source="manual_approval")
        test_db_session.add(tr)
        test_db_session.commit()

    thread_config = {"configurable": {"thread_id": "thread-test-auto-1"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-201",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "We are seeking a Lead AI Engineer with Python, FastAPI, Docker, and LLM experience. Send CV to jobs@deepmind.com",
        "autonomy_mode": "autonomous",
    }

    # Patch review_cv to return strong ATS score (88%) and 1 page
    with patch("app.services.cv_tailor.reviewer.CVReviewerService.review_cv", new_callable=AsyncMock) as mock_review:
        mock_review.return_value = CVReviewOutput(
            is_valid=True,
            final_tailored_latex="\\documentclass{article}\\begin{document}Tailored CV\\end{document}",
            final_summary_bullet="\\resumeItem{Lead AI Engineer}",
            final_cover_letter="Cover letter",
            confirmed_gaps=[],
            ats_score=88.0,
            fact_audit_passed=True,
            hallucination_detected=False,
            line_count=60,
            computed_page_count=1,
            reviewer_notes="Pass",
        )
        # Execute graph
        await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    # Autonomy barrier satisfied -> bypassed hitl_gate directly to dispatch -> END
    assert state.next == ()
    assert state.values["status"] == "queued_in_hold"
    assert state.values["downgrade_reason"] is None


@pytest.mark.asyncio
async def test_apply_graph_autonomous_downgrades_on_untrusted_tofu(mock_llm_responses, test_db_session):
    """Verifies that an autonomous attempt to email an untrusted corporate recipient triggers TOFU downgrade."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    # Ensure careers@deepmind.com is untrusted initially
    test_db_session.query(TrustedRecipient).filter_by(account_id="acc-tenant-1", email="careers@deepmind.com").delete()
    test_db_session.commit()

    thread_config = {"configurable": {"thread_id": "thread-test-auto-tofu"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-203",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "Send CV to careers@deepmind.com with Python and FastAPI experience.",
        "autonomy_mode": "autonomous",
    }

    await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    # Must halt at hitl_gate because recipient is not in trusted_recipients
    assert state.next == ("hitl_gate",)
    assert state.values["downgrade_reason"] is not None
    assert "TOFU" in state.values["downgrade_reason"]

    # Resuming with approve confirms trust and dispatches
    resume_command = Command(resume={"action": "approve"})
    await graph.ainvoke(resume_command, config=thread_config)

    state_after = await graph.aget_state(thread_config)
    assert state_after.next == ()
    assert state_after.values["status"] == "queued_in_hold"


@pytest.mark.asyncio
async def test_apply_graph_autonomous_downgrades_on_free_webmail(mock_llm_responses):
    """Verifies that an autonomous attempt to email a public webmail address (@gmail.com) downgrades to HITL gate."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-auto-downgrade"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-202",
        "user_email": "candidate@example.com",
        "company_name": "StartupLab",
        "role_title": "Lead AI Engineer",
        "job_description": "Email resumes to startuplab.recruiter@gmail.com with Python and FastAPI background.",
        "autonomy_mode": "autonomous",
    }

    await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    # Must be halted at hitl_gate due to webmail domain barrier
    assert state.next == ("hitl_gate",)
    assert state.values["downgrade_reason"] is not None
    assert "public webmail address" in state.values["downgrade_reason"]


@pytest.mark.asyncio
async def test_apply_graph_drops_low_fit(mock_llm_responses):
    """Verifies that low fit score (<60) routes to skip_job (END)."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-drop-1"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-301",
        "user_email": "candidate@example.com",
        "company_name": "BioPharma",
        "role_title": "Senior Clinical Nurse",
        "job_description": "Pediatric nursing and patient rounds with medical doctorate.",
        "autonomy_mode": "supervised",
    }

    # Patch fit analyzer output to have score 30
    with patch("app.services.matching.fit_analyzer.FitAnalyzerService.analyze_fit", new_callable=AsyncMock) as mock_fit:
        mock_fit.return_value = FitAnalyzerOutput(
            company="BioPharma",
            role="Senior Clinical Nurse",
            overall_score=30,
            recommendation="MISALIGNED",
            should_proceed=False,
            dimensions={},
            language_gate_passed=True,
        )
        await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    assert state.next == ()
    assert state.values.get("cv_draft") is None  # Never proceeded to drafting


@pytest.mark.asyncio
async def test_apply_graph_self_correction_redraft(mock_llm_responses):
    """Verifies that fact check failure triggers redrafting and bounded retry."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-redraft-1"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-401",
        "user_email": "candidate@example.com",
        "company_name": "DeepMind",
        "role_title": "Lead AI Engineer",
        "job_description": "Python, FastAPI, Docker, and LLM experience.",
        "autonomy_mode": "supervised",
    }

    # First review fails fact check, second review succeeds
    review_call_count = 0
    async def mock_review_side_effect(*args, **kwargs):
        nonlocal review_call_count
        review_call_count += 1
        if review_call_count == 1:
            return CVReviewOutput(
                is_valid=False,
                final_tailored_latex="\\documentclass{article}\\begin{document}Unverified claim\\end{document}",
                final_summary_bullet="\\resumeItem{Unverified}",
                final_cover_letter="Cover",
                confirmed_gaps=[],
                ats_score=50.0,
                fact_audit_passed=False,
                hallucination_detected=True,
                hallucination_reasons=["Unverified claim detected"],
                line_count=60,
                computed_page_count=1,
                reviewer_notes="Failed fact check",
            )
        else:
            return CVReviewOutput(
                is_valid=True,
                final_tailored_latex="\\documentclass{article}\\begin{document}Verified claim\\end{document}",
                final_summary_bullet="\\resumeItem{Verified}",
                final_cover_letter="Cover",
                confirmed_gaps=[],
                ats_score=85.0,
                fact_audit_passed=True,
                hallucination_detected=False,
                hallucination_reasons=[],
                line_count=60,
                computed_page_count=1,
                reviewer_notes="Passed fact check",
            )

    with patch("app.services.cv_tailor.reviewer.CVReviewerService.review_cv", side_effect=mock_review_side_effect):
        await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    assert review_call_count == 2
    assert state.values["review_iteration"] == 2
    assert state.next == ("hitl_gate",)


@pytest.mark.asyncio
async def test_apply_graph_fact_audit_failure_hard_stops_at_needs_edit(mock_llm_responses):
    """Verifies S1: Persistent fact audit failure after retry terminates at needs_edit node."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-hardstop-1"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-501",
        "user_email": "candidate@example.com",
        "company_name": "OpenAI",
        "role_title": "Research Scientist",
        "job_description": "LLM pretraining and alignment.",
        "autonomy_mode": "supervised",
    }

    failed_review = CVReviewOutput(
        is_valid=False,
        final_tailored_latex="\\documentclass{article}\\begin{document}Unverified claim\\end{document}",
        final_summary_bullet="\\resumeItem{Unverified}",
        final_cover_letter="Cover",
        confirmed_gaps=[],
        ats_score=50.0,
        fact_audit_passed=False,
        hallucination_detected=True,
        hallucination_reasons=["Unverified claim persists"],
        line_count=60,
        computed_page_count=1,
        reviewer_notes="Failed fact check persistently",
    )

    with patch("app.services.cv_tailor.reviewer.CVReviewerService.review_cv", return_value=failed_review):
        await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    # Exceeded max_retries=1 -> S1 Hard Stop -> transitions to needs_edit -> END
    assert state.next == ()
    assert state.values["status"] == "needs_edit"
    assert "CV tailoring failed fact audit" in (state.values.get("error") or "")


@pytest.mark.asyncio
async def test_apply_graph_approval_gate_edit_loop(mock_llm_responses):
    """Verifies G3: In-place edits at approval gate loop back to assemble_package to re-audit & re-hash."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-edit-loop"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-601",
        "user_email": "candidate@example.com",
        "company_name": "Anthropic",
        "role_title": "Safety Engineer",
        "job_description": "Safety evaluation and alignment testing.",
        "autonomy_mode": "supervised",
    }

    # 1. First run halts at hitl_gate
    await graph.ainvoke(initial_state, config=thread_config)
    state_step1 = await graph.aget_state(thread_config)
    assert state_step1.next == ("hitl_gate",)
    initial_hash = state_step1.values["package_ref"].content_hash

    # 2. User provides in-place edits (G3 edit loop)
    edit_command = Command(resume={
        "action": "edit",
        "edited_body": "Custom edited email body by candidate.",
        "edited_subject": "Application for Safety Engineer - Custom",
        "edited_latex": "\\documentclass{article}\\begin{document}Custom Tailored LaTeX\\end{document}",
    })
    await graph.ainvoke(edit_command, config=thread_config)

    # 3. Graph loops through assemble_package and pauses AGAIN at hitl_gate with new hash
    state_step2 = await graph.aget_state(thread_config)
    assert state_step2.next == ("hitl_gate",)
    new_package = state_step2.values["package_ref"]
    assert new_package.content_hash != initial_hash
    assert state_step2.values["outreach"].body_content == "Custom edited email body by candidate."
    assert state_step2.values["outreach"].subject_line == "Application for Safety Engineer - Custom"
    assert state_step2.values["cv_draft"].draft_assembled_latex == "\\documentclass{article}\\begin{document}Custom Tailored LaTeX\\end{document}"

    # 4. Final approval releases package to dispatch
    approve_command = Command(resume={"action": "approve"})
    await graph.ainvoke(approve_command, config=thread_config)

    state_step3 = await graph.aget_state(thread_config)
    assert state_step3.next == ()
    assert state_step3.values["status"] == "queued_in_hold"


@pytest.mark.asyncio
async def test_apply_graph_dispatch_contract3_database_records(mock_llm_responses, test_db_session):
    """Verifies Contract 3 / G4: dispatch_node reserves quota and enqueues HoldQueueItem with correct delay."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-test-dispatch-contract"}}
    initial_state = {
        "account_id": "acc-tenant-1",
        "job_id": "job-701",
        "user_email": "candidate@example.com",
        "company_name": "Microsoft",
        "role_title": "AI Systems Engineer",
        "job_description": "Azure AI systems engineering.",
        "autonomy_mode": "supervised",
    }

    # 1. Run to gate
    await graph.ainvoke(initial_state, config=thread_config)
    # 2. Approve
    await graph.ainvoke(Command(resume={"action": "approve"}), config=thread_config)

    state_after = await graph.aget_state(thread_config)
    assert state_after.next == ()
    assert state_after.values["status"] == "queued_in_hold"

    # Verify real DB records in test_db_session
    hold_item = test_db_session.query(HoldQueueItem).filter(
        HoldQueueItem.account_id == "acc-tenant-1",
        HoldQueueItem.status == "pending",
        HoldQueueItem.hold_kind == "review_required",
    ).order_by(HoldQueueItem.created_at.desc()).first()

    assert hold_item is not None
    assert hold_item.account_id == "acc-tenant-1"
    assert hold_item.status == "pending"
    assert hold_item.hold_kind == "review_required"  # Supervised -> 30s review_required
    assert hold_item.reservation_id is not None
    assert hold_item.authorization_id is not None

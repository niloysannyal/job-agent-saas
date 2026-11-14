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

from app.services.agent.workflows.state import ApplyState
from app.services.agent.workflows.apply_graph import build_apply_graph
from app.services.matching.fit_analyzer import FitAnalyzerOutput, DimensionDiagnostic
from app.services.cv_tailor.reviewer import CVReviewOutput
from app.services.outreach.drafter_service import OutreachDrafterOutput, FormAnswerPair


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
async def test_apply_graph_autonomous_flow_passes_gates(mock_llm_responses):
    """Verifies legitimate corporate email with trusted recipient executes autonomously without interrupt."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

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

    from unittest.mock import MagicMock
    mock_db = MagicMock()
    mock_tr = MagicMock()
    mock_tr.email = "jobs@deepmind.com"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tr

    # Patch review_cv to return strong ATS score (88%) and 1 page, and DB to return trusted recipient
    with patch("app.services.cv_tailor.reviewer.CVReviewerService.review_cv", new_callable=AsyncMock) as mock_review, \
         patch("app.db.session.SessionLocal", return_value=MagicMock(__enter__=MagicMock(return_value=mock_db))):
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
async def test_apply_graph_autonomous_downgrades_on_untrusted_tofu(mock_llm_responses):
    """Verifies that an autonomous attempt to email an untrusted corporate recipient triggers TOFU downgrade."""
    checkpointer = MemorySaver()
    graph = build_apply_graph(checkpointer=checkpointer)

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

    from unittest.mock import MagicMock
    mock_db = MagicMock()
    # Return None for TrustedRecipient query to simulate first-time recipient (TOFU)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with patch("app.db.session.SessionLocal", return_value=MagicMock(__enter__=MagicMock(return_value=mock_db))):
        await graph.ainvoke(initial_state, config=thread_config)

    state = await graph.aget_state(thread_config)
    # Must halt at hitl_gate because recipient is not in trusted_recipients
    assert state.next == ("hitl_gate",)
    assert state.values["downgrade_reason"] is not None
    assert "TOFU" in state.values["downgrade_reason"]

    # Resuming with approve confirms trust and dispatches
    resume_command = Command(resume={"action": "approve"})
    with patch("app.db.session.SessionLocal", return_value=MagicMock(__enter__=MagicMock(return_value=mock_db))):
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
async def test_apply_graph_dispatch_contract3_database_records(mock_llm_responses):
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

    from unittest.mock import MagicMock
    mock_db = MagicMock()
    # Mock query responses
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with patch("app.db.session.SessionLocal", return_value=MagicMock(__enter__=MagicMock(return_value=mock_db))):
        # 1. Run to gate
        await graph.ainvoke(initial_state, config=thread_config)
        # 2. Approve
        await graph.ainvoke(Command(resume={"action": "approve"}), config=thread_config)

    # Verify db_session.add was called for QuotaReservation, HoldQueueItem, TrustedRecipient
    added_instances = [call.args[0] for call in mock_db.add.call_args_list]
    types_added = [type(inst).__name__ for inst in added_instances]

    assert "TrustedRecipient" in types_added
    assert "QuotaReservation" in types_added
    assert "HoldQueueItem" in types_added

    # Verify hold queue item parameters
    hold_item = next(inst for inst in added_instances if type(inst).__name__ == "HoldQueueItem")
    assert hold_item.account_id == "acc-tenant-1"
    assert hold_item.status == "pending"
    assert hold_item.hold_kind == "review_required"  # Supervised -> 30s review_required
    mock_db.commit.assert_called()

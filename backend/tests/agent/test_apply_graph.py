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
    assert state_after.values["status"] == "enqueued_hold"
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
    """Verifies legitimate corporate email application executes autonomously without interrupt."""
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
    assert state.values["status"] == "enqueued_hold"
    assert state.values["downgrade_reason"] is None


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

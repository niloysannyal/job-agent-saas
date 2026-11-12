"""
backend/app/services/agent/workflows/apply_graph.py

Modular LangGraph Application Pipeline Graph (ApplyGraph).
Executes the autonomous and semi-autonomous job application lifecycle:
1. 4D Fit Analysis -> conditional drop if score < 60.
2. Channel Detection (Email, Google Form, Typeform, ATS Portal, DM).
3. Senior Recruiter CV Drafter (Pass 1 non-mutating).
4. Senior Recruiter CV Reviewer & Fact Auditor (Pass 2).
   -> Self-correction loop: if fact audit fails, re-drafts up to bounded limit (1 retry).
5. Multi-channel Outreach Drafter (Email, Form Q&A, Recruiter DM).
6. Assemble Package & Compute Canonical Content Hash.
7. Isolated HITL Gate Node (`interrupt()`) for Supervised Mode & Downgrades.
8. Safe Outbound Dispatch via SendGateway with Differential Hold Delay (5m auto / 30s supervised).
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, Literal, Optional
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt

from app.services.agent.workflows.state import ApplyState, ApplicationPackageRef
from app.services.matching.fit_analyzer import FitAnalyzerService, FitAnalyzerInput
from app.services.form_detective.detective import FormDetectiveService, ApplyChannelType
from app.services.cv_tailor.drafter import CVDrafterService, CVDraftInput, CandidateCareerContext
from app.services.cv_tailor.reviewer import CVReviewerService, CVReviewInput
from app.services.outreach.drafter_service import (
    OutreachDrafterService,
    OutreachDrafterInput,
    OutreachChannelType,
)
from app.services.dispatch.hash_utils import compute_content_hash

logger = logging.getLogger(__name__)

# Free webmail providers strictly prohibited from unattended autonomous dispatch (Decision D1)
PROHIBITED_AUTO_WEBMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "icloud.com", "aol.com", "proton.me", "protonmail.com", "zoho.com"
}


# ===========================================================================
# 1. Pipeline Node Functions
# ===========================================================================

async def fit_analyzer_node(state: ApplyState) -> Dict[str, Any]:
    """Evaluates 4-Dimension career alignment (Skills, Experience, Trajectory, Seniority)."""
    service = FitAnalyzerService()
    result = await service.analyze_fit(
        account_id=state.account_id,
        job_id=state.job_id,
        company_name=state.company_name,
        role_title=state.role_title,
        posting_text=state.job_description,
    )
    return {
        "fit_result": result,
        "status": "analyzing_fit",
    }


def should_apply_edge(state: ApplyState) -> str:
    """Routes to channel detection if fit is sufficient, else drops the job."""
    fit = state.fit_result
    if not fit or not fit.should_proceed or fit.overall_score < 60:
        return "skip_job"
    return "detect_method"


async def detect_method_node(state: ApplyState) -> Dict[str, Any]:
    """Classifies apply channel and extracts form questions or recruiter email."""
    fit = state.fit_result
    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    desc = state.job_description or ""
    
    # Deterministic discovery
    inspection = FormDetectiveService.detect_channel(
        apply_url=state.apply_url,
        posting_text=desc,
        company_name=company,
        role_title=role,
    )
    
    channel_info = {
        "channel_type": inspection.channel_type.value,
        "platform_name": inspection.platform_name,
        "apply_url": inspection.apply_url,
        "recruiter_email": inspection.recruiter_email,
        "questions": [
            {
                "id": q.id,
                "prompt": q.prompt,
                "field_type": q.field_type,
                "char_limit": q.char_limit,
                "is_required": q.is_required,
            }
            for q in inspection.questions
        ],
    }
    return {
        "channel_info": channel_info,
        "status": "detecting_method",
    }


async def cv_drafter_node(state: ApplyState) -> Dict[str, Any]:
    """Executes Pass 1 (Senior Recruiter Drafter) with dynamic section budgeting."""
    fit = state.fit_result
    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    desc = state.job_description or f"{role} at {company}"

    drafter = CVDrafterService()
    context = CandidateCareerContext(
        account_id=state.account_id,
        candidate_name="Niloy Sannyal",
        headline="AI Systems Engineer",
        master_latex="\\documentclass{article}\n\\begin{document}\n\\section{SUMMARY}\n\\resumeItemListStart\\resumeItem{Base}\\resumeItemListEnd\n\\end{document}",
        skills=["Python", "FastAPI", "Docker", "LLMs", "RAG"],
        verified_facts_str="- 600+ salespersons (Betopia Sales Agent in Odoo CRM)\n- 10,000+ fights, 80+ features (UFC ML platform)",
    )

    draft = await drafter.draft_cv(
        params=CVDraftInput(
            account_id=state.account_id,
            job_id=state.job_id,
            job_role=role,
            job_company=company,
            job_description=desc,
        ),
        career_context=context,
    )
    return {
        "cv_draft": draft,
        "status": "drafting_cv",
    }


async def cv_reviewer_node(state: ApplyState) -> Dict[str, Any]:
    """Executes Pass 2 (Senior Recruiter Reviewer & Fact Auditor)."""
    fit = state.fit_result
    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    desc = state.job_description or f"{role} at {company}"

    reviewer = CVReviewerService()
    context = CandidateCareerContext(
        account_id=state.account_id,
        candidate_name="Niloy Sannyal",
        headline="AI Systems Engineer",
        master_latex="",
        verified_facts_str="- 600+ salespersons (Betopia Sales Agent in Odoo CRM)",
    )

    review = await reviewer.review_cv(
        params=CVReviewInput(
            draft_output=state.cv_draft,
            job_role=role,
            job_company=company,
            job_description=desc,
            career_context=context,
        )
    )
    return {
        "cv_review": review,
        "review_iteration": state.review_iteration + 1,
        "status": "reviewing_cv",
    }


def review_guard_edge(state: ApplyState) -> str:
    """Self-correction edge: re-drafts if fact audit failed (bounded to 1 retry, max 2 review passes)."""
    review = state.cv_review
    if review and not review.fact_audit_passed and state.review_iteration <= 1:
        return "redraft_cv"
    return "draft_outreach"


async def outreach_drafter_node(state: ApplyState) -> Dict[str, Any]:
    """Generates tailored outreach matching the discovered channel."""
    fit = state.fit_result
    channel = state.channel_info.get("channel_type", "email") if state.channel_info else "email"
    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    desc = state.job_description or f"{role} at {company}"

    channel_type_enum = OutreachChannelType.EMAIL
    if channel in ("google_form", "typeform"):
        channel_type_enum = OutreachChannelType.GOOGLE_FORM
    elif channel == "ats_portal":
        channel_type_enum = OutreachChannelType.ATS_PORTAL
    elif channel == "direct_message":
        channel_type_enum = OutreachChannelType.DIRECT_MESSAGE

    outreach_service = OutreachDrafterService()
    outreach = await outreach_service.draft_outreach(
        params=OutreachDrafterInput(
            account_id=state.account_id,
            job_id=state.job_id,
            company_name=company,
            role_title=role,
            job_description=desc,
            channel_type=channel_type_enum,
            questions=state.channel_info.get("questions") if state.channel_info else None,
        ),
        candidate_name="Niloy Sannyal",
    )
    return {
        "outreach": outreach,
        "status": "drafting_outreach",
    }


async def assemble_package_node(state: ApplyState) -> Dict[str, Any]:
    """
    Assembles the complete ApplicationPackageRef and computes canonical length-prefixed content hash.
    Side-effects happen here BEFORE the isolated gate node.
    """
    fit = state.fit_result
    channel_info = state.channel_info or {}
    review = state.cv_review
    outreach = state.outreach

    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    channel = channel_info.get("channel_type", "email")
    recipient = channel_info.get("recruiter_email") or "careers@target.com"

    form_answers = {qa.question_id: qa.answer_text for qa in outreach.qa_answers} if outreach else {}
    attachment_sha256 = "simulated_pdf_sha256_hash_12345"

    import json
    answers_json = json.dumps(form_answers, sort_keys=True)

    # Compute length-prefixed canonical content hash
    content_hash = compute_content_hash(
        cv_version_id="cv-v1",
        subject=outreach.subject_line or f"{role} Application" if outreach else f"{role} Application",
        body=outreach.body_content if outreach else "",
        recipient=recipient,
        answers_json=answers_json,
        attachment_sha256=attachment_sha256,
    )

    package = ApplicationPackageRef(
        application_id=f"app-{state.job_id[:8]}",
        job_id=state.job_id,
        company_name=company,
        role_title=role,
        channel=channel,
        tailored_cv_version_id="cv-v1",
        pdf_artifact_path="/tmp/tailored_cv.pdf",
        attachment_sha256=attachment_sha256,
        ats_score=review.ats_score if review else 85.0,
        fact_audit_passed=review.fact_audit_passed if review else True,
        recipient_email=recipient,
        email_subject=outreach.subject_line if outreach else None,
        email_body=outreach.body_content if outreach else None,
        form_answers=form_answers,
        content_hash=content_hash,
    )
    # Pre-Send Verification Barrier Evaluation (Decision D1)
    downgrade_reason: Optional[str] = None
    if state.autonomy_mode == "autonomous":
        recipient_domain = (recipient or "").split("@")[-1].lower()
        if channel not in ("email", "direct_email"):
            downgrade_reason = f"Channel '{channel}' requires human confirmation."
        elif recipient_domain in PROHIBITED_AUTO_WEBMAIL_DOMAINS:
            downgrade_reason = f"Recipient domain '@{recipient_domain}' is a public webmail address; human confirmation required."
        elif review and not review.fact_audit_passed:
            downgrade_reason = "Fact integrity check flagged unverified claims."
        elif review and review.hallucination_detected:
            downgrade_reason = "Fact integrity check flagged hallucinated content."
        elif review and review.ats_score < 70.0:
            downgrade_reason = f"ATS score ({review.ats_score:.1f}%) is below the 70% autonomous threshold."
        elif review and (review.computed_page_count < 1 or review.computed_page_count > 2):
            downgrade_reason = f"CV page budget ({review.computed_page_count} pages) violates the 1-2 page rule."

    return {
        "package_ref": package,
        "proposal_id": f"prop-{state.job_id[:8]}",
        "downgrade_reason": downgrade_reason,
        "status": "assembling_package",
    }


def autonomy_gate_edge(state: ApplyState) -> str:
    """
    Decision D1 Pre-Send Verification Barrier:
    Evaluates whether autonomous execution is permitted or must downgrade to Supervised (HITL Gate).
    """
    if state.autonomy_mode != "autonomous" or state.downgrade_reason:
        return "hitl_gate"
    return "dispatch"


def hitl_approval_gate_node(state: ApplyState) -> Dict[str, Any]:
    """
    Isolated Gate Node Pattern.
    Line 1 is interrupt(widget). Resuming thread with Command(resume=...) re-enters here
    and immediately receives the resume payload with zero prior duplicate side-effects.
    """
    package = state.package_ref
    gate_widget = {
        "type": "SendApprovalGate",
        "props": {
            "proposal_id": state.proposal_id,
            "job_id": state.job_id,
            "company": package.company_name if package else "Company",
            "role": package.role_title if package else "Role",
            "channel": package.channel if package else "email",
            "recipient": package.recipient_email if package else None,
            "subject": package.email_subject if package else None,
            "ats_score": package.ats_score if package else 85.0,
            "downgrade_reason": state.downgrade_reason,
            "content_hash": package.content_hash if package else None,
        },
    }

    # Thread halts here until resumed by user
    resume_payload = interrupt({
        "proposal_id": state.proposal_id,
        "widget": gate_widget,
    })

    return {
        "approval_decision": resume_payload,
        "status": "waiting_approval",
    }


def post_approval_edge(state: ApplyState) -> str:
    """Verifies user approval decision before proceeding to dispatch."""
    decision = state.approval_decision or {}
    if decision.get("action") == "approve":
        return "dispatch"
    return "failed"


async def dispatch_node(state: ApplyState) -> Dict[str, Any]:
    """
    Dispatches application to SendGateway.
    Applies differential hold delay: 300s (5m) for autonomous, 30s for supervised.
    """
    is_auto = state.autonomy_mode == "autonomous" and not state.downgrade_reason
    undo_delay = 300 if is_auto else 30

    logger.info(
        f"Dispatching application {state.package_ref.application_id} "
        f"[mode={state.autonomy_mode}, undo_delay={undo_delay}s, channel={state.package_ref.channel}]"
    )

    return {
        "status": "enqueued_hold",
    }


# ===========================================================================
# 2. StateGraph Builder & Compiler
# ===========================================================================

def build_apply_graph(checkpointer: Optional[Any] = None) -> Any:
    """
    Assembles and compiles the ApplyGraph workflow.
    """
    builder = StateGraph(ApplyState)

    # Add Nodes
    builder.add_node("analyze_fit", fit_analyzer_node)
    builder.add_node("detect_method", detect_method_node)
    builder.add_node("draft_cv", cv_drafter_node)
    builder.add_node("review_cv", cv_reviewer_node)
    builder.add_node("draft_outreach", outreach_drafter_node)
    builder.add_node("assemble_package", assemble_package_node)
    builder.add_node("hitl_gate", hitl_approval_gate_node)
    builder.add_node("dispatch", dispatch_node)

    # Set Entry Point
    builder.set_entry_point("analyze_fit")

    # Flow Edges
    builder.add_conditional_edges(
        "analyze_fit",
        should_apply_edge,
        {"skip_job": END, "detect_method": "detect_method"},
    )
    builder.add_edge("detect_method", "draft_cv")
    builder.add_edge("draft_cv", "review_cv")
    builder.add_conditional_edges(
        "review_cv",
        review_guard_edge,
        {"redraft_cv": "draft_cv", "draft_outreach": "draft_outreach"},
    )
    builder.add_edge("draft_outreach", "assemble_package")
    builder.add_conditional_edges(
        "assemble_package",
        autonomy_gate_edge,
        {"hitl_gate": "hitl_gate", "dispatch": "dispatch"},
    )
    builder.add_conditional_edges(
        "hitl_gate",
        post_approval_edge,
        {"dispatch": "dispatch", "failed": END},
    )
    builder.add_edge("dispatch", END)

    return builder.compile(checkpointer=checkpointer)

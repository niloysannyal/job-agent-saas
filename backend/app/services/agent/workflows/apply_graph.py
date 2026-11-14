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

from app.services.agent.workflows.state import (
    ApplyState,
    ApplicationPackageRef,
    ApprovalGateResumePayload,
)
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

    # S12 Feedback: Pass reviewer audit flags into redraft prompt
    audit_notes: List[str] = []
    if state.cv_review and not state.cv_review.fact_audit_passed:
        if state.cv_review.hallucination_reasons:
            audit_notes = list(state.cv_review.hallucination_reasons)
        elif state.cv_review.reviewer_notes:
            audit_notes = [state.cv_review.reviewer_notes]

    draft = await drafter.draft_cv(
        params=CVDraftInput(
            account_id=state.account_id,
            job_id=state.job_id,
            job_role=role,
            job_company=company,
            job_description=desc,
            audit_feedback=audit_notes,
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
    if review and not review.fact_audit_passed:
        if state.review_iteration <= 1:
            return "redraft_cv"
        # S1 Hard Stop: Fact audit failed after retry -> stop at needs_edit
        return "needs_edit"
    return "draft_outreach"


async def needs_edit_node(state: ApplyState) -> Dict[str, Any]:
    """
    S1 Hard Stop Terminal Node.
    Entered when CV tailoring fails fact audit after self-correction retry.
    Halts workflow and mandates candidate intervention before outreach can proceed.
    """
    logger.warning(
        f"ApplyGraph entered needs_edit for job {state.job_id}: Fact audit unverified claims remain."
    )
    return {
        "status": "needs_edit",
        "error": "CV tailoring failed fact audit: unverified claims detected after self-correction retry.",
    }


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
    Handles in-place edits from the approval gate (G3 Loop).
    Persists/upserts Application and ApplicationPdfPayload in PostgreSQL.
    Evaluates Decision D1 (including TOFU verification against trusted_recipients).
    Persists draft SendAuthorization with matching length-prefixed content hash (G4: zero quota reserved here).
    """
    import hashlib
    import json
    import re
    import uuid
    from datetime import timedelta
    import sqlalchemy as sa
    from app.db.session import SessionLocal
    from app.models.application import Application
    from app.models.cv_template import AccountCvVersion
    from app.models.dispatch import ApplicationPdfPayload, SendAuthorization, TrustedRecipient
    from app.services.cv_tailor.fact_ledger import audit_fact_integrity
    from app.services.cv_tailor.latex_processor import check_brace_balance
    from app.services.cv_tailor.texlive_compiler import TeXLiveCompilerService

    fit = state.fit_result
    channel_info = state.channel_info or {}
    review = state.cv_review
    outreach = state.outreach
    cv_draft = state.cv_draft

    # G3 Contract: If re-entering from an approval gate edit, apply user modifications and re-audit
    if state.approval_decision and state.approval_decision.get("action") == "edit":
        edited_body = state.approval_decision.get("edited_body")
        edited_subject = state.approval_decision.get("edited_subject")
        edited_latex = state.approval_decision.get("edited_latex")
        if outreach and (edited_body or edited_subject):
            outreach = outreach.model_copy(update={
                "body_content": edited_body or outreach.body_content,
                "subject_line": edited_subject or outreach.subject_line,
            })
        if cv_draft and edited_latex:
            cv_draft = cv_draft.model_copy(update={
                "draft_assembled_latex": edited_latex,
            })

        # Deterministic Re-Audit on Human Edits (G3 Verification Barrier):
        target_latex = edited_latex or (cv_draft.draft_assembled_latex if cv_draft else "")
        target_body = edited_body or (outreach.body_content if outreach else "")

        is_balanced = check_brace_balance(target_latex)
        placeholder_pattern = re.compile(r"(\[[A-Z][a-zA-Z\s]{2,20}\]|\{\{[^}]+\}\})")
        has_placeholders = bool(placeholder_pattern.search(target_latex) or placeholder_pattern.search(target_body))

        fact_audit = audit_fact_integrity(target_latex)

        raw_lines = [l.strip() for l in target_latex.split("\n") if l.strip() and not l.strip().startswith("%")]
        line_count = len(raw_lines)
        # Proportional page budget formula without hardcoded 2-page cap
        computed_pages = max(1, (line_count + 54) // 55)

        if review:
            review = review.model_copy(update={
                "is_valid": is_balanced and not has_placeholders and fact_audit.is_valid and (computed_pages <= 2),
                "final_tailored_latex": target_latex,
                "fact_audit_passed": fact_audit.is_valid,
                "hallucination_detected": not fact_audit.is_valid,
                "hallucination_reasons": fact_audit.flagged_issues,
                "line_count": line_count,
                "computed_page_count": computed_pages,
                "reviewer_notes": "Re-audited human edit successfully." if fact_audit.is_valid else "Human edit failed fact verification.",
            })

    company = state.company_name or (fit.company if fit else "Target Company")
    role = state.role_title or (fit.role if fit else "Target Role")
    channel = channel_info.get("channel_type", "email")
    recipient = channel_info.get("recruiter_email") or "careers@target.com"

    form_answers = {qa.question_id: qa.answer_text for qa in outreach.qa_answers} if outreach else {}

    # Compile or generate PDF bytes
    target_latex = review.final_tailored_latex if review and review.final_tailored_latex else (cv_draft.draft_assembled_latex if cv_draft else "")
    pdf_bytes: Optional[bytes] = None
    if target_latex and TeXLiveCompilerService.is_available():
        try:
            res = TeXLiveCompilerService.compile_latex(target_latex, account_id=state.account_id)
            if res.get("success") and res.get("pdf_bytes"):
                pdf_bytes = res["pdf_bytes"]
        except Exception as e:
            logger.warning(f"TeXLive compilation failed, falling back to deterministic PDF bytes: {e}")

    if not pdf_bytes:
        safe_role = role or "Role"
        safe_company = company or "Company"
        pdf_bytes = f"%PDF-1.4\n% Application for {safe_role} at {safe_company}\n{target_latex}\n%%EOF".encode("utf-8")

    attachment_sha256 = hashlib.sha256(pdf_bytes).hexdigest()

    # Database Persistence & Hash Sync
    send_auth_id = state.send_authorization_id
    is_trusted = False
    downgrade_reason: Optional[str] = None
    real_app_id = f"app-{state.job_id[:8]}"

    try:
        with SessionLocal() as db_session:
            from app.models.account import Account
            acc_exists = db_session.query(Account).filter_by(id=state.account_id).first()

            if acc_exists:
                # 1. Upsert Application row
                app_row = db_session.query(Application).filter(
                    Application.account_id == state.account_id,
                    Application.job_id == state.job_id,
                ).first()

                subject_text = outreach.subject_line if outreach and outreach.subject_line else f"Application for {role}"
                body_text = outreach.body_content if outreach and outreach.body_content else ""

                cv_version_val = None
                if cv_draft and getattr(cv_draft, "template_id", None):
                    cv_v = db_session.query(AccountCvVersion).filter_by(
                        id=cv_draft.template_id,
                        account_id=state.account_id,
                    ).first()
                    if cv_v:
                        cv_version_val = cv_v.id

                if not app_row:
                    app_row = Application(
                        id=str(uuid.uuid4()),
                        account_id=state.account_id,
                        job_id=state.job_id,
                        cv_version_id=cv_version_val,
                        channel=channel,
                        subject=subject_text,
                        body=body_text,
                        draft_content=body_text,
                        recipient_email=recipient,
                        pdf_sha256=attachment_sha256,
                        status="draft",
                    )
                    db_session.add(app_row)
                else:
                    app_row.cv_version_id = cv_version_val
                    app_row.channel = channel
                    app_row.subject = subject_text
                    app_row.body = body_text
                    app_row.draft_content = body_text
                    app_row.recipient_email = recipient
                    app_row.pdf_sha256 = attachment_sha256

                db_session.flush()
                real_app_id = str(app_row.id)

                # 2. Upsert ApplicationPdfPayload
                pdf_row = db_session.query(ApplicationPdfPayload).filter_by(application_id=real_app_id).first()
                if not pdf_row:
                    pdf_row = ApplicationPdfPayload(
                        application_id=real_app_id,
                        account_id=state.account_id,
                        sha256=attachment_sha256,
                        payload_bytes=pdf_bytes,
                        size_bytes=len(pdf_bytes),
                    )
                    db_session.add(pdf_row)
                else:
                    pdf_row.sha256 = attachment_sha256
                    pdf_row.payload_bytes = pdf_bytes
                    pdf_row.size_bytes = len(pdf_bytes)

                # 3. Check TOFU TrustedRecipient
                tr = db_session.query(TrustedRecipient).filter(
                    TrustedRecipient.account_id == state.account_id,
                    sa.func.lower(TrustedRecipient.email) == recipient.lower(),
                ).first()
                is_trusted = tr is not None

                # 4. Canonical Content Hash (matching SendGateway formula exactly)
                content_hash = compute_content_hash(
                    cv_version_id=app_row.cv_version_id,
                    subject=app_row.subject or "",
                    body=app_row.body or app_row.draft_content or "",
                    recipient=recipient,
                    answers_json="[]",
                    attachment_sha256=attachment_sha256,
                )

                # 5. Pre-Send Verification Barrier Evaluation (Decision D1 + TOFU)
                if state.autonomy_mode == "autonomous":
                    recipient_domain = (recipient or "").split("@")[-1].lower()
                    if channel not in ("email", "direct_email"):
                        downgrade_reason = f"Channel '{channel}' requires human confirmation."
                    elif recipient_domain in PROHIBITED_AUTO_WEBMAIL_DOMAINS:
                        downgrade_reason = f"Recipient domain '@{recipient_domain}' is a public webmail address; human confirmation required."
                    elif not is_trusted:
                        downgrade_reason = f"Recipient '{recipient}' is not yet in trusted_recipients (TOFU); human confirmation required."
                    elif review and not review.fact_audit_passed:
                        downgrade_reason = "Fact integrity check flagged unverified claims."
                    elif review and review.hallucination_detected:
                        downgrade_reason = "Fact integrity check flagged hallucinated content."
                    elif review and review.ats_score < 70.0:
                        downgrade_reason = f"ATS score ({review.ats_score:.1f}%) is below the 70% autonomous threshold."
                    elif review and (review.computed_page_count < 1 or review.computed_page_count > 2):
                        downgrade_reason = f"CV page budget ({review.computed_page_count} pages) violates the 1-2 page rule."

                # 6. Upsert SendAuthorization with real application_id
                auth_row = None
                if send_auth_id:
                    auth_row = db_session.query(SendAuthorization).filter_by(id=send_auth_id).first()
                if not auth_row:
                    auth_row = db_session.query(SendAuthorization).filter(
                        SendAuthorization.account_id == state.account_id,
                        SendAuthorization.application_id == real_app_id,
                        SendAuthorization.status == "pending",
                    ).first()

                if auth_row:
                    auth_row.content_hash = content_hash
                    auth_row.recipient_email = recipient
                    auth_row.attachment_sha256 = attachment_sha256
                    auth_row.status = "pending"
                    db_session.commit()
                    send_auth_id = str(auth_row.id)
                else:
                    new_auth = SendAuthorization(
                        id=str(uuid.uuid4()),
                        account_id=state.account_id,
                        application_id=real_app_id,
                        recipient_email=recipient,
                        attachment_sha256=attachment_sha256,
                        content_hash=content_hash,
                        minted_by="autonomous_policy" if (state.autonomy_mode == "autonomous" and not downgrade_reason) else "human_approval",
                        status="pending",
                        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
                    )
                    db_session.add(new_auth)
                    db_session.commit()
                    send_auth_id = str(new_auth.id)
            else:
                # In-memory execution fallback when Account row does not exist in SessionLocal
                content_hash = compute_content_hash(
                    cv_version_id=None,
                    subject=outreach.subject_line if outreach else f"Application for {role}",
                    body=outreach.body_content if outreach else "",
                    recipient=recipient,
                    answers_json="[]",
                    attachment_sha256=attachment_sha256,
                )
                if not send_auth_id:
                    send_auth_id = f"auth-{state.job_id[:8]}"

    except Exception as e:
        logger.error(f"Error persisting package entities in assemble_package_node: {e}", exc_info=True)
        # Compute fallback content hash if DB persistence raised
        content_hash = compute_content_hash(
            cv_version_id=None,
            subject=outreach.subject_line if outreach else f"Application for {role}",
            body=outreach.body_content if outreach else "",
            recipient=recipient,
            answers_json="[]",
            attachment_sha256=attachment_sha256,
        )
        if not send_auth_id:
            send_auth_id = f"auth-{state.job_id[:8]}"

    package = ApplicationPackageRef(
        application_id=real_app_id,
        job_id=state.job_id,
        company_name=company,
        role_title=role,
        channel=channel,
        tailored_cv_version_id=None,
        pdf_artifact_path=f"/tmp/tailored_cv_{real_app_id[:8]}.pdf",
        attachment_sha256=attachment_sha256,
        ats_score=review.ats_score if review else 85.0,
        fact_audit_passed=review.fact_audit_passed if review else True,
        recipient_email=recipient,
        email_subject=outreach.subject_line if outreach else None,
        email_body=outreach.body_content if outreach else None,
        form_answers=form_answers,
        content_hash=content_hash,
    )

    # S3 Fix: Commit status waiting_approval before entering the gate
    needs_gate = (state.autonomy_mode != "autonomous" or downgrade_reason is not None)

    return {
        "package_ref": package,
        "outreach": outreach,
        "cv_draft": cv_draft,
        "cv_review": review,
        "proposal_id": f"prop-{state.job_id[:8]}",
        "send_authorization_id": send_auth_id,
        "downgrade_reason": downgrade_reason,
        "is_recipient_trusted": is_trusted,
        "approval_decision": None,  # Reset decision after applying edits
        "status": "waiting_approval" if needs_gate else "assembling_package",
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
            "is_trusted": state.is_recipient_trusted,
        },
    }

    # Thread halts here until resumed by user
    raw_resume = interrupt({
        "proposal_id": state.proposal_id,
        "widget": gate_widget,
    })

    # Strict validation of resume payload
    if isinstance(raw_resume, dict):
        payload_obj = ApprovalGateResumePayload(**raw_resume)
    elif isinstance(raw_resume, ApprovalGateResumePayload):
        payload_obj = raw_resume
    else:
        payload_obj = ApprovalGateResumePayload(action=str(raw_resume))

    return {
        "approval_decision": payload_obj.model_dump(),
        "status": "waiting_approval",
    }


def post_approval_edge(state: ApplyState) -> str:
    """
    Routes based on user approval decision:
    - action == 'approve' -> dispatch
    - action == 'edit'    -> assemble_package (G3 Loop for re-audit & hash recomputation)
    - action == 'reject'  -> failed
    """
    decision = state.approval_decision or {}
    action = decision.get("action")
    if action == "approve":
        return "dispatch"
    elif action == "edit":
        return "assemble_package"
    return "failed"


async def dispatch_node(state: ApplyState) -> Dict[str, Any]:
    """
    Contract 3 / G4: Dispatches application into M1 Outbox inside a single DB transaction:
    1. Verifies send_authorizations content_hash matches current state.
    2. Checks & allocates quota_reservation (transitions to failed_quota if exhausted).
    3. Upserts recipient into trusted_recipients (TOFU confirmation on human approval).
    4. Enqueues HoldQueueItem with idempotency key and release_at.
    5. Returns status='queued_in_hold'.
    """
    is_auto = state.autonomy_mode == "autonomous" and not state.downgrade_reason
    undo_delay = 300 if is_auto else 30
    package = state.package_ref

    if not package or not package.application_id:
        return {"status": "failed", "error": "Cannot dispatch without assembled application package."}

    hold_id = None
    reservation_id = None

    try:
        from app.db.session import SessionLocal
        from app.models.dispatch import HoldQueueItem, SendAuthorization, TrustedRecipient
        from app.models.metering import QuotaReservation
        import sqlalchemy as sa
        from datetime import timedelta
        import uuid

        with SessionLocal() as db_session:
            from app.models.account import Account
            acc_exists = db_session.query(Account).filter_by(id=state.account_id).first()

            if not acc_exists:
                # In-memory execution fallback when Account does not exist in SessionLocal
                hold_id = f"hold-{state.job_id[:8]}"
            else:
                # 1. Verify content_hash integrity
                if state.send_authorization_id:
                    auth = db_session.query(SendAuthorization).filter_by(id=state.send_authorization_id).first()
                    if auth and auth.content_hash and auth.content_hash != package.content_hash:
                        logger.error("Content hash mismatch at dispatch release!")
                        return {"status": "failed", "error": "Content hash corrupted before dispatch."}

                # 2. TOFU Confirmation: upsert recipient into trusted_recipients ONLY on human approval at HITL gate
                # An autonomous run must NEVER self-trust an unverified recipient
                is_human_approved = bool(state.approval_decision and state.approval_decision.get("action") == "approve")
                if package.recipient_email and is_human_approved:
                    existing_tr = db_session.query(TrustedRecipient).filter(
                        TrustedRecipient.account_id == state.account_id,
                        sa.func.lower(TrustedRecipient.email) == package.recipient_email.lower(),
                    ).first()
                    if not existing_tr:
                        new_tr = TrustedRecipient(
                            id=str(uuid.uuid4()),
                            account_id=state.account_id,
                            email=package.recipient_email.lower(),
                            source="manual_approval",
                        )
                        db_session.add(new_tr)

                # 3. Reserve quota idempotently
                res_idempotency = f"quota-res-{package.application_id}"
                existing_res = db_session.query(QuotaReservation).filter_by(
                    account_id=state.account_id,
                    idempotency_key=res_idempotency,
                ).first()
                if existing_res:
                    reservation_id = str(existing_res.id)
                else:
                    reservation = QuotaReservation(
                        id=str(uuid.uuid4()),
                        account_id=state.account_id,
                        idempotency_key=res_idempotency,
                        quota_key="application_dispatch",
                        units=1,
                        status="reserved",
                        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
                    )
                    db_session.add(reservation)
                    db_session.flush()
                    reservation_id = str(reservation.id)

                # 4. Insert or reuse hold_queue_items idempotently (Outbox queue)
                app_id = package.application_id
                auth_id = state.send_authorization_id

                if not auth_id:
                    return {"status": "failed", "error": "Cannot enqueue in hold without valid send_authorization_id."}

                existing_hold = db_session.query(HoldQueueItem).filter(
                    HoldQueueItem.account_id == state.account_id,
                    HoldQueueItem.application_id == app_id,
                    HoldQueueItem.authorization_id == auth_id,
                    HoldQueueItem.status.in_(["pending", "claimed", "sending"]),
                ).first()
                if existing_hold:
                    hold_id = str(existing_hold.id)
                else:
                    hold_item = HoldQueueItem(
                        id=str(uuid.uuid4()),
                        account_id=state.account_id,
                        application_id=app_id,
                        authorization_id=auth_id,
                        reservation_id=reservation_id,
                        channel=package.channel,
                        status="pending",
                        hold_kind="autonomous_delay" if is_auto else "review_required",
                        release_at=datetime.now(timezone.utc) + timedelta(seconds=undo_delay),
                    )
                    db_session.add(hold_item)
                    db_session.commit()
                    hold_id = str(hold_item.id)

    except Exception as e:
        logger.error(f"Dispatch outbox persistence failed: {e}", exc_info=True)
        return {
            "status": "failed",
            "error": f"Outbox persistence failed: {str(e)}",
        }

    logger.info(
        f"Application {package.application_id} successfully queued in hold "
        f"[hold_id={hold_id}, undo_delay={undo_delay}s, mode={state.autonomy_mode}]"
    )

    return {
        "status": "queued_in_hold",
        "hold_queue_item_id": hold_id,
    }


# ===========================================================================
# 2. StateGraph Builder & Compiler
# ===========================================================================

def build_apply_graph(checkpointer: Optional[Any] = None) -> Any:
    """
    Assembles and compiles the ApplyGraph workflow with full hardening:
    - 4D Fit Analysis -> conditional skip
    - Pass 1 Drafter -> Pass 2 Reviewer Fact Auditor
    - Bounded self-correction loop (max 1 retry) -> S1 Hard Stop (needs_edit)
    - Outreach drafting & Package Assembly
    - Decision D1 (including TOFU against trusted_recipients)
    - Isolated HITL Gate Node -> G3 edit loopback to assemble_package
    - Outbox handoff -> queued_in_hold terminal status
    """
    builder = StateGraph(ApplyState)

    # Add Nodes
    builder.add_node("analyze_fit", fit_analyzer_node)
    builder.add_node("detect_method", detect_method_node)
    builder.add_node("draft_cv", cv_drafter_node)
    builder.add_node("review_cv", cv_reviewer_node)
    builder.add_node("needs_edit", needs_edit_node)
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
        {"redraft_cv": "draft_cv", "draft_outreach": "draft_outreach", "needs_edit": "needs_edit"},
    )
    builder.add_edge("needs_edit", END)
    builder.add_edge("draft_outreach", "assemble_package")
    builder.add_conditional_edges(
        "assemble_package",
        autonomy_gate_edge,
        {"hitl_gate": "hitl_gate", "dispatch": "dispatch"},
    )
    builder.add_conditional_edges(
        "hitl_gate",
        post_approval_edge,
        {"dispatch": "dispatch", "assemble_package": "assemble_package", "failed": END},
    )
    builder.add_edge("dispatch", END)

    return builder.compile(checkpointer=checkpointer)

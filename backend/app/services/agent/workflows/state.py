"""
backend/app/services/agent/workflows/state.py

Decoupled State Schemas for LangGraph Orchestration.
Defines `ApplyState` for isolated per-job application executions and `CopilotState` for conversational turns.
"""

from typing import Annotated, Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

from app.services.matching.fit_analyzer import FitAnalyzerOutput
from app.services.cv_tailor.drafter import CVDraftOutput
from app.services.cv_tailor.reviewer import CVReviewOutput
from app.services.outreach.drafter_service import OutreachDrafterOutput


class ApprovalGateResumePayload(BaseModel):
    action: Literal["approve", "reject", "edit"]
    edited_body: Optional[str] = None
    edited_subject: Optional[str] = None
    edited_latex: Optional[str] = None
    notes: Optional[str] = None


class ApplicationPackageRef(BaseModel):
    application_id: str
    job_id: str
    company_name: str
    role_title: str
    channel: Literal["email", "direct_email", "google_form", "typeform", "ats_portal", "direct_message", "generic_web"]
    tailored_cv_version_id: Optional[str] = None
    pdf_artifact_path: Optional[str] = None
    attachment_sha256: Optional[str] = None
    ats_score: float = 0.0
    fact_audit_passed: bool = True
    recipient_email: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    form_answers: Dict[str, str] = Field(default_factory=dict)
    content_hash: Optional[str] = None


class ApplyState(BaseModel):
    account_id: str
    job_id: str
    user_email: str
    autonomy_mode: Literal["supervised", "autonomous"] = "supervised"
    
    # Target Job Context (optional override or preloaded from DB)
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    job_description: Optional[str] = None
    apply_url: Optional[str] = None
    
    # Workflow Pipeline Artifacts
    fit_result: Optional[FitAnalyzerOutput] = None
    channel_info: Optional[Dict[str, Any]] = None
    cv_draft: Optional[CVDraftOutput] = None
    cv_review: Optional[CVReviewOutput] = None
    outreach: Optional[OutreachDrafterOutput] = None
    package_ref: Optional[ApplicationPackageRef] = None
    
    # Autonomy & Decision Invariants
    command_id: Optional[str] = None
    authorization_id: Optional[str] = None
    proposal_id: Optional[str] = None
    review_iteration: int = 0  # Bounded self-correction loop: max 1 retry
    audit_flags: List[str] = Field(default_factory=list)
    downgrade_reason: Optional[str] = None
    approval_decision: Optional[Dict[str, Any]] = None
    send_authorization_id: Optional[str] = None
    hold_queue_item_id: Optional[str] = None
    is_recipient_trusted: bool = False
    
    # Status
    status: Literal[
        "idle",
        "analyzing_fit",
        "detecting_method",
        "drafting_cv",
        "reviewing_cv",
        "needs_edit",
        "drafting_outreach",
        "assembling_package",
        "waiting_approval",
        "queued_in_hold",
        "failed_quota",
        "dispatched",
        "skipped",
        "failed",
    ] = "idle"
    error: Optional[str] = None


class CopilotState(BaseModel):
    account_id: str
    user_email: str
    messages: Annotated[List[Dict[str, Any]], add_messages] = Field(default_factory=list)
    active_job_id: Optional[str] = None
    spawned_apply_thread_ids: List[str] = Field(default_factory=list)

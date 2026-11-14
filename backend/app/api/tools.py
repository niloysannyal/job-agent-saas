"""
backend/app/api/tools.py

Decoupled Modular Tools API.
Exposes standalone endpoints for each phase of the job application lifecycle:
1. POST /api/v1/tools/analyze-fit: 4D Diagnostic Career Alignment (Skills, Experience, Trajectory, Seniority)
2. POST /api/v1/tools/detect-method: Application Channel Discovery & Question Extraction
3. POST /api/v1/tools/draft-cv: Senior Recruiter AI Pass 1 LaTeX Tailoring & Page Budgeting
4. POST /api/v1/tools/review-cv: Senior Recruiter AI Pass 2 Fact Integrity & ATS Scoring
5. POST /api/v1/tools/draft-outreach: Multi-Channel Outreach & Form Q&A Generator
6. POST /api/v1/tools/apply-workflow/start: LangGraph ApplyGraph SSE Stream
7. POST /api/v1/tools/apply-workflow/resume: LangGraph ApplyGraph Resume Approval Stream
"""

import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.auth import get_current_account, resolve_tenant_id
from app.db.session import get_db
from app.models.account import Account
from app.models.job import Job
from app.models.profile import UserProfile, ProfileSkill, WorkExperience

# Core Decoupled Services
from app.services.matching.fit_analyzer import (
    FitAnalyzerService,
    FitAnalyzerOutput,
)
from app.services.form_detective.detective import (
    FormDetectiveService,
    FormInspectionResult,
)
from app.services.cv_tailor.drafter import (
    CVDrafterService,
    CVDraftInput,
    CVDraftOutput,
    CandidateCareerContext,
)
from app.services.cv_tailor.reviewer import (
    CVReviewerService,
    CVReviewInput,
    CVReviewOutput,
)
from app.services.outreach.drafter_service import (
    OutreachDrafterService,
    OutreachDrafterInput,
    OutreachDrafterOutput,
    OutreachChannelType,
)
from app.services.agent.workflows.apply_graph import build_apply_graph
from app.services.agent.workflows.sse_adapter import LangGraphSSEAdapter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tools", tags=["tools"])

# In-memory checkpointer registry for active workflow sessions (backed by DB checkpointer in production)
_ACTIVE_CHECKPOINTER = MemorySaver()


# ===========================================================================
# Request / Response Schemas
# ===========================================================================

class AnalyzeFitRequest(BaseModel):
    job_id: Optional[str] = None
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    posting_text: Optional[str] = None


class DetectMethodRequest(BaseModel):
    job_id: Optional[str] = None
    apply_url: Optional[str] = None
    posting_text: Optional[str] = None
    company_name: Optional[str] = None
    role_title: Optional[str] = None


class DraftCVRequest(BaseModel):
    job_id: Optional[str] = None
    job_role: str
    job_company: str
    job_description: str
    master_latex_override: Optional[str] = None


class ReviewCVRequest(BaseModel):
    draft_latex: str
    draft_summary_bullet: str
    draft_cover_letter: str
    job_role: str
    job_company: str
    job_description: str
    preamble: Optional[str] = None
    budgeted_latex_body: Optional[str] = None


class DraftOutreachRequest(BaseModel):
    job_id: Optional[str] = None
    company_name: str
    role_title: str
    job_description: str
    channel_type: OutreachChannelType = OutreachChannelType.EMAIL
    questions: Optional[List[Dict[str, Any]]] = None


class WorkflowStartRequest(BaseModel):
    job_id: str
    autonomy_mode: str = "supervised"  # "supervised" | "autonomous"
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    job_description: Optional[str] = None
    apply_url: Optional[str] = None


class WorkflowResumeRequest(BaseModel):
    thread_id: str
    action: str = "approve"  # "approve" | "reject" | "edit"
    edited_body: Optional[str] = None
    edited_subject: Optional[str] = None
    edited_latex: Optional[str] = None
    notes: Optional[str] = None


# ===========================================================================
# 1. Fit Analysis Tool
# ===========================================================================

@router.post("/analyze-fit", response_model=FitAnalyzerOutput)
async def analyze_fit_endpoint(
    payload: AnalyzeFitRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Evaluates 4-Dimension career alignment (Skills, Experience, Trajectory, Seniority).
    Pure diagnostic tool.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    service = FitAnalyzerService(db=db)

    return await service.analyze_fit(
        account_id=tenant_id,
        job_id=payload.job_id,
        posting_text=payload.posting_text,
        company_name=payload.company_name,
        role_title=payload.role_title,
    )


# ===========================================================================
# 2. Application Method Detection Tool
# ===========================================================================

@router.post("/detect-method")
def detect_method_endpoint(
    payload: DetectMethodRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Classifies application channel (Email, Google Form, ATS, DM) and extracts form questions.
    """
    apply_url = payload.apply_url
    posting_text = payload.posting_text
    company = payload.company_name or "Target Company"
    role = payload.role_title or "Target Role"

    if payload.job_id:
        job = db.query(Job).filter_by(id=payload.job_id).first()
        if job:
            company = job.company or company
            role = job.role or role
            posting_text = posting_text or job.description or ""
            apply_url = apply_url or job.apply_link

    inspection = FormDetectiveService.detect_channel(
        apply_url=apply_url,
        posting_text=posting_text,
        company_name=company,
        role_title=role,
    )

    return {
        "channel_type": inspection.channel_type.value,
        "platform_name": inspection.platform_name,
        "apply_url": inspection.apply_url,
        "recruiter_email": inspection.recruiter_email,
        "target_handle": inspection.target_handle,
        "action_summary": inspection.action_summary,
        "questions": [
            {
                "id": q.id,
                "prompt": q.prompt,
                "field_type": q.field_type,
                "char_limit": q.char_limit,
                "is_required": q.is_required,
                "suggested_focus": q.suggested_focus,
            }
            for q in inspection.questions
        ],
    }


# ===========================================================================
# 3. Senior Recruiter CV Tailoring Drafter (Pass 1)
# ===========================================================================

@router.post("/draft-cv", response_model=CVDraftOutput)
async def draft_cv_endpoint(
    payload: DraftCVRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Executes Pass 1 Senior Recruiter CV tailoring.
    Budgets LaTeX to strictly 1-2 pages without database mutation.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    profile = db.query(UserProfile).filter_by(account_id=tenant_id).first()
    candidate_name = profile.full_name if profile and profile.full_name else "Niloy Sannyal"
    headline = profile.headline if profile and profile.headline else "AI Systems Engineer"

    # Default master LaTeX if not overridden
    master_latex = payload.master_latex_override or (
        "\\documentclass[a4paper,11pt]{article}\n\\begin{document}\n"
        "\\section{SUMMARY}\n\\resumeItemListStart\n"
        "\\resumeItem{AI Engineer building production agentic AI systems.}\n"
        "\\resumeItemListEnd\n\\end{document}"
    )

    context = CandidateCareerContext(
        account_id=tenant_id,
        candidate_name=candidate_name,
        headline=headline,
        master_latex=master_latex,
        verified_facts_str="- 600+ salespersons (Betopia Sales Agent in Odoo CRM)\n- 10,000+ UFC fights, 80+ features",
    )

    drafter = CVDrafterService()
    return await drafter.draft_cv(
        params=CVDraftInput(
            account_id=tenant_id,
            job_id=payload.job_id,
            job_role=payload.job_role,
            job_company=payload.job_company,
            job_description=payload.job_description,
        ),
        career_context=context,
    )


# ===========================================================================
# 4. Senior Recruiter CV Reviewer & Fact Auditor (Pass 2)
# ===========================================================================

@router.post("/review-cv", response_model=CVReviewOutput)
async def review_cv_endpoint(
    payload: ReviewCVRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Executes Pass 2 Senior Recruiter CV review.
    Audits for unverified claims, verifies ATS text layer, and enforces brace balance.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    reviewer = CVReviewerService()

    context = CandidateCareerContext(
        account_id=tenant_id,
        candidate_name="Niloy Sannyal",
        headline="AI Systems Engineer",
        master_latex="",
        verified_facts_str="- 600+ salespersons (Betopia Sales Agent in Odoo CRM)\n- 10,000+ UFC fights, 80+ features",
    )

    mock_draft = CVDraftOutput(
        draft_summary_bullet=payload.draft_summary_bullet,
        draft_cover_letter=payload.draft_cover_letter,
        raw_gaps=[],
        preamble=payload.preamble or "\\documentclass[a4paper,11pt]{article}",
        budgeted_latex_body=payload.budgeted_latex_body or payload.draft_latex,
        draft_assembled_latex=payload.draft_latex,
        drafter_raw_response="",
    )

    return await reviewer.review_cv(
        params=CVReviewInput(
            draft_output=mock_draft,
            job_role=payload.job_role,
            job_company=payload.job_company,
            job_description=payload.job_description,
            career_context=context,
        )
    )


# ===========================================================================
# 5. Multi-Channel Outreach Drafter Tool
# ===========================================================================

@router.post("/draft-outreach", response_model=OutreachDrafterOutput)
async def draft_outreach_endpoint(
    payload: DraftOutreachRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Synthesizes tailored outreach copy (Email, Form Q&A answers, or Recruiter DM).
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    service = OutreachDrafterService()

    return await service.draft_outreach(
        params=OutreachDrafterInput(
            account_id=tenant_id,
            job_id=payload.job_id,
            company_name=payload.company_name,
            role_title=payload.role_title,
            job_description=payload.job_description,
            channel_type=payload.channel_type,
            questions=payload.questions,
        ),
        candidate_name="Niloy Sannyal",
    )


# ===========================================================================
# 6. Autonomous LangGraph Workflow Streaming (SSE)
# ===========================================================================

@router.post("/apply-workflow/start")
async def start_apply_workflow(
    payload: WorkflowStartRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Initiates the full LangGraph ApplyGraph autonomous/supervised pipeline.
    Streams real-time SSE frames.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    import uuid
    thread_id = f"apply-{tenant_id}-{uuid.uuid4().hex[:12]}"

    # Fetch job context if available
    job = db.query(Job).filter_by(id=payload.job_id).first()
    company = payload.company_name or (job.company if job else "Target Company")
    role = payload.role_title or (job.role if job else "Target Role")
    description = payload.job_description or (job.description if job else "")
    apply_url = payload.apply_url or (job.apply_link if job else None)

    graph = build_apply_graph(checkpointer=_ACTIVE_CHECKPOINTER)
    thread_config = {"configurable": {"thread_id": thread_id, "account_id": tenant_id}}

    initial_state = {
        "account_id": tenant_id,
        "job_id": payload.job_id,
        "user_email": current_account.email,
        "autonomy_mode": payload.autonomy_mode,
        "company_name": company,
        "role_title": role,
        "job_description": description,
        "apply_url": apply_url,
    }

    import asyncio
    queue = asyncio.Queue()

    async def run_apply_background():
        try:
            stream = graph.astream(initial_state, config=thread_config, stream_mode="updates")
            async for sse_frame in LangGraphSSEAdapter.stream_apply_graph(stream, conversation_id=thread_id):
                await queue.put(sse_frame)
        except Exception as e:
            logger.error(f"Error executing ApplyGraph workflow: {e}")
            import json
            await queue.put(f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n")
        finally:
            await queue.put(None)

    # Decouple execution from client disconnect (Contract 4)
    asyncio.create_task(run_apply_background())

    async def event_generator():
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/apply-workflow/resume")
async def resume_apply_workflow(
    payload: WorkflowResumeRequest,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
):
    """
    Resumes an interrupted ApplyGraph thread at the SendApprovalGate.
    Supports action: 'approve' (dispatch), 'edit' (G3 loopback to re-audit), or 'reject'.
    Executes in decoupled background task so client disconnect cannot corrupt state.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    graph = build_apply_graph(checkpointer=_ACTIVE_CHECKPOINTER)
    thread_config = {"configurable": {"thread_id": payload.thread_id, "account_id": tenant_id}}

    resume_payload_dict = {
        "action": payload.action,
        "edited_body": payload.edited_body,
        "edited_subject": payload.edited_subject,
        "edited_latex": payload.edited_latex,
        "notes": payload.notes,
    }
    resume_command = Command(resume=resume_payload_dict)

    import asyncio
    queue = asyncio.Queue()

    async def run_resume_background():
        try:
            stream = graph.astream(resume_command, config=thread_config, stream_mode="updates")
            async for sse_frame in LangGraphSSEAdapter.stream_apply_graph(stream, conversation_id=payload.thread_id):
                await queue.put(sse_frame)
        except Exception as e:
            logger.error(f"Error resuming ApplyGraph workflow: {e}")
            import json
            await queue.put(f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n")
        finally:
            await queue.put(None)

    asyncio.create_task(run_resume_background())

    async def event_generator():
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

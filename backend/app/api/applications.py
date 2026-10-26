from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.account import Account
from app.models.application import Application, ApplicationRead
from app.models.cv_template import AccountCvVersion, AccountCvVersionRead
from app.models.job import Job
from app.services.cv_tailor.tailor_service import CVTailorService
from app.services.llm.service import LLMService

router = APIRouter(prefix="/applications", tags=["applications"])


def get_llm_service(db: Session = Depends(get_db)) -> LLMService:
    """Dependency provider for LLMService."""
    return LLMService(db_session=db)


class TailorRequest(BaseModel):
    account_id: str = Field(..., description="Multi-tenant account identifier")
    job_id: str = Field(..., description="Job posting ID to tailor CV and outreach for")
    channel: str = Field(default="email", description="Channel: email | form | dm | portal")


class TailorResponse(BaseModel):
    cv_version: AccountCvVersionRead
    application: ApplicationRead
    ats_score: float
    fact_audit_passed: bool
    gaps_detected: List[str]
    notes: Optional[str] = None


class StatusSummary(BaseModel):
    total: int
    draft: int
    sent: int
    follow_ups_due: int
    responded: int
    interview: int
    offer: int
    rejected: int


class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="New status: draft | sent | responded | interview | offer | rejected")
    notes: Optional[str] = None


class FollowUpDraftResponse(BaseModel):
    application_id: str
    company: str
    role: str
    follow_up_number: int
    draft_content: str
    cap_reached: bool


@router.post("/tailor", response_model=TailorResponse, status_code=status.HTTP_201_CREATED)
async def tailor_application(
    request: TailorRequest,
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Module 2 (Apply): Tailor LaTeX CV and draft outreach (email/form/DM).
    Executes Drafter + Reviewer two-pass generation against verified fact ledger.
    Strict human-in-the-loop: sets status='draft' and sent_at=None.
    """
    account = db.query(Account).filter_by(id=request.account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{request.account_id}' not found.",
        )

    job = db.query(Job).filter_by(id=request.job_id, account_id=request.account_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{request.job_id}' not found for account '{request.account_id}'.",
        )

    tailor_service = CVTailorService(llm_service=llm_service, db_session=db)
    result = await tailor_service.tailor_for_job(
        account_id=request.account_id,
        job=job,
        channel=request.channel,
    )

    return TailorResponse(
        cv_version=AccountCvVersionRead.model_validate(result.cv_version),
        application=ApplicationRead.model_validate(result.application),
        ats_score=result.ats_score,
        fact_audit_passed=result.fact_audit_passed,
        gaps_detected=result.gaps_detected,
        notes=result.drafter_notes,
    )


@router.get("/monitor/summary", response_model=StatusSummary)
def get_monitor_summary(
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
):
    """
    Module 3 (Monitor): Aggregated status summary view across all pipeline stages.
    (Total / Sent / Follow-ups Due / Responded / Interview / Offer / Rejected)
    """
    now = datetime.now(timezone.utc)
    apps = db.query(Application).filter(Application.account_id == account_id).all()

    total = len(apps)
    draft = sum(1 for a in apps if a.status == "draft")
    sent = sum(1 for a in apps if a.status == "sent")
    responded = sum(1 for a in apps if a.status == "responded")
    interview = sum(1 for a in apps if a.status in ["interview", "interviewing"])
    offer = sum(1 for a in apps if a.status in ["offer", "offered"])
    rejected = sum(1 for a in apps if a.status in ["rejected", "declined"])

    def is_due(due_dt):
        if not due_dt:
            return False
        if due_dt.tzinfo is None:
            return due_dt <= now.replace(tzinfo=None)
        return due_dt <= now

    # Follow-ups due: sent_at is set, status is 'sent', follow_up_due <= now, and cap (2) not exceeded
    follow_ups_due = sum(
        1 for a in apps
        if a.status == "sent" and a.sent_at is not None and is_due(a.follow_up_due) and a.follow_up_count < 2
    )

    return StatusSummary(
        total=total,
        draft=draft,
        sent=sent,
        follow_ups_due=follow_ups_due,
        responded=responded,
        interview=interview,
        offer=offer,
        rejected=rejected,
    )


@router.get("", response_model=List[ApplicationRead])
def list_applications(
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    status_filter: Optional[str] = Query(None, description="Optional status filter: draft, sent, interview, etc."),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    List applications for a tenant account.
    """
    query = (
        db.query(Application)
        .options(joinedload(Application.job))
        .filter(Application.account_id == account_id)
    )
    if status_filter:
        query = query.filter(Application.status == status_filter)

    applications = query.order_by(Application.created_at.desc()).limit(limit).all()
    return applications


@router.post("/{application_id}/send", response_model=ApplicationRead)
def mark_application_sent(
    application_id: str,
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
):
    """
    Strict Human-in-the-loop Send gate:
    Only a human can trigger this endpoint to confirm review and transition
    an application from 'draft' to 'sent'. Records timestamp sent_at and sets follow_up_due (10 days).
    """
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.account_id == account_id)
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application '{application_id}' not found.",
        )

    now = datetime.now(timezone.utc)
    application.sent_at = now
    application.status = "sent"
    # Default 10 days follow-up schedule per ARCHITECTURE.md §6
    application.follow_up_due = now + timedelta(days=10)

    # Sync corresponding Job row
    job = db.query(Job).filter_by(id=application.job_id, account_id=account_id).first()
    if job:
        job.status = "applied"
        job.applied_at = now
        job.follow_up_due = application.follow_up_due

    db.commit()
    db.refresh(application)

    return application


@router.patch("/{application_id}/status", response_model=ApplicationRead)
def update_application_status(
    application_id: str,
    body: StatusUpdateRequest,
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
):
    """
    Update application status in the pipeline (e.g. responded, interview, offer, rejected).
    """
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.account_id == account_id)
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application '{application_id}' not found.",
        )

    application.status = body.status
    if body.notes:
        application.notes = body.notes

    # Sync Job status
    job = db.query(Job).filter_by(id=application.job_id, account_id=account_id).first()
    if job:
        if body.status == "interview":
            job.status = "interviewing"
        elif body.status == "offer":
            job.status = "offered"
        elif body.status == "rejected":
            job.status = "rejected"

    db.commit()
    db.refresh(application)
    return application


@router.post("/{application_id}/follow-up/draft", response_model=FollowUpDraftResponse)
async def draft_follow_up(
    application_id: str,
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
):
    """
    Module 3 (Monitor): Generates a personalized follow-up email draft.
    Strictly capped at most 2 follow-ups per application (ARCHITECTURE.md §6).
    Draft-only: never auto-sent.
    """
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.account_id == account_id)
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application '{application_id}' not found.",
        )

    # Enforce maximum cap of 2 per application (ARCHITECTURE.md §6)
    if application.follow_up_count >= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum follow-up cap of 2 reached for this application to avoid spamming recruiters.",
        )

    job = db.query(Job).filter_by(id=application.job_id, account_id=account_id).first()
    company = job.company if job else "Hiring Team"
    role = job.role if job else "the position"

    follow_up_num = application.follow_up_count + 1

    prompt = f"""
You are drafting a professional, polite follow-up email for Niloy Sannyal.
Target Company: {company}
Target Role: {role}
Follow-up Number: {follow_up_num} of 2 (Maximum cap: 2)
Original Submitted Cover Letter:
{application.draft_content or ''}

RULES:
1. Keep the follow-up concise (1-2 short paragraphs).
2. Restate enthusiasm for the role and check on application status.
3. Use ONLY facts already mentioned in the submitted materials (e.g. Betopia Sales Agent, 600+ salespersons).
4. Tone: confident, courteous, respectful of their time.
"""
    draft = await llm_service.generate(
        prompt=prompt,
        context="You are a respectful, high-impact job follow-up email drafter.",
    )

    return FollowUpDraftResponse(
        application_id=application_id,
        company=company,
        role=role,
        follow_up_number=follow_up_num,
        draft_content=draft.strip(),
        cap_reached=follow_up_num >= 2,
    )


@router.post("/{application_id}/follow-up/send", response_model=ApplicationRead)
def mark_follow_up_sent(
    application_id: str,
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
):
    """
    Human confirmation gate to mark a follow-up email sent.
    Increments follow_up_count and schedules next follow-up (if under cap).
    """
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.account_id == account_id)
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application '{application_id}' not found.",
        )

    if application.follow_up_count >= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send further follow-ups; cap of 2 already reached.",
        )

    now = datetime.now(timezone.utc)
    application.follow_up_count += 1

    # Schedule next follow-up in 10 days if under cap, otherwise clear due date
    if application.follow_up_count < 2:
        application.follow_up_due = now + timedelta(days=10)
    else:
        application.follow_up_due = None

    db.commit()
    db.refresh(application)
    return application


class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Target status: draft | sent | responded | interview | offer | rejected")
    notes: Optional[str] = None


@router.patch("/{application_id}/status", response_model=ApplicationRead)
def update_application_status(
    application_id: str,
    req: StatusUpdateRequest,
    account_id: str = Query(..., description="Account ID for multi-tenant isolation"),
    db: Session = Depends(get_db),
):
    """
    Module 3 (Monitor): Update application status across pipeline stages:
    draft -> sent -> responded -> interview -> offer -> rejected.
    Synchronizes status with the linked Job entity.
    """
    application = (
        db.query(Application)
        .options(joinedload(Application.job))
        .filter(Application.id == application_id, Application.account_id == account_id)
        .first()
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application '{application_id}' not found.",
        )

    application.status = req.status
    if req.notes is not None:
        application.notes = req.notes

    if application.job:
        application.job.status = req.status
        if req.notes:
            application.job.notes = req.notes

    db.commit()
    db.refresh(application)
    return application


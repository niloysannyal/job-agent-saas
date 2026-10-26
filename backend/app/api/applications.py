from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

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
    query = db.query(Application).filter(Application.account_id == account_id)
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
    an application from 'draft' to 'sent'. Records timestamp sent_at.
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

    application.sent_at = datetime.now(timezone.utc)
    application.status = "sent"
    db.commit()
    db.refresh(application)

    return application

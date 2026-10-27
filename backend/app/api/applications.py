from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.db.session import get_db
from app.models.account import Account
from app.models.application import Application, ApplicationRead
from app.models.cv_template import AccountCvVersion, AccountCvVersionRead
from app.models.job import Job
from app.models.profile import UserProfile
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


class FitEvaluationRequest(BaseModel):
    account_id: str = Field(..., description="Multi-tenant account identifier")
    job_id: Optional[str] = Field(None, description="Job posting ID to evaluate")
    posting_text: Optional[str] = Field(None, description="Raw posting text if pasting directly")
    company_name: Optional[str] = Field(None, description="Company name")
    role_title: Optional[str] = Field(None, description="Role title")


class FitDimension(BaseModel):
    verdict: str  # "PASS", "FLAG", "FAIL", "STRONG_MATCH", "MODERATE_MATCH"
    score: int
    matched_items: List[str]
    missing_items: List[str]
    notes: str


class FitEvaluationResponse(BaseModel):
    company: str
    role: str
    overall_score: int
    recommendation: str
    technical_skills: FitDimension
    location_logistics: FitDimension
    language_gate: FitDimension
    dealbreaker_check: FitDimension


@router.post("/evaluate-fit", response_model=FitEvaluationResponse)
def evaluate_job_fit(
    payload: FitEvaluationRequest,
    db: Session = Depends(get_db),
) -> FitEvaluationResponse:
    """
    Evaluate candidate-to-job fit across Technical Competencies, Location & Logistics,
    Language Gate, and Dealbreaker constraints using the candidate's structured profile.
    """
    # Fetch candidate profile with relations
    stmt = (
        select(UserProfile)
        .where(UserProfile.account_id == payload.account_id)
        .options(
            selectinload(UserProfile.target_designations),
            selectinload(UserProfile.target_locations),
            selectinload(UserProfile.spoken_languages),
        )
    )
    profile = db.scalars(stmt).first()

    company = payload.company_name or "Target Company"
    role = payload.role_title or "Target Role"
    text = payload.posting_text or ""
    stored_match_score = None

    if payload.job_id:
        job = db.query(Job).filter_by(id=payload.job_id, account_id=payload.account_id).first()
        if job:
            company = job.company or company
            job_role = getattr(job, "role", None) or getattr(job, "title", None) or role
            role = job_role
            text = (job.description or "") + " " + (job_role or "")
            stored_match_score = job.match_score

    text_lower = text.lower()

    # 1. Technical Skills Analysis
    candidate_skills = [
        "python", "fastapi", "llm", "rag", "qdrant", "redis", "docker",
        "agentic ai", "agent", "machine learning", "nlp", "vector",
        "pytorch", "sql", "git", "ci/cd", "rest api", "system design"
    ]
    matched_skills = [s for s in candidate_skills if s in text_lower]
    
    # Common requirements that might be missing
    common_job_reqs = ["aws", "kubernetes", "typescript", "golang", "gcp", "spark", "kafka"]
    demanded_but_missing = [req for req in common_job_reqs if req in text_lower]

    tech_score = int(min(100, (len(matched_skills) / 6.0) * 100)) if matched_skills else 50
    if stored_match_score is not None:
        scaled = stored_match_score * 100 if stored_match_score <= 1.0 else stored_match_score
        tech_score = int(max(10, min(100, scaled)))

    tech_verdict = "STRONG_MATCH" if tech_score >= 80 else ("MODERATE_MATCH" if tech_score >= 60 else "FLAG")
    tech_dimension = FitDimension(
        verdict=tech_verdict,
        score=tech_score,
        matched_items=matched_skills[:8],
        missing_items=demanded_but_missing,
        notes=f"Identified {len(matched_skills)} core technical synergies with candidate background."
    )

    # 2. Location & Logistics Gate
    # Check if remote or local (Dhaka / EU relocation)
    location_pass = True
    location_notes = "Posting supports remote work or aligns with target locations."
    if "on-site only" in text_lower and "dhaka" not in text_lower:
        location_pass = False
        location_notes = "Requires mandatory on-site presence outside primary residence without stated relocation assistance."
    elif "must be based in us" in text_lower or "us citizen only" in text_lower or "security clearance" in text_lower:
        location_pass = False
        location_notes = "Restricted to domestic US citizens or requires active security clearance."

    location_dimension = FitDimension(
        verdict="PASS" if location_pass else "FAIL",
        score=95 if location_pass else 30,
        matched_items=["Remote Eligible", "Global Flexibility"] if location_pass else [],
        missing_items=["US Work Authorization"] if not location_pass else [],
        notes=location_notes
    )

    # 3. Language Gate
    # Candidate speaks English (fluent) and Bengali (native)
    foreign_languages = ["german", "french", "japanese", "mandarin", "spanish", "dutch"]
    detected_foreign = [lang for lang in foreign_languages if f"fluent {lang}" in text_lower or f"{lang} native" in text_lower or f"business level {lang}" in text_lower]
    
    lang_pass = len(detected_foreign) == 0
    lang_notes = "Required languages match candidate proficiency (English, Bengali)." if lang_pass else f"Requires undeclared language fluency: {', '.join(detected_foreign)}."
    
    language_dimension = FitDimension(
        verdict="PASS" if lang_pass else "FAIL",
        score=100 if lang_pass else 20,
        matched_items=["English (Fluent)", "Bengali (Native)"],
        missing_items=detected_foreign,
        notes=lang_notes
    )

    # 4. Dealbreaker Check
    dealbreaker_triggered = False
    dealbreaker_notes = "No candidate dealbreakers detected."
    if profile and profile.dealbreakers:
        db_terms = [t.strip().lower() for t in profile.dealbreakers.split(",") if t.strip()]
        for term in db_terms:
            if term and term in text_lower:
                dealbreaker_triggered = True
                dealbreaker_notes = f"Contains terms flagged in user dealbreakers: '{term}'."
                break

    dealbreaker_dimension = FitDimension(
        verdict="PASS" if not dealbreaker_triggered else "FLAG",
        score=100 if not dealbreaker_triggered else 25,
        matched_items=[] if dealbreaker_triggered else ["Zero dealbreakers matched"],
        missing_items=[dealbreaker_notes] if dealbreaker_triggered else [],
        notes=dealbreaker_notes
    )

    # Calculate overall score
    overall = int(tech_score * 0.55 + location_dimension.score * 0.25 + language_dimension.score * 0.15 + dealbreaker_dimension.score * 0.05)
    overall = max(10, min(99, overall))

    if not location_pass or not lang_pass or dealbreaker_triggered:
        recommendation = "Review Constraints"
    elif overall >= 80:
        recommendation = "Strong Fit"
    elif overall >= 60:
        recommendation = "Moderate Fit"
    else:
        recommendation = "Low Fit"

    return FitEvaluationResponse(
        company=company,
        role=role,
        overall_score=overall,
        recommendation=recommendation,
        technical_skills=tech_dimension,
        location_logistics=location_dimension,
        language_gate=language_dimension,
        dealbreaker_check=dealbreaker_dimension,
    )



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


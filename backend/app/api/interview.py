"""
STAR Interview Coach API — CRUD for interview stories + tag-based querying.

All endpoints are scoped to account_id (multi-tenant, Phase 0 trusted parameter).
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.interview import (
    StarStory,
    StarStoryCreate,
    StarStoryRead,
    StarStoryUpdate,
)
from app.models.job import Job
from app.models.profile import UserProfile

router = APIRouter(prefix="/interview", tags=["interview"])


# ---------------------------------------------------------------------------
# STAR Stories CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/stories",
    response_model=List[StarStoryRead],
    summary="List all STAR stories for an account",
)
def list_stories(
    account_id: str = Query(..., description="Target account ID"),
    tag: Optional[str] = Query(
        None,
        description="Filter stories containing this tag (case-insensitive substring match on good_for_tags)",
    ),
    verified_only: bool = Query(
        False,
        description="Only return stories marked as verified",
    ),
    db: Session = Depends(get_db),
) -> List[StarStoryRead]:
    """Fetch STAR stories, optionally filtered by tag or verification status."""
    stmt = (
        select(StarStory)
        .where(StarStory.account_id == account_id)
        .order_by(StarStory.sort_order, StarStory.created_at.desc())
    )

    if verified_only:
        stmt = stmt.where(StarStory.is_verified == True)

    stories = list(db.scalars(stmt).all())

    # Client-side tag filtering (simple substring match)
    if tag:
        tag_lower = tag.strip().lower()
        stories = [
            s for s in stories
            if tag_lower in (s.good_for_tags or "").lower()
        ]

    return stories


@router.get(
    "/stories/{story_id}",
    response_model=StarStoryRead,
    summary="Get a single STAR story by ID",
)
def get_story(
    story_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")
    return story


@router.post(
    "/stories",
    response_model=StarStoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new STAR story",
)
def create_story(
    account_id: str = Query(...),
    payload: StarStoryCreate = ...,
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = StarStory(account_id=account_id, **payload.model_dump())
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


@router.patch(
    "/stories/{story_id}",
    response_model=StarStoryRead,
    summary="Update a STAR story",
)
def update_story(
    story_id: str,
    account_id: str = Query(...),
    payload: StarStoryUpdate = ...,
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(story, field, value)

    db.commit()
    db.refresh(story)
    return story


@router.delete(
    "/stories/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a STAR story",
)
def delete_story(
    story_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")
    db.delete(story)
    db.commit()


@router.get(
    "/tags",
    response_model=List[str],
    summary="List all unique STAR story tags for an account",
)
def list_tags(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[str]:
    """Extract all unique tags across the account's STAR stories."""
    stories = db.scalars(
        select(StarStory).where(StarStory.account_id == account_id)
    ).all()
    tags: set[str] = set()
    for story in stories:
        if story.good_for_tags:
            for tag in story.good_for_tags.split(","):
                cleaned = tag.strip()
                if cleaned:
                    tags.add(cleaned)
    return sorted(tags)


# ---------------------------------------------------------------------------
# STAR Interview Simulator & Prep Guide
# ---------------------------------------------------------------------------

class InterviewPrepRequest(BaseModel):
    account_id: str = Field(..., description="Target account ID")
    job_id: Optional[str] = Field(None, description="Optional job ID to tailor interview prep for")
    role_title: Optional[str] = Field(None, description="Target role title, e.g. 'AI Engineer'")
    company_name: Optional[str] = Field(None, description="Target company name, e.g. 'Anthropic'")
    job_description: Optional[str] = Field(None, description="Raw job description / requirements")


class PrepQuestion(BaseModel):
    id: str
    question: str
    category: str
    suggested_story_id: Optional[str] = None
    suggested_story_title: Optional[str] = None
    talking_points: List[str]
    pitfalls_to_avoid: str


class InterviewPrepResponse(BaseModel):
    role_title: str
    company_name: str
    questions: List[PrepQuestion]
    narrative_advice: str
    dealbreaker_reminder: Optional[str] = None


@router.post(
    "/prep",
    response_model=InterviewPrepResponse,
    summary="Generate tailored interview questions, STAR story mappings, and prep advice",
)
def generate_interview_prep(
    payload: InterviewPrepRequest,
    db: Session = Depends(get_db),
) -> InterviewPrepResponse:
    """
    Generate tailored interview prep questions for a specific role or job posting,
    mapping each question to the candidate's verified STAR story library.
    """
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == payload.account_id)
    ).first()

    stories = list(
        db.scalars(
            select(StarStory)
            .where(StarStory.account_id == payload.account_id)
            .order_by(StarStory.sort_order)
        ).all()
    )

    company = payload.company_name or "Target Company"
    role = payload.role_title or (profile.current_role if profile else "AI Engineer")

    # If job_id was provided, load job metadata
    if payload.job_id:
        job = db.scalars(
            select(Job).where(Job.id == payload.job_id, Job.account_id == payload.account_id)
        ).first()
        if job:
            company = job.company or company
            role = getattr(job, "role", None) or getattr(job, "title", None) or role

    # Map candidate's stories
    sales_agent_story = next((s for s in stories if "sales" in s.title.lower() or "ownership" in (s.good_for_tags or "").lower()), None)
    adaptability_story = next((s for s in stories if "stack" in s.title.lower() or "learning" in (s.good_for_tags or "").lower()), None)
    multimodal_story = next((s for s in stories if "vision" in s.title.lower() or "multimodal" in (s.good_for_tags or "").lower()), None)

    first_story = stories[0] if stories else None

    questions: List[PrepQuestion] = [
        PrepQuestion(
            id="q1",
            question=f"Tell me about a complex {role} system you designed, built, and shipped into real production end-to-end.",
            category="System Architecture & Ownership",
            suggested_story_id=sales_agent_story.id if sales_agent_story else (first_story.id if first_story else None),
            suggested_story_title=sales_agent_story.title if sales_agent_story else (first_story.title if first_story else "Production System Ownership"),
            talking_points=[
                "Lead with the business problem: Embed AI assistant into Odoo CRM with zero existing infrastructure.",
                "Detail the architecture: Dynamic multi-provider routing (OpenAI, Anthropic, Gemini) with failover.",
                "Highlight the measurable outcome: 700+ active salespersons using it in production with 99.9% uptime.",
                "Emphasize solo ownership across requirements, RAG pipeline, CI/CD, and production debugging."
            ],
            pitfalls_to_avoid="Avoid speaking only about model prompts; recruiters want to hear about database state, caching, API gateways, and failure handling."
        ),
        PrepQuestion(
            id="q2",
            question="Describe a time you had to deliver on an urgent deadline using an unfamiliar technology stack or database.",
            category="Adaptability & Learning Velocity",
            suggested_story_id=adaptability_story.id if adaptability_story else (first_story.id if first_story else None),
            suggested_story_title=adaptability_story.title if adaptability_story else (first_story.title if first_story else "Self-onboarding on Unfamiliar Stack"),
            talking_points=[
                "Acknowledge unfamiliarity calmly: Needed Odoo, Redis, Qdrant, and Next.js without prior production usage.",
                "Explain the hands-on approach: Learned while prototyping inside a staging build instead of delaying delivery.",
                "Emphasize execution over theory: Turned all four technologies into reliable production pillars."
            ],
            pitfalls_to_avoid="Don't claim you knew everything upfront; technical leaders respect rapid pragmatic assimilation far more than inflated confidence."
        ),
        PrepQuestion(
            id="q3",
            question=f"How do you evaluate model performance, latency, and cost trade-offs when building practical AI features at {company}?",
            category="Applied AI Evaluation & MLOps",
            suggested_story_id=multimodal_story.id if multimodal_story else (first_story.id if first_story else None),
            suggested_story_title=multimodal_story.title if multimodal_story else (first_story.title if first_story else "Vision & Document Information Extraction"),
            talking_points=[
                "Mention empirical testing: Benchmarked commercial vision models vs self-hosted options on real messy PDFs.",
                "Discuss engineering principle: 'The model is only one component — reliability comes from preprocessing, schema validation, and fallback loops.'",
                "Highlight latency-cost balance: Used structured JSON output with aggressive caching for predictable throughput."
            ],
            pitfalls_to_avoid="Avoid generic benchmark numbers (MMLU, HumanEval); talk about domain-specific test sets and production error cases."
        ),
        PrepQuestion(
            id="q4",
            question=f"Why are you interested in joining {company} for this {role} opportunity, and what are you looking for next?",
            category="Motivation & Culture Fit",
            suggested_story_id=None,
            suggested_story_title=None,
            talking_points=[
                f"Refer to {company}'s specific domain challenge and why your hands-on AI systems background directly aligns.",
                f"State career trajectory clearly: {profile.reason_for_leaving if profile else 'Seeking broader ownership and high-scale production AI challenges'}.",
                f"Tone rule: {profile.tone_preferences if profile else 'Direct, technically precise, no corporate fluff.'}"
            ],
            pitfalls_to_avoid=f"Do not mention buzzwords like '{profile.avoid_phrases if profile else 'passionate enthusiast'}'; focus on real engineering rigor."
        )
    ]

    narrative_advice = (
        profile.tone_preferences
        if profile and profile.tone_preferences
        else "Direct, technically precise, no corporate fluff, concise and credible."
    )

    dealbreaker_reminder = profile.dealbreakers if profile else None

    return InterviewPrepResponse(
        role_title=role,
        company_name=company,
        questions=questions,
        narrative_advice=narrative_advice,
        dealbreaker_reminder=dealbreaker_reminder,
    )


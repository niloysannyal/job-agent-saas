from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_account, get_optional_account, resolve_tenant_id
from app.db.session import get_db
from app.models.account import Account
from app.models.job import Job, JobRead, JobSearchQuery
from app.services.job_ingestion import JobIngestionService
from app.services.job_sources import get_available_sources

router = APIRouter(prefix="/jobs", tags=["jobs"])


class IngestionRequest(BaseModel):
    """Payload for triggering a job ingestion run."""
    account_id: str = Field(..., description="Target tenant account UUID")
    search_queries: Optional[List[Union[JobSearchQuery, str]]] = Field(
        default=["AI Engineer"],
        description="List of search queries or keyword strings for general sources",
    )
    target_companies: Optional[List[str]] = Field(
        default=None,
        description="Company slugs for ATS sources (e.g. ['optimizely', 'therap'])",
    )
    sources: Optional[List[str]] = Field(
        default=None,
        description=(
            "Specific sources to query: 'adzuna', 'remotive', 'remoteok', "
            "'greenhouse', 'lever', 'freehire'. Omit to run all available."
        ),
    )


class IngestionResponse(BaseModel):
    """Summary metrics of an executed ingestion and matching run."""
    total_fetched: int
    saved_count: int
    duplicate_count: int
    flagged_count: int
    scored_count: int
    vetoed_count: int
    errors: List[str]


@router.post(
    "/ingest",
    response_model=IngestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Trigger job ingestion and automatic match scoring",
    description=(
        "Fetches postings from requested or default job sources, runs them through the "
        "posting integrity guard, deduplicates, persists new jobs, and synchronously "
        "evaluates language gate vetoes and semantic match scores against the user's profile."
    ),
)
async def trigger_ingestion(
    payload: IngestionRequest,
    current_account: Optional[Account] = Depends(get_optional_account),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    """Trigger job ingestion pipeline for an account."""
    if current_account:
        effective_account_id = resolve_tenant_id(current_account, payload.account_id)
    else:
        effective_account_id = payload.account_id

    # 1. Resolve selected job sources
    job_sources = get_available_sources(payload.sources)
    if not job_sources:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid job sources could be initialized with current configuration.",
        )

    # 2. Normalize search queries
    queries = payload.search_queries or ["AI Engineer"]

    # 3. Execute ingestion and synchronous matching
    service = JobIngestionService(db=db)
    result = await service.ingest(
        account_id=effective_account_id,
        sources=job_sources,
        search_queries=queries,
        target_companies=payload.target_companies,
    )

    scored = result.matching_result.scored_count if result.matching_result else 0
    vetoed = result.matching_result.vetoed_count if result.matching_result else 0

    return IngestionResponse(
        total_fetched=result.total_fetched,
        saved_count=len(result.saved_jobs),
        duplicate_count=result.duplicate_count,
        flagged_count=result.flagged_count,
        scored_count=scored,
        vetoed_count=vetoed,
        errors=result.errors,
    )


@router.get(
    "",
    response_model=List[JobRead],
    summary="List ranked jobs for an account",
    description=(
        "Returns jobs for a given account_id, ordered by match_score descending. "
        "By default, excludes vetoed jobs (vetoed=True) and postings flagged by the "
        "integrity gate (integrity_status='flagged'). "
        "Query params allow human reviewers to inspect flagged and vetoed postings."
    ),
)
def list_jobs(
    account_id: Optional[str] = Query(None, description="Target account ID"),
    include_vetoed: bool = Query(
        False,
        description="Include jobs vetoed by the deal-breaker/language gate",
    ),
    include_flagged: bool = Query(
        False,
        description="Include jobs flagged by the posting integrity gate",
    ),
    show_all: bool = Query(
        False,
        description="Override to include both vetoed and flagged jobs for human review",
    ),
    limit: int = Query(100, ge=1, le=500, description="Max number of jobs to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> List[JobRead]:
    """
    Fetch jobs for an account ordered by match_score descending.
    Excludes vetoed and flagged postings by default.
    """
    effective_account_id = resolve_tenant_id(current_account, account_id)
    stmt = select(Job).where(Job.account_id == effective_account_id)

    # Exclude vetoed jobs unless explicitly requested or show_all is set
    allow_vetoed = include_vetoed or show_all
    if not allow_vetoed:
        stmt = stmt.where(Job.vetoed == False)

    # Exclude flagged postings unless explicitly requested or show_all is set
    allow_flagged = include_flagged or show_all
    if not allow_flagged:
        stmt = stmt.where(Job.integrity_status != "flagged")

    # Order by match_score descending with un-scored / NULL values last,
    # breaking ties by creation date descending
    stmt = stmt.order_by(Job.match_score.desc().nulls_last(), Job.created_at.desc())
    stmt = stmt.offset(offset).limit(limit)

    jobs = db.scalars(stmt).all()
    return list(jobs)

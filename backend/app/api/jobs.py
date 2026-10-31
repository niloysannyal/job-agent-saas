from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
import httpx
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
    summary="List ranked jobs for an account with workplace and recency filters",
    description=(
        "Returns jobs for a given account_id, ordered by match_score descending. "
        "By default, excludes vetoed jobs, flagged jobs, and expired jobs. "
        "Query params allow filtering by workplace type (remote, hybrid, on-site) and recency."
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
    location_type: Optional[str] = Query(
        None,
        description="Filter by workplace mode: 'remote', 'hybrid', 'on-site'",
    ),
    posted_within_days: Optional[int] = Query(
        None,
        ge=1,
        le=365,
        description="Only return jobs posted within the last N days",
    ),
    exclude_expired: bool = Query(
        True,
        description="Filter out expired deadlines or inactive jobs",
    ),
    sort_by: str = Query(
        "match_score",
        description="'match_score' | 'posted_at' | 'created_at'",
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
    now = datetime.now(timezone.utc)

    # Exclude vetoed jobs unless explicitly requested or show_all is set
    allow_vetoed = include_vetoed or show_all
    if not allow_vetoed:
        stmt = stmt.where(Job.vetoed == False)

    # Exclude flagged postings unless explicitly requested or show_all is set
    allow_flagged = include_flagged or show_all
    if not allow_flagged:
        stmt = stmt.where(Job.integrity_status != "flagged")

    # Workplace filter (remote, hybrid, on-site)
    if location_type:
        loc_normalized = location_type.strip().lower()
        if loc_normalized in ("onsite", "on-site"):
            stmt = stmt.where(Job.location_type.in_(["onsite", "on-site"]))
        else:
            stmt = stmt.where(Job.location_type == loc_normalized)

    # Recency filter
    if posted_within_days:
        cutoff = now - timedelta(days=posted_within_days)
        stmt = stmt.where(
            (Job.posted_at >= cutoff) | ((Job.posted_at == None) & (Job.created_at >= cutoff))
        )

    # Expiration filter
    if exclude_expired and not show_all:
        stmt = stmt.where(Job.is_active == True)
        stmt = stmt.where(
            (Job.deadline == None) | (Job.deadline >= now)
        )

    # Sorting
    if sort_by == "posted_at":
        stmt = stmt.order_by(Job.posted_at.desc().nulls_last(), Job.created_at.desc())
    elif sort_by == "created_at":
        stmt = stmt.order_by(Job.created_at.desc())
    else:
        # Default: match_score desc
        stmt = stmt.order_by(Job.match_score.desc().nulls_last(), Job.created_at.desc())

    stmt = stmt.offset(offset).limit(limit)
    jobs = db.scalars(stmt).all()
    return list(jobs)


@router.post(
    "/{job_id}/check-liveness",
    summary="Check if a job posting URL is still active and alive",
)
async def check_job_liveness(
    job_id: str,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    effective_account_id = resolve_tenant_id(current_account, account_id)
    job = db.scalars(
        select(Job).where(Job.id == job_id, Job.account_id == effective_account_id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    is_alive = True
    status_code = 200
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=8.0) as client:
            resp = await client.get(job.apply_link)
            status_code = resp.status_code
            url_str = str(resp.url).lower()
            if status_code >= 400 or "maintenance-page.html" in url_str or "error=true" in url_str:
                is_alive = False
    except Exception:
        is_alive = False

    job.is_active = is_alive
    if not is_alive:
        job.integrity_status = "dead_link"
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "is_active": job.is_active,
        "integrity_status": job.integrity_status,
        "http_status": status_code,
    }

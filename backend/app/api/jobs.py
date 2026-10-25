from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import Job, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])


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
    account_id: str = Query(..., description="Target account ID"),
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
    db: Session = Depends(get_db),
) -> List[JobRead]:
    """
    Fetch jobs for an account ordered by match_score descending.
    Excludes vetoed and flagged postings by default.
    """
    stmt = select(Job).where(Job.account_id == account_id)

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

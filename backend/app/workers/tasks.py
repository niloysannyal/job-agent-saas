from datetime import datetime, timezone, timedelta
import logging
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.account import Account
from app.models.application import Application
from app.models.job import Job
from app.services.job_ingestion import JobIngestionService
from app.services.matching.service import MatchingService
from app.services.matching.experience_reflector import ExperienceReflector
from app.services.job_sources.remotive import RemotiveJobSource
from app.services.job_sources.remoteok import RemoteOKJobSource

logger = logging.getLogger(__name__)


async def ingest_jobs_task(
    ctx: Dict[str, Any],
    account_id: str,
    query: str = "AI Engineer",
) -> Dict[str, Any]:
    """
    Background worker task to fetch fresh job postings from enabled sources,
    deduplicate, run posting guard, and persist to database.
    """
    logger.info("Starting background job ingestion for account %s, query: %s", account_id, query)
    db: Session = SessionLocal()
    try:
        sources = [RemotiveJobSource(), RemoteOKJobSource()]
        ingestion_service = JobIngestionService(db=db)
        result = await ingestion_service.ingest(
            account_id=account_id,
            sources=sources,
            search_queries=query,
        )
        logger.info(
            "Ingestion complete: %d saved, %d duplicates, %d flagged",
            result.saved_count,
            result.duplicate_count,
            result.flagged_count,
        )

        if result.saved_jobs:
            matching_service = MatchingService(db=db)
            await matching_service.score_and_gate_jobs(account_id=account_id, jobs=result.saved_jobs)

        return {
            "status": "success",
            "saved_count": result.saved_count,
            "duplicate_count": result.duplicate_count,
            "flagged_count": result.flagged_count,
        }
    finally:
        db.close()


async def embed_jobs_batch_task(
    ctx: Dict[str, Any],
    account_id: str,
    job_ids: List[str],
) -> Dict[str, Any]:
    """
    Background worker task to compute vector embeddings and gate jobs.
    """
    db: Session = SessionLocal()
    try:
        jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
        matching_service = MatchingService(db=db)
        result = await matching_service.score_and_gate_jobs(account_id=account_id, jobs=jobs)
        return {
            "status": "success",
            "scored_count": result.scored_count,
            "vetoed_count": result.vetoed_count,
        }
    finally:
        db.close()


async def monitor_followups_task(
    ctx: Dict[str, Any],
    account_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Cron / periodic worker task to identify applications awaiting response > 7 days,
    marking them for follow-up reminders.
    """
    logger.info("Running periodic application follow-up monitor")
    db: Session = SessionLocal()
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query = db.query(Application).filter(
            Application.status.in_(["applied", "ready_to_send"]),
            Application.created_at <= seven_days_ago,
        )
        if account_id:
            query = query.filter_by(account_id=account_id)

        overdue_apps = query.all()
        flagged_count = 0
        for app in overdue_apps:
            # Can attach a follow-up badge or notification state
            flagged_count += 1

        logger.info("Identified %d applications due for follow-up outreach", flagged_count)
        return {"status": "success", "followup_due_count": flagged_count}
    finally:
        db.close()


async def reflect_experience_task(
    ctx: Dict[str, Any],
    account_id: str,
) -> Dict[str, Any]:
    """
    Worker task to run Experience Reflector and update learning insights.
    """
    db: Session = SessionLocal()
    try:
        reflector = ExperienceReflector(db=db)
        insights = reflector.reflect_for_account(account_id)
        return {
            "status": "success",
            "conversion_rate": insights.overall_conversion_rate,
            "recommendations_count": len(insights.strategic_recommendations),
        }
    finally:
        db.close()

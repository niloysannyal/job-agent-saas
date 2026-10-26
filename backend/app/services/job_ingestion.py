import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job, JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource
from app.services.matching.service import MatchingService, MatchingResult
from app.services.posting_guard import GateResult, run_posting_guard

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# FLAG / OPEN DESIGN DECISION (ARCHITECTURE.md §4 & §7):
# ---------------------------------------------------------------------------
# Cross-Source Duplicate Resolution:
# How should postings appearing across multiple sources (e.g., the same role
# listed on both Adzuna and Freehire, or on Greenhouse and RemoteOK) be handled?
#
# Current implementation behavior:
#   1. Exact Source Duplicates: If (account_id, source, source_job_id) already
#      exists in the DB or in the current batch, it is skipped as a duplicate.
#   2. Exact URL Duplicates: If (account_id, apply_link) already exists, it is
#      skipped as a duplicate.
#
# Open decision for future phases:
#   - Should cross-source postings for the same (company, role) with different
#     apply URLs be merged (e.g., preferring direct ATS like Greenhouse/Lever
#     over aggregators)?
#   - Or should they remain distinct records with a cross-reference link?
# We flag this here rather than silently deciding a business rule.
# ---------------------------------------------------------------------------


@dataclass
class IngestionResult:
    """Summary metrics of a job ingestion run."""
    total_fetched: int = 0
    saved_jobs: List[Job] = field(default_factory=list)
    flagged_count: int = 0
    duplicate_count: int = 0
    errors: List[str] = field(default_factory=list)
    matching_result: Optional[MatchingResult] = None


class JobIngestionService:
    """
    Job ingestion orchestration service matching ARCHITECTURE.md §4 and §7.

    Orchestrates the ingestion pipeline:
      1. Sourcing:
         - Inspects each JobSource.is_per_company flag.
         - General sources (is_per_company=False) are invoked with search keywords.
         - Per-company sources (is_per_company=True) are invoked once per company slug.
      2. Security Gate:
         - Every fetched JobPosting is immediately passed through posting_guard
           to strip hidden/invisible Unicode and flag potential prompt-injections
           before any database persistence or LLM access.
      3. Deduplication & Persistence:
         - Deduplicates against existing records in the database and within the batch.
         - Maps cleaned JobPosting to the multi-tenant Job SQLAlchemy model and commits.
    """

    def __init__(
        self,
        db: Session,
        matching_service: Optional[MatchingService] = None,
    ) -> None:
        self.db = db
        self.matching_service = matching_service or MatchingService(db=db)

    def _normalize_target_slugs(
        self,
        target_companies: Optional[Sequence[str]],
    ) -> List[str]:
        if not target_companies:
            return []
        return [slug.strip().lower() for slug in target_companies if slug and slug.strip()]

    def _normalize_queries(
        self,
        queries: Union[JobSearchQuery, str, Dict[str, Any], Sequence[Union[JobSearchQuery, str, Dict[str, Any]]]],
    ) -> List[Union[JobSearchQuery, str, Dict[str, Any]]]:
        if isinstance(queries, (JobSearchQuery, str, dict)):
            return [queries]
        return list(queries)

    async def ingest(
        self,
        account_id: str,
        sources: Sequence[JobSource],
        search_queries: Union[
            JobSearchQuery, str, Dict[str, Any], Sequence[Union[JobSearchQuery, str, Dict[str, Any]]]
        ],
        target_companies: Optional[Sequence[str]] = None,
    ) -> IngestionResult:
        """
        Orchestrate fetching, integrity verification, and persistence of jobs.

        Args:
            account_id: Tenant account UUID (multi-tenant isolation).
            sources: List of JobSource instances to query.
            search_queries: One or more search queries for general sources.
            target_companies: List of company slugs for per-company sources.

        Returns:
            IngestionResult containing counts, saved jobs, and any errors.
        """
        result = IngestionResult()
        normalized_queries = self._normalize_queries(search_queries)
        normalized_targets = self._normalize_target_slugs(target_companies)
        target_slug_set = set(normalized_targets)

        # -------------------------------------------------------------------
        # 1. Fetch postings from all sources
        # -------------------------------------------------------------------
        raw_postings: List[Tuple[JobPosting, bool]] = []  # (posting, is_target_company)

        for source in sources:
            source_name = getattr(source, "__class__", type(source)).__name__

            if source.is_per_company:
                # Per-company ATS source: invoke once per target company
                if not normalized_targets:
                    logger.debug(
                        f"Skipping per-company source {source_name}: no target_companies provided."
                    )
                    continue

                for company_slug in normalized_targets:
                    try:
                        postings = await source.fetch(company_slug)
                        result.total_fetched += len(postings)
                        for p in postings:
                            raw_postings.append((p, True))
                    except Exception as exc:
                        err_msg = (
                            f"Error fetching from per-company source {source_name} "
                            f"for company '{company_slug}': {exc}"
                        )
                        logger.error(err_msg)
                        result.errors.append(err_msg)
            else:
                # General aggregator source: broadcast general search queries
                for q in normalized_queries:
                    try:
                        postings = await source.fetch(q)
                        result.total_fetched += len(postings)
                        for p in postings:
                            # Exact-normalized matching against target company list (case-insensitive, trimmed)
                            # Strictly exact set membership — no substring or fuzzy matching
                            is_target = (
                                (p.company.strip().lower() in target_slug_set)
                                if p.company else False
                            )
                            raw_postings.append((p, is_target))
                    except Exception as exc:
                        query_desc = q.what if isinstance(q, JobSearchQuery) else str(q)
                        err_msg = (
                            f"Error fetching from general source {source_name} "
                            f"for query '{query_desc}': {exc}"
                        )
                        logger.error(err_msg)
                        result.errors.append(err_msg)

        if not raw_postings:
            return result

        # -------------------------------------------------------------------
        # 2. Existing database records for deduplication
        # -------------------------------------------------------------------
        stmt = select(Job.source, Job.source_job_id, Job.apply_link).where(
            Job.account_id == account_id
        )
        existing_rows = self.db.execute(stmt).all()

        existing_source_ids: Set[Tuple[str, str]] = {
            (row[0], row[1]) for row in existing_rows if row[0] and row[1]
        }
        existing_links: Set[str] = {
            row[2] for row in existing_rows if row[2]
        }

        # In-batch deduplication trackers
        seen_source_ids_batch: Set[Tuple[str, str]] = set()
        seen_links_batch: Set[str] = set()

        # -------------------------------------------------------------------
        # 3. Process each posting through integrity gate and persist
        # -------------------------------------------------------------------
        jobs_to_save: List[Job] = []
        now = datetime.now(timezone.utc)

        for posting, is_target in raw_postings:
            # A. Deduplication check
            source_id_key = (posting.source, posting.id)
            link_key = posting.apply_link.strip() if posting.apply_link else ""

            if (
                source_id_key in existing_source_ids
                or source_id_key in seen_source_ids_batch
                or (link_key and (link_key in existing_links or link_key in seen_links_batch))
            ):
                result.duplicate_count += 1
                continue

            seen_source_ids_batch.add(source_id_key)
            if link_key:
                seen_links_batch.add(link_key)

            # B. Posting Integrity Gate (posting_guard)
            gate_result: GateResult = run_posting_guard(posting)
            cleaned = gate_result.posting

            if not gate_result.passed:
                result.flagged_count += 1
                logger.warning(
                    f"Job posting {posting.id} raised integrity flags: "
                    f"{[f.detail for f in gate_result.flags]}"
                )

            # Prepare raw_data, embedding integrity flags if present
            raw_dict = dict(cleaned.raw_data or {})
            if gate_result.flags:
                raw_dict["_integrity_flags"] = [
                    {
                        "kind": f.kind.value,
                        "field": f.field,
                        "detail": f.detail,
                        "line_text": f.line_text,
                    }
                    for f in gate_result.flags
                ]

            # Integrity outcome recorded in dedicated field; pipeline status defaults to 'new'
            integrity_status = "flagged" if not gate_result.passed else "clean"
            pipeline_status = "new"

            # C. Map to SQLAlchemy Job model
            job = Job(
                account_id=account_id,
                company=cleaned.company,
                role=cleaned.role,
                description=cleaned.description,
                salary=cleaned.salary,
                salary_min=cleaned.salary_min,
                salary_max=cleaned.salary_max,
                currency=cleaned.currency,
                deadline=cleaned.deadline,
                location_type=cleaned.location_type,
                country=cleaned.country,
                city=cleaned.city,
                visa_required=False,
                target_company=is_target,
                match_score=None,
                status=pipeline_status,
                integrity_status=integrity_status,
                source=cleaned.source,
                source_job_id=cleaned.id,
                apply_link=cleaned.apply_link,
                found_at=now,
                created_at=now,
                updated_at=now,
                raw_data=raw_dict,
            )
            jobs_to_save.append(job)

        if jobs_to_save:
            self.db.add_all(jobs_to_save)
            self.db.commit()
            for j in jobs_to_save:
                self.db.refresh(j)
            result.saved_jobs = jobs_to_save

            # ---------------------------------------------------------------
            # 4. Synchronously score and gate newly saved jobs per ARCHITECTURE.md §4
            # (Background worker not needed yet per ARCHITECTURE.md §9).
            # Clean jobs are embedded and scored; flagged jobs are skipped.
            # ---------------------------------------------------------------
            if self.matching_service is not None:
                match_res = await self.matching_service.score_and_gate_jobs(
                    account_id=account_id,
                    jobs=jobs_to_save,
                )
                result.matching_result = match_res
                for j in jobs_to_save:
                    self.db.refresh(j)

        return result

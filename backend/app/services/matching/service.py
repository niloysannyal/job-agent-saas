import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    from qdrant_client.models import Distance, PointStruct, VectorParams
except ImportError:
    Distance = None
    PointStruct = None
    VectorParams = None

from app.models.job import Job
from app.services.matching.embedding import (
    EmbeddingClient,
    MockEmbeddingClient,
    compute_cosine_similarity,
    get_embedding_client,
)
from app.services.matching.language_gate import LanguageGate
from app.services.matching.profile_parser import ProfileParser

logger = logging.getLogger(__name__)

DEFAULT_COLLECTION_NAME = "profile_embeddings"


@dataclass
class MatchingResult:
    """Summary of a match scoring run."""
    total_clean_evaluated: int = 0
    scored_count: int = 0
    vetoed_count: int = 0
    skipped_flagged_count: int = 0


class MatchingService:
    """
    Two-layer job match scoring service matching ARCHITECTURE.md §4:
      Layer 1: Coarse ranking via cosine similarity between profile embedding
               (MASTER_CV.tex + USER_PROFILE.md target roles) and job description.
               Profile point is stored in Qdrant.
      Layer 2: Deal-breaker / language gate: hard-vetoes jobs requiring
               undeclared spoken languages without deleting the row.

    Rules:
      - Only jobs with integrity_status = 'clean' are scored.
      - Flagged postings are strictly excluded until reviewed.
    """

    def __init__(
        self,
        db: Session,
        qdrant_client: Optional[Any] = None,
        embedder: Optional[EmbeddingClient] = None,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.db = db
        self.qdrant_client = qdrant_client
        self.embedder = embedder or get_embedding_client()
        self.collection_name = collection_name
        self._cached_profile_vectors: Dict[str, List[float]] = {}

    def _get_qdrant_point_id(self, account_id: str) -> str:
        """Derive a deterministic UUID point ID for the account."""
        try:
            return str(uuid.UUID(account_id))
        except (ValueError, AttributeError):
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(account_id)))

    async def embed_and_upsert_profile(
        self,
        account_id: str,
        cv_path: Optional[Path] = None,
        profile_path: Optional[Path] = None,
    ) -> List[float]:
        """
        Embed the Master CV and target-roles section of USER_PROFILE.md,
        upserting the vector into Qdrant.
        """
        parsed = ProfileParser.parse(cv_path=cv_path, profile_path=profile_path)
        vector = await self.embedder.embed(parsed.combined_embedding_text)
        self._cached_profile_vectors[account_id] = vector

        point_id = self._get_qdrant_point_id(account_id)

        if self.qdrant_client is not None:
            # Check or create collection if supported
            try:
                if hasattr(self.qdrant_client, "collection_exists"):
                    res = self.qdrant_client.collection_exists(self.collection_name)
                    exists = await res if hasattr(res, "__await__") else res
                    if not exists and hasattr(self.qdrant_client, "create_collection") and VectorParams and Distance:
                        create_res = self.qdrant_client.create_collection(
                            collection_name=self.collection_name,
                            vectors_config=VectorParams(size=len(vector), distance=Distance.COSINE),
                        )
                        if hasattr(create_res, "__await__"):
                            await create_res
            except Exception as e:
                logger.debug(f"Qdrant collection setup note: {e}")

            # Upsert vector into Qdrant
            payload = {
                "account_id": account_id,
                "target_roles": parsed.target_roles_text,
                "dealbreakers": parsed.dealbreakers_text,
                "declared_languages": parsed.declared_languages,
            }
            if PointStruct is not None and hasattr(self.qdrant_client, "upsert"):
                point = PointStruct(id=point_id, vector=vector, payload=payload)
                upsert_res = self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=[point],
                )
                if hasattr(upsert_res, "__await__"):
                    await upsert_res

        return vector

    async def score_and_gate_jobs(
        self,
        account_id: str,
        profile_vector: Optional[List[float]] = None,
        profile_path: Optional[Path] = None,
        cv_path: Optional[Path] = None,
        jobs: Optional[Sequence[Job]] = None,
    ) -> MatchingResult:
        """
        Score clean jobs with cosine similarity and apply language/dealbreaker gate.

        Excludes postings with integrity_status = 'flagged'.
        """
        result = MatchingResult()

        # 1. Obtain profile vector
        vec = profile_vector or self._cached_profile_vectors.get(account_id)
        if vec is None:
            vec = await self.embed_and_upsert_profile(
                account_id=account_id,
                cv_path=cv_path,
                profile_path=profile_path,
            )

        # 2. Parse language rules from profile
        parsed_profile = ProfileParser.parse(cv_path=cv_path, profile_path=profile_path)
        language_gate = LanguageGate(declared_languages=parsed_profile.declared_languages)

        # 3. Determine clean and flagged jobs to evaluate
        if jobs is not None:
            clean_jobs = [
                j for j in jobs
                if j.account_id == account_id and j.integrity_status == "clean"
            ]
            flagged_jobs = [
                j for j in jobs
                if j.account_id == account_id and j.integrity_status == "flagged"
            ]
            result.skipped_flagged_count = len(flagged_jobs)
            result.total_clean_evaluated = len(clean_jobs)
        else:
            stmt_flagged = select(Job.id).where(
                Job.account_id == account_id,
                Job.integrity_status == "flagged",
            )
            flagged_jobs = self.db.execute(stmt_flagged).all()
            result.skipped_flagged_count = len(flagged_jobs)

            stmt_clean = select(Job).where(
                Job.account_id == account_id,
                Job.integrity_status == "clean",
            )
            clean_jobs = self.db.scalars(stmt_clean).all()
            result.total_clean_evaluated = len(clean_jobs)

        for job in clean_jobs:
            desc = job.description or ""

            # Check Language / Dealbreaker Gate
            is_vetoed, veto_reason = language_gate.check(desc)
            job.vetoed = is_vetoed
            job.veto_reason = veto_reason
            if is_vetoed:
                result.vetoed_count += 1

            # Compute Cosine Similarity embedding score
            if desc.strip() or (job.role and job.role.strip()):
                embed_text = f"Role: {job.role}\nCompany: {job.company}\nDescription:\n{desc}"
                job_vec = await self.embedder.embed(embed_text)
                similarity = compute_cosine_similarity(vec, job_vec)
                
                # Calibrate cosine similarity to realistic 0-100 percentage
                # Baseline for unrelated content is ~0.25; strong match is ~0.75+
                calibrated = (similarity - 0.25) / (0.75 - 0.25) * 100.0
                score = max(15.0, min(95.0, calibrated))

                # Role & target designation alignment boost
                job_title_lower = (job.role or "").lower()
                target_roles = parsed_profile.target_roles_text.lower()
                matched_role = False
                for line in target_roles.splitlines():
                    cleaned_line = line.strip().strip("- *").lower()
                    if cleaned_line and (cleaned_line in job_title_lower or job_title_lower in cleaned_line):
                        matched_role = True
                        break

                if matched_role:
                    score = min(99.0, score + 8.0)
                elif any(kw in job_title_lower for kw in ["ai", "llm", "engineer", "machine learning", "mlops", "python"]):
                    score = min(95.0, score + 3.0)

                job.match_score = round(score, 1)
            else:
                job.match_score = 0.0

            result.scored_count += 1

        if clean_jobs:
            self.db.commit()

        return result

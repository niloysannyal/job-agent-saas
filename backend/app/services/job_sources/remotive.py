import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# Remotive API — no key required, public endpoint.
# Rate-limit advisory: ≤2 req/min, ≤4 req/day recommended by Remotive.
REMOTIVE_BASE_URL = "https://remotive.com/api/remote-jobs"

# Remotive job_type → normalized location/contract label
JOB_TYPE_LABEL: Dict[str, str] = {
    "full_time": "Full-time",
    "part_time": "Part-time",
    "contract": "Contract",
    "freelance": "Freelance",
    "internship": "Internship",
    "other": "Other",
}


def _clean_html(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_publication_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO-ish publication_date from Remotive (no TZ suffix — treat as UTC)."""
    if not date_str:
        return None
    try:
        # Remotive returns e.g. "2026-10-24T12:00:00" — no 'Z', no offset.
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


class RemotiveJobSource(JobSource):
    """
    Remotive API implementation of the JobSource interface (ARCHITECTURE.md §4).
    Covers remote-specific roles worldwide; no API key required.

    Endpoint: GET https://remotive.com/api/remote-jobs
    Optional params: search (keyword), limit (max results).
    The JobSearchQuery.what field is mapped to 'search';
    results_per_page is mapped to 'limit'.
    All Remotive jobs are remote by definition — location_type is always 'remote'.
    """

    def __init__(
        self,
        base_url: str = REMOTIVE_BASE_URL,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url
        self.client = client
        self.timeout = timeout

    def _build_params(self, norm_query: JobSearchQuery) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "search": norm_query.what,
            "limit": norm_query.results_per_page,
        }
        return params

    def _parse_results(self, raw_jobs: List[Dict[str, Any]]) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_jobs:
            source_id = str(item.get("id") or len(postings))
            title = _clean_html(item.get("title") or "Unknown Role")
            company = item.get("company_name") or "Unknown Company"
            description = _clean_html(item.get("description") or "")
            apply_link = item.get("url") or ""
            # Remotive salary is a free-text string (e.g. "$120k - $140k") or blank.
            salary_str: Optional[str] = item.get("salary") or None
            if salary_str:
                salary_str = salary_str.strip() or None

            candidate_location: Optional[str] = item.get("candidate_required_location")
            posted_at = _parse_publication_date(item.get("publication_date"))
            job_type = item.get("job_type") or ""
            tags: List[str] = item.get("tags") or []

            posting = JobPosting(
                id=f"remotive:{source_id}",
                source="remotive",
                company=company,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=salary_str,
                # Remotive does not expose structured min/max salary numbers.
                salary_min=None,
                salary_max=None,
                currency=None,
                location=candidate_location,
                # All Remotive listings are remote by definition.
                location_type="remote",
                # Remotive doesn't provide a single country field; use candidate
                # location as a best-effort proxy and leave country/city unset.
                country=None,
                city=None,
                posted_at=posted_at,
                raw_data=item,
            )
            postings.append(posting)

        return postings

    async def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> List[JobPosting]:
        """
        Asynchronously fetch remote job postings from Remotive matching the query.

        Maps JobSearchQuery.what → 'search' and results_per_page → 'limit'.
        All returned postings have location_type='remote'.
        """
        norm_query = self.normalize_query(query)
        params = self._build_params(norm_query)

        if self.client:
            response = await self.client.get(self.base_url, params=params, timeout=self.timeout)
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)

        if response.status_code != 200:
            raise JobSourceHTTPError(
                f"Remotive API request failed with status {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_text=response.text,
            )

        data = response.json()
        raw_jobs: List[Dict[str, Any]] = data.get("jobs") or []
        return self._parse_results(raw_jobs)

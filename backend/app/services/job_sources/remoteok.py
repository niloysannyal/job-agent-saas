import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# RemoteOK API — no key required, public endpoint.
#
# ToS attribution requirements (from the "legal" field in every API response):
#   1. Link back to the RemoteOK listing URL (the `url` / `apply_url` field) — this
#      URL is stored in JobPosting.apply_link so the data is available.
#   2. The link must be dofollow — NO rel="nofollow" on the <a> tag. This is a
#      render-time constraint: the frontend/template must not add rel="nofollow".
#   3. Mention "Remote OK" as the source visibly near each listing (e.g. "via Remote OK").
#      This is also a render-time constraint — nothing in the current backend enforces it.
#
# Items 2 and 3 are NOT yet satisfied — they require explicit handling when the
# job listing UI is built. The JobPosting.source field contains "remoteok" which
# can be used by the frontend to apply these rules. Until then, do not display
# RemoteOK listings publicly without implementing both requirements.
REMOTEOK_BASE_URL = "https://remoteok.com/api"


def _clean_html(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO 8601 date string from RemoteOK (e.g. '2026-10-24T00:00:02+00:00')."""
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def _format_salary(
    salary_min: Optional[float],
    salary_max: Optional[float],
) -> Optional[str]:
    """Format RemoteOK's numeric salary_min/salary_max into a display string."""
    if salary_min and salary_max and salary_min == salary_max:
        return f"${salary_min:,.0f}"
    if salary_min and salary_max:
        return f"${salary_min:,.0f} - ${salary_max:,.0f}"
    if salary_min:
        return f"From ${salary_min:,.0f}"
    if salary_max:
        return f"Up to ${salary_max:,.0f}"
    return None


class RemoteOKJobSource(JobSource):
    """
    RemoteOK API implementation of the JobSource interface (ARCHITECTURE.md §4).
    Covers remote-specific roles; no API key required.

    Endpoint: GET https://remoteok.com/api?tag=<keyword>
    The response is a JSON array whose first element is a legal-notice object
    (keyed "legal"); the remaining elements are job objects.

    Attribution requirement per RemoteOK ToS: every job's apply_link is set to
    the RemoteOK listing URL so callers honour the link-back requirement.
    All RemoteOK jobs are remote — location_type is always 'remote'.

    Note on query mapping: RemoteOK's ?tag= param performs a tag/keyword search.
    It works best with a single keyword or technology (e.g. "python", "react").
    JobSearchQuery.what is used verbatim.
    """

    def __init__(
        self,
        base_url: str = REMOTEOK_BASE_URL,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url
        self.client = client
        self.timeout = timeout

    def _build_params(self, norm_query: JobSearchQuery) -> Dict[str, Any]:
        # RemoteOK uses ?tag= for keyword/technology filtering.
        return {"tag": norm_query.what}

    def _parse_results(self, raw_jobs: List[Dict[str, Any]]) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_jobs:
            # Skip the legal-notice entry (first element, has no 'id' as an int).
            if "legal" in item or not item.get("id"):
                continue

            source_id = str(item["id"])
            title = _clean_html(item.get("position") or "Unknown Role")
            company = item.get("company") or "Unknown Company"
            description = _clean_html(item.get("description") or "")
            # apply_url is the canonical RemoteOK listing URL — required for ToS attribution.
            apply_link = item.get("apply_url") or item.get("url") or ""

            salary_min_raw = item.get("salary_min")
            salary_max_raw = item.get("salary_max")
            # RemoteOK returns 0 when salary is not specified — treat 0 as absent.
            salary_min = float(salary_min_raw) if salary_min_raw else None
            salary_max = float(salary_max_raw) if salary_max_raw else None
            salary_str = _format_salary(salary_min, salary_max)

            location: Optional[str] = item.get("location") or None
            posted_at = _parse_date(item.get("date"))

            posting = JobPosting(
                id=f"remoteok:{source_id}",
                source="remoteok",
                company=company,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=salary_str,
                salary_min=salary_min,
                salary_max=salary_max,
                # RemoteOK salaries are USD-denominated (no per-country variant).
                currency="$" if (salary_min or salary_max) else None,
                location=location,
                # All RemoteOK listings are remote by definition.
                location_type="remote",
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
        Asynchronously fetch remote job postings from RemoteOK matching the query.

        Maps JobSearchQuery.what → '?tag=' query parameter.
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
                f"RemoteOK API request failed with status {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_text=response.text,
            )

        raw_array: List[Dict[str, Any]] = response.json()
        # The first element is always the legal-notice dict; _parse_results skips it.
        return self._parse_results(raw_array)

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource, classify_location_type
from app.services.job_sources.exceptions import JobSourceHTTPError

# freehire.me public REST API — keyless for personal/non-commercial use.
# Endpoint: GET https://freehire.me/api/v1/jobs/search
# General/aggregator tech job source (is_per_company = False).
FREEHIRE_BASE_URL = "https://freehire.me/api/v1/jobs/search"


def _clean_html(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_iso_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO 8601 date string with timezone."""
    if not date_str:
        return None
    try:
        normalized = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except (ValueError, TypeError):
        return None


def _detect_location_type(
    work_mode: Optional[str],
    location_name: Optional[str],
    title: str,
) -> str:
    """Determine location type using centralized classifier."""
    return classify_location_type(
        explicit_mode=work_mode,
        location_name=location_name,
        title=title,
    )


class FreehireJobSource(JobSource):
    """
    freehire.me API implementation of the JobSource interface (ARCHITECTURE.md §4).
    General/aggregator source covering tech roles worldwide (is_per_company = False).

    Endpoint: GET https://freehire.me/api/v1/jobs/search
    Query mapping:
      - JobSearchQuery.what → 'q' (search keyword/title)
      - results_per_page   → 'limit'
      - page               → 'offset' ((page - 1) * results_per_page)
      - country            → 'countries' (if specified)
      - salary_min         → 'salary_min' (if specified)
    """

    is_per_company: bool = False

    def __init__(
        self,
        base_url: str = FREEHIRE_BASE_URL,
        api_key: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.client = client
        self.timeout = timeout

    def _build_params(self, norm_query: JobSearchQuery) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "q": norm_query.what,
            "limit": norm_query.results_per_page,
        }
        if norm_query.page > 1:
            params["offset"] = (norm_query.page - 1) * norm_query.results_per_page

        if norm_query.country and norm_query.country.lower() not in ("all", ""):
            params["countries"] = norm_query.country.lower()

        if norm_query.salary_min is not None:
            params["salary_min"] = norm_query.salary_min

        return params

    def _build_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": "JobAgentSaaS/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _parse_results(self, raw_jobs: List[Dict[str, Any]]) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_jobs:
            source_id = str(
                item.get("public_slug")
                or item.get("external_id")
                or len(postings)
            )
            title = _clean_html(item.get("title") or "Unknown Role")
            company = item.get("company") or item.get("company_slug") or "Unknown Company"
            description = _clean_html(item.get("description") or "")
            apply_link = item.get("url") or ""

            location_name = item.get("location") or None
            work_mode = item.get("work_mode")
            location_type = _detect_location_type(work_mode, location_name, title)

            # Countries & Cities are arrays in freehire
            countries: List[str] = item.get("countries") or []
            cities: List[str] = item.get("cities") or []
            country = countries[0] if countries else None
            city = cities[0] if cities else None

            # Salary extraction
            salary_str: Optional[str] = None
            salary_min: Optional[float] = None
            salary_max: Optional[float] = None
            currency: Optional[str] = item.get("currency")

            raw_salary = item.get("salary")
            if isinstance(raw_salary, str) and raw_salary.strip():
                salary_str = raw_salary.strip()
            elif isinstance(raw_salary, (int, float)):
                salary_str = str(raw_salary)

            raw_s_min = item.get("salary_min")
            if raw_s_min is not None:
                try:
                    salary_min = float(raw_s_min)
                except (ValueError, TypeError):
                    pass

            raw_s_max = item.get("salary_max")
            if raw_s_max is not None:
                try:
                    salary_max = float(raw_s_max)
                except (ValueError, TypeError):
                    pass

            if not salary_str and salary_min is not None and salary_max is not None:
                curr_prefix = f"{currency} " if currency else ""
                salary_str = f"{curr_prefix}{int(salary_min) if salary_min.is_integer() else salary_min} - {int(salary_max) if salary_max.is_integer() else salary_max}"

            posted_at = _parse_iso_date(item.get("posted_at") or item.get("created_at"))

            posting = JobPosting(
                id=f"freehire:{source_id}",
                source="freehire",
                company=company,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=salary_str,
                salary_min=salary_min,
                salary_max=salary_max,
                currency=currency,
                location=location_name or city,
                location_type=location_type,
                country=country,
                city=city,
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
        Asynchronously fetch job postings from freehire.me matching the query.

        Query is normalized into JobSearchQuery where .what is sent as keyword parameter 'q'.
        """
        norm_query = self.normalize_query(query)
        params = self._build_params(norm_query)
        headers = self._build_headers()

        if self.client:
            response = await self.client.get(
                self.base_url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=headers,
                )

        if response.status_code != 200:
            raise JobSourceHTTPError(
                f"freehire.me API request failed with status {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_text=response.text,
            )

        data = response.json()
        raw_jobs: List[Dict[str, Any]] = data.get("data") if isinstance(data, dict) else []
        return self._parse_results(raw_jobs)

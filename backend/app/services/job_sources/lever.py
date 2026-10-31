import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource, classify_location_type
from app.services.job_sources.exceptions import JobSourceHTTPError

# Lever public Postings API — no API key required.
# Endpoint: GET https://api.lever.co/v0/postings/{company}?mode=json
#
# Query mapping: JobSearchQuery.what is treated as the company board token/slug
# (e.g. "spotify", "netflix"). This source is per-company, not a general
# keyword search — it returns all open roles for that company.
LEVER_BASE_URL = "https://api.lever.co/v0/postings"


def _clean_html(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_created_at(val: Any) -> Optional[datetime]:
    """Parse createdAt which Lever provides as epoch milliseconds or ISO string."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        try:
            return datetime.fromtimestamp(val / 1000.0, tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None
    if isinstance(val, str):
        try:
            # Handle numeric string timestamp
            num = float(val)
            return datetime.fromtimestamp(num / 1000.0, tz=timezone.utc)
        except ValueError:
            pass
        try:
            normalized = val.replace("Z", "+00:00")
            return datetime.fromisoformat(normalized)
        except (ValueError, TypeError):
            return None
    return None


def _detect_location_type(
    workplace_type: Optional[str],
    location_name: Optional[str],
    title: str,
) -> str:
    """Determine location type using centralized classifier."""
    return classify_location_type(
        explicit_mode=workplace_type,
        location_name=location_name,
        title=title,
    )


class LeverJobSource(JobSource):
    """
    Lever public Postings API implementation of the JobSource interface
    (ARCHITECTURE.md §4).

    This source is per-company, not a general keyword search. Pass the company's
    Lever board slug as the query (e.g. "spotify", "netflix").

    Query normalization:
      - JobSearchQuery.what  → company board token/slug (required)
      - All open roles for that company are returned.

    No API key required.
    """

    is_per_company: bool = True

    def __init__(
        self,
        base_url: str = LEVER_BASE_URL,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
        page_size: int = 100,
        max_pages: int = 10,
        max_postings: int = 500,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.timeout = timeout
        self.page_size = page_size
        self.max_pages = max_pages
        self.max_postings = max_postings

    def _build_url(self, company_slug: str) -> str:
        return f"{self.base_url}/{company_slug}"

    def _extract_description(self, item: Dict[str, Any]) -> str:
        parts: List[str] = []

        # 1. Main body
        body = item.get("descriptionPlain")
        if not body:
            body = _clean_html(item.get("description"))
        if body:
            parts.append(body.strip())

        # 2. Lists sections (e.g. "What You'll Do", "Who You Are")
        lists: List[Dict[str, Any]] = item.get("lists") or []
        for lst in lists:
            header = lst.get("text") or ""
            content = _clean_html(lst.get("content"))
            if header and content:
                parts.append(f"{header.strip()}:\n{content.strip()}")
            elif content:
                parts.append(content.strip())

        # 3. Additional info (e.g. compensation, perks)
        additional = item.get("additionalPlain")
        if not additional:
            additional = _clean_html(item.get("additional"))
        if additional:
            parts.append(additional.strip())

        return "\n\n".join(parts)

    def _parse_results(
        self,
        raw_jobs: List[Dict[str, Any]],
        company_slug: str,
    ) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_jobs:
            source_id = str(item.get("id") or len(postings))
            title = item.get("text") or "Unknown Role"
            company = company_slug

            description = self._extract_description(item)
            apply_link = item.get("hostedUrl") or item.get("applyUrl") or ""

            categories: Dict[str, Any] = item.get("categories") or {}
            location_name: Optional[str] = (
                categories.get("location") if isinstance(categories, dict) else None
            )

            workplace_type = item.get("workplaceType")
            location_type = _detect_location_type(workplace_type, location_name, title)
            country = item.get("country")

            # Salary range if structured
            salary_range = item.get("salaryRange")
            salary_str: Optional[str] = None
            salary_min: Optional[float] = None
            salary_max: Optional[float] = None
            currency: Optional[str] = None

            if isinstance(salary_range, dict):
                min_raw = salary_range.get("min")
                max_raw = salary_range.get("max")
                currency = salary_range.get("currency")
                interval = salary_range.get("interval") or "year"

                try:
                    if min_raw is not None:
                        salary_min = float(min_raw)
                    if max_raw is not None:
                        salary_max = float(max_raw)
                except (ValueError, TypeError):
                    pass

                if salary_min is not None and salary_max is not None:
                    curr_prefix = f"{currency} " if currency else ""
                    salary_str = f"{curr_prefix}{int(salary_min) if salary_min.is_integer() else salary_min} - {int(salary_max) if salary_max.is_integer() else salary_max} / {interval}"
                elif salary_min is not None:
                    curr_prefix = f"{currency} " if currency else ""
                    salary_str = f"{curr_prefix}{int(salary_min) if salary_min.is_integer() else salary_min} / {interval}"

            posted_at = _parse_created_at(item.get("createdAt"))

            posting = JobPosting(
                id=f"lever:{source_id}",
                source="lever",
                company=company,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=salary_str,
                salary_min=salary_min,
                salary_max=salary_max,
                currency=currency,
                location=location_name,
                location_type=location_type,
                country=country,
                city=None,
                posted_at=posted_at,
                raw_data=item,
            )
            postings.append(posting)

        return postings

    async def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
        max_pages: Optional[int] = None,
        max_postings: Optional[int] = None,
    ) -> List[JobPosting]:
        """
        Asynchronously fetch all open job postings for a company from Lever,
        traversing offset pagination via skip/limit parameters up to the safety limit.

        Pass the company's Lever board slug as the query (string, dict with
        'what', or JobSearchQuery.what). All open roles for that company are
        returned in JSON mode.
        """
        norm_query = self.normalize_query(query)
        company_slug = norm_query.what.strip().lower()
        url = self._build_url(company_slug)

        effective_max_pages = max_pages if max_pages is not None else self.max_pages
        effective_max_postings = max_postings if max_postings is not None else self.max_postings

        all_raw_jobs: List[Dict[str, Any]] = []
        seen_job_ids = set()
        pages_fetched = 0
        skip = 0

        async def _do_fetch(client: httpx.AsyncClient) -> None:
            nonlocal skip, pages_fetched
            while pages_fetched < effective_max_pages and len(all_raw_jobs) < effective_max_postings:
                pages_fetched += 1
                params: Dict[str, Any] = {"mode": "json"}
                if self.page_size != 100:
                    params["limit"] = self.page_size
                if skip > 0:
                    params["skip"] = skip

                response = await client.get(url, params=params, timeout=self.timeout)
                if response.status_code != 200:
                    raise JobSourceHTTPError(
                        f"Lever API request failed for company '{company_slug}' "
                        f"with status {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                data = response.json()
                raw_jobs: List[Dict[str, Any]] = data if isinstance(data, list) else []
                if not raw_jobs:
                    break

                for item in raw_jobs:
                    jid = item.get("id")
                    if jid is None or jid not in seen_job_ids:
                        if jid is not None:
                            seen_job_ids.add(jid)
                        all_raw_jobs.append(item)
                        if len(all_raw_jobs) >= effective_max_postings:
                            break

                skip += len(raw_jobs)

                # If the batch returned fewer than page_size items, we have reached the end
                if len(raw_jobs) < self.page_size:
                    break

        if self.client:
            await _do_fetch(self.client)
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                await _do_fetch(client)

        return self._parse_results(all_raw_jobs, company_slug)

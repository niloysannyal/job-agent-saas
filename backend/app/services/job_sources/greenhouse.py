import re
from datetime import datetime, timezone
from html import unescape
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource, classify_location_type
from app.services.job_sources.exceptions import JobSourceHTTPError

# Greenhouse public Job Board API — no API key required.
# Endpoint: GET https://boards-api.greenhouse.io/v1/boards/{company}/jobs
# Optional: ?content=true to include the full HTML job description.
#
# Query mapping: JobSearchQuery.what is treated as the company board token/slug
# (e.g. "greenhouse", "stripe", "shopify"). This source is per-company, not
# a general keyword search — it returns all open roles for that company.
# The caller filters by company slug, not by keyword.
#
# Content encoding note: Greenhouse double-encodes the `content` field.
# The JSON value is an HTML string that has itself been HTML-entity-escaped,
# so \u0026lt; = &lt; = < and \u0026amp; = &amp; = &. We unescape twice.
GREENHOUSE_BASE_URL = "https://boards-api.greenhouse.io/v1/boards"


def _unescape_greenhouse_content(raw: Optional[str]) -> str:
    """
    Unescape Greenhouse's double-encoded HTML content field.
    The field is HTML-escaped twice: first the content is HTML, then the whole
    string is HTML-entity-escaped again before being placed in the JSON value.
    """
    if not raw:
        return ""
    return unescape(unescape(raw))


def _clean_html(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_iso_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO 8601 date string (with optional timezone offset)."""
    if not date_str:
        return None
    try:
        # Python 3.11+ handles offset-aware ISO strings natively.
        # Replace Z with +00:00 for older Pythons.
        normalized = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except (ValueError, TypeError):
        return None


def _detect_location_type(location_name: Optional[str], title: str) -> str:
    """Infer location type from the location string and title using centralized classifier."""
    return classify_location_type(location_name=location_name, title=title)


class GreenhouseJobSource(JobSource):
    """
    Greenhouse public Job Board API implementation of the JobSource interface
    (ARCHITECTURE.md §4).

    This source is per-company, not a general keyword search. Pass the company's
    Greenhouse board token/slug as the query (e.g. "stripe", "shopify").

    Query normalization:
      - JobSearchQuery.what  → company board token/slug (required)
      - All other JobSearchQuery fields are ignored; Greenhouse returns all open
        roles for the company and does not support server-side keyword filtering
        on the public board endpoint.

    The ?content=true parameter is always included to get the full description.
    No API key required.
    """

    is_per_company: bool = True

    def __init__(
        self,
        base_url: str = GREENHOUSE_BASE_URL,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
        max_pages: int = 10,
        max_postings: int = 500,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.timeout = timeout
        self.max_pages = max_pages
        self.max_postings = max_postings

    @staticmethod
    def _extract_next_link(response: httpx.Response) -> Optional[str]:
        """
        Extract the RFC 5988 'next' relation URL from the HTTP Link response header.
        Supports both httpx.Response.links parsing and regex extraction fallback.
        """
        try:
            if hasattr(response, "links") and response.links:
                next_entry = response.links.get("next")
                if next_entry and isinstance(next_entry, dict) and next_entry.get("url"):
                    return str(next_entry["url"])
        except Exception:
            pass

        link_header = response.headers.get("link") or response.headers.get("Link")
        if link_header:
            match = re.search(r'<([^>]+)>;\s*rel="?next"?', link_header, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _build_url(self, company_slug: str) -> str:
        return f"{self.base_url}/{company_slug}/jobs"

    def _parse_results(
        self,
        raw_jobs: List[Dict[str, Any]],
        company_slug: str,
    ) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_jobs:
            source_id = str(item.get("id") or len(postings))
            title = item.get("title") or "Unknown Role"
            # company_name is included in the response when ?content=true is set
            company = item.get("company_name") or company_slug

            # content is double-encoded HTML; unescape then strip tags
            raw_content = item.get("content") or ""
            description = _clean_html(_unescape_greenhouse_content(raw_content))

            apply_link = item.get("absolute_url") or ""

            location_info = item.get("location") or {}
            location_name: Optional[str] = (
                location_info.get("name") if isinstance(location_info, dict) else None
            )

            # Department and office from their respective arrays
            departments: List[Dict] = item.get("departments") or []
            offices: List[Dict] = item.get("offices") or []
            department_name: Optional[str] = (
                departments[0].get("name") if departments else None
            )
            office_name: Optional[str] = (
                offices[0].get("name") if offices else None
            )

            location_type = _detect_location_type(location_name, title)
            # Use location_name as the primary display, fall back to office
            display_location = location_name or office_name

            # Greenhouse public board has no salary field — it's sometimes
            # embedded in the description. We surface None; the posting guard
            # and/or LLM scoring will see it in the description text.
            posted_at = _parse_iso_date(item.get("first_published"))
            updated_at = _parse_iso_date(item.get("updated_at"))

            posting = JobPosting(
                id=f"greenhouse:{source_id}",
                source="greenhouse",
                company=company,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=None,         # not available on public board endpoint
                salary_min=None,
                salary_max=None,
                currency=None,
                location=display_location,
                location_type=location_type,
                country=office_name,  # closest available country-level field
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
        Asynchronously fetch all open job postings for a company from Greenhouse,
        traversing RFC 5988 Link headers across pages up to the safety limit.

        Pass the company's Greenhouse board slug as the query (string, dict with
        'what', or JobSearchQuery.what). All open roles for that company are
        returned; server-side keyword filtering is not supported by this API.
        """
        norm_query = self.normalize_query(query)
        company_slug = norm_query.what.strip().lower()
        url = self._build_url(company_slug)

        effective_max_pages = max_pages if max_pages is not None else self.max_pages
        effective_max_postings = max_postings if max_postings is not None else self.max_postings

        all_raw_jobs: List[Dict[str, Any]] = []
        seen_job_ids = set()
        visited_urls = set()
        current_url: Optional[str] = url
        current_params: Optional[Dict[str, Any]] = {"content": "true"}
        pages_fetched = 0

        async def _do_fetch(client: httpx.AsyncClient) -> None:
            nonlocal current_url, current_params, pages_fetched
            while current_url and pages_fetched < effective_max_pages and len(all_raw_jobs) < effective_max_postings:
                pages_fetched += 1

                response = await client.get(current_url, params=current_params, timeout=self.timeout)
                visited_urls.add(str(response.url))

                if response.status_code != 200:
                    raise JobSourceHTTPError(
                        f"Greenhouse API request failed for company '{company_slug}' "
                        f"with status {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                data = response.json()
                raw_jobs: List[Dict[str, Any]] = data.get("jobs") or []
                for item in raw_jobs:
                    jid = item.get("id")
                    if jid is None or jid not in seen_job_ids:
                        if jid is not None:
                            seen_job_ids.add(jid)
                        all_raw_jobs.append(item)
                        if len(all_raw_jobs) >= effective_max_postings:
                            break

                if len(all_raw_jobs) >= effective_max_postings:
                    break

                raw_next = self._extract_next_link(response)
                if raw_next:
                    next_resolved = urljoin(str(response.url), raw_next)
                    if next_resolved in visited_urls:
                        break
                    current_url = next_resolved
                    current_params = None  # Query parameters are already encoded in the link URL
                else:
                    current_url = None

        if self.client:
            await _do_fetch(self.client)
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                await _do_fetch(client)

        return self._parse_results(all_raw_jobs, company_slug)

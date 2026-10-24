import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import httpx

from app.core.config import settings
from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource
from app.services.job_sources.exceptions import (
    JobSourceConfigError,
    JobSourceHTTPError,
)

# Currency symbol mapping by Adzuna country code
COUNTRY_CURRENCY_SYMBOLS: Dict[str, str] = {
    "gb": "£",
    "us": "$",
    "ca": "CA$",
    "au": "AU$",
    "de": "€",
    "fr": "€",
    "it": "€",
    "es": "€",
    "nl": "€",
    "at": "€",
    "be": "€",
    "in": "₹",
    "pl": "zł",
    "br": "R$",
    "mx": "MX$",
    "nz": "NZ$",
    "sg": "SG$",
    "za": "R",
}


def _clean_text(text: Optional[str]) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    return " ".join(cleaned.split())


def _parse_created_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO formatted creation date from Adzuna response."""
    if not date_str:
        return None
    try:
        normalized = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except (ValueError, TypeError):
        return None


def _format_salary(
    salary_min: Optional[float],
    salary_max: Optional[float],
    country: str,
) -> Optional[str]:
    """Format salary range into a human-readable display string."""
    symbol = COUNTRY_CURRENCY_SYMBOLS.get(country.lower(), "$")
    if salary_min is not None and salary_max is not None:
        if salary_min == salary_max:
            return f"{symbol}{salary_min:,.0f}"
        return f"{symbol}{salary_min:,.0f} - {symbol}{salary_max:,.0f}"
    if salary_min is not None:
        return f"From {symbol}{salary_min:,.0f}"
    if salary_max is not None:
        return f"Up to {symbol}{salary_max:,.0f}"
    return None


def _detect_location_type(
    title: str,
    description: str,
    location_name: Optional[str],
) -> str:
    """Infer location type (remote, hybrid, on-site) from job fields."""
    combined = f"{title} {description} {location_name or ''}".lower()
    if "remote" in combined or "work from home" in combined or "wfh" in combined:
        return "remote"
    if "hybrid" in combined:
        return "hybrid"
    return "on-site"


class AdzunaJobSource(JobSource):
    """
    Adzuna API implementation of the JobSource interface (ARCHITECTURE.md §4).
    Fetches real job listings across 19 countries without web scraping.
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        base_url: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
    ):
        self.app_id = app_id or settings.ADZUNA_APP_ID
        self.app_key = app_key or settings.ADZUNA_APP_KEY
        self.base_url = (base_url or settings.ADZUNA_BASE_URL).rstrip("/")
        self.client = client
        self.timeout = timeout

    def _validate_credentials(self) -> None:
        if not self.app_id or not self.app_key:
            raise JobSourceConfigError(
                "Adzuna app_id and app_key must be configured via environment "
                "variables (ADZUNA_APP_ID, ADZUNA_APP_KEY) or provided directly to AdzunaJobSource."
            )

    def _build_url_and_params(
        self,
        norm_query: JobSearchQuery,
    ) -> tuple[str, Dict[str, Any]]:
        country = norm_query.country.lower()
        page = norm_query.page
        url = f"{self.base_url}/jobs/{country}/search/{page}"

        params: Dict[str, Any] = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": norm_query.what,
            "results_per_page": norm_query.results_per_page,
            "content-type": "application/json",
        }

        if norm_query.where:
            params["where"] = norm_query.where
        if norm_query.salary_min is not None:
            params["salary_min"] = norm_query.salary_min
        if norm_query.salary_max is not None:
            params["salary_max"] = norm_query.salary_max
        if norm_query.full_time:
            params["full_time"] = 1
        if norm_query.permanent:
            params["permanent"] = 1
        if norm_query.contract:
            params["contract"] = 1
        if norm_query.max_days_old is not None:
            params["max_days_old"] = norm_query.max_days_old
        if norm_query.distance is not None:
            params["distance"] = norm_query.distance

        return url, params

    def _parse_results(
        self,
        raw_results: List[Dict[str, Any]],
        norm_query: JobSearchQuery,
    ) -> List[JobPosting]:
        postings: List[JobPosting] = []

        for item in raw_results:
            source_id = str(item.get("id") or "")
            title = _clean_text(item.get("title") or "Unknown Role")

            company_info = item.get("company")
            company_name = (
                company_info.get("display_name")
                if isinstance(company_info, dict)
                else None
            ) or "Unknown Company"

            description = _clean_text(item.get("description") or "")
            apply_link = item.get("redirect_url") or ""

            salary_min = (
                float(item["salary_min"])
                if item.get("salary_min") is not None
                else None
            )
            salary_max = (
                float(item["salary_max"])
                if item.get("salary_max") is not None
                else None
            )
            salary_str = _format_salary(salary_min, salary_max, norm_query.country)

            location_info = item.get("location")
            location_dict = location_info if isinstance(location_info, dict) else {}
            location_display = location_dict.get("display_name")
            areas = location_dict.get("area") or []

            country = areas[0] if (areas and isinstance(areas, list)) else norm_query.country.upper()
            city = location_display or (areas[-1] if len(areas) > 1 else None)
            location_type = _detect_location_type(title, description, location_display)
            posted_at = _parse_created_date(item.get("created"))

            posting = JobPosting(
                id=f"adzuna:{source_id}" if source_id else f"adzuna:{len(postings)}",
                source="adzuna",
                company=company_name,
                role=title,
                description=description,
                apply_link=apply_link,
                salary=salary_str,
                salary_min=salary_min,
                salary_max=salary_max,
                currency=COUNTRY_CURRENCY_SYMBOLS.get(norm_query.country.lower(), "$"),
                location=location_display,
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
        Asynchronously fetch job postings matching the query from Adzuna.
        """
        self._validate_credentials()
        norm_query = self.normalize_query(query)
        url, params = self._build_url_and_params(norm_query)

        if self.client:
            response = await self.client.get(url, params=params, timeout=self.timeout)
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)

        if response.status_code != 200:
            raise JobSourceHTTPError(
                f"Adzuna API request failed with status {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_text=response.text,
            )

        data = response.json()
        raw_results = data.get("results") or []
        return self._parse_results(raw_results, norm_query)

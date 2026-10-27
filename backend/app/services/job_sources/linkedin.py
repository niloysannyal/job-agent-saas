import asyncio
import html
import logging
import random
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.base import JobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

logger = logging.getLogger(__name__)

LINKEDIN_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
LINKEDIN_USER_AGENT = "Mozilla/5.0 (compatible; linkedin-search-cli/1.0)"


def _strip_tags(text: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    return " ".join(cleaned.split())


class LinkedInJobSource(JobSource):
    """
    LinkedIn public guest API implementation of the JobSource interface (ARCHITECTURE.md §4).
    General/aggregator source covering public job postings without requiring authentication.

    Endpoint: GET https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
    Query mapping:
      - JobSearchQuery.what  -> 'keywords'
      - JobSearchQuery.where -> 'location' (default: 'Remote')
      - results_per_page     -> limit on parsed cards
      - page                 -> 'start' ((page - 1) * results_per_page)
    """

    is_per_company: bool = False

    def __init__(
        self,
        base_url: str = LINKEDIN_SEARCH_URL,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url
        self._external_client = client
        self.timeout = timeout

    async def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> List[JobPosting]:
        norm_query = self.normalize_query(query)
        keywords = norm_query.what or "AI Engineer"
        location = norm_query.where or "Remote"
        page = max(1, norm_query.page)
        limit = min(norm_query.results_per_page or 10, 50)
        start = (page - 1) * limit

        params = {
            "keywords": keywords,
            "location": location,
            "start": str(start),
        }
        headers = {
            "User-Agent": LINKEDIN_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
        }

        html_content = await self._fetch_html_with_backoff(params, headers)
        if not html_content:
            return []

        postings = self._parse_job_cards(html_content, limit=limit)
        logger.info(f"LinkedInJobSource: Fetched {len(postings)} postings for '{keywords}' in '{location}'")
        return postings

    async def _fetch_html_with_backoff(
        self,
        params: Dict[str, str],
        headers: Dict[str, str],
        max_retries: int = 3,
    ) -> str:
        delay = 0.5
        for attempt in range(max_retries + 1):
            try:
                if self._external_client:
                    resp = await self._external_client.get(
                        self.base_url,
                        params=params,
                        headers=headers,
                        timeout=self.timeout,
                    )
                else:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        resp = await client.get(
                            self.base_url,
                            params=params,
                            headers=headers,
                        )

                if resp.status_code == 200:
                    return resp.text
                if resp.status_code == 404:
                    return ""
                if resp.status_code in (429, 500, 502, 503, 504):
                    if attempt == max_retries:
                        logger.warning(f"LinkedIn jobs endpoint returned status {resp.status_code} after retries.")
                        return ""
                    jitter = random.uniform(0.1, 0.4)
                    await asyncio.sleep(delay + jitter)
                    delay *= 2
                    continue

                logger.warning(f"LinkedIn jobs endpoint unexpected status: {resp.status_code}")
                return ""
            except (httpx.TimeoutException, httpx.RequestError) as e:
                if attempt == max_retries:
                    logger.warning(f"LinkedIn jobs request failed: {e}")
                    return ""
                await asyncio.sleep(delay)
                delay *= 2

        return ""

    def _parse_job_cards(self, raw_html: str, limit: int = 10) -> List[JobPosting]:
        postings: List[JobPosting] = []
        chunks = raw_html.split('data-entity-urn="urn:li:jobPosting:')[1:]

        for chunk in chunks:
            if len(postings) >= limit:
                break

            # Extract job ID
            id_match = re.match(r"^(\d+)", chunk)
            if not id_match:
                continue
            job_id = id_match.group(1)

            # Extract Job URL
            link_match = re.search(r'class="base-card__full-link[^"]*"[^>]*href="([^"]+)"', chunk, re.I)
            url = link_match.group(1).split("?")[0] if link_match else f"https://www.linkedin.com/jobs/view/{job_id}"
            url = html.unescape(url)

            # Extract Title
            title = None
            h3_match = re.search(r'class="base-search-card__title"[^>]*>([\s\S]*?)<\/h3>', chunk, re.I)
            if h3_match:
                title = _strip_tags(h3_match.group(1))
            if not title:
                sr_match = re.search(r'class="sr-only"[^>]*>([\s\S]*?)<\/span>', chunk, re.I)
                if sr_match:
                    title = _strip_tags(sr_match.group(1))
            if not title:
                continue

            # Extract Company
            company = "Unknown Company"
            sub_match = re.search(r'class="base-search-card__subtitle"[^>]*>([\s\S]*?)<\/h4>', chunk, re.I)
            if sub_match:
                company = _strip_tags(sub_match.group(1)) or company

            # Extract Location
            location = "Remote"
            loc_match = re.search(r'class="job-search-card__location"[^>]*>([\s\S]*?)<\/span>', chunk, re.I)
            if loc_match:
                location = _strip_tags(loc_match.group(1)) or location

            # Extract Posted Date
            dt_match = re.search(r'class="job-search-card__listdate[^"]*"[^>]*datetime="([^"]+)"', chunk, re.I)
            posted_at = None
            if dt_match:
                try:
                    posted_at = datetime.fromisoformat(dt_match.group(1)).replace(tzinfo=timezone.utc)
                except Exception:
                    posted_at = datetime.now(timezone.utc)
            else:
                posted_at = datetime.now(timezone.utc)

            # Detect work mode
            work_mode = "remote" if "remote" in f"{title} {location}".lower() else "on-site"

            description = (
                f"{title} position at {company} in {location}. "
                f"Sourced via LinkedIn public jobs radar. View posting and apply directly: {url}"
            )

            posting = JobPosting(
                id=f"linkedin-{job_id}",
                source="linkedin",
                role=title,
                company=company,
                location=location,
                location_type=work_mode,
                job_type=work_mode,
                description=description,
                apply_link=url,
                salary="Negotiable / Undisclosed",
                posted_at=posted_at,
                integrity_status="clean",
                currency="USD",
            )
            postings.append(posting)

        return postings

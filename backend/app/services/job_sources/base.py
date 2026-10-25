from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from app.models.job import JobPosting, JobSearchQuery


class JobSource(ABC):
    """
    Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:
    async def fetch(query) -> list[JobPosting]
    
    Every source (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, etc.)
    implements this interface, ensuring the ingestion pipeline is decoupled
    from specific upstream APIs.

    CALLER CONTRACT — Two distinct categories of job sources:
    ---------------------------------------------------------
    1. General / Aggregator Sources (is_per_company = False):
       Examples: Adzuna, Remotive, RemoteOK, and freehire.me.
       - Query semantic: `query.what` is a role title, keyword, or skill
         (e.g., "Python Backend Developer", "ML Engineer").
       - Ingestion pattern: Broadcast the user's desired job search queries
         across these sources to find matching postings from any company.

    2. Per-Company ATS Sources (is_per_company = True):
       Examples: Greenhouse, Lever, and Ashby.
       - Query semantic: `query.what` (or string query) represents a single
         company's public job-board token / slug (e.g., "stripe", "spotify").
       - Ingestion pattern: Call ONCE PER ENTRY in the user's target-company list.
         Do NOT broadcast the same role search term to every source! Passing a
         job title like "Senior Python Developer" to a per-company source will
         attempt to query a company board with that slug and result in an HTTP 404.
    """

    is_per_company: bool = False

    @abstractmethod
    async def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> List[JobPosting]:
        """
        Asynchronously fetch job postings matching the query.
        
        IMPORTANT CALLER BEHAVIOR NOTE:
        - For general sources (Adzuna, Remotive, RemoteOK; is_per_company=False):
          `query` contains job search keywords, role titles, and location filters.
          Broadcast the user's desired job titles across these sources.
        - For per-company sources (Greenhouse, Lever; is_per_company=True):
          `query` (specifically `query.what` or a string) represents a company's
          job-board token / slug (e.g. "stripe", "spotify"). These sources must
          be invoked once per company in the user's Target Company list, NOT
          broadcast with role search keywords.

        Args:
            query: JobSearchQuery, search term or company slug string, or dict of parameters.
            
        Returns:
            list[JobPosting]: Standardized list of JobPosting objects.
        """
        pass

    def normalize_query(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> JobSearchQuery:
        """
        Helper method to normalize search input into a JobSearchQuery instance.
        """
        if isinstance(query, JobSearchQuery):
            return query
        if isinstance(query, str):
            return JobSearchQuery(what=query)
        if isinstance(query, dict):
            return JobSearchQuery(**query)
        raise TypeError(f"Unsupported query type: {type(query)}")

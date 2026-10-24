from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from app.models.job import JobSearchQuery


class JobPostingList(list):
    """
    A list of JobPosting objects that can also be awaited in async contexts.
    Enables callers to do either:
        postings = source.fetch(query)
    or:
        postings = await source.fetch(query)
    """
    def __await__(self):
        async def _identity():
            return self
        return _identity().__await__()


class JobSource(ABC):
    """
    Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:
    JobSource.fetch(query) -> list[JobPosting]
    
    Every source (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, JSearch)
    implements this interface, ensuring the ingestion pipeline is decoupled
    from specific upstream APIs.
    """

    @abstractmethod
    def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> JobPostingList:
        """
        Fetch job postings matching the query.
        
        Args:
            query: JobSearchQuery, search term string, or dict of query parameters.
            
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

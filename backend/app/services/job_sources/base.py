from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from app.models.job import JobPosting, JobSearchQuery


class JobSource(ABC):
    """
    Plugin interface for all job sourcing integrations per ARCHITECTURE.md §4:
    async def fetch(query) -> list[JobPosting]
    
    Every source (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, JSearch)
    implements this interface, ensuring the ingestion pipeline is decoupled
    from specific upstream APIs.
    """

    @abstractmethod
    async def fetch(
        self,
        query: Union[JobSearchQuery, str, Dict[str, Any]],
    ) -> List[JobPosting]:
        """
        Asynchronously fetch job postings matching the query.
        
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

from datetime import datetime, timezone

import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.remotive import RemotiveJobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# ---------------------------------------------------------------------------
# Mock response shape matching the real Remotive API
# ---------------------------------------------------------------------------
MOCK_REMOTIVE_RESPONSE = {
    "0-legal-notice": "Remotive.com legal notice",
    "job-count": 3,
    "jobs": [
        {
            "id": 165432,
            "url": "https://remotive.com/remote-jobs/software-dev/senior-backend-engineer-165432",
            "title": "Senior <strong>Python</strong> Engineer",
            "company_name": "CloudStack Inc",
            "company_logo": "https://remotive.com/job-logos/cloudstack.png",
            "category": "Software Development",
            "tags": ["python", "fastapi", "remote"],
            "job_type": "full_time",
            "publication_date": "2026-10-24T08:00:00",
            "candidate_required_location": "Worldwide",
            "salary": "$120,000 - $150,000",
            "description": "<p>Build scalable <strong>FastAPI</strong> services and data pipelines.</p>",
        },
        {
            "id": 165433,
            "url": "https://remotive.com/remote-jobs/software-dev/ml-engineer-165433",
            "title": "ML Engineer",
            "company_name": "DataAI Corp",
            "company_logo": None,
            "category": "Data",
            "tags": ["machine learning", "python", "aws"],
            "job_type": "contract",
            "publication_date": "2026-10-23T10:30:00",
            "candidate_required_location": "USA Only",
            "salary": "",  # blank salary
            "description": "<p>Join the LLM team.</p>",
        },
        {
            "id": 165434,
            "url": "https://remotive.com/remote-jobs/design/ux-designer-165434",
            "title": "UX Designer",
            "company_name": None,  # missing company
            "company_logo": None,
            "category": "Design",
            "tags": ["ux", "figma"],
            "job_type": "full_time",
            "publication_date": None,  # missing date
            "candidate_required_location": "Europe",
            "salary": None,
            "description": None,
        },
    ],
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_remotive_fetch_with_mock_client():
    """Parse a realistic Remotive response via injected MockTransport."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert "remotive.com" in request.url.host
        assert "/api/remote-jobs" in request.url.path
        assert request.url.params["search"] == "Python Engineer"
        assert request.url.params["limit"] == "10"
        return httpx.Response(200, json=MOCK_REMOTIVE_RESPONSE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemotiveJobSource(client=client)

    query = JobSearchQuery(what="Python Engineer", results_per_page=10)
    postings = await source.fetch(query)

    assert isinstance(postings, list)
    assert len(postings) == 3

    # First job — standard data with salary and HTML in title/description
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "remotive:165432"
    assert job1.source == "remotive"
    assert job1.company == "CloudStack Inc"
    assert job1.role == "Senior Python Engineer"        # HTML stripped
    assert job1.description == "Build scalable FastAPI services and data pipelines."  # HTML stripped
    assert job1.salary == "$120,000 - $150,000"
    assert job1.salary_min is None                      # Remotive has no structured min/max
    assert job1.salary_max is None
    assert job1.currency is None
    assert job1.location == "Worldwide"
    assert job1.location_type == "remote"               # always remote on Remotive
    assert job1.country is None
    assert job1.city is None
    assert job1.apply_link == "https://remotive.com/remote-jobs/software-dev/senior-backend-engineer-165432"
    assert job1.posted_at == datetime(2026, 10, 24, 8, 0, 0, tzinfo=timezone.utc)

    # Second job — blank salary treated as None
    job2 = postings[1]
    assert job2.id == "remotive:165433"
    assert job2.company == "DataAI Corp"
    assert job2.salary is None
    assert job2.location == "USA Only"
    assert job2.location_type == "remote"
    assert job2.posted_at == datetime(2026, 10, 23, 10, 30, 0, tzinfo=timezone.utc)

    # Third job — missing company, date, description
    job3 = postings[2]
    assert job3.id == "remotive:165434"
    assert job3.company == "Unknown Company"
    assert job3.description == ""
    assert job3.salary is None
    assert job3.posted_at is None


@pytest.mark.asyncio
async def test_remotive_fetch_string_query():
    """String query is normalized and sent as 'search' param."""
    recorded_params: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal recorded_params
        recorded_params = dict(request.url.params)
        return httpx.Response(200, json={"jobs": []})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemotiveJobSource(client=client)

    results = await source.fetch("Machine Learning")
    assert results == []
    assert recorded_params["search"] == "Machine Learning"


@pytest.mark.asyncio
async def test_remotive_fetch_dict_query():
    """Dict query is normalized; results_per_page is sent as 'limit'."""
    recorded_params: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal recorded_params
        recorded_params = dict(request.url.params)
        return httpx.Response(200, json={"jobs": []})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemotiveJobSource(client=client)

    await source.fetch({"what": "AI Engineer", "results_per_page": 5})
    assert recorded_params["search"] == "AI Engineer"
    assert recorded_params["limit"] == "5"


@pytest.mark.asyncio
async def test_remotive_http_error():
    """Non-200 responses raise JobSourceHTTPError."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="Too Many Requests")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemotiveJobSource(client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        await source.fetch("Python")
    assert exc_info.value.status_code == 429
    assert "Too Many Requests" in str(exc_info.value)


@pytest.mark.asyncio
async def test_remotive_empty_results():
    """Empty jobs array returns empty list."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"job-count": 0, "jobs": []})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemotiveJobSource(client=client)

    postings = await source.fetch("Obscure Role")
    assert postings == []

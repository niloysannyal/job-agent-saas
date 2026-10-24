from datetime import datetime, timezone
import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.adzuna import AdzunaJobSource
from app.services.job_sources.exceptions import (
    JobSourceConfigError,
    JobSourceHTTPError,
)

MOCK_ADZUNA_RESPONSE = {
    "__CLASS__": "Adzuna::API::Response::JobSearchResults",
    "count": 3,
    "results": [
        {
            "id": "12345",
            "title": "Senior <strong>Python</strong> Developer",
            "company": {"display_name": "TechCorp Ltd"},
            "location": {
                "display_name": "London, Greater London",
                "area": ["UK", "London", "Greater London"],
            },
            "description": "Building backend systems with <strong>FastAPI</strong> and Postgres.",
            "salary_min": 50000,
            "salary_max": 60000,
            "contract_type": "permanent",
            "created": "2026-10-24T12:00:00Z",
            "redirect_url": "https://www.adzuna.co.uk/land/ad/12345",
        },
        {
            "id": "67890",
            "title": "Remote AI/ML Engineer",
            "company": {"display_name": "Betopia Labs"},
            "location": {
                "display_name": "Remote, UK",
                "area": ["UK"],
            },
            "description": "Work from home building LLM agent pipelines and RAG workflows.",
            "salary_min": 75000,
            "salary_max": None,
            "contract_type": "permanent",
            "created": "2026-10-23T08:30:00Z",
            "redirect_url": "https://www.adzuna.co.uk/land/ad/67890",
        },
        {
            "id": "99999",
            "title": "Junior Data Analyst",
            "company": None,
            "location": None,
            "description": "Assist with report creation and data cleaning.",
            "salary_min": None,
            "salary_max": 35000,
            "contract_type": "contract",
            "created": None,
            "redirect_url": "https://www.adzuna.co.uk/land/ad/99999",
        },
    ],
}


def test_adzuna_fetch_with_mock_client():
    """Test fetch parsing with an injected httpx.Client using MockTransport."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert "api.adzuna.com" in request.url.host
        assert "/jobs/gb/search/1" in request.url.path
        assert request.url.params["app_id"] == "test_id"
        assert request.url.params["app_key"] == "test_key"
        assert request.url.params["what"] == "Python Engineer"
        assert request.url.params["where"] == "London"
        return httpx.Response(200, json=MOCK_ADZUNA_RESPONSE)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    source = AdzunaJobSource(app_id="test_id", app_key="test_key", client=client)

    query = JobSearchQuery(
        what="Python Engineer",
        where="London",
        country="gb",
        page=1,
    )
    postings = source.fetch(query)

    assert len(postings) == 3

    # Check first item (standard on-site role)
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "adzuna:12345"
    assert job1.source == "adzuna"
    assert job1.company == "TechCorp Ltd"
    # Verify HTML tags were stripped
    assert job1.role == "Senior Python Developer"
    assert job1.description == "Building backend systems with FastAPI and Postgres."
    assert job1.salary == "£50,000 - £60,000"
    assert job1.salary_min == 50000.0
    assert job1.salary_max == 60000.0
    assert job1.currency == "£"
    assert job1.country == "UK"
    assert job1.city == "London, Greater London"
    assert job1.location_type == "on-site"
    assert job1.apply_link == "https://www.adzuna.co.uk/land/ad/12345"
    assert job1.posted_at == datetime(2026, 10, 24, 12, 0, 0, tzinfo=timezone.utc)

    # Check second item (remote AI role)
    job2 = postings[1]
    assert job2.id == "adzuna:67890"
    assert job2.company == "Betopia Labs"
    assert job2.role == "Remote AI/ML Engineer"
    assert job2.location_type == "remote"
    assert job2.salary == "From £75,000"
    assert job2.salary_min == 75000.0
    assert job2.salary_max is None

    # Check third item (missing company/location, max salary only)
    job3 = postings[2]
    assert job3.id == "adzuna:99999"
    assert job3.company == "Unknown Company"
    assert job3.salary == "Up to £35,000"
    assert job3.posted_at is None


def test_adzuna_fetch_query_variations():
    """Test fetch using string and dict queries."""
    recorded_params = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal recorded_params
        recorded_params = dict(request.url.params)
        return httpx.Response(200, json={"results": []})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    source = AdzunaJobSource(app_id="test_id", app_key="test_key", client=client)

    # Test string query
    results_str = source.fetch("Machine Learning")
    assert len(results_str) == 0
    assert recorded_params["what"] == "Machine Learning"
    assert recorded_params["app_id"] == "test_id"

    # Test dict query
    results_dict = source.fetch({
        "what": "AI Engineer",
        "where": "Berlin",
        "country": "de",
        "salary_min": 60000,
        "full_time": True,
    })
    assert len(results_dict) == 0
    assert recorded_params["what"] == "AI Engineer"
    assert recorded_params["where"] == "Berlin"
    assert recorded_params["salary_min"] == "60000"
    assert recorded_params["full_time"] == "1"


def test_adzuna_missing_credentials():
    """Test that missing credentials raise JobSourceConfigError."""
    source = AdzunaJobSource(app_id=None, app_key=None)
    with pytest.raises(JobSourceConfigError) as exc_info:
        source.fetch("Python")
    assert "ADZUNA_APP_ID" in str(exc_info.value) or "app_id and app_key" in str(exc_info.value)


def test_adzuna_http_error():
    """Test that HTTP errors from Adzuna raise JobSourceHTTPError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="Unauthorized: Invalid app_key")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    source = AdzunaJobSource(app_id="bad_id", app_key="bad_key", client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        source.fetch("AI Engineer")
    assert exc_info.value.status_code == 401
    assert "Unauthorized" in str(exc_info.value)


@pytest.mark.asyncio
async def test_adzuna_afetch_async():
    """Test async afetch with AsyncClient using MockTransport."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=MOCK_ADZUNA_RESPONSE)

    async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = AdzunaJobSource(
        app_id="test_id",
        app_key="test_key",
        async_client=async_client,
    )

    postings = await source.afetch("Python Developer")
    assert len(postings) == 3
    assert postings[0].company == "TechCorp Ltd"


@pytest.mark.asyncio
async def test_adzuna_fetch_is_awaitable():
    """Test that JobSource.fetch result can be awaited in async context."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=MOCK_ADZUNA_RESPONSE)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    source = AdzunaJobSource(app_id="test_id", app_key="test_key", client=client)

    postings = await source.fetch("Python Developer")
    assert len(postings) == 3
    assert postings[1].role == "Remote AI/ML Engineer"

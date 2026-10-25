from datetime import datetime, timezone
import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.greenhouse import GreenhouseJobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# ---------------------------------------------------------------------------
# Mock response shape matching the real Greenhouse API
# (https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true)
# ---------------------------------------------------------------------------
MOCK_GREENHOUSE_RESPONSE = {
    "jobs": [
        {
            "id": 1001,
            "title": "Senior Backend Engineer",
            "company_name": "Acme Corp",
            # Greenhouse content is double HTML-entity encoded in real API responses
            "content": "&lt;p&gt;Join our team &amp;amp; build &lt;strong&gt;scale&lt;/strong&gt;!&lt;/p&gt;",
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/1001",
            "location": {"name": "San Francisco, CA"},
            "departments": [{"id": 10, "name": "Engineering"}],
            "offices": [{"id": 20, "name": "United States"}],
            "first_published": "2026-10-24T12:00:00Z",
            "updated_at": "2026-10-24T14:30:00Z",
        },
        {
            "id": 1002,
            "title": "Staff Platform Engineer (Remote)",
            "company_name": None,  # should fall back to company_slug
            "content": "<div>Work from anywhere in the world.</div>",
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/1002",
            "location": {"name": "Remote - US"},
            "departments": [{"id": 10, "name": "Engineering"}],
            "offices": [],
            "first_published": "2026-10-20T09:00:00+00:00",
            "updated_at": None,
        },
        {
            "id": 1003,
            "title": "Product Designer",
            "company_name": "Acme Corp",
            "content": None,
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/1003",
            "location": {"name": "London, UK (Hybrid)"},
            "departments": [],
            "offices": [{"id": 21, "name": "United Kingdom"}],
            "first_published": None,
            "updated_at": None,
        },
    ]
}


@pytest.mark.asyncio
async def test_greenhouse_fetch_with_mock_client():
    """Parse a realistic Greenhouse response via injected MockTransport."""
    captured_request = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_request["url"] = str(request.url)
        captured_request["params"] = dict(request.url.params)
        assert "/v1/boards/acme/jobs" in request.url.path
        assert request.url.params["content"] == "true"
        return httpx.Response(200, json=MOCK_GREENHOUSE_RESPONSE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = GreenhouseJobSource(client=client)
    assert source.is_per_company is True

    query = JobSearchQuery(what="acme")
    postings = await source.fetch(query)

    assert isinstance(postings, list)
    assert len(postings) == 3

    # Job 1 - On-site, double-unescaped HTML content, offices & departments
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "greenhouse:1001"
    assert job1.source == "greenhouse"
    assert job1.company == "Acme Corp"
    assert job1.role == "Senior Backend Engineer"
    # Unescaped twice: &amp;amp; -> &amp; -> &, &lt;strong&gt; -> <strong> -> stripped
    assert "Join our team & build scale!" in job1.description
    assert "<" not in job1.description
    assert job1.apply_link == "https://boards.greenhouse.io/acme/jobs/1001"
    assert job1.location == "San Francisco, CA"
    assert job1.location_type == "on-site"
    assert job1.country == "United States"
    assert job1.posted_at == datetime(2026, 10, 24, 12, 0, 0, tzinfo=timezone.utc)
    assert job1.salary is None

    # Job 2 - Remote, company fallback to slug
    job2 = postings[1]
    assert job2.id == "greenhouse:1002"
    assert job2.company == "acme"
    assert job2.location_type == "remote"
    assert job2.location == "Remote - US"
    assert job2.country is None

    # Job 3 - Hybrid, missing content and date
    job3 = postings[2]
    assert job3.id == "greenhouse:1003"
    assert job3.location_type == "hybrid"
    assert job3.description == ""
    assert job3.posted_at is None


@pytest.mark.asyncio
async def test_greenhouse_fetch_string_slug():
    """String company slug is normalized and targets the correct URL."""
    captured_path = ""

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_path
        captured_path = request.url.path
        return httpx.Response(200, json={"jobs": []})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = GreenhouseJobSource(client=client)

    results = await source.fetch("Stripe")
    assert results == []
    assert captured_path == "/v1/boards/stripe/jobs"


@pytest.mark.asyncio
async def test_greenhouse_http_error():
    """Non-200 responses raise JobSourceHTTPError."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="Company board not found")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = GreenhouseJobSource(client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        await source.fetch("nonexistent_company")

    assert exc_info.value.status_code == 404
    assert "nonexistent_company" in str(exc_info.value)

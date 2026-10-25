from datetime import datetime, timezone
import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.freehire import FreehireJobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# ---------------------------------------------------------------------------
# Mock response shape matching the real freehire.me API
# (https://freehire.me/api/v1/jobs/search?q=python&limit=10)
# ---------------------------------------------------------------------------
MOCK_FREEHIRE_RESPONSE = {
    "data": [
        {
            "public_slug": "python-developer-noordtechnologies-iatckqxe",
            "source": "zohorecruit",
            "external_id": "zohorecruit:572774000010708216",
            "url": "https://noordtechnologies.zohorecruit.com/jobs/Careers/572774000010708216",
            "title": "Senior <strong>Python</strong> Developer",
            "company": "Noord Technologies",
            "company_slug": "noord-technologies",
            "location": "London, UK",
            "description": "<p>Build innovative web applications using <b>Django</b> and <b>FastAPI</b>.</p>",
            "work_mode": "remote",
            "countries": ["gb"],
            "cities": ["London"],
            "skills": ["python", "django", "fastapi"],
            "salary": "£80,000 - £95,000",
            "posted_at": "2026-10-25T01:30:33Z",
            "created_at": "2026-10-25T01:30:33Z",
        },
        {
            "public_slug": None,
            "source": "greenhouse",
            "external_id": "stripe:123456",
            "url": "https://stripe.com/jobs/123456",
            "title": "Infrastructure Engineer",
            "company": None,
            "company_slug": "stripe",
            "location": "Berlin, Germany",
            "description": "<div>Scale distributed payment platforms.</div>",
            "work_mode": "hybrid",
            "countries": ["de"],
            "cities": ["Berlin"],
            "skills": ["go", "kubernetes"],
            "salary_min": 110000,
            "salary_max": 140000,
            "currency": "EUR",
            "posted_at": "2026-10-24T10:00:00Z",
            "created_at": "2026-10-24T10:00:00Z",
        },
        {
            "public_slug": "general-analyst-abc123",
            "source": "direct",
            "external_id": None,
            "url": "https://example.com/apply",
            "title": "Business Analyst",
            "company": None,
            "company_slug": None,
            "location": None,
            "description": None,
            "work_mode": None,
            "countries": [],
            "cities": [],
            "skills": [],
            "salary": None,
            "posted_at": None,
            "created_at": None,
        },
    ],
    "meta": {
        "limit": 10,
        "offset": 0,
        "total": 3,
    },
}


# ---------------------------------------------------------------------------
# 1. Data Normalization Test
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_freehire_fetch_data_normalization():
    """Verify field mapping and HTML cleaning from realistic freehire response."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/api/v1/jobs/search" in request.url.path
        assert request.url.params["q"] == "python"
        return httpx.Response(200, json=MOCK_FREEHIRE_RESPONSE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = FreehireJobSource(client=client)

    assert source.is_per_company is False

    query = JobSearchQuery(what="python", results_per_page=10)
    postings = await source.fetch(query)

    assert isinstance(postings, list)
    assert len(postings) == 3

    # Job 1 - Full data with HTML cleaned, remote work_mode, salary string
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "freehire:python-developer-noordtechnologies-iatckqxe"
    assert job1.source == "freehire"
    assert job1.company == "Noord Technologies"
    assert job1.role == "Senior Python Developer"
    assert job1.description == "Build innovative web applications using Django and FastAPI."
    assert job1.apply_link == "https://noordtechnologies.zohorecruit.com/jobs/Careers/572774000010708216"
    assert job1.location_type == "remote"
    assert job1.country == "gb"
    assert job1.city == "London"
    assert job1.salary == "£80,000 - £95,000"
    assert job1.posted_at == datetime(2026, 10, 25, 1, 30, 33, tzinfo=timezone.utc)

    # Job 2 - external_id fallback, hybrid work_mode, structured salary_min/max, company_slug fallback
    job2 = postings[1]
    assert job2.id == "freehire:stripe:123456"
    assert job2.company == "stripe"
    assert job2.location_type == "hybrid"
    assert job2.country == "de"
    assert job2.city == "Berlin"
    assert job2.salary == "EUR 110000 - 140000"
    assert job2.salary_min == 110000.0
    assert job2.salary_max == 140000.0
    assert job2.currency == "EUR"
    assert job2.posted_at == datetime(2026, 10, 24, 10, 0, 0, tzinfo=timezone.utc)

    # Job 3 - Fallback handling for missing fields
    job3 = postings[2]
    assert job3.id == "freehire:general-analyst-abc123"
    assert job3.company == "Unknown Company"
    assert job3.description == ""
    assert job3.location_type == "on-site"
    assert job3.country is None
    assert job3.city is None
    assert job3.salary is None
    assert job3.posted_at is None


# ---------------------------------------------------------------------------
# 2. Dedicated Bearer Auth Test
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_freehire_bearer_auth():
    """Verify that Authorization Bearer header is sent when api_key is set, and omitted when None."""
    captured_headers = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_headers
        captured_headers = dict(request.headers)
        return httpx.Response(200, json={"data": [], "meta": {"total": 0}})

    # Case A: api_key is provided
    client_with_key = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source_with_key = FreehireJobSource(client=client_with_key, api_key="test-api-token-123")
    await source_with_key.fetch(JobSearchQuery(what="python"))
    assert captured_headers.get("authorization") == "Bearer test-api-token-123"

    # Case B: api_key is omitted (public keyless access)
    captured_headers.clear()
    client_no_key = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source_no_key = FreehireJobSource(client=client_no_key, api_key=None)
    await source_no_key.fetch(JobSearchQuery(what="python"))
    assert "authorization" not in captured_headers


# ---------------------------------------------------------------------------
# 3. Dedicated Offset-from-Page Calculation Test
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_freehire_offset_from_page():
    """Verify offset is omitted for page 1 and correctly calculated as (page - 1) * limit for page > 1."""
    captured_params = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_params
        captured_params = dict(request.url.params)
        return httpx.Response(200, json={"data": [], "meta": {"total": 0}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = FreehireJobSource(client=client)

    # Page 1: offset should not be present
    await source.fetch(JobSearchQuery(what="python", page=1, results_per_page=20))
    assert "offset" not in captured_params
    assert captured_params["limit"] == "20"

    # Page 2 with limit 20: offset = (2 - 1) * 20 = 20
    await source.fetch(JobSearchQuery(what="python", page=2, results_per_page=20))
    assert captured_params["offset"] == "20"
    assert captured_params["limit"] == "20"

    # Page 4 with limit 15: offset = (4 - 1) * 15 = 45
    await source.fetch(JobSearchQuery(what="python", page=4, results_per_page=15))
    assert captured_params["offset"] == "45"
    assert captured_params["limit"] == "15"


# ---------------------------------------------------------------------------
# 4. Query Filters Test
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_freehire_query_filters():
    """Verify country and salary_min query filters serialization."""
    captured_params = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_params
        captured_params = dict(request.url.params)
        return httpx.Response(200, json={"data": [], "meta": {"total": 0}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = FreehireJobSource(client=client)

    query = JobSearchQuery(
        what="DevOps",
        country="gb",
        salary_min=80000,
    )
    await source.fetch(query)

    assert captured_params["q"] == "DevOps"
    assert captured_params["countries"] == "gb"
    assert captured_params["salary_min"] == "80000"


# ---------------------------------------------------------------------------
# 5. Error Handling Test
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_freehire_http_error():
    """Non-200 responses raise JobSourceHTTPError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="Internal server error")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = FreehireJobSource(client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        await source.fetch("Python")

    assert exc_info.value.status_code == 500
    assert "freehire.me API request failed" in str(exc_info.value)

from datetime import datetime, timezone

import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.remoteok import RemoteOKJobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# ---------------------------------------------------------------------------
# Mock response shape matching the real RemoteOK API
# RemoteOK returns a JSON array: first element = legal-notice dict,
# subsequent elements = job objects.
# ---------------------------------------------------------------------------
MOCK_REMOTEOK_RESPONSE = [
    # Element 0: legal notice — must be skipped by the parser
    {
        "last_updated": 1792857604,
        "legal": (
            "API Terms of Service: Please link back (with follow, and without nofollow!) "
            "to the URL on Remote OK..."
        ),
    },
    # Element 1: well-formed job with salary
    {
        "slug": "remote-senior-python-engineer-techcorp-1137500",
        "id": "1137500",
        "epoch": 1792800000,
        "date": "2026-10-24T00:00:00+00:00",
        "company": "TechCorp",
        "company_logo": "",
        "position": "Senior <strong>Python</strong> Engineer",
        "tags": ["python", "fastapi", "aws", "remote"],
        "description": "<p>Build <em>microservices</em> with FastAPI and Postgres.</p>",
        "location": "",
        "salary_min": 150000,
        "salary_max": 180000,
        "apply_url": "https://remoteOK.com/remote-jobs/remote-senior-python-engineer-techcorp-1137500",
        "logo": "",
        "url": "https://remoteOK.com/remote-jobs/remote-senior-python-engineer-techcorp-1137500",
    },
    # Element 2: job with only salary_min (no max), 0-padded salary_max
    {
        "slug": "remote-ml-engineer-dataai-1137501",
        "id": "1137501",
        "epoch": 1792713600,
        "date": "2026-10-23T00:00:00+00:00",
        "company": "DataAI",
        "company_logo": "",
        "position": "ML Engineer",
        "tags": ["machine learning", "python"],
        "description": "<p>LLM pipelines.</p>",
        "location": "USA",
        "salary_min": 130000,
        "salary_max": 0,            # 0 means "not specified" in RemoteOK
        "apply_url": "https://remoteOK.com/remote-jobs/remote-ml-engineer-dataai-1137501",
        "logo": "",
        "url": "https://remoteOK.com/remote-jobs/remote-ml-engineer-dataai-1137501",
    },
    # Element 3: job with no salary, missing company
    {
        "slug": "remote-ux-designer-unknown-1137502",
        "id": "1137502",
        "epoch": 0,
        "date": None,
        "company": None,
        "company_logo": "",
        "position": "UX Designer",
        "tags": ["ux", "figma"],
        "description": None,
        "location": None,
        "salary_min": 0,
        "salary_max": 0,
        "apply_url": "https://remoteOK.com/remote-jobs/remote-ux-designer-unknown-1137502",
        "logo": "",
        "url": "https://remoteOK.com/remote-jobs/remote-ux-designer-unknown-1137502",
    },
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_remoteok_fetch_with_mock_client():
    """Parse a realistic RemoteOK response via injected MockTransport."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert "remoteok.com" in request.url.host
        assert request.url.params["tag"] == "Python"
        return httpx.Response(200, json=MOCK_REMOTEOK_RESPONSE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    query = JobSearchQuery(what="Python")
    postings = await source.fetch(query)

    assert isinstance(postings, list)
    # Legal notice element should be skipped → 3 jobs
    assert len(postings) == 3

    # Job 1 — salary range, HTML stripped
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "remoteok:1137500"
    assert job1.source == "remoteok"
    assert job1.company == "TechCorp"
    assert job1.role == "Senior Python Engineer"          # HTML stripped
    assert job1.description == "Build microservices with FastAPI and Postgres."  # HTML stripped
    assert job1.salary == "$150,000 - $180,000"
    assert job1.salary_min == 150000.0
    assert job1.salary_max == 180000.0
    assert job1.currency == "$"
    assert job1.location_type == "remote"                 # always remote on RemoteOK
    assert job1.apply_link == (
        "https://remoteOK.com/remote-jobs/remote-senior-python-engineer-techcorp-1137500"
    )
    assert job1.posted_at == datetime(2026, 10, 24, 0, 0, 0, tzinfo=timezone.utc)

    # Job 2 — salary_min only (max is 0, treated as absent)
    job2 = postings[1]
    assert job2.id == "remoteok:1137501"
    assert job2.salary == "From $130,000"
    assert job2.salary_min == 130000.0
    assert job2.salary_max is None
    assert job2.currency == "$"
    assert job2.location == "USA"
    assert job2.location_type == "remote"

    # Job 3 — no salary, missing company/description/date
    job3 = postings[2]
    assert job3.id == "remoteok:1137502"
    assert job3.company == "Unknown Company"
    assert job3.description == ""
    assert job3.salary is None
    assert job3.salary_min is None
    assert job3.salary_max is None
    assert job3.currency is None
    assert job3.posted_at is None


@pytest.mark.asyncio
async def test_remoteok_legal_notice_only_response():
    """A response with only the legal-notice element returns an empty list."""

    def handler(request: httpx.Request) -> httpx.Response:
        legal_only = [MOCK_REMOTEOK_RESPONSE[0]]
        return httpx.Response(200, json=legal_only)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    postings = await source.fetch("Python")
    assert postings == []


@pytest.mark.asyncio
async def test_remoteok_fetch_string_query():
    """String query is normalized; 'what' is sent as 'tag' param."""
    recorded_params: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal recorded_params
        recorded_params = dict(request.url.params)
        return httpx.Response(200, json=[MOCK_REMOTEOK_RESPONSE[0]])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    results = await source.fetch("React")
    assert results == []
    assert recorded_params["tag"] == "React"


@pytest.mark.asyncio
async def test_remoteok_fetch_dict_query():
    """Dict query is normalized and 'what' is sent as 'tag' param."""
    recorded_params: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal recorded_params
        recorded_params = dict(request.url.params)
        return httpx.Response(200, json=[MOCK_REMOTEOK_RESPONSE[0]])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    await source.fetch({"what": "TypeScript"})
    assert recorded_params["tag"] == "TypeScript"


@pytest.mark.asyncio
async def test_remoteok_http_error():
    """Non-200 responses raise JobSourceHTTPError."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="Service Unavailable")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        await source.fetch("Python")
    assert exc_info.value.status_code == 503
    assert "Service Unavailable" in str(exc_info.value)


@pytest.mark.asyncio
async def test_remoteok_empty_results():
    """Response with only legal notice yields empty list."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{"last_updated": 123, "legal": "..."}])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = RemoteOKJobSource(client=client)

    postings = await source.fetch("ObscureRole")
    assert postings == []

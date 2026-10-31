from datetime import datetime, timezone
import httpx
import pytest

from app.models.job import JobPosting, JobSearchQuery
from app.services.job_sources.lever import LeverJobSource
from app.services.job_sources.exceptions import JobSourceHTTPError

# ---------------------------------------------------------------------------
# Mock response shape matching the real Lever API
# (https://api.lever.co/v0/postings/{company}?mode=json)
# ---------------------------------------------------------------------------
MOCK_LEVER_RESPONSE = [
    {
        "id": "lever-uuid-001",
        "text": "Senior Backend Engineer",
        "hostedUrl": "https://jobs.lever.co/spotify/lever-uuid-001",
        "applyUrl": "https://jobs.lever.co/spotify/lever-uuid-001/apply",
        "createdAt": 1729756800000,  # 2024-10-24 08:00:00 UTC
        "workplaceType": "hybrid",
        "country": "US",
        "categories": {
            "location": "New York, NY",
            "commitment": "Full-time",
            "team": "Platform",
            "department": "Engineering",
        },
        "descriptionPlain": "We are looking for a Senior Backend Engineer to join our team.",
        "lists": [
            {
                "text": "What You'll Do",
                "content": "<div><p>• Build robust APIs with FastAPI and Python.</p></div>",
            },
            {
                "text": "Who You Are",
                "content": "<div><p>• 5+ years of distributed systems experience.</p></div>",
            },
        ],
        "additionalPlain": "Base salary range: $150,000 - $180,000 plus equity.",
        "salaryRange": {
            "min": 150000,
            "max": 180000,
            "currency": "USD",
            "interval": "year",
        },
    },
    {
        "id": "lever-uuid-002",
        "text": "Machine Learning Engineer (Remote)",
        "hostedUrl": "https://jobs.lever.co/spotify/lever-uuid-002",
        "applyUrl": "https://jobs.lever.co/spotify/lever-uuid-002/apply",
        "createdAt": "2026-10-23T15:00:00Z",
        "workplaceType": "remote",
        "country": "UK",
        "categories": {
            "location": "Remote, UK",
            "commitment": "Permanent",
        },
        "description": "<p>Train cutting-edge recommendation models.</p>",
        "lists": [],
        "additional": None,
        "salaryRange": None,
    },
    {
        "id": "lever-uuid-003",
        "text": "Product Specialist",
        "hostedUrl": None,
        "applyUrl": "https://jobs.lever.co/spotify/lever-uuid-003/apply",
        "createdAt": None,
        "workplaceType": None,
        "country": None,
        "categories": {},
        "descriptionPlain": None,
        "description": None,
        "lists": [],
        "additional": None,
    },
]


@pytest.mark.asyncio
async def test_lever_fetch_with_mock_client():
    """Parse a realistic Lever response via injected MockTransport."""
    captured_request = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_request["url"] = str(request.url)
        captured_request["params"] = dict(request.url.params)
        assert "/v0/postings/spotify" in request.url.path
        assert request.url.params["mode"] == "json"
        return httpx.Response(200, json=MOCK_LEVER_RESPONSE)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client)
    assert source.is_per_company is True

    query = JobSearchQuery(what="spotify")
    postings = await source.fetch(query)

    assert isinstance(postings, list)
    assert len(postings) == 3

    # Job 1 - Hybrid, structured salaryRange, list sections, epoch timestamp
    job1 = postings[0]
    assert isinstance(job1, JobPosting)
    assert job1.id == "lever:lever-uuid-001"
    assert job1.source == "lever"
    assert job1.company == "spotify"
    assert job1.role == "Senior Backend Engineer"
    assert "We are looking for a Senior Backend Engineer" in job1.description
    assert "What You'll Do:" in job1.description
    assert "Build robust APIs with FastAPI and Python." in job1.description
    assert "Base salary range:" in job1.description
    assert job1.apply_link == "https://jobs.lever.co/spotify/lever-uuid-001"
    assert job1.location == "New York, NY"
    assert job1.location_type == "hybrid"
    assert job1.country == "US"
    assert job1.salary == "USD 150000 - 180000 / year"
    assert job1.salary_min == 150000.0
    assert job1.salary_max == 180000.0
    assert job1.currency == "USD"
    assert job1.posted_at == datetime.fromtimestamp(1729756800.0, tz=timezone.utc)

    # Job 2 - Remote, HTML description stripped, ISO string createdAt
    job2 = postings[1]
    assert job2.id == "lever:lever-uuid-002"
    assert job2.location_type == "remote"
    assert job2.location == "Remote, UK"
    assert job2.country == "UK"
    assert job2.salary is None
    assert job2.salary_min is None
    assert job2.description == "Train cutting-edge recommendation models."
    assert job2.posted_at == datetime(2026, 10, 23, 15, 0, 0, tzinfo=timezone.utc)

    # Job 3 - Fallback values
    job3 = postings[2]
    assert job3.id == "lever:lever-uuid-003"
    assert job3.apply_link == "https://jobs.lever.co/spotify/lever-uuid-003/apply"
    assert job3.description == ""
    assert job3.posted_at is None
    assert job3.location is None
    assert job3.location_type == "on-site"


@pytest.mark.asyncio
async def test_lever_fetch_string_slug():
    """String company slug is normalized and targets the correct URL."""
    captured_path = ""

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_path
        captured_path = request.url.path
        return httpx.Response(200, json=[])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client)

    results = await source.fetch("Netflix")
    assert results == []
    assert captured_path == "/v0/postings/netflix"


@pytest.mark.asyncio
async def test_lever_http_error():
    """Non-200 responses raise JobSourceHTTPError."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="Not found")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client)

    with pytest.raises(JobSourceHTTPError) as exc_info:
        await source.fetch("nonexistent_company")

    assert exc_info.value.status_code == 404
    assert "nonexistent_company" in str(exc_info.value)


@pytest.mark.asyncio
async def test_lever_pagination_multi_page():
    """Verify offset pagination with skip parameter across multiple pages."""
    captured_requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        captured_requests.append(params)
        skip = int(params.get("skip", 0))

        if skip == 0:
            # Page 1: returns full page of 2 items
            return httpx.Response(
                200,
                json=[
                    {"id": "lev-1", "text": "Staff Engineer"},
                    {"id": "lev-2", "text": "Senior Engineer"},
                ],
            )
        elif skip == 2:
            # Page 2: returns partial page of 1 item (< page_size)
            return httpx.Response(
                200,
                json=[
                    {"id": "lev-3", "text": "Lead Engineer"},
                ],
            )
        return httpx.Response(200, json=[])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client, page_size=2)

    postings = await source.fetch("netflix")

    assert len(captured_requests) == 2
    assert "skip" not in captured_requests[0]
    assert captured_requests[0].get("limit") == "2"
    assert captured_requests[1].get("skip") == "2"
    assert captured_requests[1].get("limit") == "2"

    assert len(postings) == 3
    assert [p.id for p in postings] == [
        "lever:lev-1",
        "lever:lev-2",
        "lever:lev-3",
    ]


@pytest.mark.asyncio
async def test_lever_pagination_default_page_size_100():
    """Verify standard 100-batch pagination traversing to page 2 with skip=100."""
    captured_requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        captured_requests.append(params)
        skip = int(params.get("skip", 0))

        if skip == 0:
            # Page 1: 100 items
            batch = [{"id": f"lev-{i}", "text": f"Role {i}"} for i in range(1, 101)]
            return httpx.Response(200, json=batch)
        elif skip == 100:
            # Page 2: 5 items (final page)
            batch = [{"id": f"lev-{i}", "text": f"Role {i}"} for i in range(101, 106)]
            return httpx.Response(200, json=batch)
        return httpx.Response(200, json=[])

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client)  # default page_size=100

    postings = await source.fetch("spotify")

    assert len(captured_requests) == 2
    assert "skip" not in captured_requests[0]
    assert captured_requests[1].get("skip") == "100"

    assert len(postings) == 105
    assert postings[0].id == "lever:lev-1"
    assert postings[99].id == "lever:lev-100"
    assert postings[104].id == "lever:lev-105"


@pytest.mark.asyncio
async def test_lever_pagination_respects_max_pages():
    """Verify max_pages safely terminates pagination even if full batches continue."""
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        # Always return 100 items
        batch = [{"id": f"lev-{call_count}-{i}", "text": "Role"} for i in range(100)]
        return httpx.Response(200, json=batch)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client, max_pages=2)

    postings = await source.fetch("spotify")

    assert call_count == 2
    assert len(postings) == 200


@pytest.mark.asyncio
async def test_lever_pagination_respects_max_postings():
    """Verify max_postings stops accumulation as soon as cap is reached."""
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(
            200,
            json=[
                {"id": f"lev-{call_count}-a", "text": "Role A"},
                {"id": f"lev-{call_count}-b", "text": "Role B"},
            ],
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    source = LeverJobSource(client=client, page_size=2, max_postings=3)

    postings = await source.fetch("spotify")

    assert len(postings) == 3
    assert [p.id for p in postings] == [
        "lever:lev-1-a",
        "lever:lev-1-b",
        "lever:lev-2-a",
    ]

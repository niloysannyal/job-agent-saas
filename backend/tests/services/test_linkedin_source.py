import pytest
from unittest.mock import AsyncMock, MagicMock
from app.models.job import JobSearchQuery
from app.services.job_sources.linkedin import LinkedInJobSource


SAMPLE_HTML = """
<ul class="jobs-search__results-list">
  <li>
    <div class="base-card" data-entity-urn="urn:li:jobPosting:4192503234">
      <a class="base-card__full-link" href="https://www.linkedin.com/jobs/view/ai-engineer-at-techcorp-4192503234?position=1">
        <span class="sr-only">AI Systems Engineer</span>
      </a>
      <h4 class="base-search-card__subtitle">
        <a href="https://www.linkedin.com/company/techcorp">TechCorp AI</a>
      </h4>
      <div class="base-search-card__metadata">
        <span class="job-search-card__location">Remote</span>
        <time class="job-search-card__listdate" datetime="2026-10-25">2 days ago</time>
      </div>
    </div>
  </li>
</ul>
"""


@pytest.mark.asyncio
async def test_linkedin_job_source_parser():
    source = LinkedInJobSource()
    postings = source._parse_job_cards(SAMPLE_HTML, limit=5)

    assert len(postings) == 1
    p = postings[0]
    assert p.id == "linkedin-4192503234"
    assert p.source == "linkedin"
    assert p.role == "AI Systems Engineer"
    assert p.company == "TechCorp AI"
    assert p.location == "Remote"
    assert p.location_type == "remote"
    assert "https://www.linkedin.com/jobs/view/ai-engineer-at-techcorp-4192503234" in p.apply_link


"""
backend/tests/services/test_decoupled_tools.py

Unit tests for decoupled core application services:
1. FitAnalyzerService (4D diagnostic: skills, experience, trajectory, seniority)
2. CVDrafterService (Pass 1 non-mutating drafter)
3. CVReviewerService (Pass 2 fact auditor & ATS validator)
4. FormDetectiveService (deterministic apply channel detection)
5. OutreachDrafterService (multi-channel outreach: email, form Q&A, DMs)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.matching.fit_analyzer import FitAnalyzerService, FitAnalyzerInput
from app.services.cv_tailor.drafter import (
    CVDrafterService,
    CVDraftInput,
    CandidateCareerContext,
    prune_and_budget_latex,
)
from app.services.cv_tailor.reviewer import CVReviewerService, CVReviewInput
from app.services.form_detective.detective import FormDetectiveService, ApplyChannelType
from app.services.outreach.drafter_service import (
    OutreachDrafterService,
    OutreachDrafterInput,
    OutreachChannelType,
)


@pytest.mark.asyncio
async def test_fit_analyzer_service():
    service = FitAnalyzerService(db=None)
    result = await service.analyze_fit(
        account_id="acc-test-123",
        posting_text="We are looking for a Senior AI Engineer with Python, FastAPI, Docker, and LLM experience.",
        company_name="TechCorp",
        role_title="Senior AI Engineer",
    )
    assert result.company == "TechCorp"
    assert result.role == "Senior AI Engineer"
    assert result.overall_score >= 60
    assert result.should_proceed is True
    assert "skills" in result.dimensions
    assert "experience" in result.dimensions
    assert "trajectory" in result.dimensions
    assert "seniority" in result.dimensions
    assert result.language_gate_passed is True


@pytest.mark.asyncio
async def test_cv_drafter_service():
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value="""---TAILORED_SUMMARY---
\\resumeItem{AI Engineer specializing in Agentic AI and FastAPI systems for TechCorp.}
---COVER_NOTE---
Dear Hiring Team at TechCorp, I am excited to apply for the AI Engineer role.
---GAPS---
- None
""")

    drafter = CVDrafterService(llm_service=mock_llm)
    context = CandidateCareerContext(
        account_id="acc-123",
        candidate_name="Niloy Sannyal",
        headline="AI Systems Engineer",
        master_latex="\\documentclass{article}\n\\begin{document}\n\\section{SUMMARY}\n\\resumeItemListStart\\resumeItem{Base}\\resumeItemListEnd\n\\end{document}",
        skills=["Python", "FastAPI"],
        verified_facts_str="- 600+ salespersons",
    )
    params = CVDraftInput(
        account_id="acc-123",
        job_role="AI Engineer",
        job_company="TechCorp",
        job_description="FastAPI, Python, Agentic AI",
    )
    draft = await drafter.draft_cv(params, context)

    assert "TechCorp" in draft.draft_summary_bullet
    assert "TechCorp" in draft.draft_cover_letter
    assert "begin{document}" in draft.draft_assembled_latex


@pytest.mark.asyncio
async def test_cv_reviewer_service():
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value="""---FINAL_SUMMARY---
\\resumeItem{AI Engineer specializing in Agentic AI and FastAPI systems for TechCorp.}
---FINAL_COVER---
Dear Hiring Team at TechCorp, I am pleased to present my application.
---CONFIRMED_GAPS---
- None
""")

    reviewer = CVReviewerService(llm_service=mock_llm)
    context = CandidateCareerContext(
        account_id="acc-123",
        candidate_name="Niloy Sannyal",
        headline="AI Systems Engineer",
        master_latex="",
        verified_facts_str="- 600+ salespersons",
    )
    from app.services.cv_tailor.drafter import CVDraftOutput
    draft = CVDraftOutput(
        draft_summary_bullet="\\resumeItem{AI Engineer}",
        draft_cover_letter="Cover letter text",
        raw_gaps=[],
        budgeted_latex_body="\\section{SUMMARY}\n\\resumeItemListStart\n  \\resumeItem{Old}\n\\resumeItemListEnd\nPython FastAPI AI Engineer",
        preamble="\\documentclass{article}",
        draft_assembled_latex="\\documentclass{article}\n\\begin{document}\nniloy@example.com linkedin.com/in/niloy github.com/niloy\nPython FastAPI AI Engineer\n\\section{SUMMARY}\n\\end{document}",
        drafter_raw_response="",
    )
    review_input = CVReviewInput(
        draft_output=draft,
        job_role="AI Engineer",
        job_company="TechCorp",
        job_description="FastAPI, Python",
        career_context=context,
    )
    review = await reviewer.review_cv(review_input)

    assert review.is_valid is True
    assert "TechCorp" in review.final_summary_bullet
    assert review.ats_score > 0.0


def test_form_detective_channels():
    # Google form
    res_gform = FormDetectiveService.detect_channel(
        apply_url="https://forms.gle/abc123xyz",
        posting_text="Apply via Google Form",
    )
    assert res_gform.channel_type == ApplyChannelType.GOOGLE_FORM

    # Email
    res_email = FormDetectiveService.detect_channel(
        apply_url="",
        posting_text="Please send your CV and portfolio to careers@innovatetech.io with subject Senior AI Engineer.",
    )
    assert res_email.channel_type == ApplyChannelType.DIRECT_EMAIL
    assert res_email.recruiter_email == "careers@innovatetech.io"

    # ATS portal
    res_ats = FormDetectiveService.detect_channel(
        apply_url="https://boards.greenhouse.io/anthropic/jobs/12345",
        posting_text="",
    )
    assert res_ats.channel_type == ApplyChannelType.ATS_PORTAL
    assert "Greenhouse" in res_ats.platform_name


@pytest.mark.asyncio
async def test_outreach_drafter_service():
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value="""---SUBJECT---
Senior AI Engineer Application -- Niloy Sannyal
---BODY---
Dear Hiring Team at TechCorp,

I am writing to express my strong enthusiasm for the Senior AI Engineer position. With a proven track record of designing and deploying production LLM systems for 600+ enterprise users, I bring immediate expertise to your team.

Looking forward to speaking soon.
""")

    service = OutreachDrafterService(llm_service=mock_llm)
    outreach = await service.draft_outreach(
        params=OutreachDrafterInput(
            account_id="acc-123",
            company_name="TechCorp",
            role_title="Senior AI Engineer",
            job_description="FastAPI, Python, Agentic AI",
            channel_type=OutreachChannelType.EMAIL,
        ),
        candidate_name="Niloy Sannyal",
    )

    assert outreach.channel_type == OutreachChannelType.EMAIL
    assert "Senior AI Engineer Application" in outreach.subject_line
    assert "TechCorp" in outreach.body_content
    assert outreach.facts_verified is True

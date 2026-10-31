import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.account import Account
from app.models.job import Job
from app.services.cv_tailor.ats_checker import run_ats_text_layer_check
from app.services.cv_tailor.fact_ledger import audit_fact_integrity
from app.services.cv_tailor.latex_processor import (
    check_brace_balance,
    escape_latex_special_chars,
    extract_preamble_and_body,
    strip_control_comments,
)
from app.services.cv_tailor.scorer import plan_relevance_cuts, score_bullet_relevance
from app.services.cv_tailor.tailor_service import CVTailorService
from app.services.llm.mock_provider import MockLLMProvider
from app.services.llm.service import LLMService


@pytest.fixture
def db_session():
    """In-memory SQLite session with all multi-tenant tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_fact_ledger_integrity():
    """Verify that truth metrics pass and invented claims fail."""
    valid_latex = """
    \\resumeItem{Betopia Sales Agent embedded for 600+ salespersons with sub-100ms latency.}
    \\resumeItem{B.Sc. ICE from University of Rajshahi.}
    """
    result = audit_fact_integrity(valid_latex)
    assert result.is_valid is True
    assert "600+ salespersons" in result.verified_metrics_found
    assert len(result.flagged_issues) == 0

    hallucinated_latex = """
    \\resumeItem{Completed Ph.D. in AI from Stanford with 15+ years of experience as an ex-Googler.}
    """
    hallucinated_result = audit_fact_integrity(hallucinated_latex)
    assert hallucinated_result.is_valid is False
    assert len(hallucinated_result.flagged_issues) >= 3


def test_latex_processor():
    """Verify preamble extraction, control comment stripping, and character escaping."""
    raw_latex = """%% CONTROL NOTE FOR AGENT
%% Line 2 control
\\documentclass[a4paper]{article}
\\usepackage{amsmath}
\\begin{document}
Hello Niloy & Partners % 100%
\\end{document}
"""
    preamble, body = extract_preamble_and_body(raw_latex)
    assert "\\documentclass" in preamble
    assert "\\begin{document}" in preamble
    assert "CONTROL NOTE" not in preamble

    cleaned = strip_control_comments(raw_latex)
    assert "CONTROL NOTE" not in cleaned

    escaped = escape_latex_special_chars("AI & Data with 99% accuracy and $500 budget")
    assert "\\&" in escaped
    assert "\\%" in escaped
    assert "\\$" in escaped

    assert check_brace_balance("{\\textbf{Hello}}") is True
    assert check_brace_balance("{\\textbf{Unbalanced") is False


def test_ats_checker():
    """Verify ATS parser plain-text inspection and keyword coverage."""
    cv_sample = """
    Niloy Sannyal -- niloysannyal@gmail.com -- linkedin.com/in/niloy -- github.com/niloy
    Skills: Python, FastAPI, Docker, Qdrant, Redis, PostgreSQL, LLM, RAG.
    """
    job_desc = "Looking for a Python backend engineer with FastAPI, Docker, and Kubernetes experience."

    res = run_ats_text_layer_check(cv_sample, job_desc)
    assert res.contact_verified is True
    assert "python" in res.matched_keywords
    assert "fastapi" in res.matched_keywords
    assert res.score > 0.4


def test_relevance_scorer_and_cuts():
    """Verify relevance scoring and trimming plan."""
    sections = {
        "work_experience": ["Bullet about FastAPI", "Bullet about Qdrant"],
        "robotics_embedded": ["Built Arduino robot with servos", "FPGA controller"],
        "career_highlights": ["Highlight 1", "Highlight 2", "Highlight 3"],
    }
    job_desc = "Seeking an AI Engineer to build LLM agents and FastAPI services."
    retained, summary = plan_relevance_cuts(sections, job_desc, target_bullets_count=4)

    assert summary["cut_count"] > 0
    # Robotics dropped to at most 1 when job is not robotics
    assert len(retained["robotics_embedded"]) <= 1


@pytest.mark.asyncio
async def test_cv_tailor_service_end_to_end(db_session: Session):
    """
    Verify complete Drafter + Reviewer pipeline, persistence,
    and strict human-in-the-loop Send gate.
    """
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()

    job = Job(
        account_id=account.id,
        company="Scale AI",
        role="AI Systems Engineer",
        description="Build LLM evaluations and RAG pipelines with Python, FastAPI, and Qdrant.",
        apply_link="https://scale.com/careers/1",
        source="greenhouse",
    )
    db_session.add(job)
    db_session.commit()

    # Mock responses for Drafter and Reviewer
    drafter_resp = """---COVER_NOTE---
Dear Scale AI Team,

I am writing to express my strong interest in the AI Systems Engineer role. Having architected the Betopia Sales Agent for 600+ salespersons with Qdrant-based RAG and sub-100ms latency, I am excited to bring my production AI experience to Scale.
---GAPS---
- Kubernetes production cluster management
---TAILORED_SUMMARY---
\\resumeItem{AI Engineer building production \\textbf{agentic AI and LLM systems}.}
"""

    reviewer_resp = """---FINAL_COVER---
Dear Scale AI Hiring Team,

I am writing to apply for the AI Systems Engineer position. With hands-on experience building agentic LLM systems in production—including the Betopia Sales Agent embedded for 600+ salespersons with sub-100ms latency and Qdrant RAG—I am ready to deliver immediate impact for Scale AI's infrastructure.
---CONFIRMED_GAPS---
- Kubernetes production cluster management
"""

    mock_llm = MockLLMProvider(responses=[drafter_resp, reviewer_resp])
    llm_service = LLMService(provider=mock_llm)

    service = CVTailorService(llm_service=llm_service, db_session=db_session)
    result = await service.tailor_for_job(
        account_id=account.id,
        job=job,
        channel="email",
    )

    # 1. Output verification
    assert result.cv_version is not None
    assert result.application is not None
    assert result.fact_audit_passed is True
    assert "Kubernetes production cluster management" in result.gaps_detected
    assert "\\documentclass" in result.cv_version.tailored_latex

    # 2. STRICT HUMAN-IN-THE-LOOP CHECK: sent_at MUST be None, status MUST be draft
    assert result.application.sent_at is None
    assert result.application.status == "draft"
    assert "Betopia Sales Agent" in result.application.draft_content

    # 3. Database persistence verification
    db_session.refresh(result.application)
    assert result.application.id is not None
    assert result.application.account_id == account.id
    assert result.application.job_id == job.id


@pytest.mark.asyncio
async def test_cv_tailor_service_with_structured_profile(db_session: Session):
    """
    Verify CVTailorService with structured career entities (universal profile)
    and curated CvTemplate placeholders compilation.
    """
    from app.models.profile import UserProfile, WorkExperience, Education, ProfileSkill, Project
    from app.models.cv_template import CvTemplate

    account = Account(email="sarah.connor@example.com")
    db_session.add(account)
    db_session.commit()

    template = CvTemplate(
        name="01_MODERN_TECH",
        description="Clean tech resume",
        latex_source=(
            "\\documentclass{article}\n"
            "\\newcommand{\\resumeItem}[1]{\\item #1}\n"
            "\\newcommand{\\resumeItemListStart}{\\begin{itemize}}\n"
            "\\newcommand{\\resumeItemListEnd}{\\end{itemize}}\n"
            "\\newcommand{\\resumeHeadingListStart}{\\begin{itemize}}\n"
            "\\newcommand{\\resumeHeadingListEnd}{\\end{itemize}}\n"
            "\\newcommand{\\resumeSectionType}[3]{\\item \\textbf{#1} #2 #3}\n"
            "\\newcommand{\\resumeQuadHeading}[4]{\\item \\textbf{#1} -- #2 -- #3 -- #4}\n"
            "\\begin{document}\n"
            "\\section{Header} {{FULL_NAME}} - {{HEADLINE}} - {{CONTACT_LINE}}\n"
            "{{SUMMARY_SECTION}}\n"
            "{{EXPERIENCE_SECTION}}\n"
            "{{EDUCATION_SECTION}}\n"
            "{{SKILLS_SECTION}}\n"
            "{{PROJECTS_SECTION}}\n"
            "\\end{document}"
        ),
        is_admin_default=True,
    )
    db_session.add(template)
    db_session.commit()

    profile = UserProfile(
        account_id=account.id,
        full_name="Sarah Connor",
        headline="Senior Systems & Distributed Architect",
        active_template_id=template.id,
        summary="Senior Systems Engineer with 8 years of distributed systems and Kubernetes infrastructure experience.",
    )
    db_session.add(profile)
    db_session.commit()

    exp = WorkExperience(
        account_id=account.id,
        profile_id=profile.id,
        company="Cyberdyne Systems",
        title="Lead Cloud Architect",
        start_date="2021-01",
        end_date=None,
        is_current=True,
        highlights="Architected multi-region Kubernetes clusters with 99.999% uptime.",
    )
    db_session.add(exp)

    edu = Education(
        account_id=account.id,
        profile_id=profile.id,
        institution="MIT",
        degree="B.S.",
        field_of_study="Computer Systems",
        start_date="2013",
        end_date="2017",
    )
    db_session.add(edu)

    skill = ProfileSkill(
        account_id=account.id,
        profile_id=profile.id,
        name="Kubernetes",
        category="Cloud & Infrastructure",
    )
    db_session.add(skill)
    db_session.commit()

    job = Job(
        account_id=account.id,
        company="Datadog",
        role="Principal Infrastructure Engineer",
        description="Scaling high-throughput distributed tracing clusters with Kubernetes.",
        apply_link="https://datadog.com/careers/1",
        source="greenhouse",
    )
    db_session.add(job)
    db_session.commit()

    drafter_resp = """---COVER_NOTE---
Dear Datadog Team,

I am excited to apply for the Principal Infrastructure Engineer role. At Cyberdyne Systems, I led the architecture of multi-region Kubernetes clusters with high availability.
---GAPS---
None
---TAILORED_SUMMARY---
\\resumeItem{Senior Systems \\& Distributed Architect specializing in \\textbf{Kubernetes} with track record of 99.999\\% uptime.}
"""

    reviewer_resp = """---FINAL_COVER---
Dear Datadog Team,

I am writing to apply for the Principal Infrastructure Engineer role at Datadog. Having architected multi-region Kubernetes clusters with 99.999% uptime at Cyberdyne Systems, I am eager to contribute to Datadog's distributed tracing infrastructure.
---CONFIRMED_GAPS---
None
---FINAL_SUMMARY---
\\resumeItem{Senior Systems \\& Distributed Architect specializing in \\textbf{Kubernetes} with track record of 99.999\\% uptime.}
"""

    mock_llm = MockLLMProvider(responses=[drafter_resp, reviewer_resp])
    llm_service = LLMService(provider=mock_llm)

    service = CVTailorService(llm_service=llm_service, db_session=db_session)
    result = await service.tailor_for_job(
        account_id=account.id,
        job=job,
        channel="email",
    )

    assert result.cv_version is not None
    assert result.application is not None
    assert "Sarah Connor" in result.cv_version.tailored_latex
    assert "Cyberdyne Systems" in result.cv_version.tailored_latex
    assert "Senior Systems" in result.cv_version.tailored_latex
    assert "{{EXPERIENCE_SECTION}}" not in result.cv_version.tailored_latex
    assert result.application.status == "draft"
    assert result.application.sent_at is None
    assert "Cyberdyne Systems" in result.application.draft_content

import pytest
from app.services.form_detective.detective import ApplyChannelType, FormDetectiveService, FormFieldQuestion


def test_detect_google_form_url():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSc-test-form-xyz/viewform"
    result = FormDetectiveService.detect_channel(
        apply_url=url,
        company_name="Google Startup",
        role_title="AI Engineer",
    )
    assert result.channel_type == ApplyChannelType.GOOGLE_FORM
    assert result.platform_name == "Google Forms"
    assert result.detection_confidence >= 0.95
    assert len(result.questions) >= 4
    assert any("why" in q.prompt.lower() for q in result.questions)


def test_detect_google_form_shortlink_in_text():
    posting = """
    We are hiring an AI Alignment Researcher!
    To apply, please fill out our candidate questionnaire:
    https://forms.gle/abCDef123456
    """
    result = FormDetectiveService.detect_channel(
        apply_url="https://company.com/jobs/1",
        posting_text=posting,
        company_name="Anthropic Lab",
        role_title="Alignment Researcher",
    )
    assert result.channel_type == ApplyChannelType.GOOGLE_FORM
    assert "forms.gle" in result.apply_url


def test_detect_direct_recruiter_email():
    posting = """
    FastAPI and Agentic AI Engineer.
    Please send your resume directly to our hiring team: jobs@deepmind-applied.com
    We look forward to meeting you!
    """
    result = FormDetectiveService.detect_channel(
        apply_url="https://adzuna.com/land/123",
        posting_text=posting,
        company_name="DeepMind Applied",
        role_title="Agentic AI Engineer",
    )
    assert result.channel_type == ApplyChannelType.DIRECT_EMAIL
    assert result.recruiter_email == "jobs@deepmind-applied.com"
    assert any(q.id == "email_cover_body" for q in result.questions)


def test_detect_ats_portal_greenhouse():
    url = "https://boards.greenhouse.io/openai/jobs/4092182004"
    result = FormDetectiveService.detect_channel(
        apply_url=url,
        company_name="OpenAI",
        role_title="Research Engineer",
    )
    assert result.channel_type == ApplyChannelType.ATS_PORTAL
    assert "Greenhouse" in result.platform_name


def test_detect_direct_message_linkedin():
    posting = """
    Hiring immediate backend lead. DM our engineering director directly at:
    https://www.linkedin.com/in/alex-recruiter-lead
    """
    result = FormDetectiveService.detect_channel(
        apply_url="https://remoteok.com/j/999",
        posting_text=posting,
        company_name="Nexus AI",
        role_title="Backend Lead",
    )
    assert result.channel_type == ApplyChannelType.DIRECT_MESSAGE
    assert result.target_handle == "alex-recruiter-lead"
    assert any(q.id == "dm_connection_note" for q in result.questions)

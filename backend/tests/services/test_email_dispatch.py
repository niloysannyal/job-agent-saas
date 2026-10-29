import pytest
from app.services.email_dispatch.dispatch_service import (
    EmailDispatchService,
    EmailDraftProvider,
)


def test_generate_mailto_link():
    link = EmailDispatchService.generate_mailto_link(
        to_email="jobs@anthropic.com",
        subject="Application: AI Systems Engineer - Niloy Sannyal",
        body_text="Hi Team,\n\nI am excited to apply.",
    )
    assert link.startswith("mailto:jobs@anthropic.com?")
    assert "subject=" in link
    assert "body=" in link
    assert "Niloy%20Sannyal" in link or "Niloy+Sannyal" in link


def test_generate_eml_message_with_pdf_attachment():
    dummy_pdf = b"%PDF-1.4 dummy pdf bytes"
    eml = EmailDispatchService.generate_eml_message(
        to_email="recruiter@openai.com",
        from_email="niloy@example.com",
        subject="AI Engineer Application",
        body_text="Please find my attached tailored CV.",
        attachment_bytes=dummy_pdf,
        attachment_filename="Tailored_CV_Niloy_Sannyal.pdf",
    )

    assert "To: recruiter@openai.com" in eml
    assert "From: niloy@example.com" in eml
    assert "Subject: AI Engineer Application" in eml
    assert "X-Unsent: 1" in eml
    assert "application/pdf" in eml
    assert "Tailored_CV_Niloy_Sannyal.pdf" in eml


def test_create_draft_rfc822():
    result = EmailDispatchService.create_draft(
        to_email="careers@scale.com",
        subject="Application: Scale AI",
        body_text="Enclosed please find my qualifications.",
        from_email="niloy@example.com",
        attachment_bytes=b"%PDF-1.4 test",
        attachment_filename="CV_Scale.pdf",
    )

    assert result.provider == EmailDraftProvider.RFC822_EML
    assert result.to_email == "careers@scale.com"
    assert result.has_attachment is True
    assert "mailto:careers@scale.com" in result.mailto_url
    assert "X-Unsent: 1" in result.eml_raw
    assert "Awaiting human review" in result.action_summary or "Click 'Launch Email'" in result.action_summary

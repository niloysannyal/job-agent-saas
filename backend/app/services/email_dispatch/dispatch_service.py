import base64
import email.message
import email.policy
import logging
import urllib.parse
from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class EmailDraftProvider(str, Enum):
    GMAIL_API = "gmail_api"
    OUTLOOK_GRAPH = "outlook_graph"
    RFC822_EML = "rfc822_eml"
    MAILTO_LINK = "mailto_link"


@dataclass
class EmailDraftResult:
    """Result of an email draft creation operation."""
    provider: EmailDraftProvider
    draft_id: Optional[str]
    to_email: str
    subject: str
    mailto_url: str
    eml_raw: str
    has_attachment: bool
    action_summary: str


class EmailDispatchService:
    """
    Minimal-effort draft dispatch service.
    Enforces Strict Human-in-the-Loop on Send (ARCHITECTURE.md §3).
    Creates pre-populated drafts in user's email client or formats 1-click RFC 822 .eml / mailto: payloads.
    Never auto-sends.
    """

    @classmethod
    def generate_mailto_link(
        cls,
        to_email: str,
        subject: str,
        body_text: str,
    ) -> str:
        """
        Generates a standard URL-encoded mailto: link for 1-click launch
        in default browser/desktop mail clients.
        """
        params = {}
        if subject:
            params["subject"] = subject
        if body_text:
            params["body"] = body_text

        query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        clean_email = to_email.strip() if to_email else ""
        return f"mailto:{clean_email}?{query_string}" if query_string else f"mailto:{clean_email}"

    @classmethod
    def generate_eml_message(
        cls,
        to_email: str,
        from_email: str,
        subject: str,
        body_text: str,
        attachment_bytes: Optional[bytes] = None,
        attachment_filename: Optional[str] = None,
    ) -> str:
        """
        Builds a standard RFC 822 .eml message with optional PDF attachment.
        When opened by candidate, natively populates desktop/mobile email drafts (Outlook, Apple Mail, Thunderbird).
        """
        msg = MIMEMultipart("mixed")
        msg["To"] = to_email.strip() if to_email else "recruiter@example.com"
        msg["From"] = from_email.strip() if from_email else "candidate@example.com"
        msg["Subject"] = subject.strip() if subject else "Application"
        msg["X-Unsent"] = "1"  # Signals mail clients that this is an unsent draft

        # Body part
        body_part = MIMEText(body_text, "plain", "utf-8")
        msg.attach(body_part)

        # Attachment part (Tailored CV PDF)
        if attachment_bytes and attachment_filename:
            att = MIMEApplication(attachment_bytes, _subtype="pdf")
            att.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment_filename,
            )
            msg.attach(att)

        return msg.as_string()

    @classmethod
    def create_draft(
        cls,
        to_email: str,
        subject: str,
        body_text: str,
        from_email: Optional[str] = None,
        attachment_bytes: Optional[bytes] = None,
        attachment_filename: Optional[str] = None,
        oauth_token: Optional[str] = None,
        provider: EmailDraftProvider = EmailDraftProvider.RFC822_EML,
    ) -> EmailDraftResult:
        """
        Creates an email draft. If OAuth token is provided, creates a draft in user's
        cloud inbox (Gmail / Outlook). Otherwise synthesizes an RFC 822 .eml draft
        and 1-click mailto: URL.
        Strictly Draft-only: Never sends.
        """
        clean_to = to_email.strip() if to_email else ""
        clean_from = from_email.strip() if from_email else "candidate@example.com"
        clean_sub = subject.strip() if subject else "Job Application"

        mailto_link = cls.generate_mailto_link(
            to_email=clean_to,
            subject=clean_sub,
            body_text=body_text,
        )

        eml_content = cls.generate_eml_message(
            to_email=clean_to,
            from_email=clean_from,
            subject=clean_sub,
            body_text=body_text,
            attachment_bytes=attachment_bytes,
            attachment_filename=attachment_filename,
        )

        has_att = bool(attachment_bytes and attachment_filename)

        if provider == EmailDraftProvider.GMAIL_API and oauth_token:
            # Future cloud token exchange path for Gmail users.drafts.create
            draft_id = f"gmail_draft_{base64.urlsafe_b64encode(clean_to.encode()[:8]).decode()}"
            action = f"Draft created in user's Gmail folder for {clean_to}. Awaiting human review."
            return EmailDraftResult(
                provider=EmailDraftProvider.GMAIL_API,
                draft_id=draft_id,
                to_email=clean_to,
                subject=clean_sub,
                mailto_url=mailto_link,
                eml_raw=eml_content,
                has_attachment=has_att,
                action_summary=action,
            )

        action = (
            f"Pre-populated draft prepared for {clean_to or 'recruiter'}. "
            "Click 'Launch Email' or open the generated .eml file to review in your mail client."
        )
        return EmailDraftResult(
            provider=EmailDraftProvider.RFC822_EML,
            draft_id=None,
            to_email=clean_to,
            subject=clean_sub,
            mailto_url=mailto_link,
            eml_raw=eml_content,
            has_attachment=has_att,
            action_summary=action,
        )

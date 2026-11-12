"""
backend/app/services/integrations/mime_builder.py

RFC 2822 & RFC 2046 Compliant MIME Message Builder for outbound email dispatch.
Enforces PDF magic-byte validation, Gmail 25 MB payload ceilings, and tracking headers.
"""

import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from typing import Dict, Optional

# Standard RFC 5322 compliant email regex
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

# Gmail hard message size ceiling (25 MB)
GMAIL_MAX_MESSAGE_BYTES = 25 * 1024 * 1024


class MimeBuilderException(Exception):
    """Base exception for MIME construction and validation errors."""
    pass


class InvalidEmailRecipientException(MimeBuilderException):
    """Raised when recipient email fails RFC 5322 validation."""
    pass


class InvalidPdfPayloadException(MimeBuilderException):
    """Raised when PDF bytes do not match valid %PDF-1. magic header."""
    pass


class MessageSizeExceededException(MimeBuilderException):
    """Raised when total MIME payload exceeds Gmail's 25 MB ceiling."""
    pass


class MimeBuilder:
    """
    Constructs compliant MIME messages with PDF attachments for Gmail API dispatch.
    """

    @staticmethod
    def validate_email_syntax(email_address: str) -> None:
        """Validate email address syntax against RFC 5322 standard."""
        if not email_address or not EMAIL_REGEX.match(email_address.strip()):
            raise InvalidEmailRecipientException(f"Invalid recipient email syntax: '{email_address}'")

    @staticmethod
    def build_message(
        to: str,
        subject: str,
        body_text: str,
        pdf_bytes: Optional[bytes] = None,
        pdf_filename: str = "Tailored_CV.pdf",
        send_id: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> bytes:
        """
        Build an RFC 2822 MIME message as raw bytes.

        Args:
            to: Recipient email address.
            subject: Subject line.
            body_text: Plaintext outreach body.
            pdf_bytes: Optional binary PDF attachment.
            pdf_filename: Attachment file name.
            send_id: Optional tracking UUID injected into X-JobEazy-Send-ID header.
            extra_headers: Optional headers (e.g. In-Reply-To, References).

        Returns:
            Raw MIME message as bytes.
        """
        # 1. Validate recipient syntax
        MimeBuilder.validate_email_syntax(to)

        # 2. Validate PDF attachment if present
        if pdf_bytes is not None:
            if not pdf_bytes.startswith(b"%PDF-1."):
                raise InvalidPdfPayloadException(
                    "Invalid PDF attachment: missing '%PDF-1.' magic byte header."
                )

        # 3. Construct MIME structure
        if pdf_bytes is not None:
            msg = MIMEMultipart("mixed")
            msg["To"] = to.strip()
            msg["Subject"] = subject

            # Plain text body part
            body_part = MIMEText(body_text, "plain", "utf-8")
            msg.attach(body_part)

            # PDF attachment part
            pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
            # Sanitize filename: replace quotes/newlines
            clean_filename = pdf_filename.replace('"', "").replace("\n", "").replace("\r", "")
            pdf_part.add_header(
                "Content-Disposition",
                "attachment",
                filename=clean_filename,
            )
            msg.attach(pdf_part)
        else:
            msg = MIMEText(body_text, "plain", "utf-8")
            msg["To"] = to.strip()
            msg["Subject"] = subject

        # 4. Inject tracking and custom headers
        if send_id:
            msg["X-JobEazy-Send-ID"] = str(send_id)

        if extra_headers:
            for k, v in extra_headers.items():
                if v and k not in msg:
                    msg[k] = v

        # 5. Serialize and check message size ceiling
        raw_bytes = msg.as_bytes()
        if len(raw_bytes) > GMAIL_MAX_MESSAGE_BYTES:
            raise MessageSizeExceededException(
                f"MIME message size ({len(raw_bytes)} bytes) exceeds Gmail 25 MB limit."
            )

        return raw_bytes

    @staticmethod
    def to_base64url(raw_bytes: bytes) -> str:
        """
        Encode raw MIME bytes to base64url string required by the Gmail API.
        """
        return base64.urlsafe_b64encode(raw_bytes).decode("ascii")


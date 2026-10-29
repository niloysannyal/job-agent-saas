import base64
import email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx

from app.core.config import settings
from app.core.crypto import encrypt_secret, decrypt_secret

logger = logging.getLogger(__name__)

GMAIL_COMPOSE_SCOPE = "https://www.googleapis.com/auth/gmail.compose https://www.googleapis.com/auth/userinfo.email"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GMAIL_DRAFT_URL = "https://gmail.googleapis.com/gmail/v1/users/me/drafts"


class GoogleIntegrationService:
    """
    Manages Google OAuth 2.0 flow and Human-In-The-Loop Gmail Draft creation.
    Strictly restricted to 'gmail.compose' scope — creates drafts only, NEVER auto-sends.
    """

    @staticmethod
    def get_authorization_url(state: str) -> str:
        """
        Generate the Google OAuth 2.0 consent URL requesting offline access
        and gmail.compose permissions.
        """
        client_id = settings.GOOGLE_CLIENT_ID or "mock-google-client-id.apps.googleusercontent.com"
        redirect_uri = settings.GOOGLE_REDIRECT_URI

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": GMAIL_COMPOSE_SCOPE,
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
        return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    @staticmethod
    async def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
        """
        Exchange an OAuth authorization code for access and refresh tokens.
        Fetches the user's primary email address.
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            # Mock exchange for local development/testing without live credentials
            logger.info("Using mock Google OAuth token exchange (no GCP credentials configured)")
            return {
                "access_token": f"mock_access_token_{code[:8]}",
                "refresh_token": f"mock_refresh_token_{code[:8]}",
                "expires_in": 3600,
                "scope": GMAIL_COMPOSE_SCOPE,
                "email": "user@gmail.com",
            }

        async with httpx.AsyncClient(timeout=15.0) as client:
            token_payload = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            resp = await client.post(GOOGLE_TOKEN_URL, data=token_payload)
            if resp.status_code != 200:
                logger.error("Failed to exchange Google OAuth code: %s", resp.text)
                raise ValueError(f"Google token exchange failed: {resp.text}")
            
            token_data = resp.json()
            access_token = token_data.get("access_token")

            # Fetch user email
            user_resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            email_addr = user_resp.json().get("email") if user_resp.status_code == 200 else None

            return {
                "access_token": access_token,
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in", 3600),
                "scope": token_data.get("scope", GMAIL_COMPOSE_SCOPE),
                "email": email_addr,
            }

    @staticmethod
    async def refresh_access_token(encrypted_refresh_token: str) -> str:
        """
        Refresh an expired access token using the stored encrypted refresh token.
        """
        refresh_token = decrypt_secret(encrypted_refresh_token)
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET or refresh_token.startswith("mock_"):
            return "mock_refreshed_access_token"

        async with httpx.AsyncClient(timeout=15.0) as client:
            payload = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            }
            resp = await client.post(GOOGLE_TOKEN_URL, data=payload)
            if resp.status_code != 200:
                raise ValueError(f"Google token refresh failed: {resp.text}")
            return resp.json().get("access_token")

    @staticmethod
    async def create_gmail_draft(
        access_token: str,
        to: str,
        subject: str,
        body_text: str,
        pdf_bytes: Optional[bytes] = None,
        pdf_filename: str = "Tailored_CV.pdf",
    ) -> Dict[str, Any]:
        """
        Create a Gmail Draft (X-Unsent) via official Gmail API.
        Never sends the email — user opens Gmail to review and click Send.
        """
        # Build RFC 2822 multipart message
        if pdf_bytes:
            msg = MIMEMultipart("mixed")
            msg["To"] = to
            msg["Subject"] = subject

            body_part = MIMEText(body_text, "plain", "utf-8")
            msg.attach(body_part)

            pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_part.add_header("Content-Disposition", "attachment", filename=pdf_filename)
            msg.attach(pdf_part)
        else:
            msg = MIMEText(body_text, "plain", "utf-8")
            msg["To"] = to
            msg["Subject"] = subject

        raw_bytes = msg.as_bytes()
        encoded_raw = base64.urlsafe_b64encode(raw_bytes).decode("ascii")

        if access_token.startswith("mock_"):
            # Mock draft creation for dev/testing
            mock_draft_id = "draft_mock_12345"
            mock_msg_id = "msg_mock_67890"
            return {
                "id": mock_draft_id,
                "message_id": mock_msg_id,
                "web_link": f"https://mail.google.com/mail/u/0/#drafts/{mock_msg_id}",
                "status": "draft_created",
            }

        async with httpx.AsyncClient(timeout=20.0) as client:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            draft_payload = {"message": {"raw": encoded_raw}}
            resp = await client.post(GMAIL_DRAFT_URL, headers=headers, json=draft_payload)
            if resp.status_code not in (200, 201):
                logger.error("Gmail draft creation error: %s", resp.text)
                raise ValueError(f"Failed to create Gmail draft: {resp.text}")

            result = resp.json()
            draft_id = result.get("id")
            message_id = result.get("message", {}).get("id")
            web_link = f"https://mail.google.com/mail/u/0/#drafts/{message_id}" if message_id else "https://mail.google.com/mail/u/0/#drafts"

            return {
                "id": draft_id,
                "message_id": message_id,
                "web_link": web_link,
                "status": "draft_created",
            }


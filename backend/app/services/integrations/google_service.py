import base64
import email
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx

from app.core.config import settings
from app.core.crypto import encrypt_oauth_token, decrypt_oauth_token
from app.services.integrations.mime_builder import MimeBuilder

logger = logging.getLogger(__name__)

# Scopes: Sensitive scopes (no CASA audit required)
GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
GMAIL_COMPOSE_SCOPE = "https://www.googleapis.com/auth/gmail.compose"
USERINFO_EMAIL_SCOPE = "https://www.googleapis.com/auth/userinfo.email"
GMAIL_FULL_OAUTH_SCOPES = f"{GMAIL_SEND_SCOPE} {GMAIL_COMPOSE_SCOPE} {USERINFO_EMAIL_SCOPE}"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GMAIL_DRAFT_URL = "https://gmail.googleapis.com/gmail/v1/users/me/drafts"
GMAIL_SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


# --- Custom Exception Hierarchy per Section 7 of Specification ---

class GmailApiException(Exception):
    """Base exception for Gmail API transmission and authorization failures."""
    pass


class GmailApiNotConfiguredException(GmailApiException):
    """Raised on 403 accessNotConfigured (Gmail API not enabled in GCP Console)."""
    pass


class GmailRateLimitException(GmailApiException):
    """Raised on 429 or 403 rateLimitExceeded / userRateLimitExceeded."""
    pass


class GmailInsufficientPermissionsException(GmailApiException):
    """Raised on 403 insufficientPermissions (token lacks required gmail.send scope)."""
    pass


class GmailServerErrorException(GmailApiException):
    """Raised on HTTP 5xx errors from Google servers."""
    pass


class GmailNetworkTimeoutException(GmailApiException):
    """Raised when Gmail dispatch exceeds the network deadline."""
    pass


class GoogleIntegrationService:
    """
    Manages Google OAuth 2.0 authentication, human-in-the-loop Gmail Draft creation,
    and verified outbound email dispatch via official Gmail API.
    Supports dynamic DB-configured platform credentials with fallback to .env settings.
    """

    @classmethod
    def resolve_platform_credentials(
        cls,
        db: Optional[Any] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Dynamically resolve platform Google OAuth 2.0 app credentials:
        1. Query 'platform_oauth_configs' for provider='google' and is_active=True.
           (Tenant override first if account_id is provided, then platform-wide account_id=NULL).
        2. If not found or incomplete in DB, fall back to backend/.env (settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET).
        """
        from app.core.crypto import decrypt_secret
        from app.models.oauth import PlatformOAuthAppConfig

        db_created = False
        if db is None:
            try:
                from app.db.session import SessionLocal
                db = SessionLocal()
                db_created = True
            except Exception:
                db = None

        if db is not None:
            try:
                query = db.query(PlatformOAuthAppConfig).filter(
                    PlatformOAuthAppConfig.provider == "google",
                    PlatformOAuthAppConfig.is_active.is_(True),
                )
                if account_id:
                    query = query.filter(
                        (PlatformOAuthAppConfig.account_id == account_id) |
                        (PlatformOAuthAppConfig.account_id.is_(None))
                    ).order_by(PlatformOAuthAppConfig.account_id.desc().nulls_last())
                else:
                    query = query.filter(PlatformOAuthAppConfig.account_id.is_(None))

                config_row = query.first()
                if config_row and config_row.client_id:
                    secret = (
                        decrypt_secret(config_row.encrypted_client_secret)
                        if config_row.encrypted_client_secret
                        else None
                    )
                    effective_secret = secret or settings.GOOGLE_CLIENT_SECRET
                    effective_redirect = config_row.redirect_uri or settings.GOOGLE_REDIRECT_URI
                    return {
                        "client_id": config_row.client_id,
                        "client_secret": effective_secret,
                        "redirect_uri": effective_redirect,
                        "source": "db",
                        "has_secret": bool(effective_secret),
                        "is_active": config_row.is_active,
                    }
            except Exception as e:
                logger.warning("Could not query platform_oauth_configs from DB: %s", e)
            finally:
                if db_created:
                    try:
                        db.close()
                    except Exception:
                        pass

        # Fallback to .env settings
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        has_secret = bool(client_secret)
        source = "env" if (client_id and client_secret) else ("partial_env" if client_id else "none")

        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "source": source,
            "has_secret": has_secret,
            "is_active": True,
        }

    @classmethod
    def get_authorization_url(
        cls,
        state: str,
        db: Optional[Any] = None,
        account_id: Optional[str] = None,
    ) -> str:
        """
        Generate the Google OAuth 2.0 consent URL requesting offline access
        and full permissions (gmail.send, gmail.compose, userinfo.email).
        """
        creds = cls.resolve_platform_credentials(db=db, account_id=account_id)
        client_id = creds.get("client_id") or "mock-google-client-id.apps.googleusercontent.com"
        redirect_uri = creds.get("redirect_uri") or settings.GOOGLE_REDIRECT_URI

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": GMAIL_FULL_OAUTH_SCOPES,
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
        return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    @classmethod
    async def exchange_code_for_tokens(
        cls,
        code: str,
        db: Optional[Any] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Exchange an OAuth authorization code for access and refresh tokens.
        Fetches the user's primary email address.
        """
        creds = cls.resolve_platform_credentials(db=db, account_id=account_id)
        client_id = creds.get("client_id")
        client_secret = creds.get("client_secret")
        redirect_uri = creds.get("redirect_uri") or settings.GOOGLE_REDIRECT_URI

        if not client_id or not client_secret:
            # Mock exchange for local development/testing without live credentials
            logger.info("Using mock Google OAuth token exchange (no GCP credentials configured)")
            return {
                "access_token": f"mock_access_token_{code[:8]}",
                "refresh_token": f"mock_refresh_token_{code[:8]}",
                "expires_in": 3600,
                "scope": GMAIL_FULL_OAUTH_SCOPES,
                "email": "user@gmail.com",
            }

        async with httpx.AsyncClient(timeout=15.0) as client:
            token_payload = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
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
                "scope": token_data.get("scope", GMAIL_FULL_OAUTH_SCOPES),
                "email": email_addr,
            }

    @classmethod
    async def refresh_access_token(
        cls,
        encrypted_refresh_token: str,
        db: Optional[Any] = None,
        account_id: Optional[str] = None,
    ) -> str:
        """
        Refresh an expired access token using the stored encrypted refresh token.
        Uses MultiFernet for decryption.
        """
        refresh_token = decrypt_oauth_token(encrypted_refresh_token)
        creds = cls.resolve_platform_credentials(db=db, account_id=account_id)
        client_id = creds.get("client_id")
        client_secret = creds.get("client_secret")

        if not client_id or not client_secret or (refresh_token and refresh_token.startswith("mock_")):
            return "mock_refreshed_access_token"

        async with httpx.AsyncClient(timeout=15.0) as client:
            payload = {
                "client_id": client_id,
                "client_secret": client_secret,
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
        raw_bytes = MimeBuilder.build_message(
            to=to,
            subject=subject,
            body_text=body_text,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
        )
        encoded_raw = MimeBuilder.to_base64url(raw_bytes)

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

    @staticmethod
    async def send_gmail_message(
        access_token: str,
        raw_mime_bytes: bytes,
        timeout: float = 30.0,
    ) -> Dict[str, Any]:
        """
        Send an outbound email message via official Gmail API messages.send.

        Args:
            access_token: Active Google OAuth access token.
            raw_mime_bytes: Raw RFC 2822 MIME bytes.
            timeout: Network timeout in seconds (default 30.0).

        Returns:
            Dict containing 'id' (message ID), 'threadId', and 'labelIds'.
        """
        raw_base64 = MimeBuilder.to_base64url(raw_mime_bytes)

        if access_token.startswith("mock_"):
            # Mock dispatch for testing/dev environments without active GCP credentials
            import uuid
            mock_msg_id = f"mock_sent_msg_{uuid.uuid4().hex[:12]}"
            mock_thread_id = f"mock_thread_{uuid.uuid4().hex[:12]}"
            logger.info("Executed mock Gmail dispatch: msg_id=%s", mock_msg_id)
            return {
                "id": mock_msg_id,
                "threadId": mock_thread_id,
                "labelIds": ["SENT"],
            }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {"raw": raw_base64}

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(GMAIL_SEND_URL, headers=headers, json=payload)
        except httpx.TimeoutException as e:
            logger.error("Gmail API timeout during dispatch: %s", e)
            raise GmailNetworkTimeoutException(f"Gmail send timed out after {timeout}s") from e
        except httpx.RequestError as e:
            logger.error("Gmail API network request error: %s", e)
            raise GmailApiException(f"Network error communicating with Gmail API: {e}") from e

        if resp.status_code in (200, 201):
            data = resp.json()
            return {
                "id": data.get("id"),
                "threadId": data.get("threadId"),
                "labelIds": data.get("labelIds", ["SENT"]),
            }

        # Handle and map error responses per Section 7 of specification
        status_code = resp.status_code
        try:
            error_json = resp.json().get("error", {})
            error_message = error_json.get("message", resp.text)
            errors_list = error_json.get("errors", [])
            reason = errors_list[0].get("reason", "") if errors_list else ""
        except Exception:
            error_message = resp.text
            reason = ""

        logger.error(
            "Gmail send failed with status %d: reason='%s', message='%s'",
            status_code, reason, error_message,
        )

        if status_code == 403:
            if reason == "accessNotConfigured":
                raise GmailApiNotConfiguredException(f"Gmail API not configured in GCP project: {error_message}")
            elif reason in ("rateLimitExceeded", "userRateLimitExceeded"):
                raise GmailRateLimitException(f"Gmail rate limit exceeded: {error_message}")
            elif reason == "insufficientPermissions":
                raise GmailInsufficientPermissionsException(
                    f"OAuth token lacks required gmail.send scope: {error_message}"
                )
            else:
                raise GmailApiException(f"Gmail API 403 forbidden ({reason}): {error_message}")

        elif status_code == 429:
            raise GmailRateLimitException(f"Gmail API 429 too many requests: {error_message}")

        elif 500 <= status_code < 600:
            raise GmailServerErrorException(f"Gmail API server error {status_code}: {error_message}")

        else:
            raise GmailApiException(f"Gmail send failed with HTTP {status_code}: {error_message}")

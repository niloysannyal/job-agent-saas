import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class OAuthConnection(Base):
    """
    Multi-tenant OAuth Connection model.
    Stores authorized OAuth 2.0 access and refresh tokens for third-party integrations
    (Google Gmail, Microsoft Outlook) encrypted at rest.
    Strictly Draft-Only: tokens are only used to create drafts, never to auto-send.
    """
    __tablename__ = "oauth_connections"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # 'google' | 'microsoft'
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # The connected account's email (e.g. niloysannyal@gmail.com)
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    # Encrypted access token
    encrypted_access_token: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    # Encrypted refresh token
    encrypted_refresh_token: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    scope: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="oauth_connections",
    )


# --- Pydantic Schemas ---

class OAuthConnectionBase(BaseModel):
    account_id: str
    provider: str
    email: Optional[str] = None
    scope: Optional[str] = None


class OAuthConnectionCreate(OAuthConnectionBase):
    encrypted_access_token: Optional[str] = None
    encrypted_refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class OAuthConnectionRead(OAuthConnectionBase):
    id: str
    token_expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


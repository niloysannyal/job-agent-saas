import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class LLMProviderConfig(Base):
    """
    LLM provider configuration table matching ARCHITECTURE.md §11.
    Allows admin/system to configure active providers, priorities (OpenAI -> Claude failover),
    and per-account BYOK overrides without code changes.
    """
    __tablename__ = "llm_providers"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Optional account_id: NULL for platform-wide default provider, UUID for tenant BYOK
    account_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    # 'openai' | 'anthropic' | 'openrouter' | 'gemini'
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    # e.g. 'gpt-4o-mini', 'gpt-4o', 'claude-3-5-sonnet'
    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    # Encrypted API key at rest per ARCHITECTURE.md §8 & AGENTS.md
    encrypted_api_key: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    # Priority for provider failover chain: lower number = higher priority (1 = primary)
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    # Provider-specific configuration (temperature, max_tokens, reasoning_effort)
    config: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
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
    account: Mapped[Optional["Account"]] = relationship(
        "Account",
        back_populates="llm_providers",
    )


# --- Pydantic Schemas ---

class LLMProviderBase(BaseModel):
    provider: str
    model_name: str
    account_id: Optional[str] = None
    is_active: bool = True
    priority: int = 1
    config: Optional[Dict[str, Any]] = None


class LLMProviderCreate(LLMProviderBase):
    api_key: Optional[str] = None  # Plaintext key at ingestion time, encrypted before DB storage


class LLMProviderUpdate(BaseModel):
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    config: Optional[Dict[str, Any]] = None


class LLMProviderRead(LLMProviderBase):
    id: str
    # Note: encrypted_api_key is never exposed in full in read schemas
    has_api_key: bool = False
    key_source: str = "missing"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

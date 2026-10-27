import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.cv_template import AccountCvVersion, CvTemplate
    from app.models.interview import StarStory
    from app.models.job import Job
    from app.models.llm_provider import LLMProviderConfig
    from app.models.profile import UserProfile
    from app.models.subscription import Entitlement


class Account(Base):
    """
    Multi-tenant Account model matching ARCHITECTURE.md §7.
    Every tenant has an account row, starting with Niloy as tenant #1.
    """
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    # Default 'free', unenforced per ARCHITECTURE.md §7
    plan_tier: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="free",
    )
    # Template limit per ARCHITECTURE.md §5 (default = unlimited, None)
    account_template_limit: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
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
    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    cv_templates: Mapped[List["CvTemplate"]] = relationship(
        "CvTemplate",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    cv_versions: Mapped[List["AccountCvVersion"]] = relationship(
        "AccountCvVersion",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    entitlement: Mapped[Optional["Entitlement"]] = relationship(
        "Entitlement",
        back_populates="account",
        cascade="all, delete-orphan",
        uselist=False,
    )
    llm_providers: Mapped[List["LLMProviderConfig"]] = relationship(
        "LLMProviderConfig",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="account",
        cascade="all, delete-orphan",
        uselist=False,
    )
    star_stories: Mapped[List["StarStory"]] = relationship(
        "StarStory",
        back_populates="account",
        cascade="all, delete-orphan",
    )


# --- Pydantic Schemas ---

class AccountBase(BaseModel):
    email: str
    plan_tier: str = "free"
    account_template_limit: Optional[int] = None


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    email: Optional[str] = None
    plan_tier: Optional[str] = None
    account_template_limit: Optional[int] = None


class AccountRead(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

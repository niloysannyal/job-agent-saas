import uuid
import bcrypt
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.cv_template import AccountCvVersion, CvTemplate
    from app.models.interview import StarStory
    from app.models.job import Job
    from app.models.llm_provider import LLMProviderConfig
    from app.models.oauth import OAuthConnection
    from app.models.profile import UserProfile, UserResume
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
    # Role: 'superadmin' | 'tenant'
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="tenant",
    )
    # Status: 'active' | 'invited' | 'suspended'
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )
    # Hashed password for authentication
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
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
    oauth_connections: Mapped[List["OAuthConnection"]] = relationship(
        "OAuthConnection",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    resumes: Mapped[List["UserResume"]] = relationship(
        "UserResume",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        """Hash and set account password with bcrypt salt."""
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify password against stored bcrypt hash."""
        if not self.hashed_password:
            return False
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                self.hashed_password.encode("utf-8")
            )
        except Exception:
            return False


class EmailVerification(Base):
    """
    Stores 6-digit OTP verification codes for user registration and email validation.
    Codes expire after OTP_EXPIRE_MINUTES (default 10) and allow max 5 attempts.
    """
    __tablename__ = "email_verifications"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    otp_code: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


# --- Pydantic Schemas ---

class AccountBase(BaseModel):
    email: str
    plan_tier: str = "free"
    role: str = "tenant"
    status: str = "active"
    account_template_limit: Optional[int] = None


class AccountCreate(AccountBase):
    password: Optional[str] = None
    full_name: Optional[str] = None


class AccountUpdate(BaseModel):
    email: Optional[str] = None
    plan_tier: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    account_template_limit: Optional[int] = None


class AccountRead(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: str
    password: str


class SendOtpRequest(BaseModel):
    email: str


class SendOtpResponse(BaseModel):
    status: str
    email: str
    message: str
    dev_otp: Optional[str] = None


class VerifyOtpSignupRequest(BaseModel):
    email: str
    otp_code: str
    password: str
    full_name: str
    headline: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    account_id: str
    email: str
    role: str
    plan_tier: str
    is_new_user: bool = False


class AuthMeResponse(BaseModel):
    id: str
    email: str
    role: str
    status: str
    plan_tier: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

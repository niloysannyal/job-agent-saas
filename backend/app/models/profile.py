"""
Multi-tenant User Profile models matching ARCHITECTURE.md §7.
Captures everything from USER_PROFILE.md that the Find/Apply/Monitor pipeline
needs as structured data rather than free-text parsing at runtime.
"""
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


# ---------------------------------------------------------------------------
# SQLAlchemy ORM models
# ---------------------------------------------------------------------------

class UserProfile(Base):
    """
    Core profile for a user (one-to-one with Account).
    Stores identity, narrative, and working-style context used by
    the CV tailoring and outreach drafting pipelines.
    """
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        unique=True, index=True, nullable=False,
    )
    # --- Basic info ---
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    current_company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    education: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location_country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    portfolio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # --- Positioning & narrative ---
    core_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    primary_identity: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    one_liner: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    engineering_principle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avoid_phrases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Working style ---
    working_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    leadership_example: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Job search context ---
    dealbreakers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notice_period: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    visa_needs: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reason_for_leaving: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Tone & preferences ---
    tone_preferences: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- CV source ---
    master_cv_latex: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Timestamps ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="profile")
    target_designations: Mapped[List["TargetDesignation"]] = relationship(
        "TargetDesignation", back_populates="profile", cascade="all, delete-orphan",
    )
    target_locations: Mapped[List["TargetLocation"]] = relationship(
        "TargetLocation", back_populates="profile", cascade="all, delete-orphan",
    )
    compensation: Mapped[Optional["CompensationExpectation"]] = relationship(
        "CompensationExpectation", back_populates="profile",
        cascade="all, delete-orphan", uselist=False,
    )
    spoken_languages: Mapped[List["SpokenLanguage"]] = relationship(
        "SpokenLanguage", back_populates="profile", cascade="all, delete-orphan",
    )


class TargetDesignation(Base):
    """
    Target job titles / designations a user is searching for.
    Per ARCHITECTURE.md §1: nothing about role is hardcoded — it's per-user config.
    """
    __tablename__ = "target_designations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    profile_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user_profiles.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
        doc="Lower = higher priority. Used to rank search queries.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="target_designations",
    )


class TargetLocation(Base):
    """
    Target work locations / regions a user is willing to work in.
    Supports remote / hybrid / on-site flags per location.
    """
    __tablename__ = "target_locations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    profile_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user_profiles.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    location_name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        doc="City, region, or country (e.g. 'EU', 'Dhaka, Bangladesh').",
    )
    location_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="any",
        doc="'remote' | 'onsite' | 'hybrid' | 'any'",
    )
    relocation_willing: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="target_locations",
    )


class CompensationExpectation(Base):
    """
    Salary / compensation expectations (one per profile).
    Marked sensitive — never auto-included in outbound messages per USER_PROFILE.md.
    """
    __tablename__ = "compensation_expectations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        unique=True, index=True, nullable=False,
    )
    profile_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user_profiles.id", ondelete="CASCADE"),
        unique=True, index=True, nullable=False,
    )
    min_salary: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_salary: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(
        String(10), nullable=False, default="USD",
    )
    period: Mapped[str] = mapped_column(
        String(20), nullable=False, default="yearly",
        doc="'yearly' | 'monthly' | 'hourly'",
    )
    is_negotiable: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,
    )
    # Never include salary in outbound messages unless user explicitly provides
    # a figure for that specific application
    is_sensitive: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="compensation",
    )


class SpokenLanguage(Base):
    """
    Languages the user speaks, with proficiency level.
    Used by the language gate in the Find module (ARCHITECTURE.md §4).
    """
    __tablename__ = "spoken_languages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    profile_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user_profiles.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    language: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    proficiency: Mapped[str] = mapped_column(
        String(50), nullable=False, default="fluent",
        doc="'native' | 'fluent' | 'professional' | 'intermediate' | 'basic'",
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="spoken_languages",
    )


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class TargetDesignationBase(BaseModel):
    title: str
    priority: int = 0
    is_active: bool = True


class TargetDesignationCreate(TargetDesignationBase):
    pass


class TargetDesignationRead(TargetDesignationBase):
    id: str
    account_id: str
    profile_id: str
    model_config = ConfigDict(from_attributes=True)


class TargetLocationBase(BaseModel):
    location_name: str
    location_type: str = "any"
    relocation_willing: bool = False
    is_active: bool = True


class TargetLocationCreate(TargetLocationBase):
    pass


class TargetLocationRead(TargetLocationBase):
    id: str
    account_id: str
    profile_id: str
    model_config = ConfigDict(from_attributes=True)


class CompensationBase(BaseModel):
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: str = "USD"
    period: str = "yearly"
    is_negotiable: bool = True
    is_sensitive: bool = True


class CompensationCreate(CompensationBase):
    pass


class CompensationRead(CompensationBase):
    id: str
    account_id: str
    profile_id: str
    model_config = ConfigDict(from_attributes=True)


class SpokenLanguageBase(BaseModel):
    language: str
    proficiency: str = "fluent"


class SpokenLanguageCreate(SpokenLanguageBase):
    pass


class SpokenLanguageRead(SpokenLanguageBase):
    id: str
    account_id: str
    profile_id: str
    model_config = ConfigDict(from_attributes=True)


class UserProfileBase(BaseModel):
    full_name: str
    current_role: Optional[str] = None
    current_company: Optional[str] = None
    education: Optional[str] = None
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    core_narrative: Optional[str] = None
    primary_identity: Optional[str] = None
    one_liner: Optional[str] = None
    engineering_principle: Optional[str] = None
    avoid_phrases: Optional[str] = None
    working_style: Optional[str] = None
    leadership_example: Optional[str] = None
    dealbreakers: Optional[str] = None
    notice_period: Optional[str] = None
    visa_needs: Optional[str] = None
    reason_for_leaving: Optional[str] = None
    tone_preferences: Optional[str] = None
    master_cv_latex: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    current_role: Optional[str] = None
    current_company: Optional[str] = None
    education: Optional[str] = None
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    core_narrative: Optional[str] = None
    primary_identity: Optional[str] = None
    one_liner: Optional[str] = None
    engineering_principle: Optional[str] = None
    avoid_phrases: Optional[str] = None
    working_style: Optional[str] = None
    leadership_example: Optional[str] = None
    dealbreakers: Optional[str] = None
    notice_period: Optional[str] = None
    visa_needs: Optional[str] = None
    reason_for_leaving: Optional[str] = None
    tone_preferences: Optional[str] = None
    master_cv_latex: Optional[str] = None


class UserProfileRead(UserProfileBase):
    id: str
    account_id: str
    target_designations: List[TargetDesignationRead] = Field(default_factory=list)
    target_locations: List[TargetLocationRead] = Field(default_factory=list)
    compensation: Optional[CompensationRead] = None
    spoken_languages: List[SpokenLanguageRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

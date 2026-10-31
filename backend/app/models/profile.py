"""
Multi-tenant User Profile models matching ARCHITECTURE.md §7.
Captures standard career entities (Work Experiences, Education, Skills, Projects,
Certifications) and preferences that the Find/Apply/Monitor pipeline needs as
structured data rather than free-text parsing at runtime.
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
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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

    # --- Template selection & legacy source ---
    active_template_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cv_templates.id", ondelete="SET NULL"),
        nullable=True,
    )
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
    work_experiences: Mapped[List["WorkExperience"]] = relationship(
        "WorkExperience", back_populates="profile", cascade="all, delete-orphan",
        order_by="WorkExperience.order_index",
    )
    educations: Mapped[List["Education"]] = relationship(
        "Education", back_populates="profile", cascade="all, delete-orphan",
        order_by="Education.order_index",
    )
    skills: Mapped[List["ProfileSkill"]] = relationship(
        "ProfileSkill", back_populates="profile", cascade="all, delete-orphan",
        order_by="ProfileSkill.order_index",
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="profile", cascade="all, delete-orphan",
        order_by="Project.order_index",
    )
    certifications: Mapped[List["Certification"]] = relationship(
        "Certification", back_populates="profile", cascade="all, delete-orphan",
        order_by="Certification.order_index",
    )


class WorkExperience(Base):
    """
    Structured work experience entity for candidates across all industries.
    Provides verifiable, chronological career history for CV tailoring.
    """
    __tablename__ = "work_experiences"

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
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="onsite",
        doc="'onsite' | 'remote' | 'hybrid'",
    )
    start_date: Mapped[str] = mapped_column(String(50), nullable=False)
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    highlights: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="JSON list of bullet points or newline-separated accomplishments",
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="work_experiences",
    )


class Education(Base):
    """
    Structured education background (degrees, high school, certifications, coursework).
    """
    __tablename__ = "educations"

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
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(255), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    grade: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    activities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="educations",
    )


class ProfileSkill(Base):
    """
    Structured skill entity with taxonomy categorization and proficiency.
    """
    __tablename__ = "profile_skills"

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
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Technical",
        doc="e.g. 'Languages', 'Frameworks', 'Tools', 'Management', 'Soft Skills'",
    )
    proficiency: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Intermediate",
        doc="'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'",
    )
    years_of_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="skills",
    )


class Project(Base):
    """
    Portfolio projects, open-source work, or major professional deliverables.
    """
    __tablename__ = "projects"

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
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    highlights: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="JSON list of bullet points or newline-separated achievements",
    )
    technologies: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="Comma-separated or JSON list of tools/tech used",
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="projects",
    )


class Certification(Base):
    """
    Professional certifications, licenses, and credentials.
    """
    __tablename__ = "certifications"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String(255), nullable=False)
    issue_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expiration_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    credential_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    credential_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="certifications",
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

# WorkExperience Schemas
class WorkExperienceBase(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    location_type: str = "onsite"
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None
    highlights: Optional[str] = None
    order_index: int = 0


class WorkExperienceCreate(WorkExperienceBase):
    pass


class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    highlights: Optional[str] = None
    order_index: Optional[int] = None


class WorkExperienceRead(WorkExperienceBase):
    id: str
    account_id: str
    profile_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Education Schemas
class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None
    activities: Optional[str] = None
    order_index: int = 0


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None
    activities: Optional[str] = None
    order_index: Optional[int] = None


class EducationRead(EducationBase):
    id: str
    account_id: str
    profile_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ProfileSkill Schemas
class ProfileSkillBase(BaseModel):
    name: str
    category: str = "Technical"
    proficiency: str = "Intermediate"
    years_of_experience: Optional[float] = None
    order_index: int = 0


class ProfileSkillCreate(ProfileSkillBase):
    pass


class ProfileSkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency: Optional[str] = None
    years_of_experience: Optional[float] = None
    order_index: Optional[int] = None


class ProfileSkillRead(ProfileSkillBase):
    id: str
    account_id: str
    profile_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Project Schemas
class ProjectBase(BaseModel):
    title: str
    role: Optional[str] = None
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[str] = None
    technologies: Optional[str] = None
    order_index: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[str] = None
    technologies: Optional[str] = None
    order_index: Optional[int] = None


class ProjectRead(ProjectBase):
    id: str
    account_id: str
    profile_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Certification Schemas
class CertificationBase(BaseModel):
    name: str
    issuing_organization: str
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    order_index: int = 0


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    order_index: Optional[int] = None


class CertificationRead(CertificationBase):
    id: str
    account_id: str
    profile_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Target & Preference Schemas
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


# Core Profile Schemas
class UserProfileBase(BaseModel):
    full_name: str
    headline: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
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
    active_template_id: Optional[str] = None
    master_cv_latex: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
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
    active_template_id: Optional[str] = None
    master_cv_latex: Optional[str] = None


class UserProfileRead(UserProfileBase):
    id: str
    account_id: str
    target_designations: List[TargetDesignationRead] = Field(default_factory=list)
    target_locations: List[TargetLocationRead] = Field(default_factory=list)
    compensation: Optional[CompensationRead] = None
    spoken_languages: List[SpokenLanguageRead] = Field(default_factory=list)
    work_experiences: List[WorkExperienceRead] = Field(default_factory=list)
    educations: List[EducationRead] = Field(default_factory=list)
    skills: List[ProfileSkillRead] = Field(default_factory=list)
    projects: List[ProjectRead] = Field(default_factory=list)
    certifications: List[CertificationRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

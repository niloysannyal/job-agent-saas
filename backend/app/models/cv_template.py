import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.application import Application
    from app.models.job import Job


class CvTemplate(Base):
    """
    LaTeX CV template model matching ARCHITECTURE.md §5 & §7.
    Admin-curated system templates have account_id = None.
    User-created/custom templates have account_id set to their account.
    """
    __tablename__ = "cv_templates"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Optional account_id: NULL for admin-curated global templates, UUID for custom
    account_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    latex_source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_admin_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
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
        back_populates="cv_templates",
    )
    cv_versions: Mapped[List["AccountCvVersion"]] = relationship(
        "AccountCvVersion",
        back_populates="template",
    )


class AccountCvVersion(Base):
    """
    Tailored CV version model matching ARCHITECTURE.md §7:
    (which tailored CV went to which job).
    Capped per account (default last 20 per §8).
    """
    __tablename__ = "account_cv_versions"

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
    job_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    cv_template_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("cv_templates.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    tailored_latex: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    pdf_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    ats_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    page_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    # Relevance-weighted line cutting decisions
    cut_summary: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
    )
    # 'draft' | 'compiled' | 'flagged' | 'sent'
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
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
        back_populates="cv_versions",
    )
    job: Mapped[Optional["Job"]] = relationship(
        "Job",
        back_populates="cv_versions",
    )
    template: Mapped[Optional["CvTemplate"]] = relationship(
        "CvTemplate",
        back_populates="cv_versions",
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="cv_version",
    )


# --- Pydantic Schemas ---

class CvTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    latex_source: str
    is_admin_default: bool = False
    account_id: Optional[str] = None


class CvTemplateCreate(CvTemplateBase):
    pass


class CvTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    latex_source: Optional[str] = None
    is_admin_default: Optional[bool] = None


class CvTemplateRead(CvTemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountCvVersionBase(BaseModel):
    account_id: str
    job_id: Optional[str] = None
    cv_template_id: Optional[str] = None
    tailored_latex: str
    pdf_path: Optional[str] = None
    ats_score: Optional[float] = None
    page_count: Optional[int] = None
    cut_summary: Optional[Dict[str, Any]] = None
    status: str = "draft"


class AccountCvVersionCreate(AccountCvVersionBase):
    pass


class AccountCvVersionUpdate(BaseModel):
    tailored_latex: Optional[str] = None
    pdf_path: Optional[str] = None
    ats_score: Optional[float] = None
    page_count: Optional[int] = None
    cut_summary: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class AccountCvVersionRead(AccountCvVersionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

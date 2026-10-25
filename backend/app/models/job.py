import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class Job(Base):
    """
    Multi-tenant Job model matching ARCHITECTURE.md §7:
    (account_id, company, role, salary, deadline, location_type, country,
     visa_required, target_company, match_score, status, source, apply_link, found_at)
    """
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Multi-tenant isolation: every row belongs to an account
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    company: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    salary: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    salary_min: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    salary_max: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    currency: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
    )
    deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    # e.g., 'on-site', 'remote', 'hybrid'
    location_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    country: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    city: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    visa_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    target_company: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    match_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    # Application-pipeline status per ARCHITECTURE.md §6 (default: 'new')
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="new",
    )
    # Posting integrity gate outcome: 'clean' | 'flagged'
    integrity_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="clean",
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    source_job_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    apply_link: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    found_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
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
    raw_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
    )

    # Relationships
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="jobs",
    )


# --- DTO and Pydantic Schemas ---

class JobSearchQuery(BaseModel):
    """Normalized query parameters for searching across job sources."""
    what: str = Field(..., description="Keywords or job title to search for")
    where: Optional[str] = Field(default=None, description="Location, city, or region")
    country: str = Field(default="gb", description="2-letter country code (e.g. gb, us, de)")
    page: int = Field(default=1, ge=1, description="Page number")
    results_per_page: int = Field(default=20, ge=1, le=50, description="Results per page")
    salary_min: Optional[int] = Field(default=None, description="Minimum salary")
    salary_max: Optional[int] = Field(default=None, description="Maximum salary")
    full_time: Optional[bool] = Field(default=None, description="Filter for full time positions")
    permanent: Optional[bool] = Field(default=None, description="Filter for permanent positions")
    contract: Optional[bool] = Field(default=None, description="Filter for contract positions")
    max_days_old: Optional[int] = Field(default=None, description="Limit to jobs posted within N days")
    distance: Optional[float] = Field(default=None, description="Distance from location in km")


class JobPosting(BaseModel):
    """
    Standardized JobPosting DTO returned by all JobSource.fetch implementations.
    Matches ARCHITECTURE.md §4 plugin contract.
    """
    id: str = Field(..., description="Unique job ID from source or composite ID")
    source: str = Field(..., description="Source name (e.g. adzuna, remotive, remoteok)")
    company: str
    role: str
    description: str = ""
    apply_link: str
    salary: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None  # on-site, remote, hybrid
    country: Optional[str] = None
    city: Optional[str] = None
    deadline: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    raw_data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="ignore")


class JobBase(BaseModel):
    company: str
    role: str
    description: Optional[str] = None
    salary: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    deadline: Optional[datetime] = None
    location_type: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    visa_required: bool = False
    target_company: bool = False
    match_score: Optional[float] = None
    status: str = "new"
    integrity_status: str = "clean"
    source: str
    source_job_id: Optional[str] = None
    apply_link: str


class JobCreate(JobBase):
    account_id: str
    found_at: Optional[datetime] = None
    raw_data: Optional[Dict[str, Any]] = None


class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    deadline: Optional[datetime] = None
    location_type: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    visa_required: Optional[bool] = None
    target_company: Optional[bool] = None
    match_score: Optional[float] = None
    status: Optional[str] = None
    integrity_status: Optional[str] = None
    source: Optional[str] = None
    source_job_id: Optional[str] = None
    apply_link: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class JobRead(JobBase):
    id: str
    account_id: str
    found_at: datetime
    created_at: datetime
    updated_at: datetime
    raw_data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

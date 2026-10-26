import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.cv_template import AccountCvVersion
    from app.models.job import Job


class Application(Base):
    """
    Multi-tenant Application model matching ARCHITECTURE.md §6 & §7:
    (job_id, channel, draft_content, sent_at, status, follow_up_due, follow_up_count)
    Enforces human-in-the-loop: sent_at is populated only upon human Send.
    Follow-up count defaults to 0 and is capped in app logic (max 2 per §6).
    """
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Multi-tenant isolation
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    cv_version_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("account_cv_versions.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    # 'email' | 'form' | 'dm' | 'portal'
    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="email",
    )
    draft_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    # Timestamp when human reviews and triggers Send (None while in draft)
    sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    # 'draft' | 'reviewed' | 'sent' | 'responded' | 'interview' | 'rejected' | 'offer'
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
    )
    follow_up_due: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    follow_up_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    notes: Mapped[Optional[str]] = mapped_column(
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
        back_populates="applications",
    )
    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="applications",
    )
    cv_version: Mapped[Optional["AccountCvVersion"]] = relationship(
        "AccountCvVersion",
        back_populates="applications",
    )

    @property
    def job_company(self) -> Optional[str]:
        return self.job.company if self.job else None

    @property
    def job_role(self) -> Optional[str]:
        return self.job.role if self.job else None


# --- Pydantic Schemas ---

class ApplicationBase(BaseModel):
    account_id: str
    job_id: str
    cv_version_id: Optional[str] = None
    channel: str = "email"
    draft_content: Optional[str] = None
    sent_at: Optional[datetime] = None
    status: str = "draft"
    follow_up_due: Optional[datetime] = None
    follow_up_count: int = 0
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    channel: Optional[str] = None
    draft_content: Optional[str] = None
    sent_at: Optional[datetime] = None
    status: Optional[str] = None
    follow_up_due: Optional[datetime] = None
    follow_up_count: Optional[int] = None
    notes: Optional[str] = None


class ApplicationRead(ApplicationBase):
    id: str
    job_company: Optional[str] = None
    job_role: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

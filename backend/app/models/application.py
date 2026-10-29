import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
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
    form_answers: Mapped[List["ApplicationFormAnswer"]] = relationship(
        "ApplicationFormAnswer",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    @property
    def job_company(self) -> Optional[str]:
        return self.job.company if self.job else None

    @property
    def job_role(self) -> Optional[str]:
        return self.job.role if self.job else None


class ApplicationFormAnswer(Base):
    """
    Stores structured questions and answers for a specific job application form.
    Maintains multi-tenant isolation with account_id.
    """
    __tablename__ = "application_form_answers"

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
    application_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applications.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    question_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    question_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    field_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="paragraph",
    )
    tailored_answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    candidate_angles: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON-encoded candidate angles from Harness² recursion",
    )
    verified_facts_used: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON-encoded verified facts cited",
    )
    char_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
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
    application: Mapped["Application"] = relationship(
        "Application",
        back_populates="form_answers",
    )


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


class ApplicationFormAnswerBase(BaseModel):
    account_id: str
    application_id: str
    question_id: str
    question_prompt: str
    field_type: str = "paragraph"
    tailored_answer: str
    candidate_angles: Optional[str] = None
    verified_facts_used: Optional[str] = None
    char_count: int = 0


class ApplicationFormAnswerCreate(ApplicationFormAnswerBase):
    pass


class ApplicationFormAnswerRead(ApplicationFormAnswerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationRead(ApplicationBase):
    id: str
    job_company: Optional[str] = None
    job_role: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    form_answers: List[ApplicationFormAnswerRead] = []

    model_config = ConfigDict(from_attributes=True)

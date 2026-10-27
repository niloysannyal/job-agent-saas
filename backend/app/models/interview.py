"""
Multi-tenant STAR Interview Coach models.
Stores STAR-format interview stories from USER_PROFILE.md §"Interview story bank"
as structured data that the Interview Coach UI can query, filter, and present.
"""
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


# ---------------------------------------------------------------------------
# SQLAlchemy ORM model
# ---------------------------------------------------------------------------

class StarStory(Base):
    """
    A single STAR-format interview story.
    Matches USER_PROFILE.md §"Interview story bank":
    - Situation/Task
    - Action
    - Result
    - Good-for tags (used by the Interview Coach to match stories to question types)
    """
    __tablename__ = "star_stories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    # --- STAR fields ---
    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
        doc="Short descriptive title for the story (e.g. 'Betopia Sales Agent — end-to-end ownership')",
    )
    situation: Mapped[str] = mapped_column(
        Text, nullable=False,
        doc="Situation/Task part of the STAR format.",
    )
    action: Mapped[str] = mapped_column(
        Text, nullable=False,
        doc="Action taken.",
    )
    result: Mapped[str] = mapped_column(
        Text, nullable=False,
        doc="Measurable result / outcome.",
    )
    # Comma-separated tags: "ownership, ambiguity, end-to-end execution, working solo"
    good_for_tags: Mapped[str] = mapped_column(
        Text, nullable=False, default="",
        doc="Comma-separated tags for matching stories to question categories.",
    )
    # Optional: link to a specific project/company for contextual matching
    company: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True,
        doc="Company where this story happened.",
    )
    role: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True,
        doc="Role held when this story happened.",
    )
    # Story verification status — only verified stories can be used in applications
    is_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
        doc="True if the user has confirmed this story's facts are accurate.",
    )
    # Display order
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
    )
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
    account: Mapped["Account"] = relationship(
        "Account", back_populates="star_stories",
    )


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class StarStoryBase(BaseModel):
    title: str
    situation: str
    action: str
    result: str
    good_for_tags: str = ""
    company: Optional[str] = None
    role: Optional[str] = None
    is_verified: bool = False
    sort_order: int = 0


class StarStoryCreate(StarStoryBase):
    pass


class StarStoryUpdate(BaseModel):
    title: Optional[str] = None
    situation: Optional[str] = None
    action: Optional[str] = None
    result: Optional[str] = None
    good_for_tags: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    is_verified: Optional[bool] = None
    sort_order: Optional[int] = None


class StarStoryRead(StarStoryBase):
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

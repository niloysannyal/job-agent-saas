import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class SubscriptionPlan(Base):
    """
    Subscription plan catalog model matching ARCHITECTURE.md §0 & §7.
    Deferred monetization puzzle piece: present with permissive/free defaults.
    """
    __tablename__ = "subscription_plans"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    # 'free' | 'pro' | 'unlimited'
    tier: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    price_cents: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="USD",
    )
    # 'month' | 'year' | 'lifetime'
    interval: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="month",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    # JSON bundle of plan limits/features
    features: Mapped[Optional[Dict[str, Any]]] = mapped_column(
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


class Entitlement(Base):
    """
    Account entitlement model matching ARCHITECTURE.md §7:
    All-access by default today; gates future quotas (e.g. applications, templates)
    when Paddle billing is activated in Phase 3.
    """
    __tablename__ = "entitlements"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    plan_tier: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="free",
    )
    # Per ARCHITECTURE.md §7: all-access by default for Phase 0/1
    all_access: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    max_active_applications: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
    )
    custom_templates_allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    max_cv_versions: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=20,
    )
    features: Mapped[Optional[Dict[str, Any]]] = mapped_column(
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
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="entitlement",
    )


# --- Pydantic Schemas ---

class SubscriptionPlanBase(BaseModel):
    name: str
    tier: str
    price_cents: int = 0
    currency: str = "USD"
    interval: str = "month"
    is_active: bool = True
    features: Optional[Dict[str, Any]] = None


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[str] = None
    price_cents: Optional[int] = None
    currency: Optional[str] = None
    interval: Optional[str] = None
    is_active: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None


class SubscriptionPlanRead(SubscriptionPlanBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EntitlementBase(BaseModel):
    account_id: str
    plan_tier: str = "free"
    all_access: bool = True
    max_active_applications: Optional[int] = None
    custom_templates_allowed: bool = True
    max_cv_versions: Optional[int] = 20
    features: Optional[Dict[str, Any]] = None


class EntitlementCreate(EntitlementBase):
    pass


class EntitlementUpdate(BaseModel):
    plan_tier: Optional[str] = None
    all_access: Optional[bool] = None
    max_active_applications: Optional[int] = None
    custom_templates_allowed: Optional[bool] = None
    max_cv_versions: Optional[int] = None
    features: Optional[Dict[str, Any]] = None


class EntitlementRead(EntitlementBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

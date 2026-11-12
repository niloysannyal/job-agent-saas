import uuid
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ModelPricing(Base):
    """
    Platform-wide model pricing catalog tracking input/output costs per 1M tokens
    in integer micro-USD (1 USD = 1,000,000 micro-USD).
    Exempt from multi-tenant account_id boundary in scripts/check_migrations.py:22.
    """
    __tablename__ = "model_pricing"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    input_price_per_1m: Mapped[int] = mapped_column(BigInteger, nullable=False)
    output_price_per_1m: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pricing_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "uq_active_model_pricing",
            "provider",
            "model",
            unique=True,
            postgresql_where=(is_active == True),
        ),
    )


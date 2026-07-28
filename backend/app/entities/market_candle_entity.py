from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.entities.instrument_entity import (
        InstrumentEntity,
    )

class MarketCandleEntity(Base):
    __tablename__ = "market_candles"

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey(
            "instruments.id",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    interval: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )

    open: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    high: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    low: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    close: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    volume: Mapped[Decimal | None] = mapped_column(
        Numeric(28, 8),
        nullable=True,
    )

    source_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    instrument: Mapped["InstrumentEntity"] = relationship(
        back_populates="market_candles",
    )
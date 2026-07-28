from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.entities.market_candle_entity import (
        MarketCandleEntity,
    )


class InstrumentEntity(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    display_symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    asset_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    base_asset: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    quote_asset: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    market_data_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider_symbol: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    supports_latest: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    supports_history: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    supports_sentiment: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
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
    
    market_candles: Mapped[
        list["MarketCandleEntity"]
    ] = relationship(
        back_populates="instrument",
    )
from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.entities.market_candle_entity import (
    MarketCandleEntity,
)


class MarketCandleRecord(TypedDict):
    instrument_id: int
    interval: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None
    source_provider: str

class MarketCandleRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
    
    def upsert_many(
        self,
        candles: list[MarketCandleRecord],
    ) -> int:
        if not candles:
            return 0

        unique_candles = self._deduplicate(
            candles
        )

        statement = insert(
            MarketCandleEntity
        ).values(
            unique_candles
        )

        statement = statement.on_conflict_do_update(
            index_elements=[
                MarketCandleEntity.instrument_id,
                MarketCandleEntity.interval,
                MarketCandleEntity.timestamp,
            ],
            set_={
                "open": statement.excluded.open,
                "high": statement.excluded.high,
                "low": statement.excluded.low,
                "close": statement.excluded.close,
                "volume": statement.excluded.volume,
                "source_provider": (
                    statement.excluded.source_provider
                ),
                "updated_at": func.now(),
            },
        )

        self.session.execute(
            statement
        )

        return len(unique_candles)
    
    @staticmethod
    def _deduplicate(
        candles: list[MarketCandleRecord],
    ) -> list[MarketCandleRecord]:
        unique_by_key: dict[
            tuple[int, str, datetime],
            MarketCandleRecord,
        ] = {}

        for candle in candles:
            key = (
                candle["instrument_id"],
                candle["interval"],
                candle["timestamp"],
            )

            unique_by_key[key] = candle

        return list(
            unique_by_key.values()
        )
    
    def list_by_range(
        self,
        instrument_id: int,
        interval: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[MarketCandleEntity]:
        statement = (
            select(MarketCandleEntity)
            .where(
                MarketCandleEntity.instrument_id
                == instrument_id,
                MarketCandleEntity.interval
                == interval,
                MarketCandleEntity.timestamp
                >= start_time,
                MarketCandleEntity.timestamp
                <= end_time,
            )
            .order_by(
                MarketCandleEntity.timestamp.asc()
            )
        )

        return list(
            self.session.scalars(
                statement
            ).all()
        )
    
    def get_latest_timestamp(
        self,
        instrument_id: int,
        interval: str,
    ) -> datetime | None:
        statement = select(
            func.max(
                MarketCandleEntity.timestamp
            )
        ).where(
            MarketCandleEntity.instrument_id
            == instrument_id,
            MarketCandleEntity.interval
            == interval,
        )

        return self.session.scalar(
            statement
        )
        
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.instrument_definition import (
    InstrumentDefinition,
)
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.repositories.market_candle_repository import (
    MarketCandleRecord,
    MarketCandleRepository,
)
from app.schemas.market import (
    HistoricalMarketDataResponse,
    MarketCandle,
)


class HistoricalMarketDataPersistenceService:
    def __init__(
        self,
        session: Session,
        instrument_repository: InstrumentRepository,
        candle_repository: MarketCandleRepository,
    ) -> None:
        self.session = session
        self.instrument_repository = (
            instrument_repository
        )
        self.candle_repository = candle_repository

    def persist(
        self,
        definition: InstrumentDefinition,
        response: HistoricalMarketDataResponse,
    ) -> int:
        instrument_code = (
            definition.instrument.code.value
        )

        entity = (
            self.instrument_repository.get_by_code(
                instrument_code
            )
        )

        if entity is None:
            raise ValueError(
                f"Unsupported instrument: "
                f"{instrument_code}"
            )

        records = [
            self._to_record(
                instrument_id=entity.id,
                source_provider=(
                    definition.market_data_provider
                ),
                candle=candle,
            )
            for candle in response.candles
        ]

        try:
            processed_count = (
                self.candle_repository.upsert_many(
                    records
                )
            )

            self.session.commit()

            return processed_count

        except Exception:
            self.session.rollback()
            raise

    @staticmethod
    def _to_record(
        *,
        instrument_id: int,
        source_provider: str,
        candle: MarketCandle,
    ) -> MarketCandleRecord:
        return {
            "instrument_id": instrument_id,
            "interval": candle.interval.value,
            "timestamp": candle.timestamp,
            "open": Decimal(str(candle.open)),
            "high": Decimal(str(candle.high)),
            "low": Decimal(str(candle.low)),
            "close": Decimal(str(candle.close)),
            "volume": (
                Decimal(str(candle.volume))
                if candle.volume is not None
                else None
            ),
            "source_provider": source_provider,
        }
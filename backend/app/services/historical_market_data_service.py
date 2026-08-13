from datetime import datetime

from app.models.instrument_definition import (
    InstrumentDefinition,
)
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.repositories.market_candle_repository import (
    MarketCandleRepository,
)
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
)
from app.mappers.market_candle_mapper import (
    map_market_candle_entity_to_schema,
)

from app.utils.market_interval_utils import (
    calculate_expected_timestamps,
)

class HistoricalMarketDataService:
    def __init__(
        self,
        instrument_repository: InstrumentRepository,
        candle_repository: MarketCandleRepository,
    ) -> None:
        self.instrument_repository = (
            instrument_repository
        )
        self.candle_repository = (
            candle_repository
        )

    def get_cached_response(
        self,
        definition: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse | None:
        instrument_code = (
            definition.instrument.code.value
        )

        instrument_entity = (
            self.instrument_repository.get_by_code(
                instrument_code
            )
        )

        if instrument_entity is None:
            raise ValueError(
                f"Unsupported instrument: "
                f"{instrument_code}"
            )

        candles = (
            self.candle_repository.list_by_range(
                instrument_id=instrument_entity.id,
                interval=request.interval.value,
                start_time=request.start_time,
                end_time=request.end_time,
            )
        )

        if not candles:
            return None

        expected_timestamps = (
            calculate_expected_timestamps(
                start_time=request.start_time,
                end_time=request.end_time,
                interval=request.interval,
            )
        )

        cached_timestamps = [
            candle.timestamp
            for candle in candles
        ]

        if not self._is_cache_complete(
            cached_timestamps=cached_timestamps,
            expected_timestamps=expected_timestamps,
        ):
            return None

        return HistoricalMarketDataResponse(
            symbol=definition.provider_symbol,
            interval=request.interval,
            currency=(
                definition.instrument.quote_asset
                or "USD"
            ),
            candles=[
                map_market_candle_entity_to_schema(
                    entity=candle,
                    symbol=definition.provider_symbol,
                )
                for candle in candles
            ],
        )

    @staticmethod
    def _is_cache_complete(
        *,
        cached_timestamps: list[datetime],
        expected_timestamps: list[datetime],
    ) -> bool:
        return set(expected_timestamps).issubset(
            set(cached_timestamps)
        )
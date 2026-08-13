from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.entities.market_candle_entity import (
    MarketCandleEntity,
)
from app.instruments.definitions import GOLD_SPOT
from app.models.market_interval import MarketInterval
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.repositories.market_candle_repository import (
    MarketCandleRepository,
)
from app.schemas.market import (
    HistoricalMarketDataRequest,
)
from app.services.historical_market_data_service import (
    HistoricalMarketDataService,
)


def create_request(
) -> HistoricalMarketDataRequest:
    return HistoricalMarketDataRequest(
        interval=MarketInterval.FIVE_MINUTES,
        start_time=datetime(
            2026,
            7,
            22,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            7,
            22,
            11,
            0,
            tzinfo=timezone.utc,
        ),
    )


def create_instrument_entity(
) -> InstrumentEntity:
    return InstrumentEntity(
        id=1,
        code="XAUUSD",
        display_symbol="XAU/USD",
        name="Gold Spot / US Dollar",
        asset_type="commodity",
        base_asset="XAU",
        quote_asset="USD",
        market_data_provider="twelve_data",
        provider_symbol="XAU/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )


def create_candle_entity(
) -> MarketCandleEntity:
    return MarketCandleEntity(
        instrument_id=1,
        interval="5m",
        timestamp=datetime(
            2026,
            7,
            22,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        open=Decimal("4055.10"),
        high=Decimal("4058.40"),
        low=Decimal("4054.70"),
        close=Decimal("4056.80"),
        volume=None,
        source_provider="twelve_data",
    )


def test_get_cached_response_returns_cached_candles():
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        create_instrument_entity()
    )

    candle_repository.list_by_range.return_value = [
        create_candle_entity()
    ]

    service = HistoricalMarketDataService(
        instrument_repository=instrument_repository,
        candle_repository=candle_repository,
    )

    request = create_request()

    result = service.get_cached_response(
        definition=GOLD_SPOT,
        request=request,
    )

    assert result is not None
    assert result.symbol == "XAU/USD"
    assert result.interval == (
        MarketInterval.FIVE_MINUTES
    )
    assert result.currency == "USD"
    assert len(result.candles) == 1

    candle = result.candles[0]

    assert candle.symbol == "XAU/USD"
    assert candle.interval == (
        MarketInterval.FIVE_MINUTES
    )
    assert candle.open == 4055.10
    assert candle.high == 4058.40
    assert candle.low == 4054.70
    assert candle.close == 4056.80
    assert candle.volume is None

    instrument_repository.get_by_code.assert_called_once_with(
        "XAUUSD"
    )

    candle_repository.list_by_range.assert_called_once_with(
        instrument_id=1,
        interval="5m",
        start_time=request.start_time,
        end_time=request.end_time,
    )


def test_get_cached_response_returns_none_when_no_candles():
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        create_instrument_entity()
    )

    candle_repository.list_by_range.return_value = []

    service = HistoricalMarketDataService(
        instrument_repository=instrument_repository,
        candle_repository=candle_repository,
    )

    result = service.get_cached_response(
        definition=GOLD_SPOT,
        request=create_request(),
    )

    assert result is None


def test_get_cached_response_rejects_unknown_instrument():
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        None
    )

    service = HistoricalMarketDataService(
        instrument_repository=instrument_repository,
        candle_repository=candle_repository,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported instrument: XAUUSD",
    ):
        service.get_cached_response(
            definition=GOLD_SPOT,
            request=create_request(),
        )

    candle_repository.list_by_range.assert_not_called()
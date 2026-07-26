from datetime import datetime, timezone
from unittest.mock import Mock#

from app.providers.mock_market_provider import MockMarketDataProvider
from app.services.market_data import MarketDataService
from app.models.market_interval import MarketInterval
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
)
from app.services.market_data import MarketDataService
from app.instruments.definitions import GOLD_FUTURES
from app.instruments.definitions import GOLD_FUTURES
from app.schemas.market import MarketPriceResponse



def test_market_service_returns_gold_price():
    provider = MockMarketDataProvider()
    service = MarketDataService(
    provider=provider,
    instrument=GOLD_FUTURES,
    )

    result = service.get_gold_price()

    assert result.currency == "USD"
    assert result.price > 0

def test_market_service_delegates_historical_request():
    provider = Mock()

    request = HistoricalMarketDataRequest(
        interval=MarketInterval.FIVE_MINUTES,
        start_time=datetime(
            2026,
            7,
            14,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            7,
            14,
            11,
            0,
            tzinfo=timezone.utc,
        ),
    )

    expected_response = HistoricalMarketDataResponse(
        symbol=GOLD_FUTURES.provider_symbol,
        interval=MarketInterval.FIVE_MINUTES,
        currency="USD",
        candles=[],
    )

    provider.get_historical_data.return_value = (
        expected_response
    )

    service = MarketDataService(
        provider=provider,
        instrument=GOLD_FUTURES,
    )

    result = service.get_historical_data(request)

    assert result == expected_response

    provider.get_historical_data.assert_called_once_with(
        GOLD_FUTURES,
        request,
    )

def test_market_service_delegates_latest_price():
    provider = Mock()

    expected_response = MarketPriceResponse(
        symbol="GC=F",
        price=4097.20,
        currency="USD",
        timestamp="2026-07-14T15:20:00Z",
    )

    provider.get_latest_price.return_value = (
        expected_response
    )

    service = MarketDataService(
        provider=provider,
        instrument=GOLD_FUTURES,
    )

    result = service.get_latest_price()

    assert result == expected_response

    provider.get_latest_price.assert_called_once_with(
        GOLD_FUTURES
    )
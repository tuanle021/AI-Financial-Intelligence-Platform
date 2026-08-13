from datetime import datetime, timezone
from unittest.mock import Mock

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

from app.services.historical_market_data_persistence_service import (
    HistoricalMarketDataPersistenceService,
)
from app.services.historical_market_data_service import (
    HistoricalMarketDataService,
)


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
        timestamp="2026-07-14T15:20:00Z", # type: ignore
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

def test_market_service_persists_historical_response():
    provider = Mock()
    persistence_service = Mock(
        spec=HistoricalMarketDataPersistenceService
    )

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
        persistence_service=persistence_service,
    )

    result = service.get_historical_data(
        request
    )

    assert result == expected_response

    provider.get_historical_data.assert_called_once_with(
        GOLD_FUTURES,
        request,
    )

    persistence_service.persist.assert_called_once_with(
        definition=GOLD_FUTURES,
        response=expected_response,
    )

def test_market_service_returns_cached_historical_response():
    provider = Mock()
    persistence_service = Mock()
    historical_service = Mock(
        spec=HistoricalMarketDataService
    )

    request = HistoricalMarketDataRequest(
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

    cached_response = HistoricalMarketDataResponse(
        symbol=GOLD_FUTURES.provider_symbol,
        interval=MarketInterval.FIVE_MINUTES,
        currency="USD",
        candles=[],
    )

    historical_service.get_cached_response.return_value = (
        cached_response
    )

    service = MarketDataService(
        provider=provider,
        instrument=GOLD_FUTURES,
        persistence_service=persistence_service,
        historical_service=historical_service,
    )

    result = service.get_historical_data(
        request
    )

    assert result == cached_response

    historical_service.get_cached_response.assert_called_once_with(
        definition=GOLD_FUTURES,
        request=request,
    )

    provider.get_historical_data.assert_not_called()
    persistence_service.persist.assert_not_called()

def test_market_service_fetches_and_persists_when_cache_empty():
    provider = Mock()
    persistence_service = Mock()
    historical_service = Mock(
        spec=HistoricalMarketDataService
    )

    request = HistoricalMarketDataRequest(
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

    provider_response = HistoricalMarketDataResponse(
        symbol=GOLD_FUTURES.provider_symbol,
        interval=MarketInterval.FIVE_MINUTES,
        currency="USD",
        candles=[],
    )

    historical_service.get_cached_response.return_value = (
        None
    )

    provider.get_historical_data.return_value = (
        provider_response
    )

    service = MarketDataService(
        provider=provider,
        instrument=GOLD_FUTURES,
        persistence_service=persistence_service,
        historical_service=historical_service,
    )

    result = service.get_historical_data(
        request
    )

    assert result == provider_response

    historical_service.get_cached_response.assert_called_once_with(
        definition=GOLD_FUTURES,
        request=request,
    )

    provider.get_historical_data.assert_called_once_with(
        GOLD_FUTURES,
        request,
    )

    persistence_service.persist.assert_called_once_with(
        definition=GOLD_FUTURES,
        response=provider_response,
    )
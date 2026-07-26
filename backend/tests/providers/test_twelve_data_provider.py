from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.models.market_interval import MarketInterval
from app.providers.twelve_data_provider import (
    TwelveDataMarketDataProvider,
)
from app.schemas.market import HistoricalMarketDataRequest
from app.instruments.definitions import (
    GOLD_SPOT,
)

def test_twelve_data_provider_returns_normalised_spot_price():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "price": "4056.79513",
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ) as mock_get:
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        result = provider.get_gold_price()

    assert result.symbol == "XAU/USD"
    assert result.price == 4056.80
    assert result.currency == "USD"
    assert result.timestamp.tzinfo == timezone.utc

    mock_get.assert_called_once_with(
        "https://test.twelvedata.com/price",
        params={
            "symbol": "XAU/USD",
            "apikey": "test-api-key",
        },
        timeout=10.0,
    )

def test_twelve_data_provider_requires_api_key():
    with pytest.raises(
        ValueError,
        match="Twelve Data API key is not configured",
    ):
        TwelveDataMarketDataProvider(
            api_key="",
            base_url="https://test.twelvedata.com",
        )

def test_twelve_data_provider_raises_error_for_provider_error_response():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "error",
        "code": 401,
        "message": "Invalid API key",
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="invalid-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(
            ValueError,
            match="Invalid API key",
        ):
            provider.get_gold_price()

def test_twelve_data_provider_raises_error_when_price_is_missing():
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(
            ValueError,
            match="Twelve Data response did not contain a price",
        ):
            provider.get_gold_price()
            
def test_twelve_data_provider_propagates_http_error():
    mock_request = httpx.Request(
        "GET",
        "https://test.twelvedata.com/price",
    )

    mock_response = httpx.Response(
        status_code=500,
        request=mock_request,
    )

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(httpx.HTTPStatusError):
            provider.get_gold_price()

def create_spot_historical_request(
    *,
    interval: MarketInterval = MarketInterval.FIVE_MINUTES,
) -> HistoricalMarketDataRequest:
    return HistoricalMarketDataRequest(
        interval=interval,
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

def test_twelve_data_provider_returns_historical_spot_candles():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "meta": {
            "symbol": "XAU/USD",
            "interval": "5min",
            "currency_base": "Gold Spot",
            "currency_quote": "US Dollar",
        },
        "values": [
            {
                "datetime": "2026-07-14 10:05:00",
                "open": "4056.10",
                "high": "4058.20",
                "low": "4055.80",
                "close": "4057.90",
            },
            {
                "datetime": "2026-07-14 10:00:00",
                "open": "4055.20",
                "high": "4057.00",
                "low": "4054.90",
                "close": "4056.10",
            },
        ],
        "status": "ok",
    }

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ) as mock_get:
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        request = create_spot_historical_request()
        result = provider.get_historical_data(
            GOLD_SPOT,
            request,
        )

    assert result.symbol == GOLD_SPOT.provider_symbol
    assert result.interval == MarketInterval.FIVE_MINUTES
    assert result.currency == "USD"
    assert len(result.candles) == 2

    first_candle = result.candles[0]

    assert first_candle.timestamp == datetime(
        2026,
        7,
        14,
        10,
        0,
        tzinfo=timezone.utc,
    )
    assert first_candle.open == 4055.20
    assert first_candle.close == 4056.10
    assert first_candle.volume is None

    mock_get.assert_called_once_with(
        "https://test.twelvedata.com/time_series",
        params={
            "symbol": "XAU/USD",
            "interval": "5min",
            "start_date": request.start_time.isoformat(),
            "end_date": request.end_time.isoformat(),
            "timezone": "UTC",
            "order": "ASC",
            "apikey": "test-api-key",
        },
        timeout=10.0,
    )

def test_twelve_data_historical_provider_raises_provider_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "status": "error",
        "code": 400,
        "message": "Invalid interval",
    }

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        request = create_spot_historical_request()

        with pytest.raises(
            ValueError,
            match="Invalid interval",
        ):
            provider.get_historical_data(
                GOLD_SPOT,
                request,
            )

def test_twelve_data_historical_provider_rejects_empty_values():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "meta": {},
        "values": [],
        "status": "ok",
    }

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        request = create_spot_historical_request()

        with pytest.raises(
            ValueError,
            match="returned no historical spot data",
        ):
            provider.get_historical_data(
                GOLD_SPOT,
                request,
            )
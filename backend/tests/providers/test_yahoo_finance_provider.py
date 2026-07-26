from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.models.market_interval import MarketInterval
from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)
from app.schemas.market import (
    HistoricalMarketDataRequest,
)
from app.instruments.definitions import GOLD_FUTURES


def test_yahoo_provider_returns_normalised_gold_price():
    mock_history = pd.DataFrame(
        {
            "Close": [4097.2001953125],
        },
        index=[
            pd.Timestamp(
                datetime(2026, 7, 14, 15, 20, tzinfo=timezone.utc)
            )
        ],
    )

    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()
        result = provider.get_gold_price()

    assert result.symbol == "GC=F"
    assert result.price == 4097.20
    assert result.currency == "USD"
    assert result.timestamp.tzinfo is not None

    mock_ticker.history.assert_called_once_with(
        period="1d",
        interval="5m",
    )

def test_yahoo_provider_raises_error_when_no_data_returned():
    empty_history = pd.DataFrame()

    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = empty_history
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()

        with pytest.raises(
            ValueError,
            match="Yahoo Finance returned no gold price data",
        ):
            provider.get_gold_price()

def create_historical_request(
    *,
    interval: MarketInterval = (
        MarketInterval.FIVE_MINUTES
    ),
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> HistoricalMarketDataRequest:
    return HistoricalMarketDataRequest(
        interval=interval,
        start_time=start_time
        or datetime(
            2026,
            7,
            14,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=end_time
        or datetime(
            2026,
            7,
            14,
            11,
            0,
            tzinfo=timezone.utc,
        ),
    )

def test_yahoo_provider_returns_historical_candles():
    index = pd.DatetimeIndex(
        [
            pd.Timestamp(
                "2026-07-14T10:00:00-04:00"
            ),
            pd.Timestamp(
                "2026-07-14T10:05:00-04:00"
            ),
        ]
    )

    mock_history = pd.DataFrame(
        {
            "Open": [4095.10, 4097.20],
            "High": [4098.40, 4100.10],
            "Low": [4094.70, 4096.80],
            "Close": [4097.20, 4099.60],
            "Volume": [1832, 1950],
        },
        index=index,
    )

    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()
        request = create_historical_request()

        result = provider.get_historical_data(
            GOLD_FUTURES,
            request,
        )

    assert result.interval == (
        MarketInterval.FIVE_MINUTES
    )
    assert len(result.candles) == 2

    first_candle = result.candles[0]

    assert first_candle.open == 4095.10
    assert first_candle.close == 4097.20
    assert first_candle.volume == 1832
    assert first_candle.timestamp.tzinfo is not None

    mock_ticker.history.assert_called_once_with(
        start=request.start_time,
        end=request.end_time,
        interval="5m",
        auto_adjust=False,
    )

def test_yahoo_provider_rejects_unsupported_interval():
    provider = YahooFinanceMarketDataProvider()

    request = create_historical_request(
        interval=MarketInterval.FOUR_HOURS
    )

    with pytest.raises(
        ValueError,
        match="does not support interval",
    ):
        provider.get_historical_data(
            GOLD_FUTURES,
            request,
        )

def test_yahoo_provider_rejects_empty_history():
    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = (
            pd.DataFrame()
        )
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()
        request = create_historical_request()

        with pytest.raises(
            ValueError,
            match="returned no historical gold data",
        ):
            provider.get_historical_data(
                GOLD_FUTURES,
                request,
            )


def test_yahoo_provider_rejects_long_intraday_range():
    provider = YahooFinanceMarketDataProvider()

    request = create_historical_request(
        start_time=datetime(
            2026,
            4,
            1,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            7,
            14,
            tzinfo=timezone.utc,
        ),
    )

    with pytest.raises(
        ValueError,
        match="cannot exceed 60 days",
    ):
        provider.get_historical_data(
            GOLD_FUTURES,
            request,
        )
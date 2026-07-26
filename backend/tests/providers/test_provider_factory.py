import pytest

from app.providers.factory import create_market_data_provider
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)


def test_factory_creates_mock_provider():
    provider = create_market_data_provider("mock")

    assert isinstance(provider, MockMarketDataProvider)


def test_factory_creates_yahoo_provider():
    provider = create_market_data_provider("yahoo")

    assert isinstance(provider, YahooFinanceMarketDataProvider)


def test_factory_is_case_insensitive():
    provider = create_market_data_provider(" YAHOO ")

    assert isinstance(provider, YahooFinanceMarketDataProvider)


def test_factory_rejects_unsupported_provider():
    with pytest.raises(
        ValueError,
        match="Unsupported market provider",
    ):
        create_market_data_provider("unknown")
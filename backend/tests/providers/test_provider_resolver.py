import pytest

from app.instruments.definitions import (
    EUR_USD,
    GBP_USD,
    GOLD_FUTURES,
    GOLD_SPOT,
)
from app.models.instrument import Instrument
from app.models.instrument_definition import InstrumentDefinition
from app.models.instrument_code import InstrumentCode
from app.models.asset_type import AssetType
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.resolver import resolve_market_data_provider
from app.providers.twelve_data_provider import (
    TwelveDataMarketDataProvider,
)
from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)


def test_resolver_returns_yahoo_provider_for_gold_futures():
    provider = resolve_market_data_provider(
        GOLD_FUTURES
    )

    assert isinstance(
        provider,
        YahooFinanceMarketDataProvider,
    )


def test_resolver_returns_twelve_data_provider_for_gold_spot():
    provider = resolve_market_data_provider(
        GOLD_SPOT
    )

    assert isinstance(
        provider,
        TwelveDataMarketDataProvider,
    )


def test_resolver_returns_mock_provider():
    mock_definition = InstrumentDefinition(
        instrument=Instrument(
            code=InstrumentCode.GOLD_SPOT,
            display_symbol="XAU/USD",
            name="Gold Spot / US Dollar",
            asset_type=AssetType.COMMODITY,
            base_asset="XAU",
            quote_asset="USD",
        ),
        market_data_provider="mock",
        provider_symbol="XAU/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
    )

    provider = resolve_market_data_provider(
        mock_definition
    )

    assert isinstance(
        provider,
        MockMarketDataProvider,
    )


def test_resolver_rejects_unsupported_provider():
    unsupported_definition = InstrumentDefinition(
        instrument=Instrument(
            code=InstrumentCode.GOLD_SPOT,
            display_symbol="XAU/USD",
            name="Gold Spot / US Dollar",
            asset_type=AssetType.COMMODITY,
            base_asset="XAU",
            quote_asset="USD",
        ),
        market_data_provider="unsupported",
        provider_symbol="XAU/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported market data provider",
    ):
        resolve_market_data_provider(
            unsupported_definition
        )

@pytest.mark.parametrize(
    "definition",
    [
        GBP_USD,
        EUR_USD,
    ],
)
def test_resolver_returns_twelve_data_provider_for_forex(
    definition: InstrumentDefinition,
):
    provider = resolve_market_data_provider(
        definition
    )

    assert isinstance(
        provider,
        TwelveDataMarketDataProvider,
    )
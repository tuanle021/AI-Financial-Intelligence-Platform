from app.models.asset_type import AssetType
from app.models.instrument import Instrument
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import InstrumentDefinition


GOLD_SPOT = InstrumentDefinition(
    instrument=Instrument(
        code=InstrumentCode.GOLD_SPOT,
        display_symbol="XAU/USD",
        name="Gold Spot / US Dollar",
        asset_type=AssetType.COMMODITY,
        base_asset="XAU",
        quote_asset="USD",
    ),
    market_data_provider="twelve_data",
    provider_symbol="XAU/USD",
    supports_latest=True,
    supports_history=True,
    supports_sentiment=True,
)


GOLD_FUTURES = InstrumentDefinition(
    instrument=Instrument(
        code=InstrumentCode.GOLD_FUTURES,
        display_symbol="GC",
        name="COMEX Gold Futures",
        asset_type=AssetType.FUTURES,
        base_asset="GOLD",
        quote_asset="USD",
    ),
    market_data_provider="yahoo",
    provider_symbol="GC=F",
    supports_latest=True,
    supports_history=True,
    supports_sentiment=True,
)

GBP_USD = InstrumentDefinition(
    instrument=Instrument(
        code=InstrumentCode.GBP_USD,
        display_symbol="GBP/USD",
        name="British Pound / US Dollar",
        asset_type=AssetType.FOREX,
        base_asset="GBP",
        quote_asset="USD",
    ),
    market_data_provider="twelve_data",
    provider_symbol="GBP/USD",
    supports_latest=True,
    supports_history=True,
    supports_sentiment=False,
)


EUR_USD = InstrumentDefinition(
    instrument=Instrument(
        code=InstrumentCode.EUR_USD,
        display_symbol="EUR/USD",
        name="Euro / US Dollar",
        asset_type=AssetType.FOREX,
        base_asset="EUR",
        quote_asset="USD",
    ),
    market_data_provider="twelve_data",
    provider_symbol="EUR/USD",
    supports_latest=True,
    supports_history=True,
    supports_sentiment=False,
)
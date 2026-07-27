from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.mappers.instrument_mapper import (
    map_instrument_entity_to_definition,
)
from app.models.asset_type import AssetType
from app.models.instrument_code import InstrumentCode

import pytest


def test_maps_entity_to_instrument_definition():
    entity = InstrumentEntity(
        code="GBPUSD",
        display_symbol="GBP/USD",
        name="British Pound / US Dollar",
        asset_type="forex",
        base_asset="GBP",
        quote_asset="USD",
        market_data_provider="twelve_data",
        provider_symbol="GBP/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )

    definition = (
        map_instrument_entity_to_definition(
            entity
        )
    )

    assert definition.instrument.code == (
        InstrumentCode.GBP_USD
    )
    assert definition.instrument.asset_type == (
        AssetType.FOREX
    )
    assert definition.instrument.display_symbol == (
        "GBP/USD"
    )
    assert definition.market_data_provider == (
        "twelve_data"
    )
    assert definition.provider_symbol == "GBP/USD"
    assert definition.supports_latest is True
    assert definition.supports_history is True
    assert definition.supports_sentiment is False

def test_mapper_rejects_unknown_instrument_code():
    entity = InstrumentEntity(
        code="UNKNOWN",
        display_symbol="UNKNOWN",
        name="Unsupported Instrument",
        asset_type="forex",
        base_asset=None,
        quote_asset=None,
        market_data_provider="twelve_data",
        provider_symbol="UNKNOWN",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )

    with pytest.raises(ValueError):
        map_instrument_entity_to_definition(
            entity
        )

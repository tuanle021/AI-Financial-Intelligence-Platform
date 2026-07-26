import pytest

from app.instruments.registry import (
    get_instrument_definition,
    list_instrument_definitions,
    resolve_instrument_code,
    resolve_instrument_definition,
)
from app.models.asset_type import AssetType
from app.models.instrument_code import InstrumentCode


def test_resolve_gold_spot_definition():
    definition = resolve_instrument_definition(
        "XAUUSD"
    )

    assert definition.instrument.code == (
        InstrumentCode.GOLD_SPOT
    )
    assert definition.provider_symbol == "XAU/USD"
    assert definition.market_data_provider == (
        "twelve_data"
    )


def test_resolve_instrument_is_case_insensitive():
    instrument_code = resolve_instrument_code(
        "  xauusd  "
    )

    assert instrument_code == (
        InstrumentCode.GOLD_SPOT
    )


def test_resolve_gold_futures_definition():
    definition = get_instrument_definition(
        InstrumentCode.GOLD_FUTURES
    )

    assert definition.provider_symbol == "GC=F"
    assert definition.instrument.asset_type == (
        AssetType.FUTURES
    )


def test_resolve_unsupported_instrument():
    with pytest.raises(
        ValueError,
        match="Unsupported instrument",
    ):
        resolve_instrument_definition(
            "INVALID"
        )


def test_list_instruments_returns_all_registered_definitions():
    definitions = list_instrument_definitions()

    assert len(definitions) == 4

    instrument_codes = {
        definition.instrument.code
        for definition in definitions
    }

    assert instrument_codes == {
        InstrumentCode.GOLD_SPOT,
        InstrumentCode.GOLD_FUTURES,
        InstrumentCode.GBP_USD,
        InstrumentCode.EUR_USD,
    }

def test_resolve_gbp_usd_definition():
    definition = resolve_instrument_definition(
        "GBPUSD"
    )

    assert definition.instrument.code == (
        InstrumentCode.GBP_USD
    )
    assert definition.instrument.asset_type == (
        AssetType.FOREX
    )
    assert definition.provider_symbol == "GBP/USD"
    assert definition.market_data_provider == (
        "twelve_data"
    )


def test_resolve_eur_usd_definition():
    definition = resolve_instrument_definition(
        "eurusd"
    )

    assert definition.instrument.code == (
        InstrumentCode.EUR_USD
    )
    assert definition.instrument.asset_type == (
        AssetType.FOREX
    )
    assert definition.provider_symbol == "EUR/USD"
    assert definition.market_data_provider == (
        "twelve_data"
    )
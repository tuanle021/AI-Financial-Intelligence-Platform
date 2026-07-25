import pytest
from app.models.asset_type import AssetType
from app.models.instrument_code import InstrumentCode
from app.services.instrument_service import (
    InstrumentService,
)
from app.instruments.definitions import EUR_USD, GBP_USD, GOLD_FUTURES, GOLD_SPOT
from app.instruments.registry import list_instrument_definitions, INSTRUMENT_REGISTRY

service = InstrumentService()


def test_service_resolves_definition():
    service = InstrumentService()

    result = service.resolve_definition("XAUUSD")

    assert result == GOLD_SPOT


def test_service_lists_instruments():
    service = InstrumentService()

    assert service.list_instruments() == [
        GOLD_SPOT,
        GOLD_FUTURES,
        EUR_USD,
        GBP_USD,
    ]

def test_list_instruments_returns_registered_definitions():
    definitions = list_instrument_definitions()

    codes = {
        definition.instrument.code
        for definition in definitions
    }

    assert InstrumentCode.GOLD_SPOT in codes
    assert InstrumentCode.GOLD_FUTURES in codes
    assert InstrumentCode.GBP_USD in codes
    assert InstrumentCode.EUR_USD in codes

def test_service_returns_public_instrument_response():
    service = InstrumentService()

    response = service.resolve_instrument_response(
        "XAUUSD"
    )

    assert response.code == InstrumentCode.GOLD_SPOT
    assert response.display_symbol == "XAU/USD"
    assert response.asset_type == AssetType.COMMODITY
    assert response.supports_latest is True
    assert response.supports_history is True

def test_service_lists_public_instrument_responses():
    service = InstrumentService()

    responses = service.list_instrument_responses()

    returned_codes = {
        response.code
        for response in responses
    }

    assert InstrumentCode.GOLD_SPOT in returned_codes
    assert InstrumentCode.GOLD_FUTURES in returned_codes
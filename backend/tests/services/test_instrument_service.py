from unittest.mock import MagicMock

import pytest

from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.instruments.registry import (
    list_instrument_definitions,
)
from app.models.instrument_code import InstrumentCode
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.services.instrument_service import (
    InstrumentService,
)


def create_gold_spot_entity(
) -> InstrumentEntity:
    return InstrumentEntity(
        code="XAUUSD",
        display_symbol="XAU/USD",
        name="Gold Spot / US Dollar",
        asset_type="commodity",
        base_asset="XAU",
        quote_asset="USD",
        market_data_provider="twelve_data",
        provider_symbol="XAU/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )

def create_gold_futures_entity() -> InstrumentEntity:
    return InstrumentEntity(
        code="GOLD_FUTURES",
        display_symbol="GC=F",
        name="Gold Futures",
        asset_type="futures",
        base_asset="GOLD",
        quote_asset="USD",
        market_data_provider="yahoo",
        provider_symbol="GC=F",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )

def create_gbp_usd_entity() -> InstrumentEntity:
    return InstrumentEntity(
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

def create_eur_usd_entity() -> InstrumentEntity:
    return InstrumentEntity(
        code="EURUSD",
        display_symbol="EUR/USD",
        name="Euro / US Dollar",
        asset_type="forex",
        base_asset="EUR",
        quote_asset="USD",
        market_data_provider="twelve_data",
        provider_symbol="EUR/USD",
        supports_latest=True,
        supports_history=True,
        supports_sentiment=False,
        is_active=True,
    )


def test_service_resolves_definition():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.get_by_code.return_value = (
        create_gold_spot_entity()
    )

    service = InstrumentService(
        repository=repository
    )

    result = service.resolve_definition(
        "XAUUSD"
    )

    assert result.instrument.code == (
        InstrumentCode.GOLD_SPOT
    )
    assert result.provider_symbol == "XAU/USD"
    assert result.market_data_provider == (
        "twelve_data"
    )
    assert result.supports_latest is True
    assert result.supports_history is True
    assert result.supports_sentiment is False


def test_service_lists_instruments():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.list_active.return_value = [
        create_eur_usd_entity(),
        create_gbp_usd_entity(),
        create_gold_futures_entity(),
        create_gold_spot_entity(),
    ]

    service = InstrumentService(
        repository=repository
    )

    results = service.list_instruments()

    returned_codes = {
        result.instrument.code
        for result in results
    }

    assert returned_codes == {
        InstrumentCode.GOLD_SPOT,
        InstrumentCode.GOLD_FUTURES,
        InstrumentCode.EUR_USD,
        InstrumentCode.GBP_USD,
    }

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
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.get_by_code.return_value = (
        create_gold_spot_entity()
    )

    service = InstrumentService(
        repository=repository
    )

    response = service.resolve_instrument_response(
        "XAUUSD"
    )

    assert response.code == (
        InstrumentCode.GOLD_SPOT
    )
    assert response.display_symbol == "XAU/USD"

def test_service_lists_public_instrument_responses():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.list_active.return_value = [
        create_gold_spot_entity(),
        create_gold_futures_entity(),
        create_eur_usd_entity(),
        create_gbp_usd_entity(),
    ]

    service = InstrumentService(
        repository=repository
    )

    responses = (
        service.list_instrument_responses()
    )

    returned_codes = {
        response.code
        for response in responses
    }

    assert returned_codes == {
        InstrumentCode.GOLD_SPOT,
        InstrumentCode.GOLD_FUTURES,
        InstrumentCode.EUR_USD,
        InstrumentCode.GBP_USD,
    }


def test_service_resolves_definition_from_repository():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.get_by_code.return_value = (
        create_gold_spot_entity()
    )

    service = InstrumentService(
        repository=repository
    )

    definition = service.resolve_definition(
        "XAUUSD"
    )

    assert definition.instrument.code == (
        InstrumentCode.GOLD_SPOT
    )

    repository.get_by_code.assert_called_once_with(
        "XAUUSD"
    )

def test_service_rejects_unknown_instrument():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.get_by_code.return_value = None

    service = InstrumentService(
        repository=repository
    )

    with pytest.raises(
        ValueError,
        match="Unsupported instrument: UNKNOWN",
    ):
        service.resolve_definition(
            "UNKNOWN"
        )


def test_service_lists_active_definitions():
    repository = MagicMock(
        spec=InstrumentRepository
    )
    repository.list_active.return_value = [
        create_gold_spot_entity()
    ]

    service = InstrumentService(
        repository=repository
    )

    definitions = service.list_instruments()

    assert len(definitions) == 1
    assert definitions[0].instrument.code == (
        InstrumentCode.GOLD_SPOT
    )

    repository.list_active.assert_called_once_with()

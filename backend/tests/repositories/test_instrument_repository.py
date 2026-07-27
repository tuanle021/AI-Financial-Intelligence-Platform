from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.repositories.instrument_repository import (
    InstrumentRepository,
)

def test_get_by_code_returns_instrument():
    mock_session = MagicMock(
        spec=Session
    )

    expected_instrument = InstrumentEntity(
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

    mock_session.scalar.return_value = (
        expected_instrument
    )

    repository = InstrumentRepository(
        session=mock_session
    )

    result = repository.get_by_code(
        "  xauusd  "
    )

    assert result is expected_instrument
    mock_session.scalar.assert_called_once()
    
def test_get_by_code_returns_none_when_missing():
    mock_session = MagicMock(
        spec=Session
    )
    mock_session.scalar.return_value = None

    repository = InstrumentRepository(
        session=mock_session
    )

    result = repository.get_by_code(
        "UNKNOWN"
    )

    assert result is None
    
def test_list_active_returns_active_instruments():
    mock_session = MagicMock(
        spec=Session
    )

    gold_spot = InstrumentEntity(
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

    gbp_usd = InstrumentEntity(
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

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [
        gbp_usd,
        gold_spot,
    ]

    mock_session.scalars.return_value = (
        mock_scalars
    )

    repository = InstrumentRepository(
        session=mock_session
    )

    result = repository.list_active()

    assert result == [
        gbp_usd,
        gold_spot,
    ]
    mock_session.scalars.assert_called_once()

def test_exists_by_code_returns_true():
    mock_session = MagicMock(
        spec=Session
    )

    mock_session.scalar.return_value = (
        InstrumentEntity(
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
    )

    repository = InstrumentRepository(
        session=mock_session
    )

    assert repository.exists_by_code(
        "eurusd"
    ) is True

def test_exists_by_code_returns_false():
    mock_session = MagicMock(
        spec=Session
    )
    mock_session.scalar.return_value = None

    repository = InstrumentRepository(
        session=mock_session
    )

    assert repository.exists_by_code(
        "INVALID"
    ) is False
    
def test_get_active_by_code_returns_instrument():
    mock_session = MagicMock(
        spec=Session
    )

    expected_instrument = InstrumentEntity(
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

    mock_session.scalar.return_value = (
        expected_instrument
    )

    repository = InstrumentRepository(
        session=mock_session
    )

    result = repository.get_active_by_code(
        " xauusd "
    )

    assert result is expected_instrument
    mock_session.scalar.assert_called_once()

def test_get_active_by_code_returns_none():
    mock_session = MagicMock(
        spec=Session
    )
    mock_session.scalar.return_value = None

    repository = InstrumentRepository(
        session=mock_session
    )

    result = repository.get_active_by_code(
        "EURUSD"
    )

    assert result is None
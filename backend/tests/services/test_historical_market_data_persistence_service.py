from datetime import datetime, timezone
from unittest.mock import MagicMock
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.instruments.definitions import GOLD_SPOT
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.repositories.market_candle_repository import (
    MarketCandleRepository,
)
from app.schemas.market import (
    HistoricalMarketDataResponse,
    MarketCandle,
)
from app.models.market_interval import MarketInterval
from app.services.historical_market_data_persistence_service import (
    HistoricalMarketDataPersistenceService,
)

def create_historical_response(
) -> HistoricalMarketDataResponse:
    return HistoricalMarketDataResponse(
        symbol="XAU/USD",
        interval=MarketInterval.FIVE_MINUTES,
        currency="USD",
        candles=[
            MarketCandle(
                symbol="XAU/USD",
                interval=(
                    MarketInterval.FIVE_MINUTES
                ),
                timestamp=datetime(
                    2026,
                    7,
                    28,
                    10,
                    0,
                    tzinfo=timezone.utc,
                ),
                open=4055.10,
                high=4058.40,
                low=4054.70,
                close=4056.80,
                volume=None,
            )
        ],
    )

def test_persist_upserts_candles_and_commits():
    session = MagicMock(
        spec=Session
    )
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        InstrumentEntity(
            id=1,
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
    )

    candle_repository.upsert_many.return_value = 1

    service = (
        HistoricalMarketDataPersistenceService(
            session=session,
            instrument_repository=(
                instrument_repository
            ),
            candle_repository=candle_repository,
        )
    )

    result = service.persist(
        definition=GOLD_SPOT,
        response=create_historical_response(),
    )

    assert result == 1
    candle_repository.upsert_many.assert_called_once()
    session.commit.assert_called_once()
    session.rollback.assert_not_called()

    records = (
        candle_repository
        .upsert_many
        .call_args
        .args[0]
    )

    assert len(records) == 1
    assert records[0]["instrument_id"] == 1
    assert records[0]["interval"] == "5m"
    assert records[0]["close"] == (
        Decimal("4056.80")
    )
    assert records[0]["volume"] is None
    assert records[0]["source_provider"] == (
        "twelve_data"
    )

def test_persist_rejects_missing_instrument():
    session = MagicMock(
        spec=Session
    )
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        None
    )

    service = (
        HistoricalMarketDataPersistenceService(
            session=session,
            instrument_repository=(
                instrument_repository
            ),
            candle_repository=candle_repository,
        )
    )

    with pytest.raises(
        ValueError,
        match="Unsupported instrument: XAUUSD",
    ):
        service.persist(
            definition=GOLD_SPOT,
            response=create_historical_response(),
        )

    candle_repository.upsert_many.assert_not_called()
    session.commit.assert_not_called()

def test_persist_rolls_back_when_upsert_fails():
    session = MagicMock(
        spec=Session
    )
    instrument_repository = MagicMock(
        spec=InstrumentRepository
    )
    candle_repository = MagicMock(
        spec=MarketCandleRepository
    )

    instrument_repository.get_by_code.return_value = (
        InstrumentEntity(
            id=1,
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
    )

    candle_repository.upsert_many.side_effect = (
        RuntimeError("database failure")
    )

    service = (
        HistoricalMarketDataPersistenceService(
            session=session,
            instrument_repository=(
                instrument_repository
            ),
            candle_repository=candle_repository,
        )
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        service.persist(
            definition=GOLD_SPOT,
            response=create_historical_response(),
        )

    session.rollback.assert_called_once()
    session.commit.assert_not_called()
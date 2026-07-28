from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.entities.market_candle_entity import (
    MarketCandleEntity,
)
from app.repositories.market_candle_repository import (
    MarketCandleRepository,
    MarketCandleRecord,
)

def create_candle_record(
    *,
    timestamp: datetime | None = None,
    close: Decimal = Decimal("4056.80"),
) -> MarketCandleRecord:
    candle_time = timestamp or datetime(
        2026,
        7,
        28,
        10,
        0,
        tzinfo=timezone.utc,
    )

    return {
        "instrument_id": 1,
        "interval": "5m",
        "timestamp": candle_time,
        "open": Decimal("4055.10"),
        "high": Decimal("4058.40"),
        "low": Decimal("4054.70"),
        "close": close,
        "volume": Decimal("1832"),
        "source_provider": "twelve_data",
    }

def test_upsert_many_returns_zero_for_empty_list():
    session = MagicMock(
        spec=Session
    )

    repository = MarketCandleRepository(
        session=session
    )

    result = repository.upsert_many([])

    assert result == 0
    session.execute.assert_not_called()

def test_upsert_many_executes_statement():
    session = MagicMock(
        spec=Session
    )

    repository = MarketCandleRepository(
        session=session
    )

    result = repository.upsert_many(
        [create_candle_record()]
    )

    assert result == 1
    session.execute.assert_called_once()

def test_deduplicate_keeps_latest_input():
    first = create_candle_record(
        close=Decimal("4056.80")
    )
    replacement = create_candle_record(
        close=Decimal("4057.20")
    )

    result = MarketCandleRepository._deduplicate(
        [
            first,
            replacement,
        ]
    )

    assert len(result) == 1
    assert result[0]["close"] == (
        Decimal("4057.20")
    )

def test_list_by_range_returns_candles():
    session = MagicMock(
        spec=Session
    )

    expected_candles = [
        MarketCandleEntity(
            instrument_id=1,
            interval="5m",
            timestamp=datetime(
                2026,
                7,
                28,
                10,
                0,
                tzinfo=timezone.utc,
            ),
            open=Decimal("4055.10"),
            high=Decimal("4058.40"),
            low=Decimal("4054.70"),
            close=Decimal("4056.80"),
            volume=Decimal("1832"),
            source_provider="twelve_data",
        )
    ]

    scalar_result = MagicMock()
    scalar_result.all.return_value = (
        expected_candles
    )
    session.scalars.return_value = (
        scalar_result
    )

    repository = MarketCandleRepository(
        session=session
    )

    result = repository.list_by_range(
        instrument_id=1,
        interval="5m",
        start_time=datetime(
            2026,
            7,
            28,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            7,
            28,
            11,
            0,
            tzinfo=timezone.utc,
        ),
    )

    assert result == expected_candles
    session.scalars.assert_called_once()

def test_get_latest_timestamp_returns_value():
    session = MagicMock(
        spec=Session
    )

    expected_timestamp = datetime(
        2026,
        7,
        28,
        10,
        55,
        tzinfo=timezone.utc,
    )

    session.scalar.return_value = (
        expected_timestamp
    )

    repository = MarketCandleRepository(
        session=session
    )

    result = repository.get_latest_timestamp(
        instrument_id=1,
        interval="5m",
    )

    assert result == expected_timestamp
    session.scalar.assert_called_once()

def test_get_latest_timestamp_returns_none_when_empty():
    session = MagicMock(
        spec=Session
    )
    session.scalar.return_value = None

    repository = MarketCandleRepository(
        session=session
    )

    result = repository.get_latest_timestamp(
        instrument_id=1,
        interval="5m",
    )

    assert result is None

def test_upsert_many_returns_unique_candle_count():
    session = MagicMock(
        spec=Session
    )

    repository = MarketCandleRepository(
        session=session
    )

    first = create_candle_record(
        close=Decimal("4056.80")
    )
    replacement = create_candle_record(
        close=Decimal("4057.20")
    )

    result = repository.upsert_many(
        [
            first,
            replacement,
        ]
    )

    assert result == 1
    session.execute.assert_called_once()
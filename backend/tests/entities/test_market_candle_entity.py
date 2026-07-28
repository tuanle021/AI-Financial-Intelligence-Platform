from app.entities.market_candle_entity import (
    MarketCandleEntity,
)


def test_market_candle_maps_to_expected_table():
    assert MarketCandleEntity.__tablename__ == (
        "market_candles"
    )


def test_market_candle_has_expected_columns():
    column_names = {
        column.name
        for column in MarketCandleEntity.__table__.columns
    }

    assert column_names == {
        "instrument_id",
        "interval",
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "source_provider",
        "created_at",
        "updated_at",
    }


def test_market_candle_uses_composite_primary_key():
    primary_key_columns = {
        column.name
        for column
        in MarketCandleEntity.__table__.primary_key.columns
    }

    assert primary_key_columns == {
        "instrument_id",
        "interval",
        "timestamp",
    }


def test_market_candle_volume_is_nullable():
    volume_column = (
        MarketCandleEntity.__table__.columns[
            "volume"
        ]
    )

    assert volume_column.nullable is True


def test_market_candle_instrument_is_foreign_key():
    instrument_column = (
        MarketCandleEntity.__table__.columns[
            "instrument_id"
        ]
    )

    foreign_keys = list(
        instrument_column.foreign_keys
    )

    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == (
        "instruments.id"
    )
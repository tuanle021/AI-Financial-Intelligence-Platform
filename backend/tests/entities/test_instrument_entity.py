from app.entities.instrument_entity import (
    InstrumentEntity,
)


def test_instrument_entity_maps_to_instruments_table():
    assert InstrumentEntity.__tablename__ == (
        "instruments"
    )


def test_instrument_entity_has_expected_columns():
    column_names = {
        column.name
        for column in InstrumentEntity.__table__.columns
    }

    assert column_names == {
        "id",
        "code",
        "display_symbol",
        "name",
        "asset_type",
        "base_asset",
        "quote_asset",
        "market_data_provider",
        "provider_symbol",
        "supports_latest",
        "supports_history",
        "supports_sentiment",
        "is_active",
        "created_at",
        "updated_at",
    }

def test_instrument_code_is_unique_and_not_nullable():
    code_column = (
        InstrumentEntity.__table__.columns["code"]
    )

    assert code_column.unique is True
    assert code_column.nullable is False
    assert code_column.index is True
    
def test_instrument_id_is_primary_key():
    id_column = (
        InstrumentEntity.__table__.columns["id"]
    )

    assert id_column.primary_key is True
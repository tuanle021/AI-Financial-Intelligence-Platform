import pytest
from pydantic import ValidationError

from app.models.asset_type import AssetType
from app.models.instrument import Instrument
from app.models.instrument_code import InstrumentCode


def create_gold_spot_instrument() -> Instrument:
    return Instrument(
        code=InstrumentCode.GOLD_SPOT,
        display_symbol="XAU/USD",
        name="Gold Spot / US Dollar",
        asset_type=AssetType.COMMODITY,
        base_asset="XAU",
        quote_asset="USD",
    )


def test_instrument_rejects_unsupported_code():
    with pytest.raises(ValidationError):
        Instrument(
            code="INVALID",
            display_symbol="INVALID",
            name="Invalid Instrument",
            asset_type=AssetType.COMMODITY,
        )


def test_instrument_rejects_extra_fields():
    with pytest.raises(ValidationError):
        Instrument(
            code=InstrumentCode.GOLD_SPOT,
            display_symbol="XAU/USD",
            name="Gold Spot / US Dollar",
            asset_type=AssetType.COMMODITY,
            unexpected_field="value",
        )


def test_instrument_is_immutable():
    instrument = create_gold_spot_instrument()

    with pytest.raises(ValidationError):
        instrument.name = "Changed name"
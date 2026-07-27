from app.entities.instrument_entity import (
    InstrumentEntity,
)
from app.models.asset_type import AssetType
from app.models.instrument import Instrument
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import (
    InstrumentDefinition,
)


def map_instrument_entity_to_definition(
    entity: InstrumentEntity,
) -> InstrumentDefinition:
    return InstrumentDefinition(
        instrument=Instrument(
            code=InstrumentCode(entity.code),
            display_symbol=entity.display_symbol,
            name=entity.name,
            asset_type=AssetType(entity.asset_type),
            base_asset=entity.base_asset,
            quote_asset=entity.quote_asset,
        ),
        market_data_provider=(
            entity.market_data_provider
        ),
        provider_symbol=entity.provider_symbol,
        supports_latest=entity.supports_latest,
        supports_history=entity.supports_history,
        supports_sentiment=(
            entity.supports_sentiment
        ),
    )
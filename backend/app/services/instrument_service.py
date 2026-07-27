from app.instruments.registry import (
    get_instrument_definition,
    list_instrument_definitions,
    resolve_instrument_definition,
)
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.instrument import InstrumentResponse
from app.mappers.instrument_mapper import (
    map_instrument_entity_to_definition,
)
from app.models.instrument_definition import (
    InstrumentDefinition,
)
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.schemas.instrument import InstrumentResponse


class InstrumentService:
    def __init__(
        self,
        repository: InstrumentRepository,
    ) -> None:
        self.repository = repository

    def get_definition(
        self,
        instrument_code: str,
    ) -> InstrumentDefinition:
        entity = self.repository.get_by_code(
            instrument_code
        )

        if entity is None:
            raise ValueError(
                f"Unsupported instrument: {instrument_code}"
            )

        return map_instrument_entity_to_definition(
            entity
        )
        
    def resolve_definition(
        self,
        instrument_code: str,
    ) -> InstrumentDefinition:
        return self.get_definition(
            instrument_code
        )

    def list_instruments(
        self,
    ) -> list[InstrumentDefinition]:
        entities = self.repository.list_active()

        return [
            map_instrument_entity_to_definition(
                entity
            )
            for entity in entities
        ]

    @staticmethod
    def to_response(
        definition: InstrumentDefinition,
    ) -> InstrumentResponse:
        instrument = definition.instrument

        return InstrumentResponse(
            code=instrument.code,
            display_symbol=instrument.display_symbol,
            name=instrument.name,
            asset_type=instrument.asset_type,
            base_asset=instrument.base_asset,
            quote_asset=instrument.quote_asset,
            supports_latest=definition.supports_latest,
            supports_history=definition.supports_history,
            supports_sentiment=(
                definition.supports_sentiment
            ),
        )
    
    def list_instrument_responses(
        self,
    ) -> list[InstrumentResponse]:
        return [
            self.to_response(definition)
            for definition in self.list_instruments()
        ]

    def resolve_instrument_response(
        self,
        raw_code: str,
    ) -> InstrumentResponse:
        definition = self.resolve_definition(
            raw_code
        )

        return self.to_response(
            definition
        )
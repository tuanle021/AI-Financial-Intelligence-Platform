from app.instruments.registry import (
    get_instrument_definition,
    list_instrument_definitions,
    resolve_instrument_definition,
)
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.instrument import InstrumentResponse


class InstrumentService:
    """Provides access to supported financial instruments."""

    def get_definition(
        self,
        instrument_code: InstrumentCode,
    ) -> InstrumentDefinition:
        return get_instrument_definition(
            instrument_code
        )

    def resolve_definition(
        self,
        raw_code: str,
    ) -> InstrumentDefinition:
        return resolve_instrument_definition(
            raw_code
        )

    def list_instruments(
        self,
    ) -> list[InstrumentDefinition]:
        return list_instrument_definitions()

    def to_response(
        self,
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
            supports_sentiment=definition.supports_sentiment,
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


instrument_service = InstrumentService()
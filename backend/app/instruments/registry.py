from app.instruments.definitions import (
    GOLD_FUTURES,
    GOLD_SPOT,
    EUR_USD,
    GBP_USD,
)
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import InstrumentDefinition


INSTRUMENT_REGISTRY: dict[
    InstrumentCode,
    InstrumentDefinition,
] = {
    InstrumentCode.GOLD_SPOT: GOLD_SPOT,
    InstrumentCode.GOLD_FUTURES: GOLD_FUTURES,
    InstrumentCode.EUR_USD: EUR_USD,
    InstrumentCode.GBP_USD: GBP_USD,
}

def get_instrument_definition(
    instrument_code: InstrumentCode,
) -> InstrumentDefinition:
    try:
        return INSTRUMENT_REGISTRY[instrument_code]
    except KeyError as error:
        raise ValueError(
            f"Unsupported instrument: {instrument_code}"
        ) from error
    
def resolve_instrument_code(
    raw_code: str,
) -> InstrumentCode:
    normalised_code = raw_code.strip().upper()

    try:
        return InstrumentCode(normalised_code)
    except ValueError as error:
        raise ValueError(
            f"Unsupported instrument: {raw_code}"
        ) from error
    
def resolve_instrument_definition(
    raw_code: str,
) -> InstrumentDefinition:
    instrument_code = resolve_instrument_code(
        raw_code
    )

    return get_instrument_definition(
        instrument_code
    )

def list_instrument_definitions(
) -> list[InstrumentDefinition]:
    return list(INSTRUMENT_REGISTRY.values())
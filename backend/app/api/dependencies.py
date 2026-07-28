from datetime import datetime

from fastapi import Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy.engine import Engine

from app.database.engine import engine
from app.database.session import DatabaseSession
from app.models.market_interval import MarketInterval
from app.providers.resolver import resolve_market_data_provider
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.schemas.market import HistoricalMarketDataRequest
from app.services.instrument_service import (
    InstrumentService,
)
from app.services.market_data import MarketDataService


def get_database_engine() -> Engine:
    return engine


def get_instrument_repository(
    session: DatabaseSession,
) -> InstrumentRepository:
    return InstrumentRepository(
        session=session,
    )


def get_instrument_service(
    repository: InstrumentRepository = Depends(
        get_instrument_repository
    ),
) -> InstrumentService:
    return InstrumentService(
        repository=repository,
    )


def create_market_data_service(
    instrument_code: str,
    instrument_service: InstrumentService,
) -> MarketDataService:
    definition = (
        instrument_service.resolve_definition(
            instrument_code
        )
    )

    provider = resolve_market_data_provider(
        definition
    )

    return MarketDataService(
        provider=provider,
        instrument=definition,
    )


def get_market_data_service(
    instrument_code: str,
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    try:
        return create_market_data_service(
            instrument_code=instrument_code,
            instrument_service=instrument_service,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


def get_gold_futures_service(
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    return create_market_data_service(
        instrument_code="GOLD_FUTURES",
        instrument_service=instrument_service,
    )


def get_gold_futures_historical_service(
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    return create_market_data_service(
        instrument_code="GOLD_FUTURES",
        instrument_service=instrument_service,
    )


def get_gold_spot_service(
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    return create_market_data_service(
        instrument_code="XAUUSD",
        instrument_service=instrument_service,
    )


def get_gold_spot_historical_service(
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    return create_market_data_service(
        instrument_code="XAUUSD",
        instrument_service=instrument_service,
    )


def get_historical_market_data_request(
    interval: MarketInterval = Query(
        default=MarketInterval.FIVE_MINUTES,
        description="Historical candle interval",
    ),
    start_time: datetime = Query(
        ...,
        description="UTC start time in ISO 8601 format",
    ),
    end_time: datetime = Query(
        ...,
        description="UTC end time in ISO 8601 format",
    ),
) -> HistoricalMarketDataRequest:
    try:
        return HistoricalMarketDataRequest(
            interval=interval,
            start_time=start_time,
            end_time=end_time,
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_CONTENT
            ),
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error

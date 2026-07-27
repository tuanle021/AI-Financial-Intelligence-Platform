from datetime import datetime

from sqlalchemy.engine import Engine

from app.database.engine import engine
from fastapi import Depends

from app.database.session import DatabaseSession
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.services.instrument_service import (
    InstrumentService,
)

def get_database_engine() -> Engine:
    return engine

from fastapi import HTTPException, Query, status, Path
from pydantic import ValidationError
from app.services.market_data import MarketDataService
from app.models.market_interval import MarketInterval
from app.schemas.market import HistoricalMarketDataRequest
from app.providers.resolver import resolve_market_data_provider
from app.services.instrument_service import InstrumentService

def create_market_data_service(
    instrument_code: str,
    instrument_service: InstrumentService,
) -> MarketDataService:
    definition = instrument_service.resolve_definition(
        instrument_code
    )

    provider = resolve_market_data_provider(
        definition
    )

    return MarketDataService(
        provider=provider,
        instrument=definition,
    )
    
def get_instrument_repository(
    session: DatabaseSession,
) -> InstrumentRepository:
    return InstrumentRepository(
        session=session
    )

def get_instrument_service(
    repository: InstrumentRepository = Depends(
        get_instrument_repository
    ),
) -> InstrumentService:
    return InstrumentService(
        repository=repository
    )

def get_market_data_service(
    instrument_code: str,
    instrument_service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> MarketDataService:
    try:
        definition = (
            instrument_service.resolve_definition(
                instrument_code
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    provider = resolve_market_data_provider(
        definition
    )

    return MarketDataService(
        provider=provider,
        instrument=definition,
    )

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

def get_gold_futures_historical_request(
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
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error

def get_gold_spot_historical_request(
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
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error

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
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error
    
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
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error
        
def get_instrument_repository(
    session: DatabaseSession,
) -> InstrumentRepository:
    return InstrumentRepository(
        session=session
    )

def get_instrument_service(
    repository: InstrumentRepository = Depends(
        get_instrument_repository
    ),
) -> InstrumentService:
    return InstrumentService(
        repository=repository
    )

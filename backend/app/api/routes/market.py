from fastapi import APIRouter, Depends

from app.services.market_data import MarketDataService
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    GoldPriceResponse
)
from app.api.dependencies import (
    get_gold_futures_service,
    get_gold_spot_service,
    get_gold_futures_historical_request,
    get_gold_futures_historical_service,
    get_gold_spot_historical_request,
    get_gold_spot_historical_service
)

from app.api.dependencies import (
    get_historical_market_data_request,
    get_market_data_service,
)
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketPriceResponse,
)

router = APIRouter(
    prefix="/market",
    tags=["Market"],
)


@router.get(
    "/gold",
    response_model=GoldPriceResponse,
    deprecated=True
)
def get_gold_price(
    service: MarketDataService = Depends(
        get_gold_futures_service
    ),
) -> GoldPriceResponse:
    """Backward-compatible gold futures endpoint."""
    return service.get_gold_price()


@router.get(
    "/gold/futures",
    response_model=GoldPriceResponse,
)
def get_gold_futures_price(
    service: MarketDataService = Depends(
        get_gold_futures_service
    ),
) -> GoldPriceResponse:
    return service.get_gold_price()


@router.get(
    "/gold/spot",
    response_model=GoldPriceResponse,
)
def get_gold_spot_price(
    service: MarketDataService = Depends(
        get_gold_spot_service
    ),
) -> GoldPriceResponse:
    return service.get_gold_price()

@router.get(
    "/gold/futures/history",
    response_model=HistoricalMarketDataResponse,
)

@router.get(
    "/gold/futures/history",
    response_model=HistoricalMarketDataResponse,
)

def get_gold_futures_history(
    request: HistoricalMarketDataRequest = Depends(
        get_gold_futures_historical_request
    ),
    service: MarketDataService = Depends(
        get_gold_futures_historical_service
    ),
) -> HistoricalMarketDataResponse:
    return service.get_historical_data(request)

@router.get(
    "/gold/spot/history",
    response_model=HistoricalMarketDataResponse,
)
def get_gold_spot_history(
    request: HistoricalMarketDataRequest = Depends(
        get_gold_spot_historical_request
    ),
    service: MarketDataService = Depends(
        get_gold_spot_historical_service
    ),
) -> HistoricalMarketDataResponse:
    return service.get_historical_data(request)

@router.get(
    "/{instrument_code}/latest",
    response_model=MarketPriceResponse,
)
def get_latest_market_data(
    service: MarketDataService = Depends(
        get_market_data_service
    ),
) -> MarketPriceResponse:
    return service.get_latest_price()

@router.get(
    "/{instrument_code}/history",
    response_model=HistoricalMarketDataResponse,
)
def get_historical_market_data(
    request: HistoricalMarketDataRequest = Depends(
        get_historical_market_data_request
    ),
    service: MarketDataService = Depends(
        get_market_data_service
    ),
) -> HistoricalMarketDataResponse:
    return service.get_historical_data(
        request
    )
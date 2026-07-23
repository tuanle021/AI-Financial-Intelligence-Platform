from datetime import datetime, timezone
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_gold_futures_service,
    get_gold_spot_service,
    get_gold_futures_historical_service,
    get_gold_spot_historical_service,
    get_market_data_service
)
from app.main import app
from app.services.market_data import MarketDataService
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle
)
from app.instruments.definitions import (
    GOLD_FUTURES,
    GOLD_SPOT,
)
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.market import MarketPriceResponse


client = TestClient(app)


class MockSpotMarketDataProvider:
    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=4056.80,
            currency=instrument.instrument.quote_asset or "USD",
            timestamp=datetime.now(timezone.utc),
        )

    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        return HistoricalMarketDataResponse(
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency=instrument.instrument.quote_asset or "USD",
            candles=[
                MarketCandle(
                    symbol=instrument.provider_symbol,
                    interval=request.interval,
                    timestamp=datetime(
                        2026,
                        7,
                        14,
                        10,
                        0,
                        tzinfo=timezone.utc,
                    ),
                    open=4055.20,
                    high=4057.00,
                    low=4054.90,
                    close=4056.10,
                    volume=None,
                )
            ],
        )


class MockFuturesMarketDataProvider:
    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=4097.20,
            currency=instrument.instrument.quote_asset or "USD",
            timestamp=datetime.now(timezone.utc),
        )

    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        return HistoricalMarketDataResponse(
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency=instrument.instrument.quote_asset or "USD",
            candles=[
                MarketCandle(
                    symbol=instrument.provider_symbol,
                    interval=request.interval,
                    timestamp=datetime(
                        2026,
                        7,
                        14,
                        10,
                        0,
                        tzinfo=timezone.utc,
                    ),
                    open=4095.10,
                    high=4098.40,
                    low=4094.70,
                    close=4097.20,
                    volume=1832,
                )
            ],
        )


def override_gold_spot_service() -> MarketDataService:
    return MarketDataService(
        provider=MockSpotMarketDataProvider(),
        instrument=GOLD_SPOT,
    )


def override_gold_futures_service() -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider(),
        instrument=GOLD_FUTURES,
    )

def override_gold_spot_historical_service() -> MarketDataService:
    return MarketDataService(
        provider=MockSpotMarketDataProvider(),
        instrument=GOLD_SPOT,
    )

def override_gold_futures_historical_service() -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider(),
        instrument=GOLD_FUTURES,
    )


def test_get_gold_spot_market_data():
    app.dependency_overrides[
        get_gold_spot_service
    ] = override_gold_spot_service

    try:
        response = client.get("/market/gold/spot")
    finally:
        app.dependency_overrides.pop(
            get_gold_spot_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAU/USD"
    assert data["price"] == 4056.80
    assert data["currency"] == "USD"
    assert "timestamp" in data


def test_get_gold_futures_market_data():
    app.dependency_overrides[
        get_gold_futures_service
    ] = override_gold_futures_service

    try:
        response = client.get("/market/gold/futures")
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "GC=F"
    assert data["price"] == 4097.20
    assert data["currency"] == "USD"
    assert "timestamp" in data

def test_get_gold_futures_historical_data():
    app.dependency_overrides[
        get_gold_futures_historical_service
    ] = override_gold_futures_historical_service

    try:
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T10:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_historical_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "GC=F"
    assert data["interval"] == "5m"
    assert data["currency"] == "USD"
    assert len(data["candles"]) == 1

    candle = data["candles"][0]

    assert candle["open"] == 4095.10
    assert candle["high"] == 4098.40
    assert candle["low"] == 4094.70
    assert candle["close"] == 4097.20
    assert candle["volume"] == 1832

def test_historical_endpoint_rejects_invalid_interval():
    response = client.get(
        "/market/gold/futures/history",
        params={
            "interval": "2h",
            "start_time": "2026-07-14T10:00:00Z",
            "end_time": "2026-07-14T11:00:00Z",
        },
    )

    assert response.status_code == 422

def test_historical_endpoint_rejects_invalid_date_range():
    app.dependency_overrides[
        get_gold_futures_historical_service
    ] = override_gold_futures_historical_service

    try:
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T12:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_historical_service,
            None,
        )

    assert response.status_code == 422

def test_get_gold_spot_historical_data():
    app.dependency_overrides[
        get_gold_spot_historical_service
    ] = override_gold_spot_historical_service

    try:
        response = client.get(
            "/market/gold/spot/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T10:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_gold_spot_historical_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAU/USD"
    assert data["interval"] == "5m"
    assert data["currency"] == "USD"
    assert len(data["candles"]) == 1
    assert data["candles"][0]["volume"] is None

def override_market_data_service(
    instrument_code: str,
) -> MarketDataService:
    normalised_code = instrument_code.strip().upper()

    if normalised_code == "XAUUSD":
        return MarketDataService(
            provider=MockSpotMarketDataProvider(),
            instrument=GOLD_SPOT,
        )

    if normalised_code == "GOLD_FUTURES":
        return MarketDataService(
            provider=MockFuturesMarketDataProvider(),
            instrument=GOLD_FUTURES,
        )

    raise HTTPException(
        status_code=404,
        detail=f"Unsupported instrument: {instrument_code}",
    )

def test_get_generic_gold_spot_latest():
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service

    try:
        response = client.get(
            "/market/XAUUSD/latest"
        )
    finally:
        app.dependency_overrides.pop(
            get_market_data_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAU/USD"
    assert data["price"] == 4056.80
    assert data["currency"] == "USD"
    assert "timestamp" in data

def test_get_generic_gold_futures_latest():
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service

    try:
        response = client.get(
            "/market/GOLD_FUTURES/latest"
        )
    finally:
        app.dependency_overrides.pop(
            get_market_data_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "GC=F"
    assert data["price"] == 4097.20
    assert data["currency"] == "USD"

def test_generic_instrument_code_is_case_insensitive():
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service

    try:
        response = client.get(
            "/market/xauusd/latest"
        )
    finally:
        app.dependency_overrides.pop(
            get_market_data_service,
            None,
        )

    assert response.status_code == 200
    assert response.json()["symbol"] == "XAU/USD"

def test_get_generic_gold_spot_history():
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service

    try:
        response = client.get(
            "/market/XAUUSD/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T10:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_market_data_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAU/USD"
    assert data["interval"] == "5m"
    assert data["currency"] == "USD"
    assert len(data["candles"]) == 1

def test_generic_endpoint_rejects_unknown_instrument():
    response = client.get(
        "/market/UNKNOWN/latest"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Unsupported instrument: UNKNOWN"
    )

def test_generic_history_rejects_invalid_date_range():
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service

    try:
        response = client.get(
            "/market/XAUUSD/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T12:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_market_data_service,
            None,
        )

    assert response.status_code == 422
from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from app.api.dependencies import (
    get_gold_futures_historical_service,
    get_gold_futures_service,
    get_gold_spot_historical_service,
    get_gold_spot_service,
    get_instrument_service,
    get_market_data_service,
)
from app.entities.instrument_entity import InstrumentEntity
from app.instruments.definitions import (
    EUR_USD,
    GBP_USD,
    GOLD_FUTURES,
    GOLD_SPOT,
)
from app.main import app
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
    MarketPriceResponse,
)
from app.services.instrument_service import InstrumentService
from app.services.market_data import MarketDataService
from fastapi import HTTPException
from fastapi.testclient import TestClient

client = TestClient(app)


class MockTwelveDataMarketDataProvider:
    PRICES = {  # noqa: RUF012
        InstrumentCode.GOLD_SPOT: 4056.80,
        InstrumentCode.GBP_USD: 1.2935,
        InstrumentCode.EUR_USD: 1.1724,
    }

    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        price = self.PRICES[
            instrument.instrument.code
        ]

        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=price,
            currency=(
                instrument.instrument.quote_asset
                or "USD"
            ),
            timestamp=datetime.now(timezone.utc),
        )

    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        price = self.PRICES[
            instrument.instrument.code
        ]

        return HistoricalMarketDataResponse(
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency=(
                instrument.instrument.quote_asset
                or "USD"
            ),
            candles=[
                MarketCandle(
                    symbol=instrument.provider_symbol,
                    interval=request.interval,
                    timestamp=request.start_time,
                    open=price,
                    high=price + 0.001,
                    low=price - 0.001,
                    close=price + 0.0005,
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
            currency=(
                instrument.instrument.quote_asset
                or "USD"
            ),
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
            currency=(
                instrument.instrument.quote_asset
                or "USD"
            ),
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


class FakeInstrumentRepository:
    def __init__(self) -> None:
        self.entities = {
            "XAUUSD": InstrumentEntity(
                code="XAUUSD",
                display_symbol="XAU/USD",
                name="Gold Spot / US Dollar",
                asset_type="commodity",
                base_asset="XAU",
                quote_asset="USD",
                market_data_provider="twelve_data",
                provider_symbol="XAU/USD",
                supports_latest=True,
                supports_history=True,
                supports_sentiment=False,
                is_active=True,
            ),
            "GOLD_FUTURES": InstrumentEntity(
                code="GOLD_FUTURES",
                display_symbol="GC=F",
                name="Gold Futures",
                asset_type="futures",
                base_asset="GOLD",
                quote_asset="USD",
                market_data_provider="yahoo",
                provider_symbol="GC=F",
                supports_latest=True,
                supports_history=True,
                supports_sentiment=False,
                is_active=True,
            ),
            "GBPUSD": InstrumentEntity(
                code="GBPUSD",
                display_symbol="GBP/USD",
                name="British Pound / US Dollar",
                asset_type="forex",
                base_asset="GBP",
                quote_asset="USD",
                market_data_provider="twelve_data",
                provider_symbol="GBP/USD",
                supports_latest=True,
                supports_history=True,
                supports_sentiment=False,
                is_active=True,
            ),
            "EURUSD": InstrumentEntity(
                code="EURUSD",
                display_symbol="EUR/USD",
                name="Euro / US Dollar",
                asset_type="forex",
                base_asset="EUR",
                quote_asset="USD",
                market_data_provider="twelve_data",
                provider_symbol="EUR/USD",
                supports_latest=True,
                supports_history=True,
                supports_sentiment=False,
                is_active=True,
            ),
        }

    def get_by_code(
        self,
        code: str,
    ) -> InstrumentEntity | None:
        return self.entities.get(
            code.strip().upper()
        )

    def list_active(
        self,
    ) -> list[InstrumentEntity]:
        return sorted(
            (
                entity
                for entity in self.entities.values()
                if entity.is_active
            ),
            key=lambda entity: entity.code,
        )


class InactiveInstrumentRepository(
    FakeInstrumentRepository
):
    def __init__(self) -> None:
        super().__init__()
        self.entities["EURUSD"].is_active = False


def override_instrument_service() -> InstrumentService:
    return InstrumentService(
        repository=FakeInstrumentRepository()
    )


def override_inactive_instrument_service(
) -> InstrumentService:
    return InstrumentService(
        repository=InactiveInstrumentRepository()
    )


def override_gold_spot_service() -> MarketDataService:
    return MarketDataService(
        provider=MockTwelveDataMarketDataProvider(),
        instrument=GOLD_SPOT,
    )


def override_gold_futures_service() -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider(),
        instrument=GOLD_FUTURES,
    )


def override_gold_spot_historical_service(
) -> MarketDataService:
    return MarketDataService(
        provider=MockTwelveDataMarketDataProvider(),
        instrument=GOLD_SPOT,
    )


def override_gold_futures_historical_service(
) -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider(),
        instrument=GOLD_FUTURES,
    )


def override_market_data_service(
    instrument_code: str,
) -> MarketDataService:
    definitions = {
        "XAUUSD": GOLD_SPOT,
        "GOLD_FUTURES": GOLD_FUTURES,
        "GBPUSD": GBP_USD,
        "EURUSD": EUR_USD,
    }
    definition = definitions.get(
        instrument_code.strip().upper()
    )

    if definition is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Unsupported instrument: "
                f"{instrument_code}"
            ),
        )

    if definition == GOLD_FUTURES:
        provider = MockFuturesMarketDataProvider()
    else:
        provider = (
            MockTwelveDataMarketDataProvider()
        )

    return MarketDataService(
        provider=provider,
        instrument=definition,
    )


@pytest.fixture(autouse=True)
def reset_dependency_overrides(
) -> Generator[None, None, None]:
    previous_overrides = dict(
        app.dependency_overrides
    )

    try:
        yield
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(
            previous_overrides
        )


@pytest.fixture
def instrument_service_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_instrument_service
    ] = override_instrument_service
    yield


@pytest.fixture
def inactive_instrument_service_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_instrument_service
    ] = override_inactive_instrument_service
    yield


@pytest.fixture
def gold_spot_service_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_gold_spot_service
    ] = override_gold_spot_service
    yield


@pytest.fixture
def gold_futures_service_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_gold_futures_service
    ] = override_gold_futures_service
    yield


@pytest.fixture
def gold_spot_history_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_gold_spot_historical_service
    ] = override_gold_spot_historical_service
    yield


@pytest.fixture
def gold_futures_history_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_gold_futures_historical_service
    ] = override_gold_futures_historical_service
    yield


@pytest.fixture
def market_data_service_override(
) -> Generator[None, None, None]:
    app.dependency_overrides[
        get_market_data_service
    ] = override_market_data_service
    yield


@pytest.mark.usefixtures(
    "gold_spot_service_override"
)
class TestLegacyGoldSpotLatest:
    def test_get_gold_spot_market_data(self):
        response = client.get(
            "/market/gold/spot"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "XAU/USD"
        assert data["price"] == 4056.80
        assert data["currency"] == "USD"
        assert "timestamp" in data


@pytest.mark.usefixtures(
    "gold_futures_service_override"
)
class TestLegacyGoldFuturesLatest:
    def test_get_gold_futures_market_data(self):
        response = client.get(
            "/market/gold/futures"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "GC=F"
        assert data["price"] == 4097.20
        assert data["currency"] == "USD"
        assert "timestamp" in data


@pytest.mark.usefixtures(
    "gold_futures_history_override"
)
class TestLegacyGoldFuturesHistory:
    def test_get_gold_futures_historical_data(
        self,
    ):
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-14T10:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
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

    def test_historical_endpoint_rejects_invalid_interval(
        self,
    ):
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "2h",
                "start_time": (
                    "2026-07-14T10:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 422

    def test_historical_endpoint_rejects_invalid_date_range(
        self,
    ):
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-14T12:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 422


@pytest.mark.usefixtures(
    "gold_spot_history_override"
)
class TestLegacyGoldSpotHistory:
    def test_get_gold_spot_historical_data(
        self,
    ):
        response = client.get(
            "/market/gold/spot/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-14T10:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "XAU/USD"
        assert data["interval"] == "5m"
        assert data["currency"] == "USD"
        assert len(data["candles"]) == 1
        assert data["candles"][0]["volume"] is None


@pytest.mark.usefixtures(
    "market_data_service_override"
)
class TestGenericMarketEndpoints:
    def test_get_generic_gold_spot_latest(self):
        response = client.get(
            "/market/XAUUSD/latest"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "XAU/USD"
        assert data["price"] == 4056.80
        assert data["currency"] == "USD"
        assert "timestamp" in data

    def test_get_generic_gold_futures_latest(self):
        response = client.get(
            "/market/GOLD_FUTURES/latest"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "GC=F"
        assert data["price"] == 4097.20
        assert data["currency"] == "USD"

    def test_generic_instrument_code_is_case_insensitive(
        self,
    ):
        response = client.get(
            "/market/xauusd/latest"
        )

        assert response.status_code == 200
        assert (
            response.json()["symbol"]
            == "XAU/USD"
        )

    def test_get_generic_gold_spot_history(self):
        response = client.get(
            "/market/XAUUSD/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-14T10:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "XAU/USD"
        assert data["interval"] == "5m"
        assert data["currency"] == "USD"
        assert len(data["candles"]) == 1

    def test_generic_endpoint_rejects_unknown_instrument(
        self,
    ):
        response = client.get(
            "/market/UNKNOWN/latest"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Unsupported instrument: UNKNOWN"
        )

    def test_generic_history_rejects_invalid_date_range(
        self,
    ):
        response = client.get(
            "/market/XAUUSD/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-14T12:00:00Z"
                ),
                "end_time": (
                    "2026-07-14T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 422

    def test_get_gbp_usd_latest(self):
        response = client.get(
            "/market/GBPUSD/latest"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "GBP/USD"
        assert data["price"] == 1.2935
        assert data["currency"] == "USD"

    def test_get_eur_usd_history(self):
        response = client.get(
            "/market/EURUSD/history",
            params={
                "interval": "5m",
                "start_time": (
                    "2026-07-22T10:00:00Z"
                ),
                "end_time": (
                    "2026-07-22T11:00:00Z"
                ),
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "EUR/USD"
        assert data["interval"] == "5m"
        assert data["currency"] == "USD"
        assert len(data["candles"]) == 1


@pytest.mark.usefixtures(
    "instrument_service_override"
)
class TestInstrumentEndpoints:
    def test_list_instruments(self):
        response = client.get(
            "/instruments"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        codes = {
            instrument["code"]
            for instrument in data
        }
        assert "XAUUSD" in codes
        assert "GOLD_FUTURES" in codes

    def test_get_gold_spot_instrument(self):
        response = client.get(
            "/instruments/XAUUSD"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "XAUUSD"
        assert data["display_symbol"] == "XAU/USD"
        assert data["asset_type"] == "commodity"
        assert data["supports_latest"] is True
        assert data["supports_history"] is True

    def test_get_instrument_is_case_insensitive(
        self,
    ):
        response = client.get(
            "/instruments/xauusd"
        )

        assert response.status_code == 200
        assert (
            response.json()["code"] == "XAUUSD"
        )

    def test_get_unknown_instrument_returns_404(
        self,
    ):
        response = client.get(
            "/instruments/UNKNOWN"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Unsupported instrument: UNKNOWN"
        )

    def test_list_instruments_includes_forex_pairs(
        self,
    ):
        response = client.get(
            "/instruments"
        )

        assert response.status_code == 200
        codes = {
            instrument["code"]
            for instrument in response.json()
        }
        assert "GBPUSD" in codes
        assert "EURUSD" in codes

    def test_get_gbp_usd_instrument(self):
        response = client.get(
            "/instruments/GBPUSD"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "GBPUSD"
        assert data["display_symbol"] == "GBP/USD"
        assert data["asset_type"] == "forex"
        assert data["base_asset"] == "GBP"
        assert data["quote_asset"] == "USD"
        assert data["supports_latest"] is True
        assert data["supports_history"] is True


def test_list_instruments_excludes_inactive_instruments(
    inactive_instrument_service_override,
):
    response = client.get(
        "/instruments"
    )

    assert response.status_code == 200
    returned_codes = {
        instrument["code"]
        for instrument in response.json()
    }
    assert "XAUUSD" in returned_codes
    assert "EURUSD" not in returned_codes

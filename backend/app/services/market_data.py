from app.models.instrument_definition import InstrumentDefinition
from app.providers.base import MarketDataProvider
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketPriceResponse,
)
from app.services.historical_market_data_persistence_service import (
    HistoricalMarketDataPersistenceService,
)


class MarketDataService:
    def __init__(
        self,
        provider: MarketDataProvider,
        instrument: InstrumentDefinition,
        persistence_service: (
            HistoricalMarketDataPersistenceService
            | None
        ) = None,
    ) -> None:
        self.provider = provider
        self.instrument = instrument
        self.persistence_service = (
            persistence_service
        )

    def get_latest_price(self) -> MarketPriceResponse:
        return self.provider.get_latest_price(
            self.instrument
        )

    def get_gold_price(self) -> MarketPriceResponse:
        """Temporary compatibility wrapper for existing routes."""
        return self.get_latest_price()

    def get_historical_data(
        self,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        response = self.provider.get_historical_data(
            self.instrument,
            request,
        )

        if self.persistence_service is not None:
            self.persistence_service.persist(
                definition=self.instrument,
                response=response,
            )

        return response
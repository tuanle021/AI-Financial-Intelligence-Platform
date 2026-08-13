from app.entities.market_candle_entity import (
    MarketCandleEntity,
)
from app.schemas.market import MarketCandle


def map_market_candle_entity_to_schema(
    entity: MarketCandleEntity,
    symbol: str,
) -> MarketCandle:
    return MarketCandle(
        symbol=symbol,
        interval=entity.interval, # pyright: ignore[reportArgumentType]
        timestamp=entity.timestamp,
        open=float(entity.open),
        high=float(entity.high),
        low=float(entity.low),
        close=float(entity.close),
        volume=(
            float(entity.volume)
            if entity.volume is not None
            else None
        ),
    )
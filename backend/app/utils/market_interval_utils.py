from datetime import timedelta, datetime

from app.models.market_interval import MarketInterval


def get_interval_duration(
    interval: MarketInterval,
) -> timedelta:
    durations = {
        MarketInterval.ONE_MINUTE: timedelta(
            minutes=1
        ),
        MarketInterval.FIVE_MINUTES: timedelta(
            minutes=5
        ),
        MarketInterval.FIFTEEN_MINUTES: timedelta(
            minutes=15
        ),
        MarketInterval.THIRTY_MINUTES: timedelta(
            minutes=30
        ),
        MarketInterval.ONE_HOUR: timedelta(
            hours=1
        ),
        MarketInterval.FOUR_HOURS: timedelta(
            hours=4
        ),
        MarketInterval.ONE_DAY: timedelta(
            days=1
        ),
    }

    try:
        return durations[interval]
    except KeyError as error:
        raise ValueError(
            f"Unsupported market interval: "
            f"{interval}"
        ) from error

def calculate_expected_timestamps(
    start_time: datetime,
    end_time: datetime,
    interval: MarketInterval,
) -> list[datetime]:
    if end_time < start_time:
        raise ValueError(
            "end_time must be greater than or "
            "equal to start_time"
        )

    duration = get_interval_duration(
        interval
    )

    timestamps: list[datetime] = []

    current = start_time

    while current <= end_time:
        timestamps.append(current)
        current += duration

    return timestamps

def calculate_expected_candle_count(
    start_time: datetime,
    end_time: datetime,
    interval: MarketInterval,
) -> int:
    return len(
        calculate_expected_timestamps(
            start_time=start_time,
            end_time=end_time,
            interval=interval,
        )
    )
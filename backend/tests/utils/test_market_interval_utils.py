from datetime import datetime, timezone

import pytest

from app.models.market_interval import MarketInterval
from app.utils.market_interval_utils import (
    calculate_expected_candle_count,
    calculate_expected_timestamps,
    get_interval_duration,
)

def test_get_interval_duration_for_five_minutes():
    result = get_interval_duration(
        MarketInterval.FIVE_MINUTES
    )

    assert result.total_seconds() == 300

def test_calculate_expected_timestamps():
    start_time = datetime(
        2026,
        7,
        22,
        10,
        0,
        tzinfo=timezone.utc,
    )

    end_time = datetime(
        2026,
        7,
        22,
        10,
        15,
        tzinfo=timezone.utc,
    )

    result = calculate_expected_timestamps(
        start_time=start_time,
        end_time=end_time,
        interval=MarketInterval.FIVE_MINUTES,
    )

    assert result == [
        datetime(
            2026,
            7,
            22,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        datetime(
            2026,
            7,
            22,
            10,
            5,
            tzinfo=timezone.utc,
        ),
        datetime(
            2026,
            7,
            22,
            10,
            10,
            tzinfo=timezone.utc,
        ),
        datetime(
            2026,
            7,
            22,
            10,
            15,
            tzinfo=timezone.utc,
        ),
    ]

def test_calculate_expected_candle_count_for_one_hour():
    start_time = datetime(
        2026,
        7,
        22,
        10,
        0,
        tzinfo=timezone.utc,
    )

    end_time = datetime(
        2026,
        7,
        22,
        11,
        0,
        tzinfo=timezone.utc,
    )

    result = calculate_expected_candle_count(
        start_time=start_time,
        end_time=end_time,
        interval=MarketInterval.FIVE_MINUTES,
    )

    assert result == 13

def test_same_start_and_end_returns_one_timestamp():
    timestamp = datetime(
        2026,
        7,
        22,
        10,
        0,
        tzinfo=timezone.utc,
    )

    result = calculate_expected_timestamps(
        start_time=timestamp,
        end_time=timestamp,
        interval=MarketInterval.FIVE_MINUTES,
    )

    assert result == [timestamp]

def test_calculate_expected_timestamps_rejects_invalid_range():
    start_time = datetime(
        2026,
        7,
        22,
        11,
        0,
        tzinfo=timezone.utc,
    )

    end_time = datetime(
        2026,
        7,
        22,
        10,
        0,
        tzinfo=timezone.utc,
    )

    with pytest.raises(
        ValueError,
        match=(
            "end_time must be greater than or "
            "equal to start_time"
        ),
    ):
        calculate_expected_timestamps(
            start_time=start_time,
            end_time=end_time,
            interval=MarketInterval.FIVE_MINUTES,
        )
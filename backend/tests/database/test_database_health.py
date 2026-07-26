from unittest.mock import MagicMock

from app.database.connection import (
    check_database_connection,
)


def test_database_health_check_returns_true():
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 1

    mock_connection = MagicMock()
    mock_connection.execute.return_value = (
        mock_result
    )

    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = (
        mock_connection
    )

    mock_engine = MagicMock()
    mock_engine.connect.return_value = (
        mock_context_manager
    )

    result = check_database_connection(
        mock_engine
    )

    assert result is True
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch
import pytest


from app.database.session import (
    SessionLocal,
    get_database_session,
)


def test_session_factory_creates_session():
    session = SessionLocal()

    try:
        assert isinstance(session, Session)
    finally:
        session.close()
        
def test_database_session_dependency_closes_session():
    mock_session = Mock(spec=Session)

    with patch(
        "app.database.session.SessionLocal",
        return_value=mock_session,
    ):
        dependency = get_database_session()

        returned_session = next(
            dependency
        )

        assert returned_session is (
            mock_session
        )

        with pytest.raises(StopIteration):
            next(dependency)

        mock_session.close.assert_called_once()
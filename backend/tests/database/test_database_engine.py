from sqlalchemy import URL
from sqlalchemy.engine import Engine
from app.core.config import settings


from app.database.engine import (
    create_database_engine,
    engine
)


def test_database_engine_is_configured():
    assert isinstance(engine, Engine)

    assert engine.url.drivername == (
        "postgresql+psycopg"
    )

    assert engine.url.host == "timescaledb"
    assert engine.url.port == 5432

def test_create_database_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username="test_user",
        password="test_password",
        host="localhost",
        port=5432,
        database="test_database",
    )

    engine = create_database_engine(
        database_url
    )

    try:
        assert isinstance(engine, Engine)
        assert engine.url == database_url
    finally:
        engine.dispose()
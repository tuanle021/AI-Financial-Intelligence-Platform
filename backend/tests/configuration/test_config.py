import pytest
from pydantic import ValidationError
from sqlalchemy import URL
from app.core.config import Settings


def create_settings(
    **overrides,
) -> Settings:
    values = {
        "app_name": "AI Market Intelligence Platform",
        "environment": "test",
        "debug": False,
        "market_provider": "mock",
        "twelve_data_api_key": "test-key",
        "twelve_data_base_url": (
            "https://api.twelvedata.com"
        ),
        "database_host": "localhost",
        "database_port": 5432,
        "database_name": "test_database",
        "database_user": "test_user",
        "database_password": "test_password",
    }

    values.update(overrides)

    return Settings(
        _env_file=None,
        **values,
    )

def test_settings_build_database_url():
    settings = create_settings()

    database_url = settings.database_url

    assert isinstance(database_url, URL)
    assert database_url.drivername == (
        "postgresql+psycopg"
    )
    assert database_url.username == "test_user"
    assert database_url.password == "test_password"
    assert database_url.host == "localhost"
    assert database_url.port == 5432
    assert database_url.database == "test_database"
    
def test_settings_accept_custom_database_port():
    settings = create_settings(
        database_port=5544
    )

    assert settings.database_url.port == 5544

@pytest.mark.parametrize(
    "invalid_port",
    [
        0,
        65536,
    ],
)
def test_settings_reject_invalid_database_port(
    invalid_port: int,
):
    with pytest.raises(ValidationError):
        create_settings(
            database_port=invalid_port
        )
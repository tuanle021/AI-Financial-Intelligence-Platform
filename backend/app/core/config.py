from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool = False
    market_provider: str = "mock"

    twelve_data_api_key: str | None = None
    twelve_data_base_url: str = (
        "https://api.twelvedata.com"
    )

    database_host: str = "localhost"
    database_port: int = Field(
        default=5432,
        ge=1,
        le=65535,
    )
    database_name: str = (
        "ai_market_intelligence"
    )
    database_user: str = "postgres"
    database_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.database_user,
            password=self.database_password,
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
        )


settings = Settings()
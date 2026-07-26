from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine

from app.core.config import settings


def create_database_engine(
    database_url: URL,
) -> Engine:
    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


engine = create_database_engine(
    settings.database_url
)
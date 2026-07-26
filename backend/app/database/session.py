from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session, sessionmaker

from app.database.engine import engine


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


def get_database_session() -> Generator[
    Session,
    None,
    None,
]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

DatabaseSession = Annotated[
    Session,
    Depends(get_database_session),
]
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

from app.api.dependencies import get_database_engine
from app.database.connection import check_database_connection
from app.schemas.health import DatabaseHealthResponse


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.environment,
    }


@router.get(
    "/database",
    response_model=DatabaseHealthResponse,
)
def database_health_check(
    database_engine: Engine = Depends(
        get_database_engine
    ),
) -> DatabaseHealthResponse:
    try:
        is_connected = check_database_connection(
            database_engine
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from error

    if not is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

    return DatabaseHealthResponse(
        status="healthy",
        database="available",
    )
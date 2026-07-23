from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.dependencies import get_instrument_service
from app.schemas.instrument import InstrumentResponse
from app.services.instrument_service import InstrumentService


router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
)


@router.get(
    "",
    response_model=list[InstrumentResponse],
)
def list_instruments(
    service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> list[InstrumentResponse]:
    return service.list_instrument_responses()


@router.get(
    "/{instrument_code}",
    response_model=InstrumentResponse,
)
def get_instrument(
    instrument_code: str = Path(
        ...,
        description="Platform instrument code, such as XAUUSD",
    ),
    service: InstrumentService = Depends(
        get_instrument_service
    ),
) -> InstrumentResponse:
    try:
        return service.resolve_instrument_response(
            instrument_code
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
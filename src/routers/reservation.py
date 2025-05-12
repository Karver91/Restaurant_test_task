from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies import reservation_service
from src.schemas.reservation import ReservationResponse, ReservationScheme
from src.services.reservation import ReservationService

router = APIRouter(prefix="/reservation", tags=["Бронирование"])

@router.post(
    path="/",
    response_model=ReservationResponse,
    summary="Забронировать столик"
)
async def add_reservation(
        request_info: ReservationScheme,
        service: Annotated[ReservationService, Depends(reservation_service)]
):
    return await service.add_one(data=request_info)

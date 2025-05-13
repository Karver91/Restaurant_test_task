from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.dependencies import reservation_service
from src.schemas.reservation import ReservationResponse, ReservationScheme
from src.services.reservation import ReservationService

router = APIRouter(prefix="/reservation", tags=["Бронирование"])


@router.get(
    path="/",
    response_model=ReservationResponse,
    summary="Получить список всех броней"
)
async def get_all_reservation(
        service: Annotated[ReservationService, Depends(reservation_service)]
):
    return await service.get_all()


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


@router.delete(
    path="/{reservation_id}",
    response_model=ReservationResponse,
    summary="Удалить бронь"
)
async def delete_reservation(
        reservation_id: PositiveInt,
        service: Annotated[ReservationService, Depends(reservation_service)]
):
    return await service.delete_one(reservation_id)

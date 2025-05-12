from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.repository.reservation import ReservationRepository
from src.repository.table import TableRepository
from src.services.reservation import ReservationService
from src.services.table import TableService


async def table_service(
        session: AsyncSession = Depends(get_async_session)
) -> TableService:
    return TableService(
        repository=TableRepository,
        session=session
    )


async def reservation_service(
        session: AsyncSession = Depends(get_async_session)
) -> ReservationService:
    return ReservationService(
        repository=ReservationRepository,
        session=session
    )

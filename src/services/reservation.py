from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from src.logginig.setting import loggers
from src.repository.reservation import ReservationRepository
from src.repository.table import TableRepository
from src.schemas.reservation import ReservationScheme, ReservationResponse

logger = loggers(__name__)


class ReservationService:
    def __init__(
            self,
            repository: type[ReservationRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def add_one(self, data: ReservationScheme):
        try:
            if not await TableRepository(session=self.repository.session).is_exists(_id=data.table_id):
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail=f"Столик с id: {data.table_id} не найден"
                )
            db_reservations = await self.repository.get_reservation_time_and_duration_minutes(
                table_id=data.table_id,
                new_reservation_time=data.reservation_time
            )
            if await self.__is_time_reserved(
                    reservation_time=data.reservation_time,
                    duration=data.duration_minutes,
                    db_reservations=db_reservations
            ):
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Столик забронирован на это время"
                )
            result = await self.repository.add_one(data.model_dump())
            if not result:
                raise
            return ReservationResponse(data=[result])
        except HTTPException as http_exp:
            logger.exception(http_exp.detail)
            raise http_exp
        except Exception as e:
            err_msg = "Ошибка добавления брони"
            logger.exception(err_msg)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg
            )

    async def get_all(self):
        try:
            result = await self.repository.get_all()
            return ReservationResponse(data=result)
        except HTTPException as http_exp:
            logger.exception(http_exp.detail)
            raise http_exp
        except Exception as e:
            err_msg = "Ошибка получения броней"
            logger.exception(err_msg)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg
            )

    async def delete_one(self):
        pass

    @staticmethod
    async def __is_time_reserved(reservation_time, duration, db_reservations) -> bool:
        new_reserv_start = reservation_time
        new_reserv_end = new_reserv_start + timedelta(minutes=duration)
        for row in db_reservations:
            db_reserv_start = row.reservation_time
            db_reserv_end = db_reserv_start + timedelta(minutes=row.duration_minutes)
            if new_reserv_start < db_reserv_end and new_reserv_end > db_reserv_start:
                return True
        return False

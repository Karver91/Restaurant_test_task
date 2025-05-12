from datetime import datetime

from sqlalchemy import select, func

from src.models import Reservation
from src.utils.repository import SQLAlchemyRepository


class ReservationRepository(SQLAlchemyRepository):
    model = Reservation

    def __init__(self, session):
        self.session = session

    async def get_reservation_time_and_duration_minutes(self, table_id, new_reservation_time: datetime):
        stmt = select(
            self.model.reservation_time,
            self.model.duration_minutes
        ).where(
            self.model.table_id == table_id,
            func.date(self.model.reservation_time) == new_reservation_time.date()
        )
        result = await self.session.execute(stmt)
        return result.all()

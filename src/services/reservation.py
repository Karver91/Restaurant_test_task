from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.reservation import ReservationRepository


class ReservationService:
    def __init__(
            self,
            repository: type[ReservationRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def add_one(self):
        pass

    async def get_all(self):
        pass

    async def delete_one(self):
        pass

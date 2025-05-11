from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.table import TableRepository


class TableService:
    def __init__(
            self,
            repository: type[TableRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def add_one(self):
        pass

    async def get_all(self):
        pass

    async def delete_one(self):
        pass


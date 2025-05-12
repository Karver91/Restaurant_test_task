from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.repository.table import TableRepository
from src.services.table import TableService


async def table_service(
        session: AsyncSession = Depends(get_async_session)
) -> TableService:
    return TableService(
        repository=TableRepository,
        session=session
    )

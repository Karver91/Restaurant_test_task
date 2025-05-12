from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from src.logginig.setting import loggers
from src.repository.table import TableRepository
from src.schemas.table import TableScheme, TableResponse

logger = loggers(__name__)


class TableService:
    def __init__(
            self,
            repository: type[TableRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def add_one(self, data: TableScheme):
        try:
            result = await self.repository.add_one(data.model_dump())
            if not result:
                raise
            return TableResponse(data=[result])
        except HTTPException as http_exp:
            logger.exception(http_exp.detail)
            raise http_exp
        except Exception as e:
            err_msg = "Ошибка добавления столика"
            logger.exception(err_msg)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg
            )

    async def get_all(self):
        try:
            result = await self.repository.get_all()
            return TableResponse(data=result)
        except HTTPException as http_exp:
            logger.exception(http_exp.detail)
            raise http_exp
        except Exception as e:
            err_msg = "Ошибка получения столиков"
            logger.exception(err_msg)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg
            )

    async def delete_one(self):
        pass

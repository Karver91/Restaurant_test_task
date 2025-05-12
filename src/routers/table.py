from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.dependencies import table_service
from src.schemas.table import TableResponse, TableScheme
from src.services.table import TableService

router = APIRouter(prefix="/tables", tags=["Столики"])


@router.get(
    path="/",
    response_model=TableResponse,
    summary="Получить список всех столиков"
)
async def get_all_tables(
        service: Annotated[TableService, Depends(table_service)]

):
    return await service.get_all()


@router.post(
    path="/",
    response_model=TableResponse,
    summary="Добавить столик",
)
async def add_table(
        request_info: TableScheme,
        service: Annotated[TableService, Depends(table_service)]
):
    return await service.add_one(data=request_info)


@router.delete(
    path="/{table_id}",
    response_model=TableResponse,
    summary="Удалить столик"
)
async def delete_table(
        table_id: PositiveInt,
        service: Annotated[TableService, Depends(table_service)]
):
    return await service.delete_one(table_id)
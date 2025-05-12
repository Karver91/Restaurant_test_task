from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.enums import TableLocationEnum
from src.models import Table
from src.schemas.table import TableScheme

TABLE_URL_PREFIX = "/tables/"


async def test_add_table(async_session: AsyncSession, ac: AsyncClient, tables: list[Table]):
    tables_amount = len(tables)
    get_max_id = lambda lst: max(lst, key=lambda x: x.id).id
    max_table_id = get_max_id(tables)
    payload = TableScheme(
        name="some table name",
        seats=4,
        location=TableLocationEnum.WINDOW
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=TABLE_URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_200_OK

    # Проверяем добавился ли столик в базу
    stmt = select(Table)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == tables_amount + 1
    assert get_max_id(res) == max_table_id + 1


async def test_get_all_tables(async_session: AsyncSession, ac: AsyncClient, tables: list[Table]):
    # вызываем ручку
    resp = await ac.get(url=TABLE_URL_PREFIX)
    assert resp.status_code == HTTP_200_OK

    # Проверяем данные в ответе
    resp_data = resp.json()
    resp_models = sorted([Table(**table) for table in resp_data['data']], key=lambda x: x.id)
    tables.sort(key=lambda x: x.id)
    assert len(resp_models) == len(tables)
    assert map(lambda x, y: x.id == y.id, zip(resp_models, tables))

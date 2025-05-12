from datetime import datetime, timedelta
from random import choice

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.models import Reservation, Table
from src.schemas.reservation import ReservationScheme

RESERVATION_URL_PREFIX = "/reservation/"


async def test_add_reservation(
        async_session: AsyncSession,
        ac: AsyncClient,
        reservations: list[Reservation],
        tables: list[Table]
):
    reservation_amount = len(reservations)
    get_max_id = lambda lst: max(lst, key=lambda x: x.id).id
    max_reservation_id = get_max_id(reservations)
    payload = ReservationScheme(
        customer_name="Some name",
        table_id=choice(tables).id,
        reservation_time=datetime.now() + timedelta(days=7),
        duration_minutes=60
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=RESERVATION_URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_200_OK

    # Проверяем добавился ли столик в базу
    stmt = select(Reservation)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == reservation_amount + 1
    assert get_max_id(res) == max_reservation_id + 1
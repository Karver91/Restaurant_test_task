from datetime import datetime, timedelta
from random import choice

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

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


@pytest.mark.parametrize(
    "reservation_minutes, duration",
    [
        (-30, 60),  # reservation_minutes = -30, duration = 60
        (-30, 120),  # reservation_minutes = -30, duration = 120
        (30, 60),  # reservation_minutes = 30, duration = 60
        (30, 10)  # reservation_minutes = 30, duration = 10
    ]
)
async def test_add_reservation_return_400_table_already_reserved(
        async_session: AsyncSession,
        ac: AsyncClient,
        reservations: list[Reservation],
        reservation_minutes,
        duration
):
    db_reservation = reservations[-1]
    db_reservation.duration_minutes = 60
    await async_session.flush()

    payload = ReservationScheme(
        customer_name="Some name",
        table_id=db_reservation.table_id,
        reservation_time=db_reservation.reservation_time + timedelta(minutes=reservation_minutes),
        duration_minutes=duration
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=RESERVATION_URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_400_BAD_REQUEST


async def test_get_reservations(
        async_session: AsyncSession,
        ac: AsyncClient,
        reservations: list[Reservation]
):
    # вызываем ручку
    resp = await ac.get(url=RESERVATION_URL_PREFIX)
    assert resp.status_code == HTTP_200_OK

    # Проверяем данные в ответе
    resp_data = resp.json()
    resp_models = sorted([Reservation(**reserv) for reserv in resp_data['data']], key=lambda x: x.id)
    reservations.sort(key=lambda x: x.id)
    assert len(resp_models) == len(reservations)
    assert map(lambda x, y: x.id == y.id, zip(resp_models, reservations))

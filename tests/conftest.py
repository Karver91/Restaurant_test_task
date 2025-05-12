from datetime import datetime, timedelta
from random import randint, choice, randrange

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings
from src.db import Base, get_async_session
from src.enums import TableLocationEnum
from src.main import app
from src.models import Table, Reservation


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_engine():
    engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def ac(async_session: AsyncSession):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/") as ac:
        app.dependency_overrides[get_async_session] = lambda: async_session
        yield ac
        app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def tables(async_session: AsyncSession) -> list[Table]:
    locations = list(TableLocationEnum)
    tables = [
        Table(
            name=f"Table_{i}",
            seats=randint(1, 4),
            location=choice(locations).value
        ) for i in range(1, 4)
    ]
    async_session.add_all(tables)
    await async_session.flush()
    return tables


@pytest_asyncio.fixture(scope="function")
async def reservations(async_session: AsyncSession, tables: list[Table]) -> list[Reservation]:
    customer_names = ["Вася", "Петя"]
    reservations = [
        Reservation(
            table_id=choice(tables).id,
            customer_name=choice(customer_names),
            reservation_time=datetime.now() + timedelta(hours=randint(1, 5)),
            duration_minutes=randrange(30, 61, 30)
        )
    ]
    async_session.add_all(reservations)
    await async_session.flush()
    return reservations

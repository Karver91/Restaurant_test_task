from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.enums import TableLocationEnum


TableLocationEnumDB = sqlalchemy.Enum(
    TableLocationEnum,
    name="table_location_enum",
    create_type=False,
    values_callable=lambda e: [field.value for field in e]
)


class Table(Base):
    __tablename__ = 'tables'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    seats: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[TableLocationEnum] = mapped_column(TableLocationEnumDB, nullable=False)


class Reservation(Base):
    __tablename__ = 'reservation'
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(
        ForeignKey(column='tables.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    customer_name: Mapped[str] = mapped_column(nullable=False)
    reservation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)

from datetime import datetime
from typing import Annotated

from asyncpg.pgproto.pgproto import timedelta
from pydantic import BaseModel, PositiveInt, Field, ConfigDict, NaiveDatetime, FutureDatetime

from src.schemas.base import BaseResponse

NaiveFutureDatetime = Annotated[
    NaiveDatetime,
    FutureDatetime
]


class ReservationScheme(BaseModel):
    customer_name: str = Field(description="Имя клиента")
    table_id: PositiveInt = Field(description="ID столика")
    reservation_time: NaiveFutureDatetime = Field(
        description="Время, на которое забронирован столик (Время должно быть в naive datetime)",
        json_schema_extra={'examples': [datetime.now().replace(microsecond=0) + timedelta(days=1)]}
    )
    duration_minutes: PositiveInt = Field(description="Продолжительность брони")


class ReservationSchemeWithID(ReservationScheme):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)


class ReservationSchemeResponse(ReservationSchemeWithID):
    reservation_time: NaiveDatetime


class ReservationResponse(BaseResponse):
    data: list[ReservationSchemeResponse]

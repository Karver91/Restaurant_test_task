from pydantic import BaseModel, Field, PositiveInt, ConfigDict

from src.enums import TableLocationEnum
from src.schemas.base import BaseResponse


class TableScheme(BaseModel):
    name: str = Field(description="Название столика")
    seats: PositiveInt = Field(description="Количество мест")
    location: TableLocationEnum = Field(description="Расположение столиков")


class TableSchemeWithID(TableScheme):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)


class TableResponse(BaseResponse):
    data: list[TableSchemeWithID]

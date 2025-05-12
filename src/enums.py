import enum


class TableLocationEnum(enum.Enum):
    WINDOW = "У окна"
    BAR = "У бара"


class ResponseStatus(enum.Enum):
    OK = "OK"
    FAILED = "FAILED"

from src.models import Table
from src.utils.repository import SQLAlchemyRepository


class TableRepository(SQLAlchemyRepository):
    model = Table

    def __init__(self, session):
        self.session = session

from src.models import Table
from src.repository.base import SQLAlchemyRepository


class TableRepository(SQLAlchemyRepository):
    model = Table

    def __init__(self, session):
        self.session = session

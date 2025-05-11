from src.models import Reservation
from src.utils.repository import SQLAlchemyRepository


class ReservationRepository(SQLAlchemyRepository):
    model = Reservation

    def __init__(self, session):
        self.session = session

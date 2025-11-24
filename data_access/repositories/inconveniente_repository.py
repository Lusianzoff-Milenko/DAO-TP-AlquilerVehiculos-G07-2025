from sqlalchemy.orm import Session
from domain.models.inconveniente import Inconveniente
from data_access.repositories.base_repository import SQLAlchemyRepository

class InconvenienteRepository(SQLAlchemyRepository[Inconveniente]):
    def __init__(self, session: Session):
        super().__init__(session, Inconveniente)
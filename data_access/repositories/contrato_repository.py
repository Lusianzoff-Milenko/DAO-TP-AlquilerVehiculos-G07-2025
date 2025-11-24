from sqlalchemy.orm import Session
from domain.models.contrato import Contrato
from data_access.repositories.base_repository import SQLAlchemyRepository

class ContratoRepository(SQLAlchemyRepository[Contrato]):
    def __init__(self, session: Session):
        super().__init__(session, Contrato)
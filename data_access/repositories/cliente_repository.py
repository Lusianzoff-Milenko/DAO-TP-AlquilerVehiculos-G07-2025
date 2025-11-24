from sqlalchemy.orm import Session
from domain.models.cliente import Cliente
from data_access.repositories.base_repository import SQLAlchemyRepository

class ClienteRepository(SQLAlchemyRepository[Cliente]):
    def __init__(self, session: Session):
        super().__init__(session, Cliente)
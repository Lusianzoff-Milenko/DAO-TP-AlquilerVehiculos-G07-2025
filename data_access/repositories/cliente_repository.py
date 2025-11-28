from sqlalchemy.orm import Session
from domain.models.cliente import Cliente
from data_access.repositories.base_repository import SQLAlchemyRepository

class ClienteRepository(SQLAlchemyRepository[Cliente]):
    def __init__(self, session: Session):
        super().__init__(session, Cliente)

    def get_by_documento(self, documento):
        return self.session.query(Cliente).filter(Cliente.documento == documento).first()

    def get_by_documento_and_tipo_documento(self, documento,tipo_documento:int):
        return self.session.query(Cliente).filter(Cliente.documento == documento and Cliente.id_tipo_documento == tipo_documento).first()
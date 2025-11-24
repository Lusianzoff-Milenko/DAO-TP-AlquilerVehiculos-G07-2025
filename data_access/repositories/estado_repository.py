from typing import Optional
from sqlalchemy.orm import Session
from domain.models.estado import Estado
from data_access.repositories.base_repository import SQLAlchemyRepository

class EstadoRepository(SQLAlchemyRepository[Estado]):
    def __init__(self, session: Session):
        super().__init__(session, Estado)

    def get_by_nombre_ambito(self, nombre: str, ambito: str) -> Optional[Estado]:
        return self.session.query(Estado).filter_by(nombre=nombre, ambito=ambito).first()

    def get_by_ambito(self, ambito: str) -> list[type[Estado]]:
        return self.session.query(Estado).filter_by(ambito=ambito).all()

    def get_by_nombre_and_ambito(self, name, ambito):
        return self.session.query(Estado).filter_by(nombre=name, ambito=ambito).first()
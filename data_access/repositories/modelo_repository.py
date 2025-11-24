from typing import Optional
from sqlalchemy.orm import Session
from domain.models.modelo import Modelo
from data_access.repositories.base_repository import SQLAlchemyRepository

class ModeloRepository(SQLAlchemyRepository[Modelo]):
    def __init__(self, session: Session):
        super().__init__(session, Modelo)

    def get_by_nombre(self, nombre: str) -> Optional[Modelo]:
        return self.session.query(Modelo).filter(Modelo.nombre == nombre).first()
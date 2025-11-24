from typing import Optional
from sqlalchemy.orm import Session
from domain.models.marca import Marca
from data_access.repositories.base_repository import SQLAlchemyRepository

class MarcaRepository(SQLAlchemyRepository[Marca]):
    def __init__(self, session: Session):
        super().__init__(session, Marca)

    def get_by_nombre(self, nombre: str) -> Optional[Marca]:
        return self.session.query(Marca).filter(Marca.nombre == nombre).first()
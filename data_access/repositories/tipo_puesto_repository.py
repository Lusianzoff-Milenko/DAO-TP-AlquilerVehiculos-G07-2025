from typing import Optional
from sqlalchemy.orm import Session
from domain.models.tipoPuesto import TipoPuesto
from data_access.repositories.base_repository import SQLAlchemyRepository

class TipoPuestoRepository(SQLAlchemyRepository[TipoPuesto]):
    def __init__(self, session: Session):
        super().__init__(session, TipoPuesto)

    def get_by_nombre(self, nombre: str) -> Optional[TipoPuesto]:
        return self.session.query(TipoPuesto).filter(TipoPuesto.nombre == nombre).first()
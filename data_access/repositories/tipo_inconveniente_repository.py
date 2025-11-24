from typing import Optional
from sqlalchemy.orm import Session
from domain.models.tipoInconveniente import TipoInconveniente
from data_access.repositories.base_repository import SQLAlchemyRepository

class TipoInconvenienteRepository(SQLAlchemyRepository[TipoInconveniente]):
    def __init__(self, session: Session):
        super().__init__(session, TipoInconveniente)

    def get_by_nombre(self, nombre: str) -> Optional[TipoInconveniente]:
        return self.session.query(TipoInconveniente).filter(TipoInconveniente.nombre == nombre).first()
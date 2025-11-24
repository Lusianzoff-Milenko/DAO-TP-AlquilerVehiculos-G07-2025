from typing import Optional
from sqlalchemy.orm import Session
from domain.models.tipoDocumento import TipoDocumento
from data_access.repositories.base_repository import SQLAlchemyRepository

class TipoDocumentoRepository(SQLAlchemyRepository[TipoDocumento]):
    def __init__(self, session: Session):
        super().__init__(session, TipoDocumento)

    def get_by_nombre(self, nombre: str) -> Optional[TipoDocumento]:
        return self.session.query(TipoDocumento).filter(TipoDocumento.nombre == nombre).first()
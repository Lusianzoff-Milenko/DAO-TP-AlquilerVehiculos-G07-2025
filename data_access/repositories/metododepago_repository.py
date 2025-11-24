from typing import Optional
from sqlalchemy.orm import Session
from domain.models.metodoDePago import MetodoDePago
from data_access.repositories.base_repository import SQLAlchemyRepository

class MetodoDePagoRepository(SQLAlchemyRepository[MetodoDePago]):
    def __init__(self, session: Session):
        super().__init__(session, MetodoDePago)

    def get_by_nombre(self, nombre: str) -> Optional[MetodoDePago]:
        return self.session.query(MetodoDePago).filter(MetodoDePago.nombre == nombre).first()
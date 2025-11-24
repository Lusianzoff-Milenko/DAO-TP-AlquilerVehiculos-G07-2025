from sqlalchemy.orm import Session
from domain.models.detalle_contrato import DetalleContrato
from data_access.repositories.base_repository import SQLAlchemyRepository

class DetalleContratoRepository(SQLAlchemyRepository[DetalleContrato]):
    def __init__(self, session: Session):
        super().__init__(session, DetalleContrato)

    def list_by_contrato(self, contrato_id: int) -> list[type[DetalleContrato]]:
        return self.session.query(DetalleContrato).filter_by(id_contrato=contrato_id).all()
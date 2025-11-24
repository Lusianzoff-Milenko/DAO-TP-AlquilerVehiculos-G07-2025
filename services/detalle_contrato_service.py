from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.detalle_contrato import DetalleContrato
from data_access.repositories.detalle_contrato_repository import DetalleContratoRepository

class DetalleContratoService:
    def __init__(self, detalle_repo: DetalleContratoRepository):
        self._repo = detalle_repo

    def create_detalle_contrato(self, detalle: DetalleContrato) -> Optional[int]:
        try:
            nuevo = self._repo.create(detalle)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def list_detalles_by_contrato(self, contrato_id: int) -> list[type[DetalleContrato]]:
        return self._repo.list_by_contrato_id(contrato_id)
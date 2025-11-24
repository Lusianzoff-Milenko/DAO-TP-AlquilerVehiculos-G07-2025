from typing import Optional
from sqlalchemy.exc import IntegrityError
from domain.models.detalle_contrato import DetalleContrato
from data_access.repositories.detalle_contrato_repository import DetalleContratoRepository

class DetalleContratoService:
    def __init__(self, detalle_repo: DetalleContratoRepository):
        self._repo = detalle_repo

    def create_detalle(self, detalle: DetalleContrato) -> Optional[int]:
        try:
            nuevo = self._repo.create(detalle)
            return nuevo.id
        except IntegrityError:
            print("Error: Contrato o Vehículo no existen.")
            self._repo.session.rollback()
            return None

    def get_detalle_by_id(self, id: int) -> Optional[DetalleContrato]:
        return self._repo.get_by_id(id)

    def list_por_contrato(self, contrato_id: int) -> list[type[DetalleContrato]]:
        return self._repo.list_by_contrato(contrato_id)

    def update_detalle(self, detalle: DetalleContrato) -> bool:
        if not detalle.id: return False
        try:
            self._repo.update(detalle)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_detalle(self, id: int) -> bool:
        try:
            return self._repo.delete(id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
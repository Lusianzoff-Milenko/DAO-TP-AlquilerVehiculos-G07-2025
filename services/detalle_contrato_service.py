from typing import Optional, List

from data_access.repositories import VehiculoRepository
from domain.models.detalle_contrato import DetalleContrato
from data_access.repositories.detalle_contrato_repository import DetalleContratoRepository
from data_access.repositories.contrato_repository import ContratoRepository
from services.validation_mapper import ValidationMapper


class DetalleContratoService:
    def __init__(self, detalle_repo: DetalleContratoRepository, contrato_repo: ContratoRepository, vehiculo_repo: VehiculoRepository, mapper: ValidationMapper):
        self._repo = detalle_repo
        self._contrato_repo = contrato_repo
        self._vehiculo_repo = vehiculo_repo
        self._mapper = mapper

    def create_detalle_contrato(self, detalle: DetalleContrato) -> Optional[int]:
        if not self._mapper.validate_fk_exists('contrato', detalle.id_contrato, 'id_contrato'):
            return None
        return self._repo.create(detalle)

    def get_detalle_contrato_by_id(self, detalle_id: int) -> Optional[DetalleContrato]:
        return self._repo.get_by_id(detalle_id)

    def list_all_detalles_contrato(self) -> List[DetalleContrato]:
        return self._repo.list_all()

    def list_detalles_by_contrato(self, contrato_id: int) -> List[DetalleContrato]:
        return [d for d in self._repo.list_all() if d.id_contrato == contrato_id]

    def update_detalle_contrato(self, detalle: DetalleContrato) -> bool:
        if not detalle.id:
            print("ID de detalle requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('contrato', detalle.id_contrato, 'id_contrato'):
            return False
        return self._repo.update(detalle)

    def delete_detalle_contrato(self, detalle_id: int) -> bool:
        return self._repo.delete(detalle_id)
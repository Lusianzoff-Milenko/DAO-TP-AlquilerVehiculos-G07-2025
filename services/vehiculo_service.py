from typing import Optional, List
from domain.models.vehiculo import Vehiculo
from data_access.repositories.vehiculo_repository import VehiculoRepository
from data_access.repositories.modelo_repository import ModeloRepository
from data_access.repositories.color_repository import ColorRepository
from data_access.repositories.estado_repository import EstadoRepository
from services.contrato_service import ContratoService
from services.validation_mapper import ValidationMapper


class VehiculoService:
    def __init__(self, vehiculo_repo: VehiculoRepository, modelo_repo: ModeloRepository, color_repo: ColorRepository,
                 estado_repo: EstadoRepository, contrato_service: ContratoService):
        self._repo = vehiculo_repo
        self._contrato_service = contrato_service
        repos_to_validate = {
            'modelo': modelo_repo,
            'color': color_repo,
            'estado': estado_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

    def create_vehiculo(self, vehiculo: Vehiculo) -> Optional[int]:
        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return None
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return None
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return None

        return self._repo.create(vehiculo)

    def get_vehiculo_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        return self._repo.get_by_id(vehiculo_id)

    def list_all_vehiculos(self) -> List[Vehiculo]:
        return self._repo.list_all()

    def update_vehiculo(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.id:
            print("ID de vehículo requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return False
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return False
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return False

        return self._repo.update(vehiculo)

    def delete_vehiculo(self, vehiculo_id: int) -> bool:
        if self._contrato_service.has_active_contracts("vehiculo", vehiculo_id):
            print(
                f"Error de Negocio: No se puede eliminar el Vehículo ID {vehiculo_id} porque está asignado a contratos activos.")
            return False
        return self._repo.delete(vehiculo_id)
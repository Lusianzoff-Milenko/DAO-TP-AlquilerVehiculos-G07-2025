# python
# file: `application/services/mantenimiento_service.py`
from typing import Optional, List
from domain.models.mantenimiento import Mantenimiento
from data_access.repositories.mantenimiento_repository import MantenimientoRepository

# Assuming existence of repositories for foreign keys
from data_access.repositories.vehiculo_repository import VehiculoRepository
from data_access.repositories.estado_repository import EstadoRepository
from data_access.repositories.empleado_repository import EmpleadoRepository
from services.validation_mapper import ValidationMapper


class MantenimientoService:
    def __init__(self, mantenimiento_repo: MantenimientoRepository, vehiculo_repo: VehiculoRepository, estado_repo: EstadoRepository, empleado_repo: EmpleadoRepository):
        self._repo = mantenimiento_repo
        repos_to_validate = {
            'vehiculo': vehiculo_repo,
            'estado': estado_repo,
            'empleado': empleado_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

    def create_mantenimiento(self, mantenimiento: Mantenimiento) -> Optional[int]:
        if not self._mapper.validate_fk_exists('vehiculo', mantenimiento.id_vehiculo, 'id_vehiculo'): return None
        if not self._mapper.validate_fk_exists('estado', mantenimiento.id_estado, 'id_estado'): return None
        if not self._mapper.validate_fk_exists('empleado', mantenimiento.id_empleado, 'id_empleado'): return None

        return self._repo.create(mantenimiento)

    def get_mantenimiento_by_id(self, mantenimiento_id: int) -> Optional[Mantenimiento]:
        return self._repo.get_by_id(mantenimiento_id)

    def list_all_mantenimientos(self) -> List[Mantenimiento]:
        return self._repo.list_all()

    def update_mantenimiento(self, mantenimiento: Mantenimiento) -> bool:
        if not mantenimiento.id:
            print("ID de mantenimiento requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('vehiculo', mantenimiento.id_vehiculo, 'id_vehiculo'): return False
        if not self._mapper.validate_fk_exists('estado', mantenimiento.id_estado, 'id_estado'): return False
        if not self._mapper.validate_fk_exists('empleado', mantenimiento.id_empleado, 'id_empleado'): return False

        return self._repo.update(mantenimiento)

    def delete_mantenimiento(self, mantenimiento_id: int) -> bool:
        return self._repo.delete(mantenimiento_id)
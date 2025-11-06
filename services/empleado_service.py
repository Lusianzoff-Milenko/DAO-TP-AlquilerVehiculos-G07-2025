from typing import Optional, List
from domain.models.empleado import Empleado
from data_access.repositories.empleado_repository import EmpleadoRepository
from data_access.repositories.persona_repository import PersonaRepository
from data_access.repositories.tipo_puesto_repository import TipoPuestoRepository
from services.contrato_service import ContratoService
from services.validation_mapper import ValidationMapper


class EmpleadoService:
    def __init__(self, empleado_repo: EmpleadoRepository, persona_repo: PersonaRepository, tipo_puesto_repo: TipoPuestoRepository, contrato_service: ContratoService):
        self._repo = empleado_repo
        self._contrato_service = contrato_service

        repos_to_validate = {
            'persona': persona_repo,
            'tipo_puesto': tipo_puesto_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)


    def create_empleado(self, empleado: Empleado) -> Optional[int]:
        if not self._mapper.validate_fk_exists('persona', empleado.id_persona, 'id_persona'):
            return None
        if not self._mapper.validate_fk_exists('tipo_puesto', empleado.id_tipo_puesto, 'id_tipo_puesto'):
            return None

        return self._repo.create(empleado)

    def get_empleado_by_id(self, empleado_id: int) -> Optional[Empleado]:
        return self._repo.get_by_id(empleado_id)

    def list_all_empleados(self) -> List[Empleado]:
        return self._repo.list_all()

    def update_empleado(self, empleado: Empleado) -> bool:
        if not empleado.id: return False
        if not self._mapper.validate_fk_exists('persona', empleado.id_persona, 'id_persona'):
            return False
        if not self._mapper.validate_fk_exists('tipo_puesto', empleado.id_tipo_puesto, 'id_tipo_puesto'):
            return False

        return self._repo.update(empleado)

    def delete_empleado(self, empleado_id: int) -> bool:
        if self._repo.get_by_id(empleado_id) is None:
            print(f"Empleado con ID {empleado_id} no encontrado.")
            return False
        if self._contrato_service.has_active_contracts("empleado", empleado_id):
            print(
                f"Error de Negocio: No se puede eliminar el Empleado ID {empleado_id} porque está asociado a contratos activos.")
            return False

        return self._repo.delete(empleado_id)
from typing import Optional, List
from domain.models.inconveniente import Inconveniente
from data_access.repositories.inconveniente_repository import InconvenienteRepository
from services.validation_mapper import ValidationMapper


class InconvenienteService:
    def __init__(self, inconveniente_repo: InconvenienteRepository, mapper: ValidationMapper):
        self._repo = inconveniente_repo
        self._mapper = mapper

    def create_inconveniente(self, inconveniente: Inconveniente) -> Optional[int]:
        if not self._mapper.validate_fk_exists('tipo_inconveniente', inconveniente.id_tipo_inconveniente,
                                               'id_tipo_inconveniente'):
            return None
        if not self._mapper.validate_fk_exists('contrato', inconveniente.id_contrato, 'id_contrato'):
            return None
        if not self._mapper.validate_fk_exists('estado', inconveniente.id_estado, 'id_estado'):
            return None

        return self._repo.create(inconveniente)

    def get_inconveniente_by_id(self, inconveniente_id: int) -> Optional[Inconveniente]:
        return self._repo.get_by_id(inconveniente_id)

    def list_all_inconvenientes(self) -> List[Inconveniente]:
        return self._repo.list_all()

    def update_inconveniente(self, inconveniente: Inconveniente) -> bool:
        if not inconveniente.id:
            print("ID de inconveniente requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('tipo_inconveniente', inconveniente.id_tipo_inconveniente, 'id_tipo_inconveniente'):
            return False
        if not self._mapper.validate_fk_exists('contrato', inconveniente.id_contrato, 'id_contrato'):
            return False
        if not self._mapper.validate_fk_exists('estado', inconveniente.id_estado, 'id_estado'):
            return False

        return self._repo.update(inconveniente)

    def delete_inconveniente(self, inconveniente_id: int) -> bool:
        return self._repo.delete(inconveniente_id)
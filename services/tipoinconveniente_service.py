from typing import Optional, List
from domain.models.tipoInconveniente import TipoInconveniente
from data_access.repositories.tipo_inconveniente_repository import TipoInconvenienteRepository

class TipoInconvenienteService:
    def __init__(self, tipo_inconveniente_repo: TipoInconvenienteRepository):
        self._repo = tipo_inconveniente_repo

    def create_tipo_inconveniente(self, tipo_inconveniente: TipoInconveniente) -> Optional[int]:
        """Crea un nuevo tipo de inconveniente si no existe."""
        return self._repo.create(tipo_inconveniente)

    def get_tipo_inconveniente_by_id(self, tipo_inconveniente_id: int) -> Optional[TipoInconveniente]:
        return self._repo.get_by_id(tipo_inconveniente_id)

    def list_all_tipos_inconveniente(self) -> List[TipoInconveniente]:
        return self._repo.list_all()

    def update_tipo_inconveniente(self, tipo_inconveniente: TipoInconveniente) -> bool:
        """Actualiza un tipo de inconveniente existente."""
        if not tipo_inconveniente.id:
            print("ID de tipo de inconveniente requerido para actualizar.")
            return False
        return self._repo.update(tipo_inconveniente)

    def delete_tipo_inconveniente(self, tipo_inconveniente_id: int) -> bool:
        """Elimina un tipo de inconveniente. Se recomienda chequear antes si está en uso por Inconvenientes."""
        return self._repo.delete(tipo_inconveniente_id)
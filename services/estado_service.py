# python
# file: `application/services/estado_service.py`
from typing import Optional, List
from domain.models.estado import Estado
from data_access.repositories.estado_repository import EstadoRepository

class EstadoService:
    def __init__(self, estado_repo: EstadoRepository):
        self._repo = estado_repo

    def create_estado(self, estado: Estado) -> Optional[int]:
        return self._repo.create(estado)

    def get_estado_by_id(self, estado_id: int) -> Optional[Estado]:
        return self._repo.get_by_id(estado_id)

    def list_all_estados(self) -> List[Estado]:
        return self._repo.list_all()

    def update_estado(self, estado: Estado) -> bool:
        if not estado.id:
            print("ID de estado requerido para actualizar.")
            return False
        return self._repo.update(estado)

    def delete_estado(self, estado_id: int) -> bool:
        # Lógica de Negocio: Evitar eliminar si está en uso por Vehículos/Contratos/Mantenimientos/Inconvenientes
        return self._repo.delete(estado_id)

    def get_estado_by_name(self, name: str) -> Optional[Estado]:
        return self._repo.get_by_name(name)

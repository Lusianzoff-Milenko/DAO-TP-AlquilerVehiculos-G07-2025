# python
# file: `application/services/tipopuesto_service.py`
from typing import Optional, List
from domain.models.tipoPuesto import TipoPuesto
from data_access.repositories.tipo_puesto_repository import TipoPuestoRepository

class TipoPuestoService:
    def __init__(self, tipo_puesto_repo: TipoPuestoRepository):
        self._repo = tipo_puesto_repo

    def create_tipo_puesto(self, tipo_puesto: TipoPuesto) -> Optional[int]:
        """Crea un nuevo tipo de puesto si no existe."""
        return self._repo.create(tipo_puesto)

    def get_tipo_puesto_by_id(self, tipo_puesto_id: int) -> Optional[TipoPuesto]:
        return self._repo.get_by_id(tipo_puesto_id)

    def list_all_tipos_puesto(self) -> List[TipoPuesto]:
        return self._repo.list_all()

    def update_tipo_puesto(self, tipo_puesto: TipoPuesto) -> bool:
        """Actualiza un tipo de puesto existente."""
        if not tipo_puesto.id:
            print("ID de tipo de puesto requerido para actualizar.")
            return False
        return self._repo.update(tipo_puesto)

    def delete_tipo_puesto(self, tipo_puesto_id: int) -> bool:
        """Elimina un tipo de puesto. Se recomienda chequear antes si está en uso por Empleados."""
        return self._repo.delete(tipo_puesto_id)
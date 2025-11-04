# python
# file: `application/services/marca_service.py`
from typing import Optional, List
from domain.models.marca import Marca
from data_access.repositories.marca_repository import MarcaRepository

class MarcaService:
    def __init__(self, marca_repo: MarcaRepository):
        self._repo = marca_repo

    def create_marca(self, marca: Marca) -> Optional[int]:
        """Crea una nueva marca si no existe."""
        return self._repo.create(marca)

    def get_marca_by_id(self, marca_id: int) -> Optional[Marca]:
        return self._repo.get_by_id(marca_id)

    def list_all_marcas(self) -> List[Marca]:
        return self._repo.list_all()

    def update_marca(self, marca: Marca) -> bool:
        """Actualiza una marca existente."""
        if not marca.id:
            print("ID de marca requerido para actualizar.")
            return False
        return self._repo.update(marca)

    def delete_marca(self, marca_id: int) -> bool:
        """Elimina una marca. Se recomienda chequear antes si tiene Modelos asociados."""
        return self._repo.delete(marca_id)
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.marca import Marca
from data_access.repositories.marca_repository import MarcaRepository

class MarcaService:
    def __init__(self, marca_repo: MarcaRepository):
        self._repo = marca_repo

    def create_marca(self, marca: Marca) -> Optional[int]:
        try:
            nuevo = self._repo.create(marca)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_marca_by_id(self, marca_id: int) -> Optional[Marca]:
        return self._repo.get_by_id(marca_id)

    def list_all_marcas(self) -> List[Marca]:
        return self._repo.list_all()

    def update_marca(self, marca: Marca) -> bool:
        if not marca.id: return False
        try:
            self._repo.update(marca)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_marca(self, marca_id: int) -> bool:
        try:
            return self._repo.delete(marca_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
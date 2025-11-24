from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.modelo import Modelo
from data_access.repositories.modelo_repository import ModeloRepository

class ModeloService:
    def __init__(self, modelo_repo: ModeloRepository):
        self._repo = modelo_repo

    def create_modelo(self, modelo: Modelo) -> Optional[int]:
        try:
            nuevo = self._repo.create(modelo)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_modelo_by_id(self, modelo_id: int) -> Optional[Modelo]:
        return self._repo.get_by_id(modelo_id)

    def list_all_modelos(self) -> List[Modelo]:
        return self._repo.list_all()

    def update_modelo(self, modelo: Modelo) -> bool:
        if not modelo.id: return False
        try:
            self._repo.update(modelo)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_modelo(self, modelo_id: int) -> bool:
        try:
            return self._repo.delete(modelo_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
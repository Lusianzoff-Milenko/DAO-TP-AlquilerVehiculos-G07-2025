from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.inconveniente import Inconveniente
from data_access.repositories.inconveniente_repository import InconvenienteRepository

class InconvenienteService:
    def __init__(self, inconveniente_repo: InconvenienteRepository, mapper=None):
        self._repo = inconveniente_repo

    def create_inconveniente(self, inconveniente: Inconveniente) -> Optional[int]:
        try:
            nuevo = self._repo.create(inconveniente)
            return nuevo.id
        except IntegrityError as e:
            print(f"Error al crear inconveniente: {e}")
            self._repo.session.rollback()
            return None

    def get_inconveniente_by_id(self, inconveniente_id: int) -> Optional[Inconveniente]:
        return self._repo.get_by_id(inconveniente_id)

    def list_all_inconvenientes(self) -> List[Inconveniente]:
        return self._repo.list_all()

    def update_inconveniente(self, inconveniente: Inconveniente) -> bool:
        if not inconveniente.id: return False
        try:
            self._repo.update(inconveniente)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_inconveniente(self, inconveniente_id: int) -> bool:
        try:
            return self._repo.delete(inconveniente_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.tipoInconveniente import TipoInconveniente
from data_access.repositories.tipo_inconveniente_repository import TipoInconvenienteRepository

class TipoInconvenienteService:
    def __init__(self, tipo_inconveniente_repo: TipoInconvenienteRepository):
        self._repo = tipo_inconveniente_repo

    def create_tipo_inconveniente(self, tipo_inconveniente: TipoInconveniente) -> Optional[int]:
        try:
            nuevo = self._repo.create(tipo_inconveniente)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_tipo_inconveniente_by_id(self, tipo_inconveniente_id: int) -> Optional[TipoInconveniente]:
        return self._repo.get_by_id(tipo_inconveniente_id)

    def list_all_tipos_inconveniente(self) -> List[TipoInconveniente]:
        return self._repo.list_all()

    def update_tipo_inconveniente(self, tipo_inconveniente: TipoInconveniente) -> bool:
        if not tipo_inconveniente.id: return False
        try:
            self._repo.update(tipo_inconveniente)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_tipo_inconveniente(self, tipo_inconveniente_id: int) -> bool:
        try:
            return self._repo.delete(tipo_inconveniente_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
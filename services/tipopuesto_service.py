from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.tipoPuesto import TipoPuesto
from data_access.repositories.tipo_puesto_repository import TipoPuestoRepository

class TipoPuestoService:
    def __init__(self, tipo_puesto_repo: TipoPuestoRepository):
        self._repo = tipo_puesto_repo

    def create_tipo_puesto(self, tipo_puesto: TipoPuesto) -> Optional[int]:
        try:
            nuevo = self._repo.create(tipo_puesto)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_tipo_puesto_by_id(self, tipo_puesto_id: int) -> Optional[TipoPuesto]:
        return self._repo.get_by_id(tipo_puesto_id)

    def list_all_tipos_puesto(self) -> List[TipoPuesto]:
        return self._repo.list_all()

    def update_tipo_puesto(self, tipo_puesto: TipoPuesto) -> bool:
        if not tipo_puesto.id: return False
        try:
            self._repo.update(tipo_puesto)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_tipo_puesto(self, tipo_puesto_id: int) -> bool:
        try:
            return self._repo.delete(tipo_puesto_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
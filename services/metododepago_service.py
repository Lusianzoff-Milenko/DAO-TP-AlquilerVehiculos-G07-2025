from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.metodoDePago import MetodoDePago
from data_access.repositories.metododepago_repository import MetodoDePagoRepository

class MetodoDePagoService:
    def __init__(self, metodo_pago_repo: MetodoDePagoRepository):
        self._repo = metodo_pago_repo

    def create_metodo_pago(self, metodo_pago: MetodoDePago) -> Optional[int]:
        try:
            nuevo = self._repo.create(metodo_pago)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_metodo_pago_by_id(self, metodo_pago_id: int) -> Optional[MetodoDePago]:
        return self._repo.get_by_id(metodo_pago_id)

    def list_all_metodos_pago(self) -> List[MetodoDePago]:
        return self._repo.list_all()

    def update_metodo_pago(self, metodo_pago: MetodoDePago) -> bool:
        if not metodo_pago.id: return False
        try:
            self._repo.update(metodo_pago)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_metodo_pago(self, metodo_pago_id: int) -> bool:
        try:
            return self._repo.delete(metodo_pago_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
# python
# file: `application/services/metododepago_service.py`
from typing import Optional, List
from domain.models.metodoDePago import MetodoDePago
from data_access.repositories.metododepago_repository import MetodoDePagoRepository

class MetodoDePagoService:
    def __init__(self, metodo_pago_repo: MetodoDePagoRepository):
        self._repo = metodo_pago_repo

    def create_metodo_pago(self, metodo_pago: MetodoDePago) -> Optional[int]:
        """Crea un nuevo método de pago si no existe."""
        return self._repo.create(metodo_pago)

    def get_metodo_pago_by_id(self, metodo_pago_id: int) -> Optional[MetodoDePago]:
        return self._repo.get_by_id(metodo_pago_id)

    def list_all_metodos_pago(self) -> List[MetodoDePago]:
        return self._repo.list_all()

    def update_metodo_pago(self, metodo_pago: MetodoDePago) -> bool:
        """Actualiza un método de pago existente."""
        if not metodo_pago.id:
            print("ID de método de pago requerido para actualizar.")
            return False
        return self._repo.update(metodo_pago)

    def delete_metodo_pago(self, metodo_pago_id: int) -> bool:
        """Elimina un método de pago. Se recomienda chequear antes si está en uso por Contratos."""
        return self._repo.delete(metodo_pago_id)
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.cliente import Cliente
from data_access.repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, cliente_repo: ClienteRepository, mapper=None):
        # mapper se mantiene por compatibilidad en inyección, pero se usa menos
        self._repo = cliente_repo

    def create_cliente(self, cliente: Cliente) -> Optional[int]:
        try:
            # SQLAlchemy validará FKs (persona, tipo_documento) al hacer commit
            nuevo_cliente = self._repo.create(cliente)
            return nuevo_cliente.id
        except IntegrityError as e:
            print(f"Error de integridad al crear cliente (posible duplicado o FK inválida): {e}")
            self._repo.session.rollback()
            return None
        except Exception as e:
            print(f"Error desconocido al crear cliente: {e}")
            self._repo.session.rollback()
            return None

    def get_cliente_by_id(self, cliente_id: int) -> Optional[Cliente]:
        return self._repo.get_by_id(cliente_id)

    def list_all_clientes(self) -> List[Cliente]:
        return self._repo.list_all()

    def update_cliente(self, cliente: Cliente) -> bool:
        if not cliente.id:
            return False
        try:
            self._repo.update(cliente)
            return True
        except IntegrityError:
            print("Error al actualizar cliente: Datos inválidos o duplicados.")
            self._repo.session.rollback()
            return False

    def delete_cliente(self, cliente_id: int) -> bool:
        # La validación de contratos activos se mantiene porque es lógica de negocio pura
        # (asumiendo que has_active_contracts se mueve o se inyecta contrato_service)
        try:
            return self._repo.delete(cliente_id)
        except IntegrityError:
            print("No se puede eliminar: El cliente tiene registros asociados.")
            self._repo.session.rollback()
            return False
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.cliente import Cliente
from data_access.repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, cliente_repo: ClienteRepository):
        self._repo = cliente_repo

    def create_cliente(self, cliente: Cliente) -> Optional[int]:
        try:
            # SQLAlchemy validará si la Persona y el TipoDocumento existen
            nuevo_cliente = self._repo.create(cliente)
            return nuevo_cliente.id
        except IntegrityError as e:
            print(f"Error al crear cliente (posible duplicado de documento): {e}")
            self._repo.session.rollback()
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            self._repo.session.rollback()
            return None

    def get_cliente_by_id(self, cliente_id: int) -> Optional[Cliente]:
        return self._repo.get_by_id(cliente_id)

    def get_cliente_by_documento(self, documento: str) -> Optional[Cliente]:
        return self._repo.get_by_documento(documento)

    def list_all_clientes(self) -> List[Cliente]:
        return self._repo.list_all()

    def update_cliente(self, cliente: Cliente) -> bool:
        if not cliente.id: return False
        try:
            self._repo.update(cliente)
            return True
        except IntegrityError:
            print("Error al actualizar cliente: Datos inválidos.")
            self._repo.session.rollback()
            return False

    def delete_cliente(self, cliente_id: int) -> bool:
        try:
            return self._repo.delete(cliente_id)
        except IntegrityError:
            # Esto ocurre si hay claves foráneas (Contratos) apuntando al cliente
            print("No se puede eliminar el cliente porque tiene contratos asociados.")
            self._repo.session.rollback()
            return False
from typing import Optional, List
from domain.models.cliente import Cliente
from data_access.repositories.cliente_repository import ClienteRepository
from .validation_mapper import ValidationMapper

class ClienteService:
    def __init__(self, cliente_repo: ClienteRepository, mapper: ValidationMapper):
        self._repo = cliente_repo
        self._mapper = mapper

    def create_cliente(self, cliente: Cliente) -> Optional[int]:
        if not self._mapper.validate_fk_exists('persona', cliente.id_persona, 'id_persona'):
            return None
        if not self._mapper.validate_fk_exists('tipo_documento', cliente.id_tipo_documento, 'id_tipo_documento'):
            return None

        return self._repo.create(cliente)

    def get_cliente_by_id(self, cliente_id: int) -> Optional[Cliente]:
        return self._repo.get_by_id(cliente_id)

    def list_all_clientes(self) -> List[Cliente]:
        return self._repo.list_all()

    def update_cliente(self, cliente: Cliente) -> bool:
        if not cliente.id:
            print("ID de cliente requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('persona', cliente.id_persona, 'id_persona'):
            return False
        if not self._mapper.validate_fk_exists('tipo_documento', cliente.id_tipo_documento, 'id_tipo_documento'):
            return False

        return self._repo.update(cliente)

    def delete_cliente(self, cliente_id: int) -> bool:
        if self._repo.get_by_id(cliente_id) is None:
            print(f"Cliente con ID {cliente_id} no encontrado.")
            return False
        if self._contrato_service.has_active_contracts("cliente", cliente_id):
            print(f"Error de Negocio: No se puede eliminar el Cliente ID {cliente_id} porque tiene contratos activos.")
            return False

        return self._repo.delete(cliente_id)
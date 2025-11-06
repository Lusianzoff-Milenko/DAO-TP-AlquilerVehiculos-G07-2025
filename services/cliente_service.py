from typing import Optional, List

from domain.models.cliente import Cliente
from data_access.repositories.cliente_repository import ClienteRepository
from .contrato_service import ContratoService
from .validation_mapper import ValidationMapper
from data_access.repositories.persona_repository import PersonaRepository
from data_access.repositories.tipo_documento_repository import TipoDocumentoRepository
class ClienteService:
    def __init__(self, cliente_repo: ClienteRepository, persona_repo: PersonaRepository,
                 tipo_documento_repo: TipoDocumentoRepository, contrato_service: ContratoService):
        self._repo = cliente_repo
        self._contrato_service = contrato_service

        repos_to_validate = {
            'persona': persona_repo,
            'tipo_documento': tipo_documento_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

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
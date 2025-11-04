# python
# file: `application/services/contrato_service.py`
from typing import Optional, List
from domain.models.contrato import Contrato
from data_access.repositories.contrato_repository import ContratoRepository

# Assuming existence of repositories for foreign keys
from data_access.repositories.cliente_repository import ClienteRepository
from data_access.repositories.vehiculo_repository import VehiculoRepository
from data_access.repositories.metododepago_repository import MetodoDePagoRepository
from data_access.repositories.empleado_repository import EmpleadoRepository
from data_access.repositories.estado_repository import EstadoRepository
from services.estado_service import EstadoService
from services.validation_mapper import ValidationMapper


class ContratoService:
    def __init__(self, contrato_repo, cliente_repo, vehiculo_repo, metodo_pago_repo, empleado_repo, estado_repo):
        self._repo = contrato_repo

        # [MODIFICADO] Inicializamos el ValidationMapper
        repos_to_validate = {
            'cliente': cliente_repo,
            'vehiculo': vehiculo_repo,
            'metodo_pago': metodo_pago_repo,
            'empleado': empleado_repo,
            'estado': estado_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

    def create_contrato(self, contrato: Contrato) -> Optional[int]:
        # [MODIFICADO] Uso de ValidationMapper
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return None
        if not self._mapper.validate_fk_exists('vehiculo', contrato.id_vehiculo, 'id_vehiculo'): return None
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return None
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return None
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return None

        # ... (Lógica de Negocio: disponibilidad de vehículo) ...

        return self._repo.create(contrato)

    def get_contrato_by_id(self, contrato_id: int) -> Optional[Contrato]:
        return self._repo.get_by_id(contrato_id)

    def list_all_contratos(self) -> List[Contrato]:
        return self._repo.list_all()

    def update_contrato(self, contrato: Contrato) -> bool:
        if not contrato.id: return False

        # [MODIFICADO] Uso de ValidationMapper
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return False
        if not self._mapper.validate_fk_exists('vehiculo', contrato.id_vehiculo, 'id_vehiculo'): return False
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return False
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return False
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return False

        return self._repo.update(contrato)

    def get_active_contracts_by_entity(self, entity_type: str, entity_id: int) -> list:
        column_map = {
            "cliente": "id_cliente",
            "vehiculo": "id_vehiculo",
            "empleado": "id_empleado",
        }
        column_name = column_map.get(entity_type)

        if not column_name:
            return []

        try:
            active_contracts = [
                contrato
                for contrato in self._repo.list_all()
                if getattr(contrato, column_name) == entity_id and contrato.id_estado == self._estado_service.get_estado_by_name("Activo").id
            ]
            return active_contracts
        except Exception as e:
            print(f"Error al buscar contratos activos: {e}")
            return []

    def has_active_contracts(self, entity_type: str, entity_id: int) -> bool:
        return len(self.get_active_contracts_by_entity(entity_type, entity_id)) > 0
from typing import Optional, List
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from services.detalle_contrato_service import DetalleContratoService
from services.estado_service import EstadoService
from services.validation_mapper import ValidationMapper


class ContratoService:
    def __init__(self, contrato_repo, cliente_repo, vehiculo_repo, metodo_pago_repo, empleado_repo, estado_repo, estado_service: EstadoService, detalle_contrato_service: DetalleContratoService):
        self._repo = contrato_repo
        self._estado_service = estado_service
        repos_to_validate = {
            'cliente': cliente_repo,
            'vehiculo': vehiculo_repo,
            'metodo_pago': metodo_pago_repo,
            'empleado': empleado_repo,
            'estado': estado_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)
        self._detalle_service = detalle_contrato_service  # Inyectamos el servicio de detalle

    def create_contrato(self, contrato: Contrato, detalles_list: List[DetalleContrato]) -> Optional[int]:
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return None
        if not self._mapper.validate_fk_exists('vehiculo', contrato.id_vehiculo, 'id_vehiculo'): return None
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return None
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return None
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return None

        # ... (Lógica de Negocio: disponibilidad de vehículo) ...

        contrato_id = self._repo.create(contrato)

        if not contrato_id:
            print("Error: Falló la creación del contrato principal.")
            return None

            # 3. Creación de los Detalles (Orquestación)
        success = True
        for detalle in detalles_list:
            detalle.id_contrato = contrato_id

            # [CORRECCIÓN] Usar argumento nominal 'detalle=detalle'
            if not self._detalle_service.create_detalle_contrato(detalle=detalle):
                success = False
                break

        if not success:
            # Lógica de Compensación: Si un detalle falla, se debería intentar eliminar el contrato principal
            # o marcarlo como pendiente de corrección. Por simplicidad, solo mostramos el error.
            print(
                f"Error: Falló la creación de al menos un DetalleContrato. Se requiere compensación para Contrato ID {contrato_id}")
            return None  # Falla toda la operación

        return contrato_id



    def get_contrato_by_id(self, contrato_id: int) -> Optional[Contrato]:
        return self._repo.get_by_id(contrato_id)

    def list_all_contratos(self) -> List[Contrato]:
        return self._repo.list_all()

    def update_contrato(self, contrato: Contrato) -> bool:
        if not contrato.id: return False
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
                if getattr(contrato, column_name) == entity_id and contrato.id_estado == self._estado_service.get_estado_by_name("EN_CURSO").id
            ]
            return active_contracts
        except Exception as e:
            print(f"Error al buscar contratos activos: {e}")
            return []

    def has_active_contracts(self, entity_type: str, entity_id: int) -> bool:
        return len(self.get_active_contracts_by_entity(entity_type, entity_id)) > 0
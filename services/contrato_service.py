from typing import Optional, List

from data_access.repositories import ContratoRepository
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from services.detalle_contrato_service import DetalleContratoService
from services.estado_service import EstadoService
from services.validation_mapper import ValidationMapper


class ContratoService:
    def __init__(
        self,
        contrato_repo: ContratoRepository,
        estado_service: EstadoService,
        validation_mapper: ValidationMapper  # <-- Inyectamos el mapper
    ):
        self._repo = contrato_repo
        self._estado_service = estado_service
        self._mapper = validation_mapper  # <-- Asignación simple

    def create_contrato(self, contrato: Contrato) -> Optional[int]:
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return None
        print("valide el cliente correctamente")
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return None
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return None
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return None

        # ... (Lógica de Negocio: disponibilidad de vehículo) ...

        contrato_id = self._repo.create(contrato)

        print("soy el id del contrato creado:", contrato_id)

        if not contrato_id:
            print("Error: Falló la creación del contrato principal.")
            return None
        return contrato_id

    def crear_contrato_con_detalles(
            self,
            contrato: Contrato,
            detalles: List[DetalleContrato],
            detalles_service: DetalleContratoService
    ) -> Optional[int]:
        """
        Orquesta la creación del Contrato principal y sus detalles.
        :param detalles_service:
        :param contrato: La instancia de Contrato principal.
        :param detalles: Una lista de instancias de DetalleContrato.
        :return: El ID del Contrato creado, o None si hay un error.
        """
        # 1. Validaciones del Contrato principal (reutilizando tu lógica existente)
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return None
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return None
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return None
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return None

        # 2. Persistir el Contrato principal y obtener su ID
        # ASUMIMOS que self._repo.create() devuelve el ID (int) del nuevo contrato.
        nuevo_contrato_id = self._repo.create(contrato)

        if nuevo_contrato_id is None:
            print("Error: Falló la creación del contrato principal en el Repositorio.")
            return None

        print(f"Contrato principal creado con ID: {nuevo_contrato_id}")

        # 3. Iterar y persistir los Detalles
        for i, detalle in enumerate(detalles):
            # 🚨 LA CLAVE: Asignar la clave foránea (id_contrato)
            detalle.id_contrato = nuevo_contrato_id

            # 4. Crear el Detalle usando su propio Service (que se encarga de las F.K. de Vehiculo)
            detalle_id = detalles_service.create_detalle_contrato(detalle)

            if detalle_id is None:
                # ⚠️ IMPORTANTE: Fallo en la integridad. Si esto pasa, debemos hacer ROLLBACK.
                print(f"ERROR: Falló la creación del detalle {i + 1}. Ejecutando rollback...")
                # Implementación de Rollback manual:
                self._repo.delete(nuevo_contrato_id)
                print(f"Rollback completo: Contrato {nuevo_contrato_id} eliminado.")
                return None

        # 5. Éxito
        return nuevo_contrato_id

    def get_contrato_by_id(self, contrato_id: int) -> Optional[Contrato]:
        return self._repo.get_by_id(contrato_id)

    def list_all_contratos(self) -> List[Contrato]:
        return self._repo.list_all()

    def update_contrato(self, contrato: Contrato) -> bool:
        if not contrato.id: return False
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return False
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return False
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return False
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return False
        return self._repo.update(contrato)

    def get_active_contracts_by_entity(self, entity_type: str, entity_id: int) -> list:
        column_map = {
            "cliente": "id_cliente",
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
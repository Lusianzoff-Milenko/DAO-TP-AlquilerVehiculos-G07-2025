from datetime import timedelta, datetime
from typing import Optional, List

from domain.models.contrato import Contrato
from domain.models.estado import Estado
from domain.models.vehiculo import Vehiculo
from data_access.repositories.vehiculo_repository import VehiculoRepository
from services import DetalleContratoService, EstadoService, MantenimientoService
from services.contrato_service import ContratoService
from services.validation_mapper import ValidationMapper


class VehiculoService:
    def __init__(self,
                 vehiculo_repo: VehiculoRepository,
                 contrato_service: ContratoService,
                 detalle_contrato_service: DetalleContratoService,
                 estado_service: EstadoService,
                 mantenimiento_service: MantenimientoService,  # 🚨 Nueva inyección
                 mapper: ValidationMapper):

        self._repo = vehiculo_repo
        self._contrato_service = contrato_service
        self._detalle_contrato_service = detalle_contrato_service
        self._estado_service = estado_service
        self._mantenimiento_service = mantenimiento_service  # 🚨 Nuevo atributo
        self._mapper = mapper
        self._estados_vehiculo: List[Estado] = self._estado_service.get_estado_by_ambito(Vehiculo.__class__.__name__)

    def create_vehiculo(self, vehiculo: Vehiculo) -> Optional[int]:  # Adaptar a tu inyección de dependencias
        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return None
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return None
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return None

        return self._repo.create(vehiculo)

    def get_vehiculo_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        return self._repo.get_by_id(vehiculo_id)

    def list_all_vehiculos(self) -> List[Vehiculo]:
        return self._repo.list_all()

    def update_vehiculo(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.id:
            print("ID de vehículo requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return False
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return False
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return False

        return self._repo.update(vehiculo)

    def delete_vehiculo(self, vehiculo_id: int) -> bool | None:
        # Lógica de Negocio: Evitar eliminar si está en uso por Contratos/Mantenimientos/Inconvenientes
        active_contracts = self._contrato_service.get_active_contracts_by_entity('vehiculo', vehiculo_id)
        if active_contracts:
            print(f"No se puede eliminar el vehículo {vehiculo_id} porque tiene contratos activos.")
            return None

        return self._repo.delete(vehiculo_id)

    def _get_active_reservation_contract(self, vehiculo_id: int) -> Optional[Contrato]:
        all_contratos = self._contrato_service.list_all_contratos()
        for contrato in all_contratos:
            if contrato.id_estado == 2:
                detalles = self._detalle_contrato_service.list_detalles_by_contrato(contrato.id)
                if any(d.id_vehiculo == vehiculo_id for d in detalles):
                    return contrato
        return None

    def verificar_vencimiento_reserva(self, vehiculo_id: int, cancelacion_forzada: bool = False) -> bool:
        """
        Verifica si la reserva de un vehículo venció por plazo de seña o cancelación.
        Si aplica, ejecuta la transición a 'Disponible' a través del State.
        """
        vehiculo = self._repo.get_by_id(vehiculo_id)

        if vehiculo is None:
            return False

        if vehiculo.get_state().__class__.__name__ != 'Reservado':
            return False

        contrato = self._get_active_reservation_contract(vehiculo_id)

        # 1. Inyectamos la lista de estados inmediatamente después de cargar el vehículo
        vehiculo.estados_disponibles = self._estados_vehiculo

        # Manejo de Contrato no encontrado
        if contrato is None:
            print(
                f"Advertencia: Vehículo {vehiculo_id} en Reservado, pero no se encontró Contrato activo. Forzando Disponible.")
            vehiculo.get_state().reincorporar(razon="Error de datos: Contrato de reserva no encontrado.")
            self._repo.update(vehiculo)
            return True

        # Manejo de Cancelación forzada
        if cancelacion_forzada:
            vehiculo.get_state().reincorporar(razon="Reserva cancelada explícitamente.")
            self._repo.update(vehiculo)
            return True

        # -----------------------------------------------------------------
        # Lógica de Vencimiento de Plazo: Inicializamos la variable
        # -----------------------------------------------------------------

        fecha_retiro = contrato.fecha_hasta
        fecha_limite_sena = fecha_retiro.date() - timedelta(days=15)
        hoy = datetime.now().date()

        # Verificamos si el plazo ha vencido (hoy es mayor o igual al límite)
        if hoy >= fecha_limite_sena:

            # El plazo ha vencido. Comprobamos la seña.
            detalles = self._detalle_contrato_service.list_detalles_by_contrato(contrato.id)

            # Actualizamos la variable hay_sena dentro de este bloque
            hay_sena = any(d.monto > 0 for d in detalles)

            if hay_sena:
                # Si hay seña, la reserva se mantiene (retornamos False)
                return False

        else:
            # Aún hay tiempo para la seña. La reserva se mantiene (retornamos False)
            return False

        # -----------------------------------------------------------------
        # Decisión Final: Si el código llega aquí, significa que:
        # 1. El plazo venció (hoy >= fecha_limite_sena) Y
        # 2. hay_sena es False.
        # -----------------------------------------------------------------

        # Solo en este caso se procede a marcar como disponible
        if not hay_sena:
            razon = "Plazo de seña vencido sin pago confirmado."
            print(f"VENCIMIENTO: {razon}")

            vehiculo.get_state().reincorporar(razon=razon)

            self._repo.update(vehiculo)
            return True

        return False

    def enviar_a_mantenimiento_desde_revision(self,
                                              vehiculo_id: int,
                                              costo_estimado: float,
                                              descripcion_problema: str,
                                              id_empleado_inicia: int) -> Optional[int]:
        """
        Mueve un vehículo de 'EnRevision' a 'EnMantenimiento' y crea el registro de Mantenimiento
        en el estado 'en diagnostico'.

        Retorna el ID del registro de Mantenimiento creado o None si falla.
        """
        vehiculo = self._repo.get_by_id(vehiculo_id)
        if vehiculo is None:
            print(f"Error: Vehículo con ID {vehiculo_id} no encontrado.")
            return None

        # Inyectar la lista de estados para que el objeto Vehiculo funcione como State Machine
        vehiculo.estados_disponibles = self._estados_vehiculo

        # 1. Validación de Estado de Vehículo
        if vehiculo.get_state().__class__.__name__ != 'EnRevision':
            print(
                f"Error: El vehículo {vehiculo_id} está en {vehiculo.get_state().__class__.__name__}, no en EnRevision.")
            return None

        # 2. Transición del Estado del Vehículo
        try:
            # Esto llama a EnRevision.iniciar_mantenimiento(), que realiza la transición a EnMantenimiento()
            vehiculo.get_state().iniciar_mantenimiento()
        except Exception as e:
            # En caso de que la transición esté mal definida o no sea posible
            print(f"Error de transición del Vehículo {vehiculo_id}: {e}")
            return None

        # 3. Creación del Registro de Mantenimiento (Estado inicial: 'en diagnostico')
        mantenimiento_id = self._mantenimiento_service.iniciar_nuevo_mantenimiento(
            id_vehiculo=vehiculo_id,
            costo=costo_estimado,
            descripcion=descripcion_problema,
            id_empleado=id_empleado_inicia
        )

        # 4. Persistencia (si el registro de mantenimiento fue exitoso)
        if mantenimiento_id is not None:

            # 4a. Actualizar el id_estado en el modelo Vehiculo para la persistencia
            estado_mantenimiento_vehiculo = self._estado_service.get_estado_by_name_and_ambito('EnMantenimiento',
                                                                                               'Vehiculo')
            if estado_mantenimiento_vehiculo:
                vehiculo.id_estado = estado_mantenimiento_vehiculo.id

            # 4b. Persistir el nuevo estado del vehículo
            if self._repo.update(vehiculo):
                print(
                    f"ÉXITO: Vehículo {vehiculo_id} en Mantenimiento. Registro de mantenimiento ID: {mantenimiento_id}")
                return mantenimiento_id
            else:
                # Manejo de error de persistencia
                print(f"Error al guardar el nuevo estado del vehículo {vehiculo_id}.")
                return None
        else:
            # Error en la creación del Mantenimiento. En un sistema con transacciones,
            # se haría rollback del cambio de estado del Vehículo. Aquí solo imprimimos error.
            print("Error: Falló la creación del registro de Mantenimiento.")
            return None

    def get_all_vehiculos(self) -> List[Vehiculo]:
        return self._repo.list_all()
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from data_access.repositories import ContratoRepository
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from domain.models.estado import Estado
from services.detalle_contrato_service import DetalleContratoService
from services.estado_service import EstadoService
from services.validation_mapper import ValidationMapper

if TYPE_CHECKING:
    from services.vehiculo_service import VehiculoService


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
        self._estados_contrato: List[Estado] = self._estado_service.get_estado_by_ambito('Contrato')

    def create_contrato(self, contrato: Contrato) -> Optional[int]:
        if not self._mapper.validate_fk_exists('cliente', contrato.id_cliente, 'id_cliente'): return None
        print("valide el cliente correctamente")
        if not self._mapper.validate_fk_exists('metodo_pago', contrato.id_metodo_de_pago,
                                               'id_metodo_de_pago'): return None
        if not self._mapper.validate_fk_exists('empleado', contrato.id_empleado, 'id_empleado'): return None
        if not self._mapper.validate_fk_exists('estado', contrato.id_estado, 'id_estado'): return None
        # ... (Lógica de Negocio: disponibilidad de vehículo) ...
        contrato_id = self._repo.create(contrato)
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
        
        # Cargar contrato original para comparar fechas
        contrato_original = self._repo.get_by_id(contrato.id)
        if contrato_original is None:
            print(f"Error: Contrato con ID {contrato.id} no encontrado.")
            return False
        
        # Validar que no se modifiquen fechas si está EnCurso
        fechas_modificadas = (
            contrato.fecha_desde != contrato_original.fecha_desde or
            contrato.fecha_hasta != contrato_original.fecha_hasta
        )
        
        if fechas_modificadas:
            # Inyectar estados para validación
            contrato_original.estados_disponibles = self._estados_contrato
            if not contrato_original.get_state().puede_modificar_fechas():
                print(f"Error: No se pueden modificar fechas del contrato {contrato.id} en estado {contrato_original.get_state().__class__.__name__}.")
                return False
        
        # Validaciones FK
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

    def confirmar_pago_reserva(self, contrato: Contrato, monto: float,
                               vehiculo_service: 'VehiculoService',
                               detalle_service: DetalleContratoService) -> bool:
        if contrato is None:
            print(f"Error: Contrato no encontrado o inexistente.")
            return False
        
        # 2. Inyectar estados disponibles
        contrato.estados_disponibles = self._estados_contrato
        
        # 3. Validar estado actual
        estado_actual = contrato.get_state().__class__.__name__
        if estado_actual != 'EnReservado':
            print(f"Error: El contrato está en estado {estado_actual}, no en EnReservado.")
            return False
        
        # 4. Ejecutar transición usando State Pattern
        exito = contrato.get_state().tomar_pago(monto)
        if not exito:
            return False
        
        # 5. Obtener vehículos del contrato
        detalles = contrato.detalles_contrato
        vehiculos = [d.Vehiculo for d in detalles]
        for vehiculo in vehiculos:
            if vehiculo:
                vehiculo.estados_disponibles = vehiculo_service._estados_vehiculo
                estado_vehiculo = vehiculo.get_state().__class__.__name__
                
                if estado_vehiculo == 'Reservado':
                    # Transición: Reservado → Alquilado
                    vehiculo.get_state().retirar(contrato)
                    vehiculo_service.update_vehiculo(vehiculo)
                    print(f"Vehículo {vehiculo.id} transicionado a Alquilado.")
                else:
                    print(f"Advertencia: Vehículo {vehiculo.id} está en {estado_vehiculo}, no en Reservado.")
        
        # 7. Persistir el contrato
        if self._repo.update(contrato):
            print(f"Contrato {contrato.id} confirmado y pasado a EnCurso.")
            return True
        else:
            print(f"Error al persistir el contrato {contrato.id}.")
            return False

    def cancelar_contrato(self, contrato: Contrato, razon: str,
                         vehiculo_service: 'VehiculoService') -> bool:
        if contrato is None:
            print(f"Error: Contrato no encontrado o inexistente.")
            return False
        
        # 2. Inyectar estados disponibles
        contrato.estados_disponibles = self._estados_contrato
        
        # 3. Validar estado actual
        estado_actual = contrato.get_state().__class__.__name__
        if estado_actual != 'EnReservado':
            print(f"Error: Solo se pueden cancelar contratos en EnReservado. Estado actual: {estado_actual}")
            return False
        
        # 4. Ejecutar transición usando State Pattern
        exito = contrato.get_state().cancelar(razon)
        if not exito:
            return False
        
        # 5. Obtener vehículos del contrato
        detalles = contrato.detalles_contrato
        vehiculos = [d.Vehiculo for d in detalles]
        for vehiculo in vehiculos:
            if vehiculo:
                vehiculo.estados_disponibles = vehiculo_service._estados_vehiculo
                estado_vehiculo = vehiculo.get_state().__class__.__name__
                
                if estado_vehiculo == 'Reservado':
                    # Transición: Reservado → Disponible
                    vehiculo.get_state().reincorporar(razon=f"Contrato {contrato.id} cancelado: {razon}")
                    vehiculo_service.update_vehiculo(vehiculo)
                    print(f"Vehículo {vehiculo.id} devuelto a Disponible.")
                else:
                    print(f"Advertencia: Vehículo {vehiculo.id} está en {estado_vehiculo}, no en Reservado.")
        
        # 7. Persistir el contrato
        if self._repo.update(contrato):
            print(f"Contrato {contrato.id} cancelado exitosamente.")
            return True
        else:
            print(f"Error al persistir el contrato {contrato.id}.")
            return False

    def recibir_devolucion(self, contrato: Contrato, fecha_devolucion: datetime,
                          vehiculo_service: 'VehiculoService',
                          detalle_service: DetalleContratoService) -> tuple[bool, float]:
        # 1. Cargar el contrato
        contrato = self._repo.get_by_id(contrato.id)
        if contrato is None:
            print(f"Error: Contrato con ID {contrato.id} no encontrado.")
            return (False, 0.0)
        
        # 2. Inyectar estados disponibles
        contrato.estados_disponibles = self._estados_contrato
        
        # 3. Validar estado actual
        estado_actual = contrato.get_state().__class__.__name__
        if estado_actual != 'EnCurso':
            print(f"Error: Solo se pueden recibir devoluciones de contratos EnCurso. Estado actual: {estado_actual}")
            return (False, 0.0)
        
        # 4. Ejecutar transición usando State Pattern (retorna días de retraso)
        exito, dias_retraso = contrato.get_state().recibir_devolucion(fecha_devolucion)
        if not exito:
            return (False, 0.0)
        
        # 5. Calcular recargo (10% por día de retraso sobre el total del contrato)
        recargo = 0.0
        if dias_retraso > 0:
            # Obtener el monto total del contrato sumando detalles
            detalles = detalle_service.list_detalles_by_contrato(contrato.id)
            total_contrato = sum(d.monto for d in detalles)
            
            # Recargo: 10% por día
            recargo = total_contrato * 0.10 * dias_retraso
            print(f"Recargo por {int(dias_retraso)} día(s) de retraso: ${recargo:.2f}")
        
        # 6. Obtener vehículos del contrato
        detalles = detalle_service.list_detalles_by_contrato(contrato.id)
        vehiculos = [d.Vehiculo for d in detalles]
        
        # 7. Transicionar vehículos de Alquilado a Entregado
        for vehiculo in vehiculos:
            if vehiculo:
                if vehiculo.get_state().__class__.__name__ == 'Alquilado':
                    # Transición: Alquilado → Entregado
                    vehiculo.get_state().entregar()
                    vehiculo_service.update_vehiculo(vehiculo)
                    print(f"Vehículo {vehiculo.id} marcado como Entregado.")
                else:
                    print(f"Advertencia: Vehículo {vehiculo.id} está en {vehiculo.get_state().__class__.__name__}, no en Alquilado.")
        
        # 8. Persistir el contrato
        if self._repo.update(contrato):
            print(f"Contrato {contrato.id} finalizado y marcado como YaEntregado.")
            return (True, recargo)
        else:
            print(f"Error al persistir el contrato {contrato.id}.")
            return (False, 0.0)

    def puede_modificar_fechas_contrato(self, contrato: Contrato) -> bool:
        if contrato is None:
            print(f"Error: Contrato no encontrado o inexistente.")
            return False
        
        # Inyectar estados disponibles
        contrato.estados_disponibles = self._estados_contrato
        
        # Consultar al estado actual
        puede_modificar = contrato.get_state().puede_modificar_fechas()
        
        if not puede_modificar:
            print(f"No se pueden modificar fechas del contrato {contrato.id} en estado {contrato.get_state().__class__.__name__}.")
        
        return puede_modificar
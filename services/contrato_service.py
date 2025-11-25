from typing import List, Optional
from datetime import datetime

from domain.exceptions import DomainError
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from domain.models.vehiculo import Vehiculo
from domain.states.contrato.state import State as ContratoState
from data_access.repositories import ContratoRepository
from services.estado_service import EstadoService
from domain.states.vehiculo.state import State as VehiculoState


class ContratoService:
    def __init__(self, contrato_repo: ContratoRepository, estado_service: EstadoService):
        self._repo = contrato_repo
        self._estado_service = estado_service

    # --- Helpers de Inicialización de Estado ---

    def _init_contrato_state(self, contrato: Contrato):
        """Inicializa el State Pattern para un contrato recuperado de BD."""
        if contrato:
            contrato.estados_disponibles = self._estado_service.get_estado_by_ambito("Contrato")
            if contrato.Estado:
                contrato._state = ContratoState.from_entity(contrato.Estado)
            else:
                from domain.states.contrato.en_reservado import EnReservado
                contrato._state = EnReservado()
            contrato._state.context = contrato

    def _init_vehiculo_state(self, vehiculo: Vehiculo):
        """Inicializa el State Pattern para un vehículo recuperado de BD."""
        if vehiculo:
            # Inyectamos estados disponibles (necesario para transition_to)
            vehiculo.estados_disponibles = self._estado_service.get_estado_by_ambito("Vehiculo")

            # Inicializamos el estado basado en la entidad Estado cargada
            if vehiculo.Estado:
                vehiculo._state = VehiculoState.from_entity(vehiculo.Estado)
            else:
                # Fallback si no hay estado o lazy loading falló (aunque debería estar si usas el ORM bien)
                from domain.states.vehiculo.disponible import Disponible
                vehiculo._state = Disponible()

            vehiculo._state.context = vehiculo

    # --- Métodos Públicos ---

    def get_contrato_by_id(self, id: int) -> Optional[Contrato]:
        contrato = self._repo.get_by_id(id)
        self._init_contrato_state(contrato)
        return contrato

    def tomar_reserva(self, vehiculo: Vehiculo, cliente, empleado, metodo_pago, tiene_seguro: bool,
                      fecha_desde: datetime, fecha_hasta: datetime) -> Optional[int]:
        """
        Facade para preparar los datos y crear la reserva.
        """
        # 1. Construir objeto Contrato
        contrato = Contrato(
            id_cliente=cliente.id,
            id_empleado=empleado.id,
            id_metodo_de_pago=metodo_pago.id,
            tiene_seguro=tiene_seguro,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )

        # 2. Calcular monto
        dias = (fecha_hasta - fecha_desde).days
        if dias < 1: dias = 1
        monto_total = vehiculo.precio_base * dias

        # 3. Construir Detalle
        detalle = DetalleContrato(
            id_vehiculo=vehiculo.id,
            monto=monto_total,
            fecha_retiro=fecha_desde,
            fecha_entrega=fecha_hasta
        )

        print(f"Iniciando reserva para {vehiculo.patente}...")
        return self.crear_contrato_reserva(contrato, [detalle])

    def crear_contrato_reserva(self, contrato: Contrato, detalles: List[DetalleContrato]) -> Optional[int]:
        """
        Crea Contrato y Detalles, y actualiza el estado de los Vehículos.
        """
        session = self._repo.session
        try:
            # 1. Configurar estado inicial del Contrato ('EnReservado')
            est_reservado = self._estado_service.get_estado_by_name_and_ambito("EnReservado", "Contrato")
            contrato.id_estado = est_reservado.id

            # 2. Agregar contrato (flush para generar ID)
            session.add(contrato)
            session.flush()

            # 3. Procesar detalles
            for det in detalles:
                det.id_contrato = contrato.id
                session.add(det)

                # 4. Obtener y Bloquear Vehículo
                # Recuperamos el vehículo de la sesión actual para asegurar que estamos trabajando con el objeto persistente
                vehiculo = session.query(Vehiculo).get(det.id_vehiculo)

                # CRÍTICO: Inicializar el estado antes de usarlo
                self._init_vehiculo_state(vehiculo)

                # Ahora sí podemos usar la lógica del State Pattern si quisiéramos:
                # vehiculo.get_state().reservar(contrato)
                # (Esto lanzaría excepciones si no está disponible, lo cual es bueno)

                # Validación manual (alternativa robusta):
                if vehiculo.get_state().__class__.__name__ != "Disponible":
                    raise Exception(
                        f"El vehículo {vehiculo.patente} no está disponible (Estado: {vehiculo.get_state().__class__.__name__})")

                # Forzar cambio de estado a 'Reservado'
                est_v_reservado = self._estado_service.get_estado_by_name_and_ambito("Reservado", "Vehiculo")
                vehiculo.id_estado = est_v_reservado.id
                session.add(vehiculo)

            session.commit()
            print(f"Reserva creada exitosamente. Contrato ID: {contrato.id}")
            return contrato.id

        except DomainError as e:
            # Aquí capturas el mensaje "La reserva debe hacerse con al menos 3 días..."
            print(f"Validación de Negocio falló: {str(e)}")
            session.rollback()
            return None
        except Exception as e:
            print(f"Error crítico: {str(e)}")
            session.rollback()
            return None

    def confirmar_pago(self, contrato_id: int, monto: float) -> bool:
        """
        Registra el pago. Si es exitoso, pasa el contrato a 'EnCurso'
        y los vehículos a 'Alquilado'.
        """
        contrato = self.get_contrato_by_id(contrato_id)
        if not contrato: return False

        # Intentar transición del contrato
        if contrato.get_state().tomar_pago(monto):

            # Si el contrato pasó a EnCurso, movemos los vehículos a Alquilado
            est_v_alquilado = self._estado_service.get_estado_by_name_and_ambito("Alquilado", "Vehiculo")

            for detalle in contrato.detalles_contrato:
                vehiculo = detalle.Vehiculo  # SQLAlchemy relationship
                vehiculo.id_estado = est_v_alquilado.id
                # Aquí podríamos usar vehiculo.get_state().retirar() si quisiéramos ser puristas

            try:
                self._repo.update(contrato)  # Guarda contrato y vehículos cascada
                return True
            except Exception as e:
                print(f"Error al confirmar pago: {e}")
                self._repo.session.rollback()
                return False

        return False

    def finalizar_alquiler(self, contrato_id: int, fecha_devolucion: datetime) -> bool:
        """Recibe la devolución y cierra el contrato."""
        contrato = self.get_contrato_by_id(contrato_id)
        if not contrato: return False

        exito, recargo = contrato.get_state().recibir_devolucion(fecha_devolucion)
        if exito:
            # Marcar vehículos como 'Entregado' (pendiente de revisión)
            est_v_entregado = self._estado_service.get_estado_by_name_and_ambito("Entregado", "Vehiculo")

            for detalle in contrato.detalles_contrato:
                vehiculo = detalle.Vehiculo
                vehiculo.id_estado = est_v_entregado.id
                # Actualizar fecha real de entrega en el detalle
                detalle.fecha_entrega = fecha_devolucion

            self._repo.update(contrato)
            print(f"Contrato finalizado. Recargo calculado: ${recargo}")
            return True

        return False
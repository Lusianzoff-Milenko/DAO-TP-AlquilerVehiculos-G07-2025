from typing import List, Optional
from datetime import datetime

from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from domain.states.contrato.state import State as ContratoState
from data_access.repositories import ContratoRepository
from services.estado_service import EstadoService


class ContratoService:
    def __init__(self, contrato_repo: ContratoRepository, estado_service: EstadoService):
        self._repo = contrato_repo
        self._estado_service = estado_service

    def _init_contrato_state(self, contrato: Contrato):
        if contrato:
            contrato.estados_disponibles = self._estado_service.get_estado_by_ambito("Contrato")

            # AQUI EL CAMBIO: Usamos from_entity pasando el objeto Estado
            # SQLAlchemy lo carga automáticamente (lazy loading) o vía joinedload
            if contrato.Estado:
                contrato._state = ContratoState.from_entity(contrato.Estado)
            else:
                # Si es un objeto nuevo o falló la carga
                from domain.states.contrato.en_reservado import EnReservado
                contrato._state = EnReservado()

            contrato._state.context = contrato

    def get_contrato_by_id(self, id: int) -> Optional[Contrato]:
        contrato = self._repo.get_by_id(id)
        self._init_contrato_state(contrato)
        return contrato

    def crear_contrato_reserva(self, contrato: Contrato, detalles: List[DetalleContrato]) -> Optional[int]:
        """
        Crea un contrato en estado 'EnReservado' y reserva los vehículos asociados.
        Todo en una sola transacción.
        """
        session = self._repo.session
        try:
            # 1. Configurar estado inicial 'EnReservado'
            est_reservado = self._estado_service.get_estado_by_name_and_ambito("EnReservado", "Contrato")
            contrato.id_estado = est_reservado.id

            # 2. Agregar contrato (flush para obtener ID)
            session.add(contrato)
            session.flush()

            # 3. Procesar detalles y Vehículos
            for det in detalles:
                det.id_contrato = contrato.id
                session.add(det)

                # BLOQUEO DE VEHÍCULO:
                # Debemos marcar los vehículos como 'Reservados'
                # Accedemos al repositorio de vehículos a través de la sesión o relación si existiera
                from domain.models.vehiculo import Vehiculo
                vehiculo = session.query(Vehiculo).get(det.id_vehiculo)

                # Inicializar state del vehículo para usar la lógica
                # (Aquí simplificamos: forzamos el estado si está disponible)
                # Idealmente usaríamos vehiculo_service, pero para atomicidad lo hacemos aquí o inyectamos el servicio

                # Búsqueda de estado 'Reservado' para vehículo
                est_v_reservado = self._estado_service.get_estado_by_name_and_ambito("Reservado", "Vehiculo")

                # Validación simple: Si no está disponible, fallar transacción
                # (Asumimos ID 1 = Disponible, o consultamos el estado actual)
                est_v_disponible = self._estado_service.get_estado_by_name_and_ambito("Disponible", "Vehiculo")

                if vehiculo.id_estado != est_v_disponible.id:
                    raise Exception(f"El vehículo {vehiculo.patente} no está disponible para reservar.")

                vehiculo.id_estado = est_v_reservado.id
                session.add(vehiculo)  # Update

            session.commit()
            return contrato.id

        except Exception as e:
            print(f"Fallo al crear reserva: {e}")
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
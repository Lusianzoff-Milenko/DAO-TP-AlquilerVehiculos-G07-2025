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

    def _init_contrato_state(self, contrato: Contrato):
        if contrato:
            contrato.estados_disponibles = self._estado_service.get_estado_by_ambito("Contrato")
            if contrato.Estado:
                contrato._state = ContratoState.from_entity(contrato.Estado)
            else:
                from domain.states.contrato.en_reservado import EnReservado
                contrato._state = EnReservado()
            contrato._state.context = contrato

    def _init_vehiculo_state(self, vehiculo: Vehiculo):
        if vehiculo:
            vehiculo.estados_disponibles = self._estado_service.get_estado_by_ambito("Vehiculo")
            if vehiculo.Estado:
                vehiculo._state = VehiculoState.from_entity(vehiculo.Estado)
            else:
                from domain.states.vehiculo.disponible import Disponible
                vehiculo._state = Disponible()
            vehiculo._state.context = vehiculo

    def get_contrato_by_id(self, id: int) -> Optional[Contrato]:
        contrato = self._repo.get_by_id(id)
        self._init_contrato_state(contrato)
        return contrato

    def tomar_reserva(self, vehiculo: Vehiculo, cliente, empleado, metodo_pago, tiene_seguro: bool,
                      fecha_desde: datetime, fecha_hasta: datetime) -> Optional[int]:
        """
        Método Legacy/Facade: Crea una reserva por defecto.
        """
        # Buscar estado EnReservado
        est_reserva = self._estado_service.get_estado_by_name_and_ambito("EnReservado", "Contrato")

        contrato = Contrato(
            id_cliente=cliente.id,
            id_empleado=empleado.id,
            id_metodo_de_pago=metodo_pago.id,
            tiene_seguro=tiene_seguro,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            id_estado=est_reserva.id  # Asignar explícitamente
        )

        dias = (fecha_hasta - fecha_desde).days
        if dias < 1: dias = 1
        monto_total = vehiculo.precio_base * dias

        detalle = DetalleContrato(
            id_vehiculo=vehiculo.id,
            monto=monto_total,
            fecha_retiro=fecha_desde,
            fecha_entrega=fecha_hasta
        )

        return self.crear_contrato_reserva(contrato, [detalle])

    def crear_contrato_reserva(self, contrato: Contrato, detalles: List[DetalleContrato]) -> Optional[int]:
        """
        Guarda contrato y detalles. Gestiona el estado del vehículo según el estado del contrato.
        """
        session = self._repo.session
        try:
            # 1. Si el contrato no tiene estado, asignar EnReservado por defecto
            if not contrato.id_estado:
                est_def = self._estado_service.get_estado_by_name_and_ambito("EnReservado", "Contrato")
                contrato.id_estado = est_def.id

            # Determinar qué estado corresponde al vehículo según el contrato
            # Recuperamos el objeto Estado para chequear el nombre
            estado_contrato = session.query(self._estado_service._repo.model).get(contrato.id_estado)
            nombre_estado_contrato = estado_contrato.nombre if estado_contrato else "EnReservado"

            nombre_estado_vehiculo = "Reservado"  # Default
            if nombre_estado_contrato == "EnCurso":
                nombre_estado_vehiculo = "Alquilado"

            est_vehiculo_target = self._estado_service.get_estado_by_name_and_ambito(nombre_estado_vehiculo, "Vehiculo")
            if not est_vehiculo_target:
                raise Exception(f"Estado de vehículo '{nombre_estado_vehiculo}' no encontrado en BD")

            # 2. Guardar Contrato
            session.add(contrato)
            session.flush()

            # 3. Procesar detalles y actualizar vehículos
            for det in detalles:
                det.id_contrato = contrato.id
                session.add(det)

                # Obtener vehículo
                vehiculo = session.query(Vehiculo).get(det.id_vehiculo)
                self._init_vehiculo_state(vehiculo)

                # Validar disponibilidad (solo si no estamos editando un contrato existente)
                if vehiculo.get_state().__class__.__name__ != "Disponible":
                    # Permitir si es el mismo contrato (logica de update), aqui asumimos create nuevo
                    raise Exception(f"El vehículo {vehiculo.patente} no está disponible.")

                # Actualizar estado del vehículo
                vehiculo.id_estado = est_vehiculo_target.id
                session.add(vehiculo)

            session.commit()
            print(
                f"Contrato #{contrato.id} creado. Estado: {nombre_estado_contrato}. Vehículos pasaron a: {nombre_estado_vehiculo}")
            return contrato.id

        except Exception as e:
            print(f"Error creando contrato/reserva: {str(e)}")
            session.rollback()
            return None

    def confirmar_pago(self, contrato_id: int, monto: float) -> bool:
        contrato = self.get_contrato_by_id(contrato_id)
        if not contrato: return False

        if contrato.get_state().tomar_pago(monto):
            for detalle in contrato.detalles_contrato:
                vehiculo = detalle.Vehiculo
                vehiculo.get_state().retirar(contrato)
                self._repo.session.add(vehiculo)

            try:
                self._repo.update(contrato)
                return True
            except Exception as e:
                self._repo.session.rollback()
                print(f"Error confirmando pago: {e}")
                return False
        return False

    def finalizar_alquiler(self, contrato_id: int, fecha_devolucion: datetime) -> bool:
        contrato = self.get_contrato_by_id(contrato_id)
        if not contrato: return False

        exito, recargo_dias = contrato.get_state().recibir_devolucion(fecha_devolucion)
        if exito:
            # Mover vehículos a Entregado
            est_v_entregado = self._estado_service.get_estado_by_name_and_ambito("Entregado", "Vehiculo")

            for detalle in contrato.detalles_contrato:
                vehiculo = detalle.Vehiculo
                vehiculo.get_state().entregar()

                # --- AGREGAR ESTA LÍNEA ---
                # Esto fuerza a SQLAlchemy a registrar el cambio en el vehículo
                self._repo.session.add(vehiculo)
                # --------------------------

                # Actualizar fecha real
                detalle.fecha_entrega = fecha_devolucion

                if recargo_dias > 0:
                    costo_extra = (detalle.monto * 0.10) * recargo_dias
                    print(f"Aplicando recargo de ${costo_extra}")

            self._repo.update(contrato)
            return True

        return False


    def cancelar_contrato(self, contrato_id: int, razon: str) -> bool:
        """
        Cancela un contrato en estado EnReservado y libera los vehículos asociados.
        """
        contrato = self.get_contrato_by_id(contrato_id)
        if not contrato:
            print("Error: Contrato no encontrado.")
            return False

        # 1. Intentar cancelar el contrato (Transición de Estado)
        # Esto llama a domain/states/contrato/en_reservado.py -> cancelar()
        if contrato.get_state().cancelar(razon):

            # 2. Liberar los vehículos (Pasar de Reservado -> Disponible)
            for detalle in contrato.detalles_contrato:
                vehiculo = detalle.Vehiculo
                # Asegurar que el vehículo tenga su estado inicializado
                self._init_vehiculo_state(vehiculo)

                try:
                    # Llamamos a reincorporar en el estado del vehículo (ver domain/states/vehiculo/reservado.py)
                    vehiculo.get_state().reincorporar(f"Cancelación de contrato #{contrato.id}")
                    self._repo.session.add(vehiculo)  # Marcar para guardar
                except Exception as e:
                    print(f"Advertencia al liberar vehículo {vehiculo.patente}: {e}")

            # 3. Guardar cambios en la BD
            try:
                self._repo.update(contrato)
                return True
            except Exception as e:
                self._repo.session.rollback()
                print(f"Error guardando cancelación: {e}")
                return False

        return False
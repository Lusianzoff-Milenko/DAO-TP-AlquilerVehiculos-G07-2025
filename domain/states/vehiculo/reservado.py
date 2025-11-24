from datetime import datetime, timedelta
from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError, BusinessRuleError


class Reservado(State):

    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("El vehículo ya se encuentra reservado para otro cliente.")

    def retirar(self, contrato: Contrato) -> None:
        from domain.states.vehiculo.alquilado import Alquilado

        hoy = datetime.now().date()
        fecha_inicio = contrato.fecha_desde.date()

        # Regla: Retiro dentro de ventana válida (ej. fecha inicio + 5 días de tolerancia)
        limite_tolerancia = fecha_inicio + timedelta(days=5)

        if fecha_inicio <= hoy <= limite_tolerancia:
            print(f"LOG: Vehículo retirado de reserva por contrato {contrato.id}")
            self.context.transition_to(Alquilado())
        else:
            raise BusinessRuleError(
                f"No se puede retirar. Fecha actual {hoy} fuera del rango permitido ({fecha_inicio} - {limite_tolerancia}).")

    def entregar(self) -> None:
        raise StateTransitionError("Un vehículo reservado no ha salido, no puede ser entregado.")

    def mover_a_revision(self) -> None:
        raise StateTransitionError(
            "Un vehículo reservado no puede moverse a revisión (debe cancelarse la reserva primero).")

    def iniciar_mantenimiento(self) -> None:
        raise StateTransitionError(
            "No se puede iniciar mantenimiento en un vehículo reservado (cancele la reserva primero).")

    def reincorporar(self, razon: str) -> None:
        # Transición válida para cancelar reserva
        from domain.states.vehiculo.disponible import Disponible
        print(f"LOG: Reserva liberada. Razón: {razon}")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        raise StateTransitionError("No se puede sacar de servicio un vehículo reservado (cancele la reserva primero).")

    def marcar_no_devolucion(self) -> None:
        raise StateTransitionError("Imposible marcar no devolución: el vehículo no ha sido retirado.")
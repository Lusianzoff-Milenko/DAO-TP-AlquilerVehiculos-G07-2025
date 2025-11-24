from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError

class Entregado(State):
    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("El vehículo acaba de ser entregado y requiere revisión antes de reservarse.")

    def retirar(self, contrato: Contrato) -> None:
        raise StateTransitionError("El vehículo no está disponible para retiro (requiere revisión).")

    def entregar(self) -> None:
        print("LOG: El vehículo ya fue registrado como entregado.")

    def mover_a_revision(self) -> None:
        from domain.states.vehiculo.en_revision import EnRevision
        print("LOG: Vehículo enviado a revisión de rutina post-alquiler.")
        self.context.transition_to(EnRevision())

    def iniciar_mantenimiento(self) -> None:
        raise StateTransitionError("Debe pasar por revisión antes de ir a mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        raise StateTransitionError("Debe pasar por revisión antes de ser reincorporado.")

    def marcar_fuera_de_servicio(self) -> None:
        raise StateTransitionError("Debe pasar por revisión antes de marcarse fuera de servicio.")

    def marcar_no_devolucion(self) -> None:
        raise StateTransitionError("El vehículo ya fue entregado, no aplica 'no devolución'.")
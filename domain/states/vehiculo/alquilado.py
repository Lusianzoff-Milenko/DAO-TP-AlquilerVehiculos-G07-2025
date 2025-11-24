from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError

class Alquilado(State):

    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("El vehículo está alquilado y no puede recibir nuevas reservas superpuestas.")

    def retirar(self, contrato: Contrato) -> None:
        raise StateTransitionError("El vehículo ya fue retirado.")

    def entregar(self) -> None:
        from domain.states.vehiculo.entregado import Entregado
        print("LOG: Vehículo devuelto por el cliente.")
        self.context.transition_to(Entregado())

    def mover_a_revision(self) -> None:
        raise StateTransitionError("El vehículo está con el cliente, no puede ir a revisión.")

    def iniciar_mantenimiento(self) -> None:
        raise StateTransitionError("El vehículo está con el cliente, no puede ir a mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        raise StateTransitionError("Un vehículo alquilado no puede marcarse como disponible directamente (debe ser devuelto).")

    def marcar_fuera_de_servicio(self) -> None:
         raise StateTransitionError("Un vehículo alquilado no puede marcarse fuera de servicio (debe ser devuelto o declarado perdido).")

    def marcar_no_devolucion(self) -> None:
        from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
        print("LOG: ALERTA - Vehículo marcado como NO DEVUELTO/ROBADO.")
        self.context.transition_to(FueraDeServicio())
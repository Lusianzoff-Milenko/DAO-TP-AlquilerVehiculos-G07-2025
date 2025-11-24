from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError

class EnRevision(State):

    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo en revisión, no disponible para reservas.")

    def retirar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo en revisión, no puede ser retirado.")

    def entregar(self) -> None:
        raise StateTransitionError(f"El vehículo ya está en {self.__class__.__name__}.")

    def mover_a_revision(self) -> None:
        print("LOG: El vehículo ya se encuentra en revisión.")

    def iniciar_mantenimiento(self) -> None:
        from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
        print("LOG: Falla detectada en revisión. Enviando a taller.")
        self.context.transition_to(EnMantenimiento())

    def reincorporar(self, razon: str) -> None:
        from domain.states.vehiculo.disponible import Disponible
        print(f"LOG: Revisión OK. Vehículo reincorporado. Razón: {razon}")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
        print("LOG: Falla grave en revisión. Vehículo fuera de servicio.")
        self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        raise StateTransitionError("El vehículo está en taller, no aplica 'no devolución'.")
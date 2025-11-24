from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError

class FueraDeServicio(State):

    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo fuera de servicio (baja/inactivo).")

    def retirar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo fuera de servicio.")

    def entregar(self) -> None:
        raise StateTransitionError("Vehículo fuera de servicio.")

    def mover_a_revision(self) -> None:
         # Quizás quieras permitir esto para intentar recuperarlo
         raise StateTransitionError("Debe reincorporarse administrativamente antes de revisar.")

    def iniciar_mantenimiento(self) -> None:
        raise StateTransitionError("Vehículo fuera de servicio.")

    def reincorporar(self, razon: str) -> None:
        from domain.states.vehiculo.disponible import Disponible
        print(f"LOG: Vehículo reactivado administrativamente. Razón: {razon}")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        print("LOG: El vehículo ya está fuera de servicio.")

    def marcar_no_devolucion(self) -> None:
        print("LOG: Ya marcado como no disponible/fuera de servicio.")
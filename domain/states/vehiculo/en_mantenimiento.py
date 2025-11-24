from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError

class EnMantenimiento(State):

    def reservar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo en mantenimiento.")

    def retirar(self, contrato: Contrato) -> None:
        raise StateTransitionError("Vehículo en mantenimiento.")

    def entregar(self) -> None:
        raise StateTransitionError("Vehículo en mantenimiento.")

    def mover_a_revision(self) -> None:
        raise StateTransitionError("El vehículo ya está en proceso de reparación.")

    def iniciar_mantenimiento(self) -> None:
        print("LOG: El vehículo ya está en mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        from domain.states.vehiculo.disponible import Disponible
        print(f"LOG: Mantenimiento finalizado. Vehículo disponible: {razon}")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
        print("LOG: Reparación fallida o inviable. Vehículo dado de baja.")
        self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        raise StateTransitionError("No aplica.")
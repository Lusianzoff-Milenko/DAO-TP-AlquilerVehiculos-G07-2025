from domain.models.contrato import Contrato
from domain.states.vehiculo.disponible import Disponible
from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
from domain.states.vehiculo.state import State


class EnMantenimiento(State):

    def reservar(self, contrato: Contrato) -> None:
        print("El vehículo está en mantenimiento y no puede ser reservado.")

    def retirar(self, contrato: Contrato) -> None:
        print("El vehículo está en mantenimiento y no puede ser retirado.")

    def entregar(self) -> None:
        print("El vehículo está en mantenimiento y no puede ser entregado.")

    def mover_a_revision(self) -> None:
        print("El vehiculo ya fue revisado.")

    def iniciar_mantenimiento(self) -> None:
        print("El vehículo ya está en mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        print(f"Vehículo reincorporado: {razon}")
        self.context.transition_to(Disponible())  # Transición a Disponible

    def marcar_fuera_de_servicio(self) -> None:
        print("Vehículo marcado como fuera de servicio por falla de mantenimiento.")
        self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        print("El vehículo está en mantenimiento y no puede ser marcado como no devolución.")
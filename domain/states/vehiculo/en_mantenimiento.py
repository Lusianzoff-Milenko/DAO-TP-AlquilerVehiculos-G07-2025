from domain.models.contrato import Contrato
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
        pass

    def marcar_fuera_de_servicio(self) -> None:
        pass

    def marcar_no_devolucion(self) -> None:
        pass
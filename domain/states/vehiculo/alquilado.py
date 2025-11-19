from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State


class Alquilado(State):
    def marcar_disponible(self) -> None:
        pass

    def reservar(self, contrato: Contrato) -> None:
        pass

    def retirar(self, contrato: Contrato) -> None:
        pass

    def entregar(self) -> None:
        pass

    def mover_a_revision(self) -> None:
        pass

    def iniciar_mantenimiento(self) -> None:
        pass

    def reincorporar(self):
        pass

    def marcar_fuera_de_servicio(self) -> None:
        pass

    def marcar_no_devolucion(self) -> None:
        pass
from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State


class FueraDeServicio(State):

    def marcar_no_devolucion(self) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def marcar_fuera_de_servicio(self) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def reincorporar(self, razon: str) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def iniciar_mantenimiento(self) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def mover_a_revision(self) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def entregar(self) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def retirar(self, contrato: Contrato) -> None:
        print("El vehiculo se encuentra fuera de servicio.")

    def reservar(self, contrato: Contrato) -> None:
        print("El vehiculo se encuentra fuera de servicio.")
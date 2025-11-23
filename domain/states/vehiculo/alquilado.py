from domain.models.contrato import Contrato
from domain.states.vehiculo.entregado import Entregado
from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
from domain.states.vehiculo.state import State


class Alquilado(State):

    def reservar(self, contrato: Contrato) -> None:
        print("El vehiculo ya se encuentra alquilado, no puede ser reservado.")

    def retirar(self, contrato: Contrato) -> None:
        print("Un vehiculo ya se encuentra alquilado, no puede ser retirado nuevamente.")

    def entregar(self) -> None:
        print("El cliente ha devuelto el vehiculo alquilado.")
        self.context.transition_to(Entregado())

    def mover_a_revision(self) -> None:
        print("Un vehiculo alquilado no puede ser movido a revision directamente.")

    def iniciar_mantenimiento(self) -> None:
        print("Un vehiculo alquilado no puede ser enviado a mantenimiento directamente.")

    def reincorporar(self, razon: str) -> None:
        print("Un vehículo alquilado no puede ser marcado como disponible directamente.")

    def marcar_fuera_de_servicio(self) -> None:
        print("Un vehículo alquilado no puede ser marcado como fuera de servicio directamente.")

    def marcar_no_devolucion(self) -> None:
        print("El vehiculo no fue devuelto por el cliente.")
        self.context.transition_to(FueraDeServicio())
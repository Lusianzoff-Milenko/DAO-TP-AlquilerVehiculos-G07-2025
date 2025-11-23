from domain.models.contrato import Contrato
from domain.states.vehiculo.disponible import Disponible
from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
from domain.states.vehiculo.state import State


class EnRevision(State):

    def reservar(self, contrato: Contrato) -> None:
        print("El vehiculo no esta disponible para ser reservado.")

    def retirar(self, contrato: Contrato) -> None:
        print("El vehiculo no esta disponible para ser retirado.")

    def entregar(self) -> None:
        print("El vehiculo no puede ser entregado ya que esta " + self.__class__.__name__)

    def mover_a_revision(self) -> None:
        print("El vehiculo ya esta " + self.__class__.__name__)

    def iniciar_mantenimiento(self) -> None:
        print("Se detecto un problema durante la revision. El vehiculo sera enviado a mantenimiento.")
        self.context.transition_to(EnMantenimiento())

    def reincorporar(self, razon: str) -> None:
        print("El vehiculo ha sido reincorporado al servicio ya que esta en perfecto estado.")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        print("Se detecto un problema grave durante la revision. El vehiculo sera marcado como fuera de servicio.")
        self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        print("Un vehiculo en revision no puede ser marcado como no devolucion.")
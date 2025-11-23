from datetime import datetime, timedelta

from domain.models.contrato import Contrato
from domain.states.vehiculo.alquilado import Alquilado
from domain.states.vehiculo.disponible import Disponible
from domain.states.vehiculo.state import State


class Reservado(State):

    def reservar(self, contrato: Contrato) -> None:
        print("El vehiculo ya se encuentra reservado.")

    def retirar(self, contrato: Contrato) -> None:
        if contrato.fecha_desde.date() <= datetime.now().date() and contrato.fecha_hasta.hour <= datetime.now().hour and contrato.fecha_desde.date()-datetime.now().date() <= timedelta(5):
            print("El vehiculo fue retirado de la playa de estacionamienot por el cliente.")
            self.context.transition_to(Alquilado())
        else:
            print("No se puede retirar el vehiculo antes de la fecha de inicio de la reserva o fuera del plazo permitido.")

    def entregar(self) -> None:
        print("Un vehiculo reservado no puede ser entregado.")

    def mover_a_revision(self) -> None:
        print("Un vehiculo reservado no puede ser movido a revision.")

    def iniciar_mantenimiento(self) -> None:
        print("Un vehiculo reservado no puede ser enviado a mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        print(f"La reserva ha sido finalizada por la razón: {razon}")
        self.context.transition_to(Disponible())

    def marcar_fuera_de_servicio(self) -> None:
        print("Un vehiculo reservado no puede ser marcado como fuera de servicio.")

    def marcar_no_devolucion(self) -> None:
        print("Un vehiculo reservado no puede ser marcado como no devolucion.")
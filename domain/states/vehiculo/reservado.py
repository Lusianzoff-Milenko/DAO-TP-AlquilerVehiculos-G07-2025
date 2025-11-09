from typing import Optional

from domain.models.estado import Estado
from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.state import State


class Reservado(State):
    def set_estado(self, context: Optional[Vehiculo]) -> Estado:
        pass

    def handle1(self) -> None:
        print("El vehículo está reservado.")
        print("No puede ser reservado nuevamente hasta que se libere.")

    def handle2(self) -> None:
        print("El vehículo reservado ahora está siendo alquilado.")
        # Aquí podrías agregar la transición a otro estado, como Alquilado
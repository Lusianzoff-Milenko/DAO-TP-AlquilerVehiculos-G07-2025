from typing import Optional

from domain.models.estado import Estado
from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.state import State


class Alquilado(State):
    def set_estado(self, context: Optional[Vehiculo]) -> Estado:
        pass

    def handle1(self) -> None:
        print("El vehículo está alquilado.")
        print("No puede ser alquilado nuevamente hasta que se devuelva.")

    def handle2(self) -> None:
        print("El vehículo alquilado ha sido devuelto y ahora está disponible.")
        # Aquí podrías agregar la transición a otro estado, como Disponible
from typing import Optional

from domain.models.estado import Estado
from domain.models.vehiculo import Vehiculo
from services.containers.container import Container
from domain.states.vehiculo.reservado import Reservado
from domain.states.vehiculo.state import State


class Disponible(State):
    def handle1(self) -> None:
        print("El vehículo está disponible para alquiler.")
        print("Puede proceder a reservarlo o alquilarlo.")
        self.context.transition_to(Reservado())

    def handle2(self) -> None:
        print("El vehículo ya está disponible, no se puede realizar esta acción.")

    def set_estado(self, contexto: Optional[Vehiculo]) -> Estado:
        container = Container()
        estado_service = container.estado_service()
        estado = estado_service.get_estado_by_name_and_ambito(self.__class__.__name__, contexto.__class__.__name__)
        return estado
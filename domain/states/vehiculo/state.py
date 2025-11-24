from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union
from domain.models.contrato import Contrato
from domain.models.estado import Estado

if TYPE_CHECKING:
    from domain.models.vehiculo import Vehiculo

class State(ABC):

    _context: Optional['Vehiculo'] = None

    def create_state(self, estado_id: int) -> 'State':
        from domain.states.vehiculo.disponible import Disponible
        from domain.states.vehiculo.reservado import Reservado
        from domain.states.vehiculo.alquilado import Alquilado
        from domain.states.vehiculo.entregado import Entregado
        from domain.states.vehiculo.en_revision import EnRevision
        from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
        from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio

        if estado_id == 1:
            return Disponible()
        elif estado_id == 2:
            return Reservado()
        elif estado_id == 3:
            return Alquilado()
        elif estado_id == 4:
            return EnMantenimiento()
        elif estado_id == 5:
            return Entregado()
        elif estado_id == 6:
            return FueraDeServicio()
        elif estado_id == 7:
            return EnRevision()
        else:
            raise ValueError(f"Estado de Vehiculo con id {estado_id} no reconocido.")

    @property
    def context(self) -> Vehiculo:
        return self._context

    @context.setter
    def context(self, context: Vehiculo) -> None:
        self._context = context


    @abstractmethod
    def reservar(self, contrato: Contrato) -> None:
        pass

    @abstractmethod
    def retirar(self, contrato: Contrato) -> None:
        pass

    @abstractmethod
    def entregar(self) -> None:
        pass

    @abstractmethod
    def mover_a_revision(self) -> None:
        pass

    @abstractmethod
    def iniciar_mantenimiento(self) -> None:
        pass

    @abstractmethod
    def reincorporar(self, razon: str) -> None:
        pass

    @abstractmethod
    def marcar_fuera_de_servicio(self) -> None:
        pass

    @abstractmethod
    def marcar_no_devolucion(self) -> None:
        pass
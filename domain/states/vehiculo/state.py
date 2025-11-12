from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from domain.models.estado import Estado
if TYPE_CHECKING:
    from domain.models.vehiculo import Vehiculo

class State(ABC):

    _context: Optional['Vehiculo'] = None

    @staticmethod
    def create_state(id_estado: int) -> 'State':
        from domain.states.vehiculo.disponible import Disponible
        if id_estado == 1:
            return Disponible()
        else:
            raise ValueError(f"Estado with id {id_estado} not recognized.")

    @property
    def context(self) -> Vehiculo:
        return self._context

    @context.setter
    def context(self, context: Vehiculo) -> None:
        self._context = context

    @abstractmethod
    def handle1(self) -> None:
        pass

    @abstractmethod
    def handle2(self) -> None:
        pass

    @abstractmethod
    def set_estado(self, context: Vehiculo) -> Estado:
        pass
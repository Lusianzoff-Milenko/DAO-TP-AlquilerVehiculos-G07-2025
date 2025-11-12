from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
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
    def reservar(self) -> None:
        pass

    @abstractmethod
    def retirar(self) -> None:
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
    def reincorporar(self):
        pass

    @abstractmethod
    def marcar_fuera_de_servicio(self) -> None:
        pass

    @abstractmethod
    def marcar_no_devolucion(self) -> None:
        pass
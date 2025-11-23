from abc import ABC, abstractmethod
from typing import Optional
from domain.models.estado import Estado
from domain.models.mantenimiento import Mantenimiento
from domain.states.mantenimiento.en_diagnostico import EnDiagnostico


class State(ABC):

    _context: Optional['Mantenimiento'] = None

    @staticmethod
    def create_state(estado: Estado) -> 'State':
        if estado.id == 12:
            return EnDiagnostico()
        else:
            raise ValueError(f"Estado with id {estado.id} not recognized.")

    @property
    def context(self) -> Mantenimiento:
        return self._context

    @context.setter
    def context(self, context: Mantenimiento) -> None:
        self._context = context

    @abstractmethod
    def diagnosticar(self) -> None:
        pass

    @abstractmethod
    def reparar(self) -> None:
        pass

    @abstractmethod
    def finalizar_reparacion(self) -> None:
        pass

    @abstractmethod
    def marcar_irreparable(self) -> None:
        pass
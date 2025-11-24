from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.mantenimiento import Mantenimiento
    from domain.models.estado import Estado


class State(ABC):
    _context: Optional['Mantenimiento'] = None

    @property
    def context(self) -> 'Mantenimiento':
        return self._context

    @context.setter
    def context(self, context: 'Mantenimiento') -> None:
        self._context = context

    @staticmethod
    def from_entity(estado_entity: 'Estado') -> 'State':
        """
        Factory Method dinámico basado en el nombre del estado en BD.
        """
        # Importaciones locales
        from domain.states.mantenimiento.en_diagnostico import EnDiagnostico
        from domain.states.mantenimiento.en_reparacion import EnReparacion
        from domain.states.mantenimiento.reparado import Reparado
        from domain.states.mantenimiento.no_reparado import NoReparado

        if not estado_entity:
            return EnDiagnostico()  # Default lógico

        # Mapeo de nombres
        mapping = {
            "EnDiagnostico": EnDiagnostico,
            "EnReparacion": EnReparacion,
            "Reparado": Reparado,
            "NoReparado": NoReparado
        }

        state_class = mapping.get(estado_entity.nombre)

        if not state_class:
            print(f"Advertencia: Estado de Mantenimiento '{estado_entity.nombre}' no reconocido. Usando EnDiagnostico.")
            return EnDiagnostico()

        return state_class()

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
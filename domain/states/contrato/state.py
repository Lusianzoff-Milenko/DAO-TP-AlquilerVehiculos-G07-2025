from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.models.contrato import Contrato
    from domain.models.estado import Estado
    from datetime import datetime


class State(ABC):
    _context: Optional['Contrato'] = None

    @property
    def context(self) -> 'Contrato':
        return self._context

    @context.setter
    def context(self, context: 'Contrato') -> None:
        self._context = context

    @staticmethod
    def from_entity(estado_entity: 'Estado') -> 'State':
        """
        Factory Method dinámico.
        Recibe la entidad Estado de la BD y decide qué clase instanciar por su NOMBRE.
        """
        # Importaciones locales para evitar ciclos
        from domain.states.contrato.en_reservado import EnReservado
        from domain.states.contrato.en_curso import EnCurso
        from domain.states.contrato.ya_entregado import YaEntregado
        from domain.states.contrato.cancelado import Cancelado

        if not estado_entity:
            print("Advertencia: Contrato sin estado asignado. Usando EnReservado por defecto.")
            return EnReservado()

        # Mapeo exacto con los nombres en tu base de datos (tabla Estado)
        mapping = {
            "EnReservado": EnReservado,
            "EnCurso": EnCurso,
            "YaEntregado": YaEntregado,
            "Cancelado": Cancelado
        }

        state_class = mapping.get(estado_entity.nombre)

        if not state_class:
            print(f"Advertencia: Estado de Contrato '{estado_entity.nombre}' no reconocido. Usando EnReservado.")
            return EnReservado()

        return state_class()

    @abstractmethod
    def tomar_pago(self, monto: float) -> bool:
        pass

    @abstractmethod
    def cancelar(self, razon: str) -> bool:
        pass

    @abstractmethod
    def recibir_devolucion(self, fecha_devolucion: 'datetime') -> tuple[bool, float]:
        pass

    @abstractmethod
    def puede_modificar_fechas(self) -> bool:
        pass
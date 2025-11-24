from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from domain.models.contrato import Contrato

class State(ABC):
    """
    Clase base abstracta para los estados del Contrato.
    Define la interfaz común para todos los estados concretos.
    """

    _context: Optional['Contrato'] = None

    @staticmethod
    def create_state(id_estado: int) -> 'State':
        """
        Factory Method: crea instancias de estados concretos según el ID.
        
        IDs de estados de Contrato en BD:
        - 8: EnCurso
        - 9: EnReservado
        - 10: YaEntregado
        - 11: Cancelado
        """
        from domain.states.contrato.en_reservado import EnReservado
        from domain.states.contrato.en_curso import EnCurso
        from domain.states.contrato.ya_entregado import YaEntregado
        from domain.states.contrato.cancelado import Cancelado
        
        if id_estado == 9:  # EnReservado
            return EnReservado()
        elif id_estado == 8:  # EnCurso
            return EnCurso()
        elif id_estado == 10:  # YaEntregado
            return YaEntregado()
        elif id_estado == 11:  # Cancelado
            return Cancelado()
        else:
            raise ValueError(f"Estado de Contrato con id {id_estado} no reconocido.")

    @property
    def context(self) -> 'Contrato':
        """Obtiene el contrato asociado a este estado."""
        return self._context

    @context.setter
    def context(self, context: 'Contrato') -> None:
        """Establece el contrato asociado a este estado."""
        self._context = context

    @abstractmethod
    def tomar_pago(self, monto: float) -> bool:
        """
        Registra un pago y puede transicionar a EnCurso.
        Retorna True si la transición fue exitosa.
        """
        pass

    @abstractmethod
    def cancelar(self, razon: str) -> bool:
        """
        Cancela el contrato.
        Solo permitido desde EnReservado.
        Retorna True si la cancelación fue exitosa.
        """
        pass

    @abstractmethod
    def recibir_devolucion(self, fecha_devolucion: datetime) -> tuple[bool, float]:
        """
        Registra la devolución del vehículo.
        Solo permitido desde EnCurso.
        Retorna (éxito: bool, recargo_por_retraso: float).
        """
        pass

    @abstractmethod
    def puede_modificar_fechas(self) -> bool:
        """
        Indica si se pueden modificar las fechas del contrato en este estado.
        Solo permitido si NO está EnCurso.
        """
        pass

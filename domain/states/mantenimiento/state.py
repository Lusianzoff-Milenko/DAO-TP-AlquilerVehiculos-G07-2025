from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from domain.models.estado import Estado
if TYPE_CHECKING:
    from domain.models.mantenimiento import Mantenimiento



class State(ABC):

    _context: Optional['Mantenimiento'] = None


    def create_state(self, estado: Estado) -> 'State':
        # 🚨 MEJORA: Implementación completa para todos los estados de Mantenimiento
        # Las importaciones se realizan localmente aquí para evitar ciclos:
        from domain.states.mantenimiento.en_diagnostico import EnDiagnostico
        from domain.states.mantenimiento.en_reparacion import EnReparacion
        from domain.states.mantenimiento.reparado import Reparado
        from domain.states.mantenimiento.no_reparado import NoReparado

        # Mapa de nombres de estado (usando el nombre de la clase)
        STATE_CLASSES = {
            'EnDiagnostico': EnDiagnostico,
            'EnReparacion': EnReparacion,
            'Reparado': Reparado,
            'NoReparado': NoReparado,
        }

        StateClass = STATE_CLASSES.get(estado.nombre)

        if StateClass:
            return StateClass()
        else:
            # Tu implementación anterior solo manejaba el ID 12. Ahora usamos el nombre.
            raise ValueError(f"Estado de Mantenimiento con nombre '{estado.nombre}' no reconocido.")

    @property
    def context(self) -> 'Mantenimiento':  # 🚨 CORRECCIÓN CLAVE: Tipo de retorno como string literal
        return self._context

    @context.setter
    def context(self, context: 'Mantenimiento') -> None:
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
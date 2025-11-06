from abc import ABC, abstractmethod
from typing import Type
STATE_MAP = {}


class BaseState(ABC):
    """Interfaz base para todos los estados de cualquier máquina."""

    def __init__(self, context):
        self._context = context  # Referencia a la entidad (Contrato, Vehiculo, Mantenimiento)

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def get_name(self) -> str:
        """Devuelve el nombre del estado."""
        pass

    @abstractmethod
    def get_db_id(self) -> int:
        """Devuelve el ID de la tabla Estado correspondiente a este estado."""
        pass

    def _transition_to(self, new_state_class: Type['BaseState']):
        """Cambia el estado actual de la entidad (context) y actualiza el ID en el modelo."""
        self.context.state = new_state_class(self.context)

        # Actualizar la columna de estado en el modelo para la persistencia
        if hasattr(self.context, 'id_estado'):
            self.context.id_estado = self.context.state.get_db_id()
        elif hasattr(self.context, 'estadoActual'):  # Para Contrato
            self.context.estadoActual = self.context.state.get_db_id()

        print(
            f"Transición: {self.context.__class__.__name__} de {self.__class__.__name__} a {new_state_class.__name__}")

    # Método para manejo de errores de transición no válidas
    def _invalid_transition(self, action: str):
        print(f"Error: La acción '{action}' no es válida en el estado actual '{self.get_name()}'.")

# ---------------------------------------------------------------------------------------
# NOTA: Los métodos de transición (ej. tomar_pago) deben ser implementados en CADA clase
# de estado, llamando a _invalid_transition() si no están permitidos.
# ---------------------------------------------------------------------------------------
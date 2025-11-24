from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.models.vehiculo import Vehiculo
    from domain.models.contrato import Contrato
    from domain.models.estado import Estado  # Importamos el modelo Estado


class State(ABC):
    _context: Optional['Vehiculo'] = None

    @property
    def context(self) -> 'Vehiculo':
        return self._context

    @context.setter
    def context(self, context: 'Vehiculo') -> None:
        self._context = context

    @staticmethod
    def from_entity(estado_entity: 'Estado') -> 'State':
        """
        Factory Method dinámico.
        Recibe la entidad Estado de la BD y decide qué clase instanciar por su NOMBRE.
        """
        if not estado_entity:
            # Fallback por defecto si es None
            from domain.states.vehiculo.disponible import Disponible
            return Disponible()

        # Importaciones locales para evitar ciclos
        from domain.states.vehiculo.disponible import Disponible
        from domain.states.vehiculo.reservado import Reservado
        from domain.states.vehiculo.alquilado import Alquilado
        from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
        from domain.states.vehiculo.entregado import Entregado
        from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
        from domain.states.vehiculo.en_revision import EnRevision

        # Mapeo usando el NOMBRE exacto que tienes en la BD (tabla Estado)
        # Asegúrate que los keys coincidan con Estado.nombre
        mapping = {
            "Disponible": Disponible,
            "Reservado": Reservado,
            "Alquilado": Alquilado,
            "EnMantenimiento": EnMantenimiento,
            "Entregado": Entregado,
            "FueraDeServicio": FueraDeServicio,
            "EnRevision": EnRevision
        }

        # Buscamos por nombre. Si no existe, lanzamos error o devolvemos default.
        state_class = mapping.get(estado_entity.nombre)

        if not state_class:
            print(f"Advertencia: Estado '{estado_entity.nombre}' no tiene clase asociada. Usando Disponible.")
            return Disponible()

        return state_class()

    # ... (Métodos abstractos igual que antes) ...
    @abstractmethod
    def reservar(self, contrato: 'Contrato') -> None:
        pass

    @abstractmethod
    def retirar(self, contrato: 'Contrato') -> None:
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
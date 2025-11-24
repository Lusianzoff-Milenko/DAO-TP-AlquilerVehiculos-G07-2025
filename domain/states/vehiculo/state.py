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
        def create_state(estado_input: Union[Estado, int]) -> 'State':
            # 1. Importaciones locales para evitar dependencia circular
            from domain.states.vehiculo.disponible import Disponible
            from domain.states.vehiculo.reservado import Reservado
            from domain.states.vehiculo.alquilado import Alquilado
            from domain.states.vehiculo.entregado import Entregado
            from domain.states.vehiculo.en_revision import EnRevision
            from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
            from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio

            # 2. Mapa por ID (Esto evita consultar la BD y evita el bloqueo)
            # Asegúrate de que estos IDs coincidan con tu base de datos
            STATE_ID_MAP = {
                1: Disponible,
                2: Reservado,
                3: Alquilado,
                4: Entregado,
                5: EnRevision,
                6: EnMantenimiento,
                7: FueraDeServicio
            }

            # 3. Mapa por Nombre (si te llega el objeto Estado)
            STATE_NAME_MAP = {
                'Disponible': Disponible,
                'Reservado': Reservado,
                'Alquilado': Alquilado,
                'Entregado': Entregado,
                'EnRevision': EnRevision,
                'EnMantenimiento': EnMantenimiento,
                'FueraDeServicio': FueraDeServicio
            }

            StateClass = None

            # Lógica de selección
            if isinstance(estado_input, int):
                StateClass = STATE_ID_MAP.get(estado_input)
            elif hasattr(estado_input, 'nombre'):  # Es un objeto Estado
                StateClass = STATE_NAME_MAP.get(estado_input.nombre)

            if StateClass:
                return StateClass()

            # Fallback o error
            raise ValueError(f"Estado no reconocido para input: {estado_input}")

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
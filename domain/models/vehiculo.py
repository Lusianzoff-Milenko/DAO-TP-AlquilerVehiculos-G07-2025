from __future__ import annotations
from datetime import datetime
from typing import Any, List
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .mantenimiento import Mantenimiento
from ..states.vehiculo.state import State
from .estado import Estado
from .color import Color
from .modelo import Modelo


class Vehiculo(Base):
    __tablename__ = 'Vehiculo'
    __allow_unmapped__ = True
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo: int = Column(Integer, ForeignKey('Modelo.id'), nullable=False)
    patente: str = Column(String(20), nullable=False, unique=True)
    nro_chasis: str = Column(String(20), nullable=False, unique=True)
    id_color: int = Column(Integer, ForeignKey('Color.id'), nullable=False)
    anio_fabricacion: datetime = Column(DateTime, default=datetime.now(), name="año_fabricacion")
    precio_base: float = Column(Float, nullable=False)
    id_estado: int = Column(Integer, ForeignKey('Estado.id'), nullable=False)
    mantenimientos: List[Mantenimiento] = relationship("Mantenimiento", back_populates="Vehiculo")
    Estado = relationship(Estado)
    Modelo = relationship(Modelo)
    Color = relationship(Color)

    _state = None
    estados_disponibles: List[Estado] = []

    def get_state(self) -> State:
        return self._state

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)
        # 1. Asigna directamente el estado para inicializar el objeto.
        if self.id_estado is None:
            self.id_estado = 1
        state = State.create_state(self._state, int(self.id_estado))
        self._state = state
        if self._state:
            self._state.context = self
        # La lógica de transición no se ejecuta, por lo que no hay UPDATE de DB.

    def transition_to(self, state: State):
        if self._state.__class__ != state.__class__:
            print(f"Vehiculo: Transicionando al estado {type(state).__name__}")
            self._state = state
            self._state.context = self
            nuevo_estado_nombre = type(state).__name__
            encontrado = False
            for estado in self.estados_disponibles:
                if estado.nombre == nuevo_estado_nombre:
                    self.id_estado = estado.id
                    encontrado = True
                    break
            if not encontrado:
                print(f"¡ADVERTENCIA! ID de estado NO encontrado en la lista inyectada para: '{nuevo_estado_nombre}'.")

    def agregar_mantenimiento(self, mantenimiento: Mantenimiento) -> None:
        self.mantenimientos.append(mantenimiento)
        mantenimiento.Vehiculo = self

    def __str__(self) -> str:
        return f"Vehiculo [id={self.id}, modelo={Modelo.nombre}, patente={self.patente}, nro_chasis={self.nro_chasis}, color={Color.nombre}, año_fabricacion={self.anio_fabricacion.year}, precio_base={self.precio_base}, estado={self._state.__class__.__name__}]"


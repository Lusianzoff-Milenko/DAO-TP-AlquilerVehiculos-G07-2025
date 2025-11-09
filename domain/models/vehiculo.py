from __future__ import annotations
from datetime import datetime
from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
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

    Estado = relationship(Estado)
    Modelo = relationship(Modelo)
    Color = relationship(Color)

    _state = None

    def __init__(self, state: State, **kw: Any) -> None:
        super().__init__(**kw)
        self.transition_to(state)
        self.set_estado()

    def transition_to(self, state: State):
        print(f"Vehiculo: Transicionando al estado {type(state).__name__}")
        self._state = state
        self._state.context = self

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()


    def set_estado(self) -> None:
        estado: Estado = self._state.set_estado(self)
        self.id_estado = estado.id


    def __str__(self) -> str:
        return f"Vehiculo [id={self.id}, modelo={Modelo.nombre}, patente={self.patente}, nro_chasis={self.nro_chasis}, color={Color.nombre}, año_fabricacion={self.anio_fabricacion.year}, precio_base={self.precio_base}, estado={self._state.__class__.__name__}]"


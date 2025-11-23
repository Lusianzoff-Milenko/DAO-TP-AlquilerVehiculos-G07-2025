from datetime import datetime
from typing import List, Any

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from ..states.mantenimiento.state import State


class Mantenimiento(Base):
    __tablename__ = 'Mantenimiento'
    __allow_unmapped__ = True
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_vehiculo: int = Column(Integer, ForeignKey("Vehiculo.id"))
    costo: float = Column(Float, nullable=False)
    descripcion: str = Column(String, nullable=False)
    id_estado: int = Column(Integer, ForeignKey("Estado.id"))
    id_empleado: int = Column(Integer, ForeignKey("Empleado.id"))
    fecha_hora: datetime = Column(DateTime, nullable=False, default=datetime.now())

    Vehiculo = relationship("Vehiculo", back_populates="mantenimientos")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    _state = None
    estados_disponibles: List[Estado] = []

    def get_state(self) -> State:
        return self._state

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)
        # 1. Asigna directamente el estado para inicializar el objeto.
        if self.id_estado is None:
            self.id_estado = 1
        state = State.create_state(self.Estado)
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

    def get_last_maintenance(self):
        if self.fecha_hora.month >= datetime.now().month - 6:
            return self
        return None
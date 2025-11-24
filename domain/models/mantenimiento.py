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

        # 1. Estado por defecto (EnDiagnostico, ID 12 según populate)
        if self.id_estado is None:
            self.id_estado = 12

        # 2. Inicializar State
        from domain.states.mantenimiento.state import State as MantenimientoState

        if self.Estado:
            self._state = MantenimientoState.from_entity(self.Estado)
        else:
            from domain.states.mantenimiento.en_diagnostico import EnDiagnostico
            self._state = EnDiagnostico()

        if self._state:
            self._state.context = self

    def transition_to(self, state: State):
        if self._state.__class__ != state.__class__:
            print(f"Mantenimiento {self.id}: Transicionando a {type(state).__name__}")
            self._state = state
            self._state.context = self

            nuevo_nombre = type(state).__name__

            if self.estados_disponibles:
                for estado_bd in self.estados_disponibles:
                    if estado_bd.nombre.lower() == nuevo_nombre.lower():
                        self.id_estado = estado_bd.id
                        self.Estado = estado_bd
                        return

                print(f"¡ADVERTENCIA! No se encontró ID para estado '{nuevo_nombre}' en Mantenimiento.")

    def get_last_maintenance(self):
        if self.fecha_hora.month >= datetime.now().month - 6:
            return self
        return None
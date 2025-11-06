from datetime import datetime
from typing import Type

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from ..states.mantenimiento_states import MantenimientoBaseState, MANTENIMIENTO_STATE_MAPPING, \
    MantenimientoUnknownState, MantenimientoNew


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

    Vehiculo = relationship("Vehiculo")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    _state: MantenimientoBaseState = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cargamos el estado desde el ID de la DB o iniciamos en New
        if self.id_estado:
            self.state = self._load_state_from_id(self.id_estado)
        else:
            self.state = MantenimientoNew(self)

    # [CÓDIGO SOLICITADO]
    def _load_state_from_id(self, db_id: int) -> MantenimientoBaseState:
        """
        Mapea el ID de estado de la base de datos a la clase de estado correspondiente.
        """
        StateClass: Type[MantenimientoBaseState] = MANTENIMIENTO_STATE_MAPPING.get(db_id)

        if StateClass:
            return StateClass(self)
        else:
            print(
                f"ADVERTENCIA: ID de estado de Mantenimiento desconocido: {db_id}. Inicializando en MantenimientoUnknownState.")
            return MantenimientoUnknownState(self)

    @property
    def state(self) -> MantenimientoBaseState:
        return self._state

    @state.setter
    def state(self, new_state: MantenimientoBaseState):
        self._state = new_state
        # Persistir el nuevo ID de estado en el modelo
        self.id_estado = self._state.get_db_id()

        # ... (métodos de delegación) ...
from datetime import datetime
from typing import Type

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from ..states.vehiculo_states import VehiculoBaseState, VEHICULO_STATE_MAPPING, VehiculoUnknownState, VehiculoDisponible


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

    Estado = relationship('Estado')
    Modelo = relationship('Modelo')
    Color = relationship('Color')

    _state: VehiculoBaseState = None

    def __init__(self, **kwargs):
        # ... (inicialización y carga de estado) ...
        super().__init__(**kwargs)
        if self.id_estado:
            self.state = self._load_state_from_id(self.id_estado)
        else:
            self.state = VehiculoDisponible(self)

    # [CÓDIGO SOLICITADO]
    def _load_state_from_id(self, db_id: int) -> VehiculoBaseState:
        """
        Mapea el ID de estado de la base de datos a la clase de estado correspondiente.
        """
        StateClass: Type[VehiculoBaseState] = VEHICULO_STATE_MAPPING.get(db_id)

        if StateClass:
            return StateClass(self)
        else:
            print(f"ADVERTENCIA: ID de estado de Vehículo desconocido: {db_id}. Inicializando en VehiculoUnknownState.")
            return VehiculoUnknownState(self)

    @property
    def state(self) -> VehiculoBaseState:
        return self._state

    @state.setter
    def state(self, new_state: VehiculoBaseState):
        self._state = new_state
        # Persistir el nuevo ID de estado en el modelo
        self.id_estado = self._state.get_db_id()

        # ... (métodos de delegación) ...

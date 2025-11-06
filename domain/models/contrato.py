from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING, Type
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from ..states.contrato_states import ContratoBaseState, ContratoNew, CONTRATO_STATE_MAPPING, ContratoUnknownState

if TYPE_CHECKING:
    from .detalle_contrato import DetalleContrato

class Contrato(Base):
    __tablename__ = 'Contrato'
    __allow_unmapped__ = True
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente: int = Column(Integer, ForeignKey('Cliente.id'), nullable=False)
    id_vehiculo: int = Column(Integer, ForeignKey('Vehiculo.id'), nullable=False)
    fecha_desde: datetime = Column(DateTime, nullable=False, default=datetime.now())
    fecha_hasta: datetime = Column(DateTime, nullable=False)
    id_metodo_de_pago: int = Column(Integer, ForeignKey('MetodoDePago.id'), nullable=False, name='id_metodoDePago')
    id_empleado: int = Column(Integer, ForeignKey('Empleado.id'), nullable=False)
    id_estado: int = Column(Integer, ForeignKey('Estado.id'), nullable=False)
    tiene_seguro: bool = Column(Boolean, nullable=False)
    detalles_contrato: List[DetalleContrato] = relationship(
        "DetalleContrato",  # <--- Correcto: Apunta a la clase DetalleContrato
        back_populates="contrato",  # <--- Correcto: Apunta al atributo 'contrato' en DetalleContrato
        cascade="all, delete-orphan",
    )
    Cliente = relationship("Cliente")
    Vehiculo = relationship("Vehiculo")
    MetodoDePago = relationship("MetodoDePago")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    _state: ContratoBaseState = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # [MODIFICADO] Aquí cargamos el estado
        if self.id_estado:
            self.state = self._load_state_from_id(self.id_estado)
        else:
            self.state = ContratoNew(self)

    # [CÓDIGO SOLICITADO]
    def _load_state_from_id(self, db_id: int) -> ContratoBaseState:
        """
        Mapea el ID de estado de la base de datos a la clase de estado correspondiente.
        """
        # 1. Busca la clase de estado en el mapa
        StateClass: Type[ContratoBaseState] = CONTRATO_STATE_MAPPING.get(db_id)

        if StateClass:
            # 2. Si se encuentra, retorna una nueva instancia de esa clase
            return StateClass(self)
        else:
            # 3. Si no se encuentra, retorna el estado de error y lanza una advertencia
            print(f"ADVERTENCIA: ID de estado de Contrato desconocido: {db_id}. Inicializando en ContratoUnknownState.")
            return ContratoUnknownState(self)

    @property
    def state(self) -> ContratoBaseState:
        return self._state

    @state.setter
    def state(self, new_state: ContratoBaseState):
        self._state = new_state
        # Opcional: Persistir el nuevo ID de estado en el modelo
        self.id_estado = self._state.get_db_id()

        # ... (métodos de delegación: tomar_pago, tomar_retiro, etc.) ...
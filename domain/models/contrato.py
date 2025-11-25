from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING, Type, Any
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from ..states.contrato.state import State

if TYPE_CHECKING:
    from .detalle_contrato import DetalleContrato


class Contrato(Base):
    __tablename__ = 'Contrato'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente: int = Column(Integer, ForeignKey('Cliente.id'), nullable=False)
    fecha_desde: datetime = Column(DateTime, nullable=False, default=datetime.now())
    fecha_hasta: datetime = Column(DateTime, nullable=False)
    id_metodo_de_pago: int = Column(Integer, ForeignKey('MetodoDePago.id'), nullable=False, name='id_metodoDePago')
    id_empleado: int = Column(Integer, ForeignKey('Empleado.id'), nullable=False)
    id_estado: int = Column(Integer, ForeignKey('Estado.id'), nullable=False)
    tiene_seguro: bool = Column(Boolean, nullable=False)

    # --- CAMBIO: ELIMINAMOS LA DEFINICIÓN DE detalles_contrato AQUÍ ---
    # Se inyectará automáticamente desde DetalleContrato usando backref
    detalles_contrato: List[DetalleContrato]

    Cliente = relationship("Cliente")
    MetodoDePago = relationship("MetodoDePago")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    _state: State = None
    estados_disponibles: List = []

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)
        if self.id_estado is None: self.id_estado = 9
        from domain.states.contrato.state import State as ContratoState
        if self.Estado:
            self._state = ContratoState.from_entity(self.Estado)
        else:
            from domain.states.contrato.en_reservado import EnReservado
            self._state = EnReservado()
        if self._state: self._state.context = self

    def transition_to(self, state: State):
        if self._state.__class__ != state.__class__:
            self._state = state
            self._state.context = self
            # Lógica de actualización de estado en BD omitida para brevedad, pero mantenla si la tenías

    def get_state(self) -> State:
        return self._state

    def add_detalle(self, detalle) -> None:
        # Al usar backref, la lista se llama igual 'detalles_contrato'
        self.detalles_contrato.append(detalle)

    def __str__(self) -> str:
        estado_nombre = self._state.__class__.__name__ if self._state else "Sin estado"
        return (f"Contrato [id={self.id}, cliente_id={self.id_cliente}, "
                f"fecha_desde={self.fecha_desde}, fecha_hasta={self.fecha_hasta}, "
                f"estado={estado_nombre}]")
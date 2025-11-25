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
    detalles_contrato: List[DetalleContrato] = relationship(
        "DetalleContrato",  # <--- Correcto: Apunta a la clase DetalleContrato
        back_populates="contrato",  # <--- Correcto: Apunta al atributo 'contrato' en DetalleContrato
        cascade="all, delete-orphan",
        uselist=True
    )
    Cliente = relationship("Cliente")
    MetodoDePago = relationship("MetodoDePago")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    # Atributos del State Pattern
    _state: State = None
    estados_disponibles: List[type[Estado]] = []

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)

        # 1. Estado por defecto (EnReservado, ID 9)
        if self.id_estado is None:
            self.id_estado = 9

        # 2. Inicializar State
        from domain.states.contrato.state import State as ContratoState

        # Si SQLAlchemy ya cargó la relación Estado, usamos la factoría dinámica
        if self.Estado:
            self._state = ContratoState.from_entity(self.Estado)
        else:
            # Si es objeto nuevo o lazy loading no activo, usamos default
            from domain.states.contrato.en_reservado import EnReservado
            self._state = EnReservado()

        if self._state:
            self._state.context = self

    def transition_to(self, state: State):
        """
        Cambia el estado y actualiza el modelo para persistencia.
        """
        if self._state.__class__ != state.__class__:
            print(f"Contrato {self.id}: Transicionando a {type(state).__name__}")
            self._state = state
            self._state.context = self

            nuevo_nombre = type(state).__name__

            # Actualizar FK y Relación buscando en la lista inyectada
            if self.estados_disponibles:
                for estado_bd in self.estados_disponibles:
                    if estado_bd.nombre.lower() == nuevo_nombre.lower():
                        self.id_estado = estado_bd.id
                        self.Estado = estado_bd
                        return

                print(f"¡ADVERTENCIA! No se encontró ID para estado '{nuevo_nombre}' en Contrato.")

    def get_state(self) -> State:
        """Obtiene el estado actual del contrato."""
        return self._state

    def get_cliente(self):
        """Obtiene el cliente asociado al contrato."""
        return self.Cliente

    def get_empleado(self):
        """Obtiene el empleado asociado al contrato."""
        return self.Empleado

    def add_detalle(self, detalle: DetalleContrato) -> None:
        """Agrega un detalle al contrato."""
        self.detalles_contrato.append(detalle)
        detalle.id_contrato = self.id

    def __str__(self) -> str:
        estado_nombre = self._state.__class__.__name__ if self._state else "Sin estado"
        return (f"Contrato [id={self.id}, cliente_id={self.id_cliente}, "
                f"fecha_desde={self.fecha_desde}, fecha_hasta={self.fecha_hasta}, "
                f"estado={estado_nombre}]")
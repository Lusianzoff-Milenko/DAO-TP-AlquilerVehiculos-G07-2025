from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING, Type, Any
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from ..states.contrato.state import State
from .estado import Estado

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
    )
    Cliente = relationship("Cliente")
    MetodoDePago = relationship("MetodoDePago")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")

    # Atributos del State Pattern
    _state: State = None
    estados_disponibles: List[Estado] = []

    def __init__(self, **kw: Any) -> None:
        """
        Inicializa el contrato y establece su estado inicial.
        Si no se especifica id_estado, se inicializa como EnReservado (id=9).
        """
        super().__init__(**kw)

        # Estado por defecto: EnReservado (9)
        if self.id_estado is None:
            self.id_estado = 9

        # Crear instancia del estado usando Factory Method
        state = State.create_state(self.id_estado)
        self._state = state
        if self._state:
            self._state.context = self

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

    def transition_to(self, state: State):
        """
        Realiza la transición a un nuevo estado.
        Actualiza tanto el objeto State en memoria como el id_estado en BD.
        """
        if self._state.__class__ != state.__class__:
            print(f"Contrato: Transicionando al estado {type(state).__name__}")
            self._state = state
            self._state.context = self
            
            # Buscar el ID correspondiente en estados_disponibles
            nuevo_estado_nombre = type(state).__name__
            encontrado = False
            for estado in self.estados_disponibles:
                if estado.nombre == nuevo_estado_nombre:
                    self.id_estado = estado.id
                    encontrado = True
                    break
            
            if not encontrado:
                print(f"¡ADVERTENCIA! ID de estado NO encontrado en la lista inyectada para: '{nuevo_estado_nombre}'.")

    def __str__(self) -> str:
        estado_nombre = self._state.__class__.__name__ if self._state else "Sin estado"
        return (f"Contrato [id={self.id}, cliente_id={self.id_cliente}, "
                f"fecha_desde={self.fecha_desde}, fecha_hasta={self.fecha_hasta}, "
                f"estado={estado_nombre}]")
from __future__ import annotations

import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base

if TYPE_CHECKING:
    from .detalle_contrato import DetalleContrato

class Contrato(Base):
    __tablename__ = 'Contrato'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente: int = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    id_vehiculo: int = Column(Integer, ForeignKey('vehiculo.id'), nullable=False)
    fecha_desde: DateTime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    fecha_hasta: DateTime = Column(DateTime, nullable=False)
    id_metodo_de_pago: int = Column(Integer, ForeignKey('metodo_pago.id'), nullable=False, name='id_metodoDePago')
    id_empleado: int = Column(Integer, ForeignKey('empleado.id'), nullable=False)
    id_estado: int = Column(Integer, ForeignKey('estado.id'), nullable=False)
    tiene_seguro: bool = Column(Boolean, nullable=False)
    detalles_contrato: List[DetalleContrato] = relationship(
        "DetalleContrato",
        back_populates="contrato",
        cascade="all, delete-orphan",
    )
    cliente = relationship("Cliente")
    vehiculo = relationship("Vehiculo")
    metodo_pago = relationship("MetodoDePago")
    estado = relationship("Estado")
    empleado = relationship("Empleado")

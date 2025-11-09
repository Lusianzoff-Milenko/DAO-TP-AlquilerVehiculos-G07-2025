from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING, Type
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base

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
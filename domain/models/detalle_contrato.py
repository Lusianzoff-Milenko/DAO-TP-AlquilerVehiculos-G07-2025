from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, backref
from .base import Base

class DetalleContrato(Base):
    __tablename__ = 'DetalleContrato'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_contrato: int = Column(Integer, ForeignKey('Contrato.id'), nullable=False)
    id_vehiculo: int = Column(Integer, ForeignKey('Vehiculo.id'), nullable=False)
    monto: float = Column(Float, nullable=False)
    fecha_entrega: datetime = Column(DateTime, nullable=False)
    fecha_retiro: datetime = Column(DateTime, nullable=False, default=datetime.now())

    # --- SOLUCIÓN MAGICA: BACKREF ---
    # Esto crea automáticamente la propiedad 'detalles_contrato' en la clase Contrato
    # como una LISTA (uselist=True).
    contrato = relationship(
        "Contrato",
        backref=backref("detalles_contrato", uselist=True, cascade="all, delete-orphan")
    )

    Vehiculo = relationship("Vehiculo")
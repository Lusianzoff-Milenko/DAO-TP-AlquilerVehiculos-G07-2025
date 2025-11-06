from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class DetalleContrato(Base):
    __tablename__ = 'DetalleContrato'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_contrato: int = Column(Integer, ForeignKey('Contrato.id'), nullable=False)
    monto: float = Column(Float, nullable=False)
    fecha_entrega: datetime = Column(DateTime, nullable=False)
    fecha_retiro: datetime = Column(DateTime, nullable=False, default=datetime.now())
    contrato = relationship("Contrato", back_populates="detalles_contrato")
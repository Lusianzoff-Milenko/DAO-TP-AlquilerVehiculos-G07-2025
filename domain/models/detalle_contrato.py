import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class DetalleContrato(Base):
    __tablename__ = 'DetalleContrato'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_contrato: int = Column(Integer, ForeignKey('contrato.id'), nullable=False)
    monto: float = Column(Float, nullable=False)
    fecha_entrega: DateTime = Column(DateTime, nullable=False)
    fecha_retiro: DateTime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    contrato = relationship("Contrato", back_populates="DetalleContrato")
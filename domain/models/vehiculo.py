import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Vehiculo(Base):
    __tablename__ = 'Vehiculo'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo: int = Column(Integer, ForeignKey('modelo.id'), nullable=False)
    patente: str = Column(String(20), nullable=False, unique=True)
    nro_chasis: str = Column(String(20), nullable=False, unique=True)
    id_color: int = Column(Integer, ForeignKey('color.id'), nullable=False)
    anio_fabricacion: DateTime = Column(DateTime, default=datetime.datetime.now(), name="año_fabricacion")
    precio_base: float = Column(Float, nullable=False)
    id_estado: int = Column(Integer, ForeignKey('estado.id'), nullable=False)

    estado = relationship('Estado')
    modelo = relationship('Modelo')
    color = relationship('Color')

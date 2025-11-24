from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .marca import Marca



class Modelo(Base):
    __tablename__ = 'Modelo'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False, unique=True)
    id_marca: int = Column(Integer, ForeignKey('Marca.id'), nullable=False)
    cantidad_pasajeros: int = Column(Integer, nullable=False)
    cantidad_puertas: int = Column(Integer, nullable=False)
    motor: str = Column(String(50), nullable=False)
    anio_lanzamiento: int = Column(Integer, nullable=False, name="año_lanzamiento")
    Marca = relationship(Marca)
from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base



class Modelo(Base):
    __tablename__ = 'Modelo'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False, unique=True)
    id_marca: Integer = Column(Integer, ForeignKey('marca.id'), nullable=False)
    cantidad_pasajeros: int = Column(Integer, nullable=False)
    cantidad_puertas: int = Column(Integer, nullable=False)
    motor: str = Column(String(50), nullable=False)
    anio_lanzamiento: DateTime = Column(String, nullable=False, name="año_lanzamiento")
    marca = relationship('Marca')
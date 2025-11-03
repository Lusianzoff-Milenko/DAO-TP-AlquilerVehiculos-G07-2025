from datetime import datetime

from sqlalchemy import Column, Integer, String,DateTime
from .base import Base

class Persona(Base):
    __tablename__ = 'persona'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False)
    apellido: str = Column(String(50), nullable=False)
    telefono: str = Column(String(50), nullable=False)
    mail: str = Column(String(100), nullable=False)
    direccion: str = Column(String(100), nullable=False)
    fecha_nacimiento: datetime = Column(DateTime, nullable=False)
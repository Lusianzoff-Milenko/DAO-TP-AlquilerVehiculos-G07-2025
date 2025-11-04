from datetime import date

from sqlalchemy import Column, Integer, String, Date
from .base import Base

class Persona(Base):
    __tablename__ = 'persona'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False)
    apellido: str = Column(String(50), nullable=False)
    telefono: str = Column(String(50), nullable=False)
    mail: str = Column(String(100), nullable=False)
    direccion: str = Column(String(100), nullable=False)
    fecha_nacimiento: date = Column(Date, nullable=False)
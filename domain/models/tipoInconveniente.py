from sqlalchemy import Column, Integer, String
from .base import Base



class TipoInconveniente(Base):
    __tablename__ = 'TipoInconveniente'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False, unique=True)
    descripcion: str = Column(String(500), nullable=False)
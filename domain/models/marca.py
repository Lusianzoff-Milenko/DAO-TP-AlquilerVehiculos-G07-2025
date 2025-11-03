from sqlalchemy import Column, Integer, String
from .base import Base


class Marca(Base):
    __tablename__ = 'Marca'
    id : int = Column(Integer, primary_key=True, autoincrement=True)
    nombre : str = Column(String(20), nullable=False, unique=True)
    descripcion : str = Column(String(255), nullable=False)
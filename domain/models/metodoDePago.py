from sqlalchemy import Column, Integer, String
from .base import Base


class MetodoDePago(Base):
    __tablename__ = 'MetodoDePago'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False, unique=True)
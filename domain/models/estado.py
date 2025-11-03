from sqlalchemy import Column, Integer, String
from .base import Base


class Estado(Base):
    __tablename__ = 'Estado'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), unique=True, nullable=False)

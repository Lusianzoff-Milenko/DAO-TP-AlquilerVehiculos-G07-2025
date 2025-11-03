from sqlalchemy import Column, Integer, String
from .base import Base

class Color(Base):
    __tablename__ = "Color"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False, unique=True)



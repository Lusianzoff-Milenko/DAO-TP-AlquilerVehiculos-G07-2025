from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FotoXModelo(Base):
    __tablename__ = "FotoXModelo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo:int = Column(Integer, ForeignKey("Modelo.id"), nullable=False)
    id_color:int = Column(Integer, ForeignKey("Color.id"), nullable=True)
    foto_path:str = Column(String, nullable=False)
    anio_fabricacion:int = Column(Integer, nullable=True, name="año_fabricacion")
    Modelo = relationship("Modelo")
    Color = relationship("Color")
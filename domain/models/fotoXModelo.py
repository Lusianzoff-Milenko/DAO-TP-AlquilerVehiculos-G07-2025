from __future__ import annotations


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class FotoXModelo(Base):
    __tablename__ = "FotoXModelo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo = Column(Integer, ForeignKey("modelo.id"), nullable=False)
    id_color = Column(Integer, ForeignKey("color.id"), nullable=True)
    foto_path = Column(String, nullable=False)
    anio_fabricacion = Column(Integer, nullable=True, name="año_fabricacion")
    modelo = relationship("Modelo", back_populates="fotos")
    color = relationship("Color")
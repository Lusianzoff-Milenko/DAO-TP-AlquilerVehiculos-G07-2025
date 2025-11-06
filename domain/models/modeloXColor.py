from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ModeloXColor(Base):
    __tablename__ = 'ModeloXColor'
    id_modelo: int = Column(Integer, ForeignKey('Modelo.id'), primary_key=True)
    id_color: int = Column(Integer, ForeignKey('Color.id'), primary_key=True)

    Modelo = relationship("Modelo")
    Color = relationship("Color")
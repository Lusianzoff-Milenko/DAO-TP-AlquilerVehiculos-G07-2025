from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Cliente(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    documento = Column(String(50), nullable=False)
    id_tipo_documento = Column(Integer, ForeignKey('tipo_documento.id'), nullable=False)
    id_persona = Column(Integer, ForeignKey('persona.id'), nullable=False)
    tipo_documento = relationship('TipoDocumento')
    persona = relationship('Persona')

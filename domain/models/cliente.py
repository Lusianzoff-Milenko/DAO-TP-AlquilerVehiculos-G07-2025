from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Cliente(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    documento = Column(String(50), nullable=False)
    id_tipo_documento = Column(Integer, ForeignKey('TipoDocumento.id'), nullable=False)
    id_persona = Column(Integer, ForeignKey('Persona.id'), nullable=False)
    TipoDocumento = relationship("TipoDocumento",
                                  primaryjoin="TipoDocumento.id == Cliente.id_tipo_documento")  # SQLAlchemy lo infiere por id_tipo_documento
    persona = relationship('Persona')

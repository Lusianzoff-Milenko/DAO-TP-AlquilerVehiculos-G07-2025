from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class Inconveniente(Base):
    __tablename__ = 'RegistroInconveniente'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nombre: str = Column(String(50), nullable=False)
    descripcion: str = Column(String(255), nullable=True)
    id_tipo_inconveniente: int = Column(Integer, ForeignKey('tipo_inconveniente.id'), name="id_tipo_inconveniente")
    costo: float = Column(Float, nullable=True)
    id_contrato: int = Column(Integer, ForeignKey('contrato.id'))
    id_estado: int = Column(Integer, ForeignKey('estado.id'))

    tipo_inconveniente = relationship("TipoInconveniente")
    contrato = relationship("Contrato", back_populates="inconvenientes")
    estado = relationship("Estado")
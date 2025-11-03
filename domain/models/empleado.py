import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Empleado(Base):
    __tablename__ = 'Empleado'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo_puesto: int = Column(Integer, ForeignKey("tipo_puesto.id"))
    id_persona: int = Column(Integer, ForeignKey("persona.id"))
    fecha_ingreso: DateTime = Column(DateTime, default=datetime.datetime.now)
    fecha_egreso: DateTime = Column(DateTime)
    tipo_puesto = relationship("TipoPuesto")
    persona = relationship("Persona")

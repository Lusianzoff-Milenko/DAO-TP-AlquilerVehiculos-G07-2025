from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Empleado(Base):
    __tablename__ = 'Empleado'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo_puesto: int = Column(Integer, ForeignKey("TipoPuesto.id"))
    id_persona: int = Column(Integer, ForeignKey("Persona.id"))
    fecha_ingreso: datetime = Column(DateTime, default=datetime.now)
    fecha_egreso: datetime = Column(DateTime)
    TipoPuesto = relationship("TipoPuesto")
    Persona = relationship("Persona",
                                  primaryjoin="Persona.id == Empleado.id_persona")

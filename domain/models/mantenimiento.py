from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Mantenimiento(Base):
    __tablename__ = 'Mantenimiento'
    __allow_unmapped__ = True
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_vehiculo: int = Column(Integer, ForeignKey("Vehiculo.id"))
    costo: float = Column(Float, nullable=False)
    descripcion: str = Column(String, nullable=False)
    id_estado: int = Column(Integer, ForeignKey("Estado.id"))
    id_empleado: int = Column(Integer, ForeignKey("Empleado.id"))
    fecha_hora: datetime = Column(DateTime, nullable=False, default=datetime.now())

    Vehiculo = relationship("Vehiculo")
    Estado = relationship("Estado")
    Empleado = relationship("Empleado")
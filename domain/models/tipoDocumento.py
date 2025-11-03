from sqlalchemy import Column, Integer, String
from .base import Base

class TipoDocumento(Base):
    __tablename__ = 'TipoDocumento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)

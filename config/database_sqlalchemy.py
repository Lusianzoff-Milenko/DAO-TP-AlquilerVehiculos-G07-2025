from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from domain.models.base import Base

# Usamos check_same_thread=False porque SQLite lo requiere si usas GUI o hilos
DATABASE_URL = "sqlite:///./alquiler_vehiculos_data_base.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

# Scoped session para manejo seguro en hilos
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Crea las tablas basadas en los modelos importados."""
    # Importa tus modelos aquí para asegurar que se registren en Base.metadata antes de create_all
    from domain.models import vehiculo, contrato, cliente, empleado, detalle_contrato, modelo, color, estado, marca, tipoDocumento, tipoPuesto, persona, metodoDePago, mantenimiento, inconveniente, fotoXModelo, modeloXColor
    Base.metadata.create_all(bind=engine)
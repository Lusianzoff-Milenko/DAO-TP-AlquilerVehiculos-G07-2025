from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload

from domain.models.modelo import Modelo
from domain.models.vehiculo import Vehiculo
from data_access.repositories.base_repository import SQLAlchemyRepository

class VehiculoRepository(SQLAlchemyRepository[Vehiculo]):
    def __init__(self, session: Session):
        super().__init__(session, Vehiculo)

    # Aquí agregas SOLO los métodos específicos que no son CRUD básico
    def get_by_patente(self, patente: str) -> Optional[Vehiculo]:
        return self.session.query(Vehiculo).filter_by(patente=patente).first()

    def get_by_id(self, id: int) -> Optional[Vehiculo]:
        # Hacemos Eager Loading de la relación 'Estado'
        return self.session.query(Vehiculo) \
            .options(joinedload(Vehiculo.Estado)) \
            .filter(Vehiculo.id == id).first()

    def list_all(self) -> list[type[Vehiculo]]:
        # Carga ansiosa (Eager Loading) de todas las relaciones necesarias para la tabla
        return self.session.query(Vehiculo) \
            .options(
                joinedload(Vehiculo.Estado),
                joinedload(Vehiculo.Color),
                joinedload(Vehiculo.Modelo).joinedload(Modelo.Marca) # Carga Modelo y su Marca
            ) \
            .all()
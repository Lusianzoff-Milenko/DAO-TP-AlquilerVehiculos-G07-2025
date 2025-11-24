from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
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

    def list_all(self) -> List[Vehiculo]:
        return self.session.query(Vehiculo) \
            .options(joinedload(Vehiculo.Estado)) \
            .all()
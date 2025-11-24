from sqlalchemy.orm import Session
from domain.models.mantenimiento import Mantenimiento
from data_access.repositories.base_repository import SQLAlchemyRepository

class MantenimientoRepository(SQLAlchemyRepository[Mantenimiento]):
    def __init__(self, session: Session):
        super().__init__(session, Mantenimiento)

    def list_by_vehiculo(self, vehiculo_id: int) -> list[type[Mantenimiento]]:
        return self.session.query(Mantenimiento).filter_by(id_vehiculo=vehiculo_id).order_by(Mantenimiento.fecha_hora.desc()).all()
from typing import Optional
from sqlalchemy.orm import Session
from domain.models.empleado import Empleado
from data_access.repositories.base_repository import SQLAlchemyRepository

class EmpleadoRepository(SQLAlchemyRepository[Empleado]):
    def __init__(self, session: Session):
        super().__init__(session, Empleado)

    def get_by_persona_id(self, persona_id: int) -> Optional[Empleado]:
        """Busca un empleado por su ID de persona asociado."""
        return self.session.query(Empleado).filter(
            Empleado.id_persona == persona_id
        ).first()
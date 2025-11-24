from typing import Optional
from sqlalchemy.orm import Session
from domain.models.color import Color
from data_access.repositories.base_repository import SQLAlchemyRepository

class ColorRepository(SQLAlchemyRepository[Color]):
    def __init__(self, session: Session):
        super().__init__(session, Color)

    def get_by_nombre(self, nombre: str) -> Optional[Color]:
        return self.session.query(Color).filter(Color.nombre == nombre).first()
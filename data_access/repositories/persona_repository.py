from typing import Optional
from sqlalchemy.orm import Session
from domain.models.persona import Persona
from data_access.repositories.base_repository import SQLAlchemyRepository

class PersonaRepository(SQLAlchemyRepository[Persona]):
    def __init__(self, session: Session):
        super().__init__(session, Persona)

    def get_by_email(self, email: str) -> Optional[Persona]:
        return self.session.query(Persona).filter(Persona.mail == email).first()

    def get_existing(self, nombre: str, apellido: str) -> Optional[Persona]:
        """Busca si existe una persona con el mismo nombre y apellido."""
        return self.session.query(Persona).filter(
            Persona.nombre == nombre,
            Persona.apellido == apellido
        ).first()
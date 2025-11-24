from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.persona import Persona
from data_access.repositories.persona_repository import PersonaRepository
from services.utils import validate_string


class PersonaService:
    def __init__(self, persona_repo: PersonaRepository):
        self._repo = persona_repo

    def create_persona(self, persona: Persona) -> Optional[int]:
        # Validaciones básicas de formato (opcional, ya que la UI suele validarlo)
        if not validate_string(persona.nombre, "nombre"): return None

        try:
            nueva_persona = self._repo.create(persona)
            return nueva_persona.id
        except IntegrityError:
            print("Error: Ya existe una persona con ese mail o datos duplicados.")
            self._repo.session.rollback()
            return None

    def get_persona_by_id(self, persona_id: int) -> Optional[Persona]:
        return self._repo.get_by_id(persona_id)

    def list_all_personas(self) -> List[Persona]:
        return self._repo.list_all()

    def update_persona(self, persona: Persona) -> bool:
        if not persona.id: return False
        try:
            self._repo.update(persona)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_persona(self, persona_id: int) -> bool:
        try:
            return self._repo.delete(persona_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
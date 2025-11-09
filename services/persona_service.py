from typing import Optional
from domain.models.persona import Persona
from data_access.repositories.persona_repository import PersonaRepository
from services.utils import validate_string
from services.validation_mapper import ValidationMapper


class PersonaService:
    def __init__(self, persona_repo: PersonaRepository, mapper=ValidationMapper):
        self._repo = persona_repo
        self._mapper = mapper

    def create_persona(self, persona: Persona) -> str | None:
        error = validate_string(persona.nombre, "nombre", max_length=100)
        if error:
            return error
        error = validate_string(persona.apellido, "apellido", max_length=100)
        if error:
            return error
        error = validate_string(persona.telefono, "telefono", max_length=20)
        if error:
            return error
        error = validate_string(persona.mail, "mail", max_length=100)
        if error:
            return error
        error = validate_string(persona.direccion, "direccion", max_length=200)
        if error:
            return error
        return self._repo.create(persona)

    def get_persona_by_id(self, persona_id: int) -> Optional[Persona]:
        return self._repo.get_by_id(persona_id)

    def update_persona(self, persona: Persona) -> bool:
        if not persona.id:
            print("ID de persona requerido para actualizar.")
            return False
        return self._repo.update(persona)

    def delete_persona(self, persona_id: int) -> bool:
        return self._repo.delete(persona_id)
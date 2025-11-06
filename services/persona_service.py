from typing import Optional
from domain.models.persona import Persona
from data_access.repositories.persona_repository import PersonaRepository

class PersonaService:
    """
    Servicio responsable de la lógica de negocio (CRUD) para la entidad Persona.
    """
    def __init__(self, persona_repo: PersonaRepository):
        # Inyección del Repositorio
        self._repo = persona_repo

    def create_persona(self, persona: Persona) -> Optional[int]:
        """
        Crea una nueva persona. La validación del esquema se hace en el repositorio.
        """
        # [Patrón de ClienteService]: Ejecutar Lógica (nula en este caso) y delegar persistencia
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
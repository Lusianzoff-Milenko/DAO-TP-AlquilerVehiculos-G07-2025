import datetime

from data_access.repositories.persona_repository import PersonaRepository
from domain.models.persona import Persona


def main():
    persona_repository = PersonaRepository()
    persona = Persona(
        nombre="",
        apellido="Perez",
        telefono="123456789",
        mail="xd@mail",
        direccion="Calle Falsa 123",
        fecha_nacimiento = datetime.datetime.now())
    persona_repository.create(persona)

if __name__ == '__main__':
    main()
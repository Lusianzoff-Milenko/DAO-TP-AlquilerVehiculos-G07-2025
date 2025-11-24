from typing import Optional, List, Iterable
from sqlalchemy.exc import IntegrityError
from domain.models.estado import Estado
from data_access.repositories.estado_repository import EstadoRepository

class EstadoService:
    def __init__(self, estado_repo: EstadoRepository):
        self._repo = estado_repo

    def create_estado(self, estado: Estado) -> Optional[Estado]:
        # Verificar existencia manual para evitar error si ya existe (idempotencia)
        existing = self._repo.get_by_nombre_and_ambito(estado.nombre, estado.ambito)
        if existing:
            return existing
        try:
            return self._repo.create(estado)
        except IntegrityError:
            self._repo.session.rollback()
            return self._repo.get_by_nombre_and_ambito(estado.nombre, estado.ambito)

    def create_estados(self, estados: Iterable[Estado]) -> None:
        for estado in estados:
            self.create_estado(estado)

    def get_estado_by_id(self, estado_id: int) -> Optional[Estado]:
        return self._repo.get_by_id(estado_id)

    def list_all_estados(self) -> List[Estado]:
        return self._repo.list_all()

    def update_estado(self, estado: Estado) -> bool:
        if not estado.id: return False
        try:
            self._repo.update(estado)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_estado(self, estado_id: int) -> bool:
        try:
            return self._repo.delete(estado_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def get_estado_by_name(self, name: str) -> Optional[Estado]:
        # Nota: Esto asume unicidad por nombre global, lo cual puede ser riesgoso si hay ámbitos
        # Mejor usar get_by_name_and_ambito si es posible.
        # Este método llama a un método custom que quizás debas agregar al repo si no existe
        # O podemos hacer un filtrado manual:
        res = [e for e in self._repo.list_all() if e.nombre == name]
        return res[0] if res else None

    def get_estado_by_ambito(self, ambito: str) -> list[type[Estado]]:
        return self._repo.get_by_ambito(ambito)

    def get_estado_by_name_and_ambito(self, name: str, ambito: str) -> Optional[Estado]:
        return self._repo.get_by_nombre_and_ambito(name, ambito)
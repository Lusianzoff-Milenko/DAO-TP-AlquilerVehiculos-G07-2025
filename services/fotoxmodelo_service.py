from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.fotoXModelo import FotoXModelo
from data_access.repositories.foto_x_modelo_repository import FotoXModeloRepository

class FotoXModeloService:
    def __init__(self, foto_repo: FotoXModeloRepository, mapper=None, modeloxcolor_repo=None):
        self._repo = foto_repo

    def create_foto_x_modelo(self, foto: FotoXModelo) -> Optional[int]:
        try:
            nuevo = self._repo.create(foto)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_foto_x_modelo_by_id(self, foto_id: int) -> Optional[FotoXModelo]:
        return self._repo.get_by_id(foto_id)

    def list_all_fotos(self) -> List[FotoXModelo]:
        return self._repo.list_all()

    def update_foto_x_modelo(self, foto: FotoXModelo) -> bool:
        if not foto.id: return False
        try:
            self._repo.update(foto)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_foto_x_modelo(self, foto_id: int) -> bool:
        try:
            return self._repo.delete(foto_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from domain.models.modeloXColor import ModeloXColor
from data_access.repositories.modelo_x_color_repository import ModeloXColorRepository

class ModeloXColorService:
    def __init__(self, mxc_repo: ModeloXColorRepository, mapper=None):
        self._repo = mxc_repo

    def create_modelo_color(self, modeloxcolor: ModeloXColor) -> bool:
        try:
            # SQLAlchemy detecta la clave compuesta
            self._repo.create(modeloxcolor)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def get_association(self, id_modelo: int, id_color: int) -> Optional[ModeloXColor]:
        # Usamos el método especial del repo para claves compuestas
        return self._repo.get_by_ids(id_modelo, id_color)

    def list_all_associations(self) -> List[ModeloXColor]:
        return self._repo.list_all()

    def remove_modelo_color(self, id_modelo: int, id_color: int) -> bool:
        try:
            return self._repo.delete_composite(id_modelo, id_color)
        except IntegrityError:
            self._repo.session.rollback()
            return False
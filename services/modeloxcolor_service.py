from typing import List, Optional
from domain.models.modeloXColor import ModeloXColor
from data_access.repositories.modelo_x_color_repository import ModeloXColorRepository
from data_access.repositories.modelo_repository import ModeloRepository
from data_access.repositories.color_repository import ColorRepository
from services.validation_mapper import ValidationMapper


class ModeloXColorService:
    def __init__(self, mxc_repo: ModeloXColorRepository, modelo_repo: ModeloRepository, color_repo: ColorRepository):
        self._repo = mxc_repo
        repos_to_validate = {
            'modelo': modelo_repo,
            'color': color_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

    def add_modelo_color(self, id_modelo: int, id_color: int) -> bool:
        if not self._mapper.validate_fk_exists('modelo', id_modelo, 'id_modelo'): return False
        if not self._mapper.validate_fk_exists('color', id_color, 'id_color'): return False
        return self._repo.create(ModeloXColor(id_modelo=id_modelo, id_color=id_color))

    def get_association(self, id_modelo: int, id_color: int) -> Optional[ModeloXColor]:
        return self._repo.get_by_composite_key(id_modelo, id_color)

    def list_all_associations(self) -> List[ModeloXColor]:
        return self._repo.list_all()

    def remove_modelo_color(self, id_modelo: int, id_color: int) -> bool:
        return self._repo.delete(id_modelo, id_color)
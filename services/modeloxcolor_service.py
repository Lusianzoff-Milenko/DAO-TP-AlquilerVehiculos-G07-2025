from typing import List, Optional
from domain.models.modeloXColor import ModeloXColor
from data_access.repositories.modelo_x_color_repository import ModeloXColorRepository
from services.validation_mapper import ValidationMapper


class ModeloXColorService:
    def __init__(self, mxc_repo: ModeloXColorRepository, mapper: ValidationMapper):
        self._repo = mxc_repo
        self._mapper = mapper

    def create_modelo_color(self, modeloxcolor: ModeloXColor) -> bool:
        if not self._mapper.validate_fk_exists('modelo',  modeloxcolor.id_modelo, 'id_modelo'): return False
        if not self._mapper.validate_fk_exists('color', modeloxcolor.id_color, 'id_color'): return False
        return self._repo.create(ModeloXColor(id_modelo=modeloxcolor.id_modelo, id_color=modeloxcolor.id_color))

    def get_association(self, id_modelo: int, id_color: int) -> Optional[ModeloXColor]:
        return self._repo.get_by_composite_key(id_modelo, id_color)

    def list_all_associations(self) -> List[ModeloXColor]:
        return self._repo.list_all()

    def remove_modelo_color(self, id_modelo: int, id_color: int) -> bool:
        return self._repo.delete(id_modelo, id_color)
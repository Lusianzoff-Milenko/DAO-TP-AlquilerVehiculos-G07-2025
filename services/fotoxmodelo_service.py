from typing import Optional, List
from domain.models.fotoXModelo import FotoXModelo
from data_access.repositories.foto_x_modelo_repository import FotoXModeloRepository
from data_access.repositories.modelo_repository import ModeloRepository
from data_access.repositories.color_repository import ColorRepository
from services.validation_mapper import ValidationMapper


class FotoXModeloService:
    def __init__(self, foto_repo: FotoXModeloRepository, modelo_repo: ModeloRepository, color_repo: ColorRepository):
        self._repo = foto_repo
        repos_to_validate = {
            'modelo': modelo_repo,
            'color': color_repo
        }
        self._mapper = ValidationMapper(repos_to_validate)

    def create_foto_x_modelo(self, foto: FotoXModelo) -> Optional[int]:
        if not self._mapper.validate_fk_exists('modelo', foto.id_modelo, 'id_modelo'): return None
        if foto.id_color is not None and not self._mapper.validate_fk_exists('color', foto.id_color,
                                                                             'id_color'): return None
        return self._repo.create(foto)

    def get_foto_x_modelo_by_id(self, foto_id: int) -> Optional[FotoXModelo]:
        return self._repo.get_by_id(foto_id)

    def list_all_fotos(self) -> List[FotoXModelo]:
        return self._repo.list_all()

    def update_foto_x_modelo(self, foto: FotoXModelo) -> bool:
        if not foto.id: return False
        if not self._mapper.validate_fk_exists('modelo', foto.id_modelo, 'id_modelo'): return False
        if foto.id_color is not None and not self._mapper.validate_fk_exists('color', foto.id_color,
                                                                             'id_color'): return False
        return self._repo.update(foto)

    def delete_foto_x_modelo(self, foto_id: int) -> bool:
        return self._repo.delete(foto_id)
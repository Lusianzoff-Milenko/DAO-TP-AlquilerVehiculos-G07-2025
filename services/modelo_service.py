from typing import Optional, List
from domain.models.modelo import Modelo
from data_access.repositories.modelo_repository import ModeloRepository
from data_access.repositories.marca_repository import MarcaRepository
from services.validation_mapper import ValidationMapper


class ModeloService:
    def __init__(self, modelo_repo: ModeloRepository, marca_repo: MarcaRepository):
        self._repo = modelo_repo
        repos_to_validate = {'marca': marca_repo}
        self._mapper = ValidationMapper(repos_to_validate)

    def create_modelo(self, modelo: Modelo) -> Optional[int]:
        if not self._mapper.validate_fk_exists('marca', modelo.id_marca, 'id_marca'):
            return None
        return self._repo.create(modelo)

    def get_modelo_by_id(self, modelo_id: int) -> Optional[Modelo]:
        return self._repo.get_by_id(modelo_id)

    def list_all_modelos(self) -> List[Modelo]:
        return self._repo.list_all()

    def update_modelo(self, modelo: Modelo) -> bool:
        if not modelo.id:
            print("ID de modelo requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('marca', modelo.id_marca, 'id_marca'):
            return False
        return self._repo.update(modelo)

    def delete_modelo(self, modelo_id: int) -> bool:
        # Aquí se debería chequear si existen vehículos asociados a este modelo.
        return self._repo.delete(modelo_id)
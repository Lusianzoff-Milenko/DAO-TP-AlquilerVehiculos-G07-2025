# python
# file: `application/services/color_service.py`
from typing import Optional, List
from domain.models.color import Color
from data_access.repositories.color_repository import ColorRepository

class ColorService:
    def __init__(self, color_repo: ColorRepository):
        self._repo = color_repo

    def create_color(self, color: Color) -> Optional[int]:
        """Crea un nuevo color si no existe."""
        return self._repo.create(color)

    def get_color_by_id(self, color_id: int) -> Optional[Color]:
        return self._repo.get_by_id(color_id)

    def list_all_colores(self) -> List[Color]:
        return self._repo.list_all()

    def update_color(self, color: Color) -> bool:
        """Actualiza un color existente."""
        if not color.id:
            print("ID de color requerido para actualizar.")
            return False
        return self._repo.update(color)

    def delete_color(self, color_id: int) -> bool:
        """Elimina un color. Se recomienda chequear antes si está en uso por Vehículos/Fotos."""
        return self._repo.delete(color_id)
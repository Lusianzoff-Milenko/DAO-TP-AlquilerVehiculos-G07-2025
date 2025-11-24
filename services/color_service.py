from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.color import Color
from data_access.repositories.color_repository import ColorRepository

class ColorService:
    def __init__(self, color_repo: ColorRepository):
        self._repo = color_repo

    def create_color(self, color: Color) -> Optional[int]:
        try:
            nuevo = self._repo.create(color)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_color_by_id(self, color_id: int) -> Optional[Color]:
        return self._repo.get_by_id(color_id)

    def list_all_colores(self) -> List[Color]:
        return self._repo.list_all()

    def update_color(self, color: Color) -> bool:
        if not color.id: return False
        try:
            self._repo.update(color)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_color(self, color_id: int) -> bool:
        try:
            return self._repo.delete(color_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False
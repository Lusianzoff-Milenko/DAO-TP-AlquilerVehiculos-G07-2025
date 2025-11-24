from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.empleado import Empleado
from data_access.repositories.empleado_repository import EmpleadoRepository

class EmpleadoService:
    def __init__(self, empleado_repo: EmpleadoRepository):
        self._repo = empleado_repo

    def create_empleado(self, empleado: Empleado) -> Optional[int]:
        try:
            nuevo_empleado = self._repo.create(empleado)
            return nuevo_empleado.id
        except IntegrityError as e:
            print(f"Error al crear empleado (integridad): {e}")
            self._repo.session.rollback()
            return None

    def get_empleado_by_id(self, empleado_id: int) -> Optional[Empleado]:
        return self._repo.get_by_id(empleado_id)

    def list_all_empleados(self) -> List[Empleado]:
        return self._repo.list_all()

    def update_empleado(self, empleado: Empleado) -> bool:
        if not empleado.id: return False
        try:
            self._repo.update(empleado)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_empleado(self, empleado_id: int) -> bool:
        try:
            return self._repo.delete(empleado_id)
        except IntegrityError:
            print("No se puede eliminar: El empleado tiene registros asociados.")
            self._repo.session.rollback()
            return False
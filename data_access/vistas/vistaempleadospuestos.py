from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_empleados_puestos_dto import VistaEmpleadosPuestosDTO

class VistaEmpleadosPuestosRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaEmpleadosPuestosDTO]:
        if row is None:
            return None
        return VistaEmpleadosPuestosDTO(
            id_empleado =row[0],
            nombre_empleado =row[1],
            apellido_empleado =row[2],
            nombre_puesto =row[3],
        )

    def list_all(self) -> list[VistaEmpleadosPuestosDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaEmpleadosPuestos
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing empleadospuestos from view: {e}")
            raise
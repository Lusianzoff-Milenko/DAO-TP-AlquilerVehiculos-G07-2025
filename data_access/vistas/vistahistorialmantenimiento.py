from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_historial_mantenimiento_dto import VistaHistorialMantenimientoDTO

class VistaHistorialMantenimientoRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaHistorialMantenimientoDTO]:
        if row is None:
            return None
        return VistaHistorialMantenimientoDTO(
            patente =row[0],
            nombre_marca =row[1],
            nombre_modelo =row[2],
            año_fabricacion =row[3],
            costo =row[4],
            descripcion =row[5],
            estado =row[6],
            nombre_empleado =row[7],
            apellido_empleado =row[8],
            fecha_hora =row[9],
            id_mantenimiento =row[10],
        )

    def list_all(self) -> list[VistaHistorialMantenimientoDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaHistorialMantenimiento
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing historialmantenimiento from view: {e}")
            raise
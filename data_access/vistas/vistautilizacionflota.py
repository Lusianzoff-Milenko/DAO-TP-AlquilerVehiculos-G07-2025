from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_utilizacion_flota_dto import VistaUtilizacionFlotaDTO

class VistaUtilizacionFlotaRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaUtilizacionFlotaDTO]:
        if row is None:
            return None
        return VistaUtilizacionFlotaDTO(
            id_vehiculo =row[0],
            patente =row[1],
            nombre_marca =row[2],
            nombre_modelo =row[3],
            año_fabricacion =row[4],
            estado_actual =row[5],
        )

    def list_all(self) -> list[VistaUtilizacionFlotaDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaUtilizacionFlota
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing vistautilizacionflota from view: {e}")
            raise
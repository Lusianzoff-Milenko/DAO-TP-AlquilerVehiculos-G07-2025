from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_vehiculos_detallados_dto import VistaVehiculosDetalladosDTO

class VistaVehiculosDetalladosRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaVehiculosDetalladosDTO]:
        if row is None:
            return None
        return VistaVehiculosDetalladosDTO(
            nombre_marca =row[0],
            nombre_modelo =row[1],
            motor =row[2],
            año_lanzamiento =row[3],
            año_fabricacion =row[4],
            patente =row[5],
            color =row[6],
            estado =row[7],
        )

    def list_all(self) -> list[VistaVehiculosDetalladosDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaVehiculosDetallados
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing vistavehiculosdetallados from view: {e}")
            raise
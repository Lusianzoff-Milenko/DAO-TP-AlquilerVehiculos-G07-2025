from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_disponibilidad_flota_dto import VistaDisponibilidadFlotaDTO

class VistaDemandaPorModeloRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaDisponibilidadFlotaDTO]:
        if row is None:
            return None
        return VistaDisponibilidadFlotaDTO(
            id_vehiculo =row[0],
            patente =row[1],
            nombre_marca =row[2],
            nombre_modelo =row[3],
            año_fabricacion =row[4],
            estado =row[5],
        )

    def list_all(self) -> list[VistaDisponibilidadFlotaDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaDisponibilidadFlota
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing disponibilidadflota from view: {e}")
            raise
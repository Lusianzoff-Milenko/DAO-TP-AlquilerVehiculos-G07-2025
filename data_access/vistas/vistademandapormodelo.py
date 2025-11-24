from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_demanda_por_modelo_dto import VistaDemandaPorModeloDTO

class VistaDemandaPorModeloRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaDemandaPorModeloDTO]:
        if row is None:
            return None
        return VistaDemandaPorModeloDTO(
            nombre_marca =row[0],
            nombre_modelo =row[1],
            año_fabricacion =row[2],
            total_dias_reservados_contratados =row[3],
        )

    def list_all(self) -> list[VistaDemandaPorModeloDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaDemandaPorModelo
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing demandapormodelo from view: {e}")
            raise
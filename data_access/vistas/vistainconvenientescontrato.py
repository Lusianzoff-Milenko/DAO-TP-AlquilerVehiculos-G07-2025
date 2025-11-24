from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_inconvenientes_contrato_dto import VistaInconvenientesContratoDTO

class VistaInconvenientesContratoRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaInconvenientesContratoDTO]:
        if row is None:
            return None
        return VistaInconvenientesContratoDTO(
            id_contrato =row[0],
            nombre_tipo_inconveniente =row[1],
            nombre_inconveniente =row[2],
            descripcion_inconveniente =row[3],
            costo =row[4],
            estado_inconveniente =row[5],
        )

    def list_all(self) -> list[VistaInconvenientesContratoDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaInconvenientesContrato
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing vistaincovenientescontrato from view: {e}")
            raise
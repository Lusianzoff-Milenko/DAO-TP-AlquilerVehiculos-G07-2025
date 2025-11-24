from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_reporte_facturacion_dto import VistaReporteFacturacionDTO

class VistaReporteFacturacionRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaReporteFacturacionDTO]:
        if row is None:
            return None
        return VistaReporteFacturacionDTO(
            id_contrato =row[0],
            nombre_cliente =row[1],
            apellido_cliente =row[2],
            fecha_desde =row[3],
            fecha_hasta =row[4],
            fecha_entrega =row[5],
            monto =row[6],
            nombre_empleado =row[7],
        )

    def list_all(self) -> list[VistaReporteFacturacionDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaReporteFacturacion
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing vistareportefacturacion from view: {e}")
            raise
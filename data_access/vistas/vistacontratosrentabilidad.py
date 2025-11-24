from typing import Optional
from data_access.database_connector import Database
from domain.dto.vista_contratos_rentabilidad_dto import VistaContratosRentabilidadDTO

class VistaContratosRentabilidadRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_dto(self, row) -> Optional[VistaContratosRentabilidadDTO]:
        if row is None:
            return None
        return VistaContratosRentabilidadDTO(
            id_contrato=row[0],
            nombre_cliente=row[1],
            apellido_cliente=row[2],
            fecha_desde=row[3],
            fecha_hasta=row[4],
            fecha_entrega=row[5],
            metodo_pago=row[6],
            estado_contrato=row[7],
            monto=row[8],
            tiene_seguro=row[9],
        )

    def list_all(self) -> list[VistaContratosRentabilidadDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaContratosRentabilidad
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing contratosrentabilidad from view: {e}")
            raise
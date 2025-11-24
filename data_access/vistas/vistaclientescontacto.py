from typing import Optional
from data_access.database_connector import Database
from domain.dto.clientes_contacto_dto import VistaClientesContactoDTO
class VistaClientesContactoRepo:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def row_to_dto(self, row) -> VistaClientesContactoDTO:
        if row is None:
            return None
        return VistaClientesContactoDTO(
            id_cliente=row[0],
            nombre=row[1],
            apellido=row[2],
            telefono=row[3],
            mail=row[4],
            direccion=row[5],
            tipo_documento=row[6],
            documento=row[7]
        )
    def list_all(self) -> list[VistaClientesContactoDTO]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM VistaClientesContacto
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                # La función de mapeo (_row_to_vehiculo) debe ser compatible
                return [self._row_to_dto(r) for r in rows]
        except Exception as e:
            print(f"Error listing clientescontacto from view: {e}")
            raise
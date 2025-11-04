from services.utils import validate_string, validate_positive_int
from typing import Optional, List
from data_access.database_connector import Database
from domain.models.cliente import Cliente

class ClienteRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_cliente(self, cliente: Cliente) -> Optional[str]:
        error = validate_string(cliente.documento, 'documento', max_length=50)
        if error: return error
        error = validate_positive_int(cliente.id_tipo_documento, 'id_tipo_documento')
        if error: return error
        error = validate_positive_int(cliente.id_persona, 'id_persona')
        if error: return error
        return None

    def _row_to_cliente(self, row) -> Cliente | None:
        if row is None:
            return None
        return Cliente(
            id=row[0],
            documento=row[1],
            id_tipo_documento=row[2],
            id_persona=row[3],
        )

    def create(self, cliente: Cliente) -> Optional[int]:
        validation_error = self._validate_cliente(cliente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM Cliente
                    WHERE documento = ? AND id_tipoDocumento = ?
                    """,
                    (cliente.documento, cliente.id_tipo_documento),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Cliente already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Cliente (documento, id_tipoDocumento, id_persona)
                    VALUES (?, ?, ?)
                    """,
                    (
                        cliente.documento,
                        cliente.id_tipo_documento,
                        cliente.id_persona,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating cliente: {e}")
            raise

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, documento, id_tipoDocumento, id_persona
                    FROM Cliente WHERE id = ?
                    """,
                    (cliente_id,),
                )
                row = cur.fetchone()
                return self._row_to_cliente(row)
        except Exception as e:
            print(f"Error retrieving cliente by id: {e}")
            raise

    def list_all(self) -> List[Cliente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, documento, id_tipoDocumento, id_persona
                    FROM Cliente ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_cliente(r) for r in rows]
        except Exception as e:
            print(f"Error listing all clientes: {e}")
            raise

    def update(self, cliente: Cliente) -> bool:
        validation_error = self._validate_cliente(cliente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Cliente
                    SET documento = ?, id_tipoDocumento = ?, id_persona = ?
                    WHERE id = ?
                    """,
                    (
                        cliente.documento,
                        cliente.id_tipo_documento,
                        cliente.id_persona,
                        cliente.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating cliente: {e}")
            raise

    def delete(self, cliente_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Cliente WHERE id = ?", (cliente_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting cliente: {e}")
            raise
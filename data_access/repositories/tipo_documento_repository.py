from typing import Optional, List
from data_access.database_connector import Database
from domain.models.tipoDocumento import TipoDocumento
from services.utils import validate_string


class TipoDocumentoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_tipo_documento(self, tipo_documento: TipoDocumento) -> Optional[str]:
        error = validate_string(tipo_documento.nombre, 'nombre', max_length=50)
        if error:
            return error
        return None

    def _row_to_tipo_documento(self, row) -> TipoDocumento | None:
        if row is None:
            return None
        return TipoDocumento(
            id=row[0],
            nombre=row[1],
        )

    def create(self, tipo_documento: TipoDocumento) -> Optional[int]:
        validation_error = self._validate_tipo_documento(tipo_documento)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM TipoDocumento WHERE nombre = ?
                    """,
                    (tipo_documento.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"TipoDocumento already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO TipoDocumento (nombre)
                    VALUES (?)
                    """,
                    (tipo_documento.nombre,),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating TipoDocumento: {e}")
            raise

    def get_by_id(self, tipo_documento_id: int) -> Optional[TipoDocumento]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM TipoDocumento WHERE id = ?
                    """,
                    (tipo_documento_id,),
                )
                row = cur.fetchone()
                return self._row_to_tipo_documento(row)
        except Exception as e:
            print(f"Error retrieving TipoDocumento by id: {e}")
            raise

    def list_all(self) -> List[TipoDocumento]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM TipoDocumento ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_tipo_documento(r) for r in rows]
        except Exception as e:
            print(f"Error listing all TipoDocumentos: {e}")
            raise

    def update(self, tipo_documento: TipoDocumento) -> bool:
        validation_error = self._validate_tipo_documento(tipo_documento)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE TipoDocumento
                    SET nombre = ?
                    WHERE id = ?
                    """,
                    (
                        tipo_documento.nombre,
                        tipo_documento.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating TipoDocumento: {e}")
            raise

    def delete(self, tipo_documento_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM TipoDocumento WHERE id = ?", (tipo_documento_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting TipoDocumento: {e}")
            raise
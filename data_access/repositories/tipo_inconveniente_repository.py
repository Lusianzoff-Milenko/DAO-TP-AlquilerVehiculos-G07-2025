# python
# file: `data_access/repositories/tipo_inconveniente_repository.py`
from typing import Optional, List
from data_access.database_connector import Database
from domain.models.tipoInconveniente import TipoInconveniente
from services.utils import validate_string


class TipoInconvenienteRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_tipo_inconveniente(self, tipo_inconveniente: TipoInconveniente) -> Optional[str]:
        error = validate_string(tipo_inconveniente.nombre, 'nombre', max_length=50)
        if error:
            return error
        error = validate_string(tipo_inconveniente.descripcion, 'descripcion', max_length=500)
        if error:
            return error
        return None

    def _row_to_tipo_inconveniente(self, row) -> TipoInconveniente | None:
        if row is None:
            return None
        return TipoInconveniente(
            id=row[0],
            nombre=row[1],
            descripcion=row[2],
        )

    def create(self, tipo_inconveniente: TipoInconveniente) -> Optional[int]:
        validation_error = self._validate_tipo_inconveniente(tipo_inconveniente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM TipoInconveniente WHERE nombre = ?
                    """,
                    (tipo_inconveniente.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"TipoInconveniente already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO TipoInconveniente (nombre, descripcion)
                    VALUES (?, ?)
                    """,
                    (tipo_inconveniente.nombre, tipo_inconveniente.descripcion),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating TipoInconveniente: {e}")
            raise

    def get_by_id(self, tipo_inconveniente_id: int) -> Optional[TipoInconveniente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion
                    FROM TipoInconveniente WHERE id = ?
                    """,
                    (tipo_inconveniente_id,),
                )
                row = cur.fetchone()
                return self._row_to_tipo_inconveniente(row)
        except Exception as e:
            print(f"Error retrieving TipoInconveniente by id: {e}")
            raise

    def list_all(self) -> List[TipoInconveniente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion
                    FROM TipoInconveniente ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_tipo_inconveniente(r) for r in rows]
        except Exception as e:
            print(f"Error listing all TipoInconvenientes: {e}")
            raise

    def update(self, tipo_inconveniente: TipoInconveniente) -> bool:
        validation_error = self._validate_tipo_inconveniente(tipo_inconveniente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE TipoInconveniente
                    SET nombre = ?, descripcion = ?
                    WHERE id = ?
                    """,
                    (
                        tipo_inconveniente.nombre,
                        tipo_inconveniente.descripcion,
                        tipo_inconveniente.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating TipoInconveniente: {e}")
            raise

    def delete(self, tipo_inconveniente_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM TipoInconveniente WHERE id = ?", (tipo_inconveniente_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting TipoInconveniente: {e}")
            raise
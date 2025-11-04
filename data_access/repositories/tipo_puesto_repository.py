from typing import Optional, List
from data_access.database_connector import Database
from domain.models.tipoPuesto import TipoPuesto
from services.utils import validate_string


class TipoPuestoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_tipo_puesto(self, tipo_puesto: TipoPuesto) -> Optional[str]:
        error = validate_string(tipo_puesto.nombre, 'nombre', max_length=50)
        if error:
            return error
        return None

    def _row_to_tipo_puesto(self, row) -> TipoPuesto:
        if row is None:
            return None
        return TipoPuesto(
            id=row[0],
            nombre=row[1],
        )

    def create(self, tipo_puesto: TipoPuesto) -> Optional[int]:
        validation_error = self._validate_tipo_puesto(tipo_puesto)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                # Check for existing tipo puesto by nombre (unique constraint)
                cur.execute(
                    """
                    SELECT id FROM TipoPuesto WHERE nombre = ?
                    """,
                    (tipo_puesto.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"TipoPuesto already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO TipoPuesto (nombre)
                    VALUES (?)
                    """,
                    (tipo_puesto.nombre,),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating TipoPuesto: {e}")
            raise

    def get_by_id(self, tipo_puesto_id: int) -> Optional[TipoPuesto]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM TipoPuesto WHERE id = ?
                    """,
                    (tipo_puesto_id,),
                )
                row = cur.fetchone()
                return self._row_to_tipo_puesto(row)
        except Exception as e:
            print(f"Error retrieving TipoPuesto by id: {e}")
            raise

    def list_all(self) -> List[TipoPuesto]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM TipoPuesto ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_tipo_puesto(r) for r in rows]
        except Exception as e:
            print(f"Error listing all TipoPuestos: {e}")
            raise

    def update(self, tipo_puesto: TipoPuesto) -> bool:
        validation_error = self._validate_tipo_puesto(tipo_puesto)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE TipoPuesto
                    SET nombre = ?
                    WHERE id = ?
                    """,
                    (
                        tipo_puesto.nombre,
                        tipo_puesto.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating TipoPuesto: {e}")
            raise

    def delete(self, tipo_puesto_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM TipoPuesto WHERE id = ?", (tipo_puesto_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting TipoPuesto: {e}")
            raise
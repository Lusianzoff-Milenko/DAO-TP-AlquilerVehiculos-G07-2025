from typing import Optional, List
from data_access.database_connector import Database
from domain.models.metodoDePago import MetodoDePago
from services.utils import validate_string


class MetodoDePagoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_metodo_de_pago(self, metodo_pago: MetodoDePago) -> Optional[str]:
        error = validate_string(metodo_pago.nombre, 'nombre', max_length=50)
        if error:
            return error
        return None

    def _row_to_metodo_de_pago(self, row) -> MetodoDePago | None:
        # row order: id, nombre
        if row is None:
            return None
        return MetodoDePago(
            id=row[0],
            nombre=row[1],
        )

    def create(self, metodo_pago: MetodoDePago) -> Optional[int]:
        validation_error = self._validate_metodo_de_pago(metodo_pago)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM MetodoDePago WHERE nombre = ?
                    """,
                    (metodo_pago.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"MetodoDePago already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO MetodoDePago (nombre)
                    VALUES (?)
                    """,
                    (metodo_pago.nombre,),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating MetodoDePago: {e}")
            raise

    def get_by_id(self, metodo_pago_id: int) -> Optional[MetodoDePago]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM MetodoDePago WHERE id = ?
                    """,
                    (metodo_pago_id,),
                )
                row = cur.fetchone()
                return self._row_to_metodo_de_pago(row)
        except Exception as e:
            print(f"Error retrieving MetodoDePago by id: {e}")
            raise

    def list_all(self) -> List[MetodoDePago]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM MetodoDePago ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_metodo_de_pago(r) for r in rows]
        except Exception as e:
            print(f"Error listing all MetodoDePagos: {e}")
            raise

    def update(self, metodo_pago: MetodoDePago) -> bool:
        validation_error = self._validate_metodo_de_pago(metodo_pago)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE MetodoDePago
                    SET nombre = ?
                    WHERE id = ?
                    """,
                    (
                        metodo_pago.nombre,
                        metodo_pago.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating MetodoDePago: {e}")
            raise

    def delete(self, metodo_pago_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM MetodoDePago WHERE id = ?", (metodo_pago_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting MetodoDePago: {e}")
            raise
from typing import Optional, List
from data_access.database_connector import Database
from domain.models.inconveniente import Inconveniente

class InconvenienteRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_inconveniente(self, inconveniente: Inconveniente) -> Optional[str]:
        if not isinstance(inconveniente.nombre, str) or not inconveniente.nombre.strip():
            return "Invalid 'nombre' — must be a non-empty string"
        if len(inconveniente.nombre) > 50:
            return "Invalid 'nombre' — maximum length is 50 characters"
        if inconveniente.descripcion is not None and not isinstance(inconveniente.descripcion, str):
            return "Invalid 'descripcion' — must be a string or None"
        if not isinstance(inconveniente.id_tipo_inconveniente, int) or inconveniente.id_tipo_inconveniente <= 0:
            return "Invalid 'id_tipo_inconveniente' — must be a positive integer"
        if inconveniente.costo is not None and not isinstance(inconveniente.costo, (float, int)) or (inconveniente.costo is not None and inconveniente.costo < 0):
            return "Invalid 'costo' — must be a non-negative number or None"
        if not isinstance(inconveniente.id_contrato, int) or inconveniente.id_contrato <= 0:
            return "Invalid 'id_contrato' — must be a positive integer"
        if not isinstance(inconveniente.id_estado, int) or inconveniente.id_estado <= 0:
            return "Invalid 'id_estado' — must be a positive integer"
        return None

    def _row_to_inconveniente(self, row) -> Inconveniente | None:
        if row is None:
            return None
        return Inconveniente(
            id=row[0],
            nombre=row[1],
            descripcion=row[2],
            id_tipo_inconveniente=row[3],
            costo=row[4],
            id_contrato=row[5],
            id_estado=row[6],
        )

    def create(self, inconveniente: Inconveniente) -> Optional[int]:
        validation_error = self._validate_inconveniente(inconveniente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    INSERT INTO RegistroInconvenientes (nombre, descripcion, id_tipoInconveniente, costo, id_contrato, id_estado)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        inconveniente.nombre,
                        inconveniente.descripcion,
                        inconveniente.id_tipo_inconveniente,
                        inconveniente.costo,
                        inconveniente.id_contrato,
                        inconveniente.id_estado,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating inconveniente: {e}")
            raise

    def get_by_id(self, inconveniente_id: int) -> Optional[Inconveniente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion, id_tipoInconveniente, costo, id_contrato, id_estado
                    FROM RegistroInconvenientes WHERE id = ?
                    """,
                    (inconveniente_id,),
                )
                row = cur.fetchone()
                return self._row_to_inconveniente(row)
        except Exception as e:
            print(f"Error retrieving inconveniente by id: {e}")
            raise

    def list_all(self) -> List[Inconveniente]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion, id_tipoInconveniente, costo, id_contrato, id_estado
                    FROM RegistroInconvenientes ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_inconveniente(r) for r in rows]
        except Exception as e:
            print(f"Error listing all inconvenientes: {e}")
            raise

    def update(self, inconveniente: Inconveniente) -> bool:
        validation_error = self._validate_inconveniente(inconveniente)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE RegistroInconvenientes
                    SET nombre = ?, descripcion = ?, id_tipoInconveniente = ?, costo = ?, id_contrato = ?, id_estado = ?
                    WHERE id = ?
                    """,
                    (
                        inconveniente.nombre,
                        inconveniente.descripcion,
                        inconveniente.id_tipo_inconveniente,
                        inconveniente.costo,
                        inconveniente.id_contrato,
                        inconveniente.id_estado,
                        inconveniente.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating inconveniente: {e}")
            raise

    def delete(self, inconveniente_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM RegistroInconvenientes WHERE id = ?", (inconveniente_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting inconveniente: {e}")
            raise
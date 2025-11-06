from typing import Optional, List
from data_access.database_connector import Database
from domain.models.estado import Estado

class EstadoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_estado(self, estado: Estado) -> Optional[str]:
        if not isinstance(estado.nombre, str) or not estado.nombre.strip():
            return "Invalid 'nombre' — must be a non-empty string"
        if len(estado.nombre) > 50:
            return "Invalid 'nombre' — maximum length is 50 characters"
        if not isinstance(estado.ambito, str) or not estado.ambito.strip():
            return "Invalid 'ambito' — must be a non-empty string"
        if len(estado.ambito) > 50:
            return "Invalid 'ambito' — maximum length is 50 characters"
        return None

    def _row_to_estado(self, row) -> Estado | None:
        # row order: id, nombre, ambito
        if row is None:
            return None
        return Estado(
            id=row[0],
            nombre=row[1],
            ambito=row[2],
        )

    def create(self, estado: Estado) -> Optional[int]:
        validation_error = self._validate_estado(estado)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                # Check for existing estado by nombre and ambito (unique constraint if applicable)
                cur.execute(
                    """
                    SELECT id FROM Estado WHERE nombre = ? AND ambito = ?
                    """,
                    (estado.nombre, estado.ambito),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Estado already exists with id {existing[0]}")
                    return existing[0]
                cur.execute(
                    """
                    INSERT INTO Estado (nombre, ambito)
                    VALUES (?, ?)
                    """,
                    (estado.nombre, estado.ambito),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating estado: {e}")
            raise

    def get_by_id(self, estado_id: int) -> Optional[Estado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, ambito
                    FROM Estado WHERE id = ?
                    """,
                    (estado_id,),
                )
                row = cur.fetchone()
                return self._row_to_estado(row)
        except Exception as e:
            print(f"Error retrieving estado by id: {e}")
            raise

    def list_all(self) -> List[Estado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, ambito
                    FROM Estado ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_estado(r) for r in rows if r is not None]
        except Exception as e:
            print(f"Error listing all estados: {e}")
            raise

    def update(self, estado: Estado) -> bool:
        validation_error = self._validate_estado(estado)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Estado
                    SET nombre = ?, ambito = ?
                    WHERE id = ?
                    """,
                    (
                        estado.nombre,
                        estado.ambito,
                        estado.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating estado: {e}")
            raise

    def delete(self, estado_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Estado WHERE id = ?", (estado_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting estado: {e}")
            raise

    def get_by_name(self, name: str) -> Optional[Estado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, ambito
                    FROM Estado WHERE nombre = ?
                    """,
                    (name,),
                )
                row = cur.fetchone()
                return self._row_to_estado(row)
        except Exception as e:
            print(f"Error retrieving estado by name: {e}")
            raise

    def get_by_ambito(self, ambito: str) -> List[Estado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, ambito
                    FROM Estado WHERE ambito = ?
                    """,
                    (ambito,),
                )
                rows = cur.fetchall()
                return [self._row_to_estado(r) for r in rows if r is not None]
        except Exception as e:
            print(f"Error retrieving estados by ambito: {e}")
            raise
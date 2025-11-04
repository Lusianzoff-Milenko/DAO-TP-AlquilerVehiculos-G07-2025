from typing import Optional, List
from data_access.database_connector import Database
from domain.models.color import Color
from services.utils import validate_string


class ColorRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_color(self, color: Color) -> Optional[str]:
        error = validate_string(color.nombre, 'nombre', max_length=50)
        if error:
            return error
        return None

    def _row_to_color(self, row) -> Color | None:
        if row is None:
            return None
        return Color(
            id=row[0],
            nombre=row[1],
        )

    def create(self, color: Color) -> Optional[int]:
        validation_error = self._validate_color(color)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                # Check for existing color by nombre (unique constraint)
                cur.execute(
                    """
                    SELECT id FROM Color WHERE nombre = ?
                    """,
                    (color.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Color already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Color (nombre)
                    VALUES (?)
                    """,
                    (color.nombre,),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating color: {e}")
            raise

    def get_by_id(self, color_id: int) -> Optional[Color]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM Color WHERE id = ?
                    """,
                    (color_id,),
                )
                row = cur.fetchone()
                return self._row_to_color(row)
        except Exception as e:
            print(f"Error retrieving color by id: {e}")
            raise

    def list_all(self) -> List[Color]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM Color ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_color(r) for r in rows]
        except Exception as e:
            print(f"Error listing all colors: {e}")
            raise

    def update(self, color: Color) -> bool:
        validation_error = self._validate_color(color)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Color
                    SET nombre = ?
                    WHERE id = ?
                    """,
                    (
                        color.nombre,
                        color.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating color: {e}")
            raise

    def delete(self, color_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Color WHERE id = ?", (color_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting color: {e}")
            raise
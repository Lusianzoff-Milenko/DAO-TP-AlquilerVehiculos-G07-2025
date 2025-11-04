from typing import Optional, List
from data_access.database_connector import Database
from domain.models.modeloXColor import ModeloXColor

class ModeloXColorRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_modelo_x_color(self, modelo_x_color: ModeloXColor) -> Optional[str]:
        if not isinstance(modelo_x_color.id_modelo, int) or modelo_x_color.id_modelo <= 0:
            return "Invalid 'id_modelo' — must be a positive integer"
        if not isinstance(modelo_x_color.id_color, int) or modelo_x_color.id_color <= 0:
            return "Invalid 'id_color' — must be a positive integer"
        return None

    def _row_to_modelo_x_color(self, row) -> ModeloXColor | None:
        if row is None:
            return None
        return ModeloXColor(
            id_modelo=row[0],
            id_color=row[1],
        )

    def create(self, modelo_x_color: ModeloXColor) -> bool:
        validation_error = self._validate_modelo_x_color(modelo_x_color)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id_modelo FROM ModeloXColor
                    WHERE id_modelo = ? AND id_color = ?
                    """,
                    (modelo_x_color.id_modelo, modelo_x_color.id_color),
                )
                if cur.fetchone():
                    print("ModeloXColor association already exists.")
                    return False

                cur.execute(
                    """
                    INSERT INTO ModeloXColor (id_modelo, id_color)
                    VALUES (?, ?)
                    """,
                    (modelo_x_color.id_modelo, modelo_x_color.id_color),
                )
                return True
        except Exception as e:
            print(f"Error creating ModeloXColor: {e}")
            raise

    def get_by_composite_key(self, id_modelo: int, id_color: int) -> Optional[ModeloXColor]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id_modelo, id_color
                    FROM ModeloXColor WHERE id_modelo = ? AND id_color = ?
                    """,
                    (id_modelo, id_color),
                )
                row = cur.fetchone()
                return self._row_to_modelo_x_color(row)
        except Exception as e:
            print(f"Error retrieving ModeloXColor by composite key: {e}")
            raise

    def list_all(self) -> List[ModeloXColor]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id_modelo, id_color
                    FROM ModeloXColor ORDER BY id_modelo, id_color
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_modelo_x_color(r) for r in rows]
        except Exception as e:
            print(f"Error listing all ModeloXColors: {e}")
            raise

    def delete(self, id_modelo: int, id_color: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM ModeloXColor WHERE id_modelo = ? AND id_color = ?", (id_modelo, id_color))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting ModeloXColor: {e}")
            raise
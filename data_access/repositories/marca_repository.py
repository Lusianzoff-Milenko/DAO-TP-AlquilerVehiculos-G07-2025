from typing import Optional, List
from data_access.database_connector import Database
from domain.models.marca import Marca
from services.utils import validate_string


class MarcaRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_marca(self, marca: Marca) -> Optional[str]:
        error = validate_string(marca.nombre, 'nombre', max_length=20)
        if error:
            return error
        error = validate_string(marca.descripcion, 'descripcion', max_length=255)
        if error:
            return error
        return None

    def _row_to_marca(self, row) -> Marca | None:
        # row order: id, nombre, descripcion
        if row is None:
            return None
        return Marca(
            id=row[0],
            nombre=row[1],
            descripcion=row[2],
        )

    def create(self, marca: Marca) -> Optional[int]:
        validation_error = self._validate_marca(marca)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM Marca WHERE nombre = ?
                    """,
                    (marca.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Marca already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Marca (nombre, descripcion)
                    VALUES (?, ?)
                    """,
                    (marca.nombre, marca.descripcion),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating Marca: {e}")
            raise

    def get_by_id(self, marca_id: int) -> Optional[Marca]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion
                    FROM Marca WHERE id = ?
                    """,
                    (marca_id,),
                )
                row = cur.fetchone()
                return self._row_to_marca(row)
        except Exception as e:
            print(f"Error retrieving Marca by id: {e}")
            raise

    def list_all(self) -> List[Marca]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, descripcion
                    FROM Marca ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_marca(r) for r in rows]
        except Exception as e:
            print(f"Error listing all Marcas: {e}")
            raise

    def update(self, marca: Marca) -> bool:
        validation_error = self._validate_marca(marca)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Marca
                    SET nombre = ?, descripcion = ?
                    WHERE id = ?
                    """,
                    (
                        marca.nombre,
                        marca.descripcion,
                        marca.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating Marca: {e}")
            raise

    def delete(self, marca_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Marca WHERE id = ?", (marca_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting Marca: {e}")
            raise
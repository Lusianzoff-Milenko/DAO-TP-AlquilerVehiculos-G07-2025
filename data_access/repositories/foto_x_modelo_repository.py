from typing import Optional, List
from data_access.database_connector import Database
from domain.models.fotoXModelo import FotoXModelo


class FotoXModeloRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_foto_x_modelo(self, foto_x_modelo: FotoXModelo) -> Optional[str]:
        if not isinstance(foto_x_modelo.id_modelo, int) or foto_x_modelo.id_modelo <= 0:
            return "Invalid 'id_modelo' — must be a positive integer"
        if foto_x_modelo.id_color is not None and (not isinstance(foto_x_modelo.id_color, int) or foto_x_modelo.id_color <= 0):
            return "Invalid 'id_color' — must be a positive integer or None"
        if not isinstance(foto_x_modelo.foto_path, str) or not foto_x_modelo.foto_path.strip():
            return "Invalid 'foto_path' — must be a non-empty string"
        if foto_x_modelo.anio_fabricacion is not None and (not isinstance(foto_x_modelo.anio_fabricacion, int) or foto_x_modelo.anio_fabricacion < 1900):
            return "Invalid 'anio_fabricacion' — must be a reasonable positive integer or None"
        return None

    def _row_to_foto_x_modelo(self, row) -> FotoXModelo | None:
        if row is None:
            return None
        return FotoXModelo(
            id=row[0],
            id_modelo=row[1],
            id_color=row[2],
            foto_path=row[3],
            anio_fabricacion=row[4],
        )

    def create(self, foto_x_modelo: FotoXModelo) -> Optional[int]:
        validation_error = self._validate_foto_x_modelo(foto_x_modelo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM FotoXModelo
                    WHERE id_modelo = ? AND (id_color IS ? OR id_color = ?) AND foto_path = ?
                    """,
                    (
                        foto_x_modelo.id_modelo,
                        None if foto_x_modelo.id_color is None else foto_x_modelo.id_color,
                        foto_x_modelo.id_color,
                        foto_x_modelo.foto_path,
                    ),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"FotoXModelo already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO FotoXModelo (id_modelo, id_color, foto_path, año_fabricacion)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        foto_x_modelo.id_modelo,
                        foto_x_modelo.id_color,
                        foto_x_modelo.foto_path,
                        foto_x_modelo.anio_fabricacion,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating foto_x_modelo: {e}")
            raise

    def get_by_id(self, foto_x_modelo_id: int) -> Optional[FotoXModelo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_modelo, id_color, foto_path, año_fabricacion
                    FROM FotoXModelo WHERE id = ?
                    """,
                    (foto_x_modelo_id,),
                )
                row = cur.fetchone()
                return self._row_to_foto_x_modelo(row)
        except Exception as e:
            print(f"Error retrieving foto_x_modelo by id: {e}")
            raise

    def list_all(self) -> List[FotoXModelo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_modelo, id_color, foto_path, año_fabricacion
                    FROM FotoXModelo ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_foto_x_modelo(r) for r in rows]
        except Exception as e:
            print(f"Error listing all foto_x_modelos: {e}")
            raise

    def update(self, foto_x_modelo: FotoXModelo) -> bool:
        validation_error = self._validate_foto_x_modelo(foto_x_modelo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE FotoXModelo
                    SET id_modelo = ?, id_color = ?, foto_path = ?, año_fabricacion = ?
                    WHERE id = ?
                    """,
                    (
                        foto_x_modelo.id_modelo,
                        foto_x_modelo.id_color,
                        foto_x_modelo.foto_path,
                        foto_x_modelo.anio_fabricacion,
                        foto_x_modelo.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating foto_x_modelo: {e}")
            raise

    def delete(self, foto_x_modelo_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM FotoXModelo WHERE id = ?", (foto_x_modelo_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting foto_x_modelo: {e}")
            raise
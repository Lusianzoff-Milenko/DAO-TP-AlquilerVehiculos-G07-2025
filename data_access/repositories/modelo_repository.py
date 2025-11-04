from typing import Optional, List
from data_access.database_connector import Database
from domain.models.modelo import Modelo


class ModeloRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_modelo(self, modelo: Modelo) -> Optional[str]:
        if not isinstance(modelo.nombre, str) or not modelo.nombre.strip():
            return "Invalid 'nombre' — must be a non-empty string"
        if len(modelo.nombre) > 50:
            return "Invalid 'nombre' — maximum length is 50 characters"
        if not isinstance(modelo.id_marca, int) or modelo.id_marca <= 0:
            return "Invalid 'id_marca' — must be a positive integer"
        if not isinstance(modelo.cantidad_pasajeros, int) or modelo.cantidad_pasajeros <= 0:
            return "Invalid 'cantidad_pasajeros' — must be a positive integer"
        if not isinstance(modelo.cantidad_puertas, int) or modelo.cantidad_puertas <= 0:
            return "Invalid 'cantidad_puertas' — must be a positive integer"
        if not isinstance(modelo.motor, str) or not modelo.motor.strip():
            return "Invalid 'motor' — must be a non-empty string"
        if len(modelo.motor) > 50:
            return "Invalid 'motor' — maximum length is 50 characters"
        if not isinstance(modelo.anio_lanzamiento, str) or not modelo.anio_lanzamiento.strip():
            # Note: The SQLAlchemy model defined it as DateTime but the type is String in the model.
            return "Invalid 'anio_lanzamiento' — must be a non-empty string (representing year)"
        return None

    def _row_to_modelo(self, row) -> Modelo | None:
        if row is None:
            return None
        return Modelo(
            id=row[0],
            nombre=row[1],
            id_marca=row[2],
            cantidad_pasajeros=row[3],
            cantidad_puertas=row[4],
            motor=row[5],
            anio_lanzamiento=row[6], # Stored as string/text in DB
        )

    def create(self, modelo: Modelo) -> Optional[int]:
        validation_error = self._validate_modelo(modelo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM Modelo WHERE nombre = ?
                    """,
                    (modelo.nombre,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Modelo already exists with id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Modelo (nombre, id_marca, cantidad_pasajeros, cantidad_puertas, motor, año_lanzamiento)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        modelo.nombre,
                        modelo.id_marca,
                        modelo.cantidad_pasajeros,
                        modelo.cantidad_puertas,
                        modelo.motor,
                        modelo.anio_lanzamiento,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating Modelo: {e}")
            raise

    def get_by_id(self, modelo_id: int) -> Optional[Modelo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, id_marca, cantidad_pasajeros, cantidad_puertas, motor, año_lanzamiento
                    FROM Modelo WHERE id = ?
                    """,
                    (modelo_id,),
                )
                row = cur.fetchone()
                return self._row_to_modelo(row)
        except Exception as e:
            print(f"Error retrieving Modelo by id: {e}")
            raise

    def list_all(self) -> List[Modelo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, id_marca, cantidad_pasajeros, cantidad_puertas, motor, año_lanzamiento
                    FROM Modelo ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_modelo(r) for r in rows]
        except Exception as e:
            print(f"Error listing all Modelos: {e}")
            raise

    def update(self, modelo: Modelo) -> bool:
        validation_error = self._validate_modelo(modelo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Modelo
                    SET nombre = ?, id_marca = ?, cantidad_pasajeros = ?, cantidad_puertas = ?, motor = ?, año_lanzamiento = ?
                    WHERE id = ?
                    """,
                    (
                        modelo.nombre,
                        modelo.id_marca,
                        modelo.cantidad_pasajeros,
                        modelo.cantidad_puertas,
                        modelo.motor,
                        modelo.anio_lanzamiento,
                        modelo.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating Modelo: {e}")
            raise

    def delete(self, modelo_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Modelo WHERE id = ?", (modelo_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting Modelo: {e}")
            raise
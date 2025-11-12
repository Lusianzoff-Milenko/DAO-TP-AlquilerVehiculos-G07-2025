from typing import Optional, List
import datetime

from data_access.database_connector import Database
from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.state import State
from services.utils import datetime_to_iso, iso_to_datetime, validate_positive_int, validate_string


class VehiculoRepository:
    def __init__(self, db: Optional[Database] = None, state: State = State):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")
        self.IState = state

    def _validate_vehiculo(self, vehiculo: Vehiculo) -> Optional[str]:
        error = validate_positive_int(vehiculo.id_modelo, 'id_modelo')
        if error: return error
        error = validate_string(vehiculo.patente, 'patente', max_length=20)
        if error: return error
        error = validate_string(vehiculo.nro_chasis, 'nro_chasis', max_length=20)
        if error: return error
        error = validate_positive_int(vehiculo.id_color, 'id_color')
        if error: return error
        if vehiculo.anio_fabricacion is not None and not isinstance(vehiculo.anio_fabricacion, datetime.datetime):
            return "Invalid 'anio_fabricacion' — must be a datetime object or None"
        if not isinstance(vehiculo.precio_base, (float, int)) or vehiculo.precio_base <= 0:
            return "Invalid 'precio_base' — must be a positive number"

        print("Validating id_estado:", vehiculo.id_estado)
        error = validate_positive_int(vehiculo.id_estado, 'id_estado')
        if error: return error

        return None

    def _row_to_vehiculo(self, row) -> Vehiculo | None:
        if row is None: return None
        print(row)
        return Vehiculo(
            id=row[0],
            id_modelo=row[1],
            patente=row[2],
            nro_chasis=row[3],
            id_color=row[4],
            anio_fabricacion=iso_to_datetime(row[5]),
            precio_base=row[6],
            id_estado=row[7],
        )

    def create(self, vehiculo: Vehiculo) -> Optional[int]:
        validation_error = self._validate_vehiculo(vehiculo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        print(vehiculo.get_state().__class__.__name__)

        try:
            anio_fabricacion_iso = datetime_to_iso(vehiculo.anio_fabricacion)

            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id
                    FROM Vehiculo
                    WHERE patente = ?
                       OR nro_chasis = ?
                    """,
                    (vehiculo.patente, vehiculo.nro_chasis),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Vehiculo already exists with id {existing[0]} (duplicate patente or chasis)")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Vehiculo (id_modelo, patente, nro_chasis, Color, año_fabricacion, precio_base,
                                          id_estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        vehiculo.id_modelo,
                        vehiculo.patente,
                        vehiculo.nro_chasis,
                        vehiculo.id_color,
                        anio_fabricacion_iso,
                        vehiculo.precio_base,
                        vehiculo.id_estado,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating vehiculo: {e}")
            raise

    def get_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id,
                           id_modelo,
                           patente,
                           nro_chasis,
                           color,
                           año_fabricacion,
                           precio_base,
                           id_estado
                    FROM Vehiculo
                    WHERE id = ?
                    """,
                    (vehiculo_id,),
                )
                row = cur.fetchone()
                return self._row_to_vehiculo(row)
        except Exception as e:
            print(f"Error retrieving vehiculo by id: {e}")
            raise

    def list_all(self) -> List[Vehiculo]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_modelo, patente, nro_chasis, color, año_fabricacion, precio_base, id_estado
                    FROM Vehiculo ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_vehiculo(r) for r in rows]
        except Exception as e:
            print(f"Error listing all vehiculos: {e}")
            raise

    def update(self, vehiculo: Vehiculo) -> bool:
        validation_error = self._validate_vehiculo(vehiculo)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False
        anio_fabricacion_iso = datetime_to_iso(vehiculo.anio_fabricacion)

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM Vehiculo
                    WHERE (patente = ? OR nro_chasis = ?) AND id != ?
                    """,
                    (vehiculo.patente, vehiculo.nro_chasis, vehiculo.id),
                )
                if cur.fetchone():
                    print("Validation failed: Updated patente or nro_chasis already exists on another vehicle.")
                    return False

                cur.execute(
                    """
                    UPDATE Vehiculo
                    SET id_modelo = ?, patente = ?, nro_chasis = ?, color = ?, año_fabricacion = ?, precio_base = ?, id_estado = ?
                    WHERE id = ?
                    """,
                    (
                        vehiculo.id_modelo,
                        vehiculo.patente,
                        vehiculo.nro_chasis,
                        vehiculo.id_color,
                        anio_fabricacion_iso,
                        vehiculo.precio_base,
                        vehiculo.id_estado,
                        vehiculo.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating vehiculo: {e}")
            raise

    def delete(self, vehiculo_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Vehiculo WHERE id = ?", (vehiculo_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting vehiculo: {e}")
            raise

    def _desechar_vehiculo(self, vehiculo_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Vehiculo
                    SET id_estado = (SELECT id FROM Estado WHERE nombre = 'DESECHADO' LIMIT 1)
                    WHERE id = ?
                    """,
                    (vehiculo_id,),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error desechando vehiculo: {e}")
            raise

    def _fuerza_de_servicio_vehiculo(self, vehiculo_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Vehiculo
                    SET id_estado = (SELECT id FROM Estado WHERE nombre = 'FUERA_DE_SERVICIO' LIMIT 1)
                    WHERE id = ?
                    """,
                    (vehiculo_id,),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error poniendo fuera de servicio el vehiculo: {e}")
            raise

    def get_estado_actual(self, vehiculo_id: int) -> Optional[int]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id_estado
                    FROM Vehiculo
                    WHERE id = ?
                    """,
                    (vehiculo_id,),
                )
                row = cur.fetchone()
                if row:
                    return row
                return None
        except Exception as e:
            print(f"Error obteniendo estado actual del vehiculo: {e}")
            raise
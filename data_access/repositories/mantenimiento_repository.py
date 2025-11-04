from typing import Optional, List
from data_access.database_connector import Database
from domain.models.mantenimiento import Mantenimiento
from services.utils import validate_positive_int, validate_non_negative_number, validate_string, iso_to_datetime, \
    datetime_to_iso


class MantenimientoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_mantenimiento(self, mantenimiento: Mantenimiento) -> Optional[str]:
        error = validate_positive_int(mantenimiento.id_vehiculo, 'id_vehiculo')
        if error: return error
        error = validate_non_negative_number(mantenimiento.costo, 'costo')
        if error: return error
        error = validate_string(mantenimiento.descripcion, 'descripcion')
        if error: return error
        error = validate_positive_int(mantenimiento.id_estado, 'id_estado')
        if error: return error
        error = validate_positive_int(mantenimiento.id_empleado, 'id_empleado')
        if error: return error
        return None

    def _row_to_mantenimiento(self, row) -> Mantenimiento | None:
        if row is None: return None
        return Mantenimiento(
            id=row[0],
            id_vehiculo=row[1],
            costo=row[2],
            descripcion=row[3],
            id_estado=row[4],
            id_empleado=row[5],
            fecha_hora=iso_to_datetime(row[6]),
        )

    def create(self, mantenimiento: Mantenimiento) -> Optional[int]:
        validation_error = self._validate_mantenimiento(mantenimiento)
        if validation_error: return None
        try:
            fecha_hora_iso = datetime_to_iso(mantenimiento.fecha_hora)

            with self._db.transaction() as cur:
                # ...
                cur.execute(
                    """
                    INSERT INTO Mantenimiento (id_vehiculo, costo, descripcion, id_estado, id_empleado, fecha_hora)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (mantenimiento.id_vehiculo, mantenimiento.costo, mantenimiento.descripcion, mantenimiento.id_estado,
                     mantenimiento.id_empleado, fecha_hora_iso),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating mantenimiento: {e}")
            raise

    def get_by_id(self, mantenimiento_id: int) -> Optional[Mantenimiento]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_vehiculo, costo, descripcion, id_estado, id_empleado, fecha_hora
                    FROM Mantenimiento WHERE id = ?
                    """,
                    (mantenimiento_id,),
                )
                row = cur.fetchone()
                return self._row_to_mantenimiento(row)
        except Exception as e:
            print(f"Error retrieving mantenimiento by id: {e}")
            raise

    def list_all(self) -> List[Mantenimiento]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_vehiculo, costo, descripcion, id_estado, id_empleado, fecha_hora
                    FROM Mantenimiento ORDER BY fecha_hora DESC
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_mantenimiento(r) for r in rows]
        except Exception as e:
            print(f"Error listing all mantenimientos: {e}")
            raise

    def update(self, mantenimiento: Mantenimiento) -> bool:
        validation_error = self._validate_mantenimiento(mantenimiento)
        if validation_error: return False
        fecha_hora_iso = datetime_to_iso(mantenimiento.fecha_hora)
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Mantenimiento
                    SET id_vehiculo = ?, costo = ?, descripcion = ?, id_estado = ?, id_empleado = ?, fecha_hora = ?
                    WHERE id = ?
                    """,
                    (mantenimiento.id_vehiculo, mantenimiento.costo, mantenimiento.descripcion, mantenimiento.id_estado, mantenimiento.id_empleado, fecha_hora_iso, mantenimiento.id),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating mantenimiento: {e}")
            raise

    def delete(self, mantenimiento_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Mantenimiento WHERE id = ?", (mantenimiento_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting mantenimiento: {e}")
            raise
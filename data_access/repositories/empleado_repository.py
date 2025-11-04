from typing import Optional, List
from data_access.database_connector import Database
from domain.models.empleado import Empleado
from services.utils import iso_to_datetime, validate_positive_int, datetime_to_iso


class EmpleadoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_empleado(self, empleado: Empleado) -> Optional[str]:
        error = validate_positive_int(empleado.id_tipo_puesto, 'id_tipo_puesto')
        if error: return error
        error = validate_positive_int(empleado.id_persona, 'id_persona')
        if error: return error
        # La validación de fechas (tipo datetime.datetime) se mantiene manual o con una utility de fecha más específica.
        return None

    def _row_to_empleado(self, row) -> Empleado | None:
        if row is None: return None
        return Empleado(
            id=row[0],
            id_tipo_puesto=row[1],
            id_persona=row[2],
            fecha_ingreso=iso_to_datetime(row[3]),
            fecha_egreso=iso_to_datetime(row[4]),
        )

    def create(self, empleado: Empleado) -> Optional[int]:
        validation_error = self._validate_empleado(empleado)
        if validation_error: return None
        try:
            fecha_ingreso_iso = datetime_to_iso(empleado.fecha_ingreso)
            fecha_egreso_iso = datetime_to_iso(empleado.fecha_egreso)

            with self._db.transaction() as cur:
                # Check for existing empleado by id_persona
                cur.execute(
                    """
                    SELECT id FROM Empleado
                    WHERE id_persona = ?
                    """,
                    (empleado.id_persona,),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Empleado already exists for persona id {empleado.id_persona} with empleado id {existing[0]}")
                    return existing[0]

                cur.execute(
                    """
                    INSERT INTO Empleado (id_tipoPuesto, id_persona, fecha_ingreso, fecha_egreso)
                    VALUES (?, ?, ?, ?)
                    """,
                    (empleado.id_tipo_puesto, empleado.id_persona, fecha_ingreso_iso, fecha_egreso_iso),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating empleado: {e}")
            raise

    def get_by_id(self, empleado_id: int) -> Optional[Empleado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_tipoPuesto, id_persona, fecha_ingreso, fecha_egreso
                    FROM Empleado WHERE id = ?
                    """,
                    (empleado_id,),
                )
                row = cur.fetchone()
                return self._row_to_empleado(row)
        except Exception as e:
            print(f"Error retrieving empleado by id: {e}")
            raise

    def list_all(self) -> List[Empleado]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_tipoPuesto, id_persona, fecha_ingreso, fecha_egreso
                    FROM Empleado ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_empleado(r) for r in rows]
        except Exception as e:
            print(f"Error listing all empleados: {e}")
            raise

    def update(self, empleado: Empleado) -> bool:
        # [MODIFICADO] Uso de datetime_to_iso
        validation_error = self._validate_empleado(empleado)
        if validation_error: return False
        fecha_ingreso_iso = datetime_to_iso(empleado.fecha_ingreso)
        fecha_egreso_iso = datetime_to_iso(empleado.fecha_egreso)

        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Empleado
                    SET id_tipoPuesto = ?,
                        id_persona     = ?,
                        fecha_ingreso  = ?,
                        fecha_egreso   = ?
                    WHERE id = ?
                    """,
                    (empleado.id_tipo_puesto, empleado.id_persona, fecha_ingreso_iso, fecha_egreso_iso, empleado.id),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating empleado: {e}")
            raise

    def delete(self, empleado_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Empleado WHERE id = ?", (empleado_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting empleado: {e}")
            raise
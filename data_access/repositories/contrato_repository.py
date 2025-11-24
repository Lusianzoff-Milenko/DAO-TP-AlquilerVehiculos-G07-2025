from typing import Optional, List
from data_access.database_connector import Database
from domain.models.contrato import Contrato
from services.utils import datetime_to_iso, iso_to_datetime, validate_positive_int, validate_boolean, validate_fecha_rango


class ContratoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_contrato(self, contrato: Contrato) -> Optional[str]:
        error = validate_positive_int(contrato.id_cliente, 'id_cliente')
        if error: return error
        error = validate_positive_int(contrato.id_metodo_de_pago, 'id_metodo_de_pago')
        if error: return error
        error = validate_positive_int(contrato.id_empleado, 'id_empleado')
        if error: return error
        error = validate_positive_int(contrato.id_estado, 'id_estado')
        if error: return error
        error = validate_boolean(contrato.tiene_seguro, 'tiene_seguro')
        if error: return error
        error = validate_fecha_rango(contrato.fecha_desde, contrato.fecha_hasta)
        if error: return error
        return None

    def _row_to_contrato(self, row) -> Contrato | None:
        if row is None: return None
        return Contrato(
            id=row[0],
            id_cliente=row[1],
            fecha_desde=iso_to_datetime(row[2]),
            fecha_hasta=iso_to_datetime(row[3]),
            id_metodo_de_pago=row[4],
            id_empleado=row[5],
            id_estado=row[6],
            tiene_seguro=bool(row[7]),
        )

    def create(self, contrato: Contrato) -> Optional[int]:
        validation_error = self._validate_contrato(contrato)
        if validation_error: return None
        try:
            fecha_desde_iso = datetime_to_iso(contrato.fecha_desde)
            fecha_hasta_iso = datetime_to_iso(contrato.fecha_hasta)
            with self._db.transaction() as cur:
                # ...
                cur.execute(
                    """
                    INSERT INTO Contrato (id_cliente, fecha_desde, fecha_hasta, id_metodoDePago, id_empleado, id_estado, tiene_seguro)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (contrato.id_cliente, fecha_desde_iso, fecha_hasta_iso, contrato.id_metodo_de_pago, contrato.id_empleado, contrato.id_estado, 1 if contrato.tiene_seguro else 0),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating contrato: {e}")
            raise

    def get_by_id(self, contrato_id: int) -> Optional[Contrato]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_cliente, fecha_desde, fecha_hasta, id_metodoDePago, id_empleado, id_estado, tiene_seguro
                    FROM Contrato WHERE id = ?
                    """,
                    (contrato_id,),
                )
                row = cur.fetchone()
                return self._row_to_contrato(row)
        except Exception as e:
            print(f"Error retrieving contrato by id: {e}")
            raise

    def list_all(self) -> List[Contrato]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_cliente, fecha_desde, fecha_hasta, id_metodoDePago, id_empleado, id_estado, tiene_seguro
                    FROM Contrato ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_contrato(r) for r in rows]
        except Exception as e:
            print(f"Error listing all contratos: {e}")
            raise

    def update(self, contrato: Contrato) -> bool:
        validation_error = self._validate_contrato(contrato)
        if validation_error: return False
        fecha_desde_iso = datetime_to_iso(contrato.fecha_desde)
        fecha_hasta_iso = datetime_to_iso(contrato.fecha_hasta)
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Contrato
                    SET id_cliente = ?,, fecha_desde = ?, fecha_hasta = ?, id_metodoDePago = ?, id_empleado = ?, id_estado = ?, tiene_seguro = ?
                    WHERE id = ?
                    """,
                    (contrato.id_cliente, fecha_desde_iso, fecha_hasta_iso, contrato.id_metodo_de_pago, contrato.id_empleado, contrato.id_estado, 1 if contrato.tiene_seguro else 0, contrato.id),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating contrato: {e}")
            raise

    def delete(self, contrato_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Contrato WHERE id = ?", (contrato_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting contrato: {e}")
            raise

    def has_active_contracts(self, name, empleado_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*) FROM Contrato
                    WHERE id_empleado = ? AND id_estado = (
                        SELECT id FROM Estado WHERE nombre = 'Activo'
                    )
                    """,
                    (empleado_id,),
                )
                count = cur.fetchone()[0]
                return count > 0
        except Exception as e:
            print(f"Error checking active contracts for {name} ID {empleado_id}: {e}")
            raise
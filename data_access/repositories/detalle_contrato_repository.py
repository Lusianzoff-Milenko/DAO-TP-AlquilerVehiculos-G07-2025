from typing import Optional, List
import datetime
from data_access.database_connector import Database
from domain.models.detalle_contrato import DetalleContrato
from services.utils import datetime_to_iso, iso_to_datetime, validate_non_negative_number, validate_positive_int


# Assuming Contrato model exists

class DetalleContratoRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_detalle_contrato(self, detalle_contrato: DetalleContrato) -> Optional[str]:
        error = validate_positive_int(detalle_contrato.id_contrato, 'id_contrato')
        if error: return error
        error = validate_non_negative_number(detalle_contrato.monto, 'monto')
        if error: return error
        error = validate_positive_int(detalle_contrato.id_vehiculo, 'id_vehiculo')
        if error: return error
        if not isinstance(detalle_contrato.fecha_entrega, datetime.datetime):
            return "Invalid 'fecha_entrega' — must be a datetime object"
        if not isinstance(detalle_contrato.fecha_retiro, datetime.datetime):
            return "Invalid 'fecha_retiro' — must be a datetime object"
        return None

    def _row_to_detalle_contrato(self, row) -> DetalleContrato | None:
        if row is None: return None
        return DetalleContrato(
            id=row[0],
            id_contrato=row[1],
            id_vehiculo=row[2],
            monto=row[3],
            fecha_entrega=iso_to_datetime(row[4]),
            fecha_retiro=iso_to_datetime(row[5]),
        )

    def create(self, detalle_contrato: DetalleContrato) -> Optional[int]:
        validation_error = self._validate_detalle_contrato(detalle_contrato)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            fecha_entrega_iso = datetime_to_iso(detalle_contrato.fecha_entrega)
            fecha_retiro_iso = datetime_to_iso(detalle_contrato.fecha_retiro)

            with self._db.transaction() as cur:
                cur.execute(
                    """
                    INSERT INTO DetalleContrato (id_contrato, id_vehiculo, monto, fecha_entrega, fecha_retiro)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        detalle_contrato.id_contrato,
                        detalle_contrato.id_vehiculo,
                        detalle_contrato.monto,
                        fecha_entrega_iso,
                        fecha_retiro_iso,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating detalle_contrato: {e}")
            raise

    def get_by_id(self, detalle_contrato_id: int) -> Optional[DetalleContrato]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_contrato, id_vehiculo, monto, fecha_entrega, fecha_retiro
                    FROM DetalleContrato WHERE id = ?
                    """,
                    (detalle_contrato_id,),
                )
                row = cur.fetchone()
                return self._row_to_detalle_contrato(row)
        except Exception as e:
            print(f"Error retrieving detalle_contrato by id: {e}")
            raise

    def list_all(self) -> List[DetalleContrato]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, id_contrato, id_vehiculo, monto, fecha_entrega, fecha_retiro
                    FROM DetalleContrato ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_detalle_contrato(r) for r in rows]
        except Exception as e:
            print(f"Error listing all detalle_contratos: {e}")
            raise

    def update(self, detalle_contrato: DetalleContrato) -> bool:
        validation_error = self._validate_detalle_contrato(detalle_contrato)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return False
        fecha_entrega_iso = datetime_to_iso(detalle_contrato.fecha_entrega)
        fecha_retiro_iso = datetime_to_iso(detalle_contrato.fecha_retiro)
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE DetalleContrato
                    SET id_contrato = ?, id_vehiculo = ?, monto = ?, fecha_entrega = ?, fecha_retiro = ?
                    WHERE id = ?
                    """,
                    (
                        detalle_contrato.id_contrato,
                        detalle_contrato.id_vehiculo,
                        detalle_contrato.monto,
                        fecha_entrega_iso,
                        fecha_retiro_iso,
                        detalle_contrato.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating detalle_contrato: {e}")
            raise

    def delete(self, detalle_contrato_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM DetalleContrato WHERE id = ?", (detalle_contrato_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting detalle_contrato: {e}")
            raise
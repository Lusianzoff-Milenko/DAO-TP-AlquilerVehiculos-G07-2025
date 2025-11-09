from typing import Optional, List
from services import utils
import datetime
from data_access.database_connector import Database
from domain.models.persona import Persona


class PersonaRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _validate_persona(self, persona: Persona) -> Optional[str]:
        if not persona.nombre or not persona.apellido:
            return "Nombre y apellido son obligatorios."
        if persona.mail and "@" not in persona.mail:
            return "Mail inválido."
        if persona.fecha_nacimiento and persona.fecha_nacimiento > datetime.datetime.now():
            return "Fecha de nacimiento no puede ser en el futuro."
        return None

    def _row_to_persona(self, row) -> Persona | None:
        if row is None:
            return None
        fecha = None
        if row[6] is not None:
            try:
                fecha = utils.iso_to_datetime(row[6])
            except Exception:
                fecha = None
        return Persona(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            telefono=row[3],
            mail=row[4],
            direccion=row[5],
            fecha_nacimiento=fecha
        )

    def create(self, persona: Persona) -> Optional[int]:
        validation_error = self._validate_persona(persona)
        if validation_error:
            print(f"Validation failed: {validation_error}")
            return None

        try:
            fecha_iso = (
                persona.fecha_nacimiento.isoformat() if persona.fecha_nacimiento else None
            )
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id FROM Persona
                    WHERE (mail IS NOT NULL AND mail = ?)
                       OR (nombre = ? AND apellido = ? AND (fecha_nacimiento IS ? OR fecha_nacimiento = ?))
                    """,
                    (persona.mail, persona.nombre, persona.apellido, None if fecha_iso is None else fecha_iso, fecha_iso),
                )
                existing = cur.fetchone()
                if existing:
                    print(f"Persona already exists with id {existing[0]}")
                    return existing[0]
                cur.execute(
                    """
                    INSERT INTO Persona (nombre, apellido, telefono, mail, direccion, fecha_nacimiento)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        persona.nombre,
                        persona.apellido,
                        persona.telefono,
                        persona.mail,
                        persona.direccion,
                        fecha_iso,
                    ),
                )
                return cur.lastrowid
        except Exception as e:
            print(f"Error creating persona: {e}")
            raise

    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, apellido, telefono, mail, direccion, fecha_nacimiento
                    FROM Persona WHERE id = ?
                    """,
                    (persona_id,),
                )
                row = cur.fetchone()
                return self._row_to_persona(row)
        except Exception as e:
            print(f"Error retrieving persona by id: {e}")
            raise

    def list_all(self) -> List[Persona]:
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, apellido, telefono, mail, direccion, fecha_nacimiento
                    FROM Persona ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [self._row_to_persona(r) for r in rows]
        except Exception as e:
            print(f"Error listing all personas: {e}")
            raise

    def update(self, persona: Persona) -> bool:
        fecha_iso = (
            persona.fecha_nacimiento.isoformat() if persona.fecha_nacimiento else None
        )
        try:
            with self._db.transaction() as cur:
                cur.execute(
                    """
                    UPDATE Persona
                    SET nombre = ?, apellido = ?, telefono = ?, mail = ?, direccion = ?, fecha_nacimiento = ?
                    WHERE id = ?
                    """,
                    (
                        persona.nombre,
                        persona.apellido,
                        persona.telefono,
                        persona.mail,
                        persona.direccion,
                        fecha_iso,
                        persona.id,
                    ),
                )
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating persona: {e}")
            raise

    def delete(self, persona_id: int) -> bool:
        try:
            with self._db.transaction() as cur:
                cur.execute("DELETE FROM Persona WHERE id = ?", (persona_id,))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting persona: {e}")
            raise

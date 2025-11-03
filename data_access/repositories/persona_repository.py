from typing import Optional, List
import datetime

from data_access.database_connector import Database
from domain.models.persona import Persona


class PersonaRepository:
    def __init__(self, db: Optional[Database] = None):
        self._db = db or Database("./alquiler_vehiculos_data_base.db")

    def _row_to_persona(self, row) -> Persona:
        # row order: id, nombre, apellido, telefono, mail, direccion, fecha_nacimiento
        if row is None:
            return None
        fecha = None
        if row[6] is not None:
            try:
                fecha = datetime.datetime.fromisoformat(row[6])
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

    def create(self, persona: Persona) -> int:
        fecha_iso = (
            persona.fecha_nacimiento.isoformat() if persona.fecha_nacimiento else None
        )
        with self._db.transaction() as cur:
            # Check for existing persona by mail OR by (nombre, apellido, fecha_nacimiento)
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
            else:
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
                print(f"Creating new persona with id {cur.lastrowid}")
                return cur.lastrowid

    def get_by_id(self, persona_id: int) -> Optional[Persona]:
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

    def list_all(self) -> List[Persona]:
        with self._db.transaction() as cur:
            cur.execute(
                """
                SELECT id, nombre, apellido, telefono, mail, direccion, fecha_nacimiento
                FROM Persona ORDER BY id
                """
            )
            rows = cur.fetchall()
            return [self._row_to_persona(r) for r in rows]

    def update(self, persona: Persona) -> bool:
        fecha_iso = (
            persona.fecha_nacimiento.isoformat() if persona.fecha_nacimiento else None
        )
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

    def delete(self, persona_id: int) -> bool:
        with self._db.transaction() as cur:
            cur.execute("DELETE FROM Persona WHERE id = ?", (persona_id,))
            return cur.rowcount > 0

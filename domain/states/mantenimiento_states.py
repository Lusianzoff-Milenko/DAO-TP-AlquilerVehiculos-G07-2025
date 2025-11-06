from .base_state import BaseState
from typing import Type, Dict

# IDs de la DB (según tu análisis)
ID_MANTENIMIENTO_EN_DIAGNOSTICO = 12
ID_MANTENIMIENTO_EN_REPARACION = 13
ID_MANTENIMIENTO_REPARADO = 14
ID_MANTENIMIENTO_NO_REPARADO = 15

# --- Estados Concretos (Definidos anteriormente) ---

class MantenimientoBaseState(BaseState):
    """Define la interfaz de métodos de transición para Mantenimiento."""
    def new(self): self._invalid_transition("new()")
    def diagnosticar(self): self._invalid_transition("diagnosticar()")
    def reparar(self): self._invalid_transition("reparar()")
    def entregar(self): self._invalid_transition("entregar()")

class MantenimientoNew(MantenimientoBaseState):
    def get_db_id(self) -> int: return None
    def get_name(self) -> str: return "Inicio"
    def new(self): self._transition_to(MantenimientoEnDiagnostico)

class MantenimientoEnDiagnostico(MantenimientoBaseState):
    def get_db_id(self) -> int: return ID_MANTENIMIENTO_EN_DIAGNOSTICO
    def get_name(self) -> str: return "En Diagnóstico"
    def diagnosticar(self): self._transition_to(MantenimientoEnReparacion)
# ... (otras clases de estado MantenimientoEnReparacion, MantenimientoReparado, etc.) ...

# Clase de estado para IDs no reconocidos
class MantenimientoUnknownState(MantenimientoBaseState):
    def get_db_id(self) -> int: return -1
    def get_name(self) -> str: return "Desconocido/Error"


class MantenimientoEnDiagnostico(MantenimientoBaseState):
    def get_db_id(self) -> int: return ID_MANTENIMIENTO_EN_DIAGNOSTICO

    def get_name(self) -> str: return "En Diagnóstico"

    def diagnosticar(self):
        # Transición: en diagnostico -> en reparacion
        self._transition_to(MantenimientoEnReparacion)


class MantenimientoEnReparacion(MantenimientoBaseState):
    def get_db_id(self) -> int:
        return ID_MANTENIMIENTO_EN_REPARACION

    def get_name(self) -> str:
        return "En Reparación"

    def reparar(self, success: bool):
        # Transición: en reparacion -> (reparado | no reparado)
        if success:
            self._transition_to(MantenimientoReparado)
        else:
            self._transition_to(MantenimientoNoReparado)


class MantenimientoReparado(MantenimientoBaseState):
    def get_db_id(self) -> int: return ID_MANTENIMIENTO_REPARADO

    def get_name(self) -> str: return "Reparado"

    def entregar(self):
        # Reparado -> Fin (Se asume que la entidad Mantenimiento termina su ciclo)
        self._transition_to(MantenimientoFin)


class MantenimientoNoReparado(MantenimientoBaseState):
    def get_db_id(self) -> int: return ID_MANTENIMIENTO_NO_REPARADO

    def get_name(self) -> str: return "No Reparado"

    def entregar(self):
        # No Reparado -> Fin
        self._transition_to(MantenimientoFin)


class MantenimientoFin(MantenimientoBaseState):
    # Estado final sin ID de DB (la entidad queda con el ID anterior: 14 o 15)
    # Se usa como marcador para la máquina de estados.
    def get_db_id(self) -> int: return None

    def get_name(self) -> str: return "Fin del Proceso"

# --- MAPEO DE LA BASE DE DATOS A CLASES ---

MANTENIMIENTO_STATE_MAPPING: Dict[int, Type[MantenimientoBaseState]] = {
    ID_MANTENIMIENTO_EN_DIAGNOSTICO: MantenimientoEnDiagnostico,
    ID_MANTENIMIENTO_EN_REPARACION: MantenimientoEnReparacion,
    ID_MANTENIMIENTO_REPARADO: MantenimientoReparado,
    ID_MANTENIMIENTO_NO_REPARADO: MantenimientoNoReparado,
}
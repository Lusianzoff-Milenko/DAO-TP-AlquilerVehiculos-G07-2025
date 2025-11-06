from .base_state import BaseState
from typing import Type, Dict

# IDs de la DB (según tu análisis)
ID_VEHICULO_DISPONIBLE = 5
ID_VEHICULO_RESERVADO = 6
ID_VEHICULO_ALQUILADO = 7
ID_VEHICULO_ENTREGADO = 8
ID_VEHICULO_EN_REVISION = 9
ID_VEHICULO_EN_MANTENIMIENTO = 10
ID_VEHICULO_FUERA_DE_SERVICIO = 11
ID_VEHICULO_DESECHADO = 16

# --- Estados Concretos (Definidos anteriormente) ---

class VehiculoBaseState(BaseState):
    """Define la interfaz de métodos de transición para Vehiculo."""
    # ... (métodos de transición: reservar, retirar, entregar, etc.) ...
    def reservar(self): self._invalid_transition("reservar()")
    def retirar(self): self._invalid_transition("retirar()")
    def entregar(self): self._invalid_transition("entregar()")
    def marcar_no_devolucion(self): self._invalid_transition("marcarNoDevolucion()")
    def mover_a_revision(self): self._invalid_transition("moverARevision()")
    def iniciar_mantenimiento(self): self._invalid_transition("iniciarMantenimiento()")
    def reincorporar(self): self._invalid_transition("reincorporar()")
    def marcar_fuera_de_servicio(self): self._invalid_transition("marcarFueraDeServicio()")
    def desechar(self): self._invalid_transition("desechar()")

class VehiculoDisponible(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_DISPONIBLE
    def get_name(self) -> str: return "Disponible"
    def reservar(self): self._transition_to(VehiculoReservado)
    def iniciar_mantenimiento(self): self._transition_to(VehiculoEnMantenimiento)
# ... (otras clases de estado VehiculoReservado, VehiculoAlquilado, etc.) ...

# Clase de estado para IDs no reconocidos
class VehiculoUnknownState(VehiculoBaseState):
    def get_db_id(self) -> int: return -1
    def get_name(self) -> str: return "Desconocido/Error"


class VehiculoReservado(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_RESERVADO

    def get_name(self) -> str: return "Reservado"

    def retirar(self):
        # Transición: reservado -> alquilado
        self._transition_to(VehiculoAlquilado)

    def cancelar_reserva(self):
        # Transición: reservado -> disponible (según el diagrama)
        self._transition_to(VehiculoDisponible)


class VehiculoAlquilado(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_ALQUILADO

    def get_name(self) -> str: return "Alquilado"

    def entregar(self):
        # Transición: alquilado -> entregado
        self._transition_to(VehiculoEntregado)

    def marcar_no_devolucion(self):
        # Transición: alquilado -> fuera de servicio
        self._transition_to(VehiculoFueraDeServicio)


class VehiculoEntregado(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_ENTREGADO

    def get_name(self) -> str: return "Entregado"

    def mover_a_revision(self):
        # Transición: entregado -> en revisión
        self._transition_to(VehiculoEnRevision)

    def iniciar_mantenimiento(self):
        # Transición: entregado -> en mantenimiento
        self._transition_to(VehiculoEnMantenimiento)


class VehiculoEnRevision(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_EN_REVISION

    def get_name(self) -> str: return "En Revisión"

    def reincorporar(self):
        # Transición: en revisión -> disponible
        self._transition_to(VehiculoDisponible)

    def marcar_fuera_de_servicio(self):
        # Transición: en revisión -> fuera de servicio
        self._transition_to(VehiculoFueraDeServicio)


class VehiculoEnMantenimiento(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_EN_MANTENIMIENTO

    def get_name(self) -> str: return "En Mantenimiento"

    def reincorporar(self):
        # Transición: en mantenimiento -> disponible
        self._transition_to(VehiculoDisponible)

    def marcar_fuera_de_servicio(self):
        # Transición: en mantenimiento -> fuera de servicio
        self._transition_to(VehiculoFueraDeServicio)


class VehiculoFueraDeServicio(VehiculoBaseState):
    def get_db_id(self) -> int: return ID_VEHICULO_FUERA_DE_SERVICIO

    def get_name(self) -> str: return "Fuera de Servicio"

    def desechar(self):
        # Transición: fuera de servicio -> desechado (Fin)
        self._transition_to(VehiculoDesechado)


class VehiculoDesechado(VehiculoBaseState):
    # [Clase que faltaba en el mapeo]
    def get_db_id(self) -> int: return ID_VEHICULO_DESECHADO

    def get_name(self) -> str: return "Desechado"
    # No hay transiciones de salida

# --- MAPEO DE LA BASE DE DATOS A CLASES ---

VEHICULO_STATE_MAPPING: Dict[int, Type[VehiculoBaseState]] = {
    ID_VEHICULO_DISPONIBLE: VehiculoDisponible,
    ID_VEHICULO_RESERVADO: VehiculoReservado,
    ID_VEHICULO_ALQUILADO: VehiculoAlquilado,
    ID_VEHICULO_ENTREGADO: VehiculoEntregado,
    ID_VEHICULO_EN_REVISION: VehiculoEnRevision,
    ID_VEHICULO_EN_MANTENIMIENTO: VehiculoEnMantenimiento,
    ID_VEHICULO_FUERA_DE_SERVICIO: VehiculoFueraDeServicio,
    ID_VEHICULO_DESECHADO: VehiculoDesechado,
}
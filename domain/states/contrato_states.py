# python
# file: `domain/states/contrato_states.py`
from .base_state import BaseState
from typing import Type, Dict

# IDs de la DB (según tu análisis)
ID_CONTRATO_RESERVADO = 1
ID_CONTRATO_EN_CURSO  = 2
ID_CONTRATO_CANCELADO = 3
ID_CONTRATO_ENTREGADO = 4

# ----------------------------------------------------------------------
# CLASES DE ESTADO (las mismas que definimos antes)
# ----------------------------------------------------------------------

class ContratoBaseState(BaseState):
    """Define la interfaz de métodos de transición para Contrato."""
    def tomar_pago(self): self._invalid_transition("tomarPago()")
    def tomar_retiro(self): self._invalid_transition("tomarRetiro()")
    def recibir_devolucion(self): self._invalid_transition("recibirDevolucion()")
    def cancelar(self): self._invalid_transition("cancelar()")
    def renovar(self): self._invalid_transition("renovar()")

class ContratoNew(ContratoBaseState):
    def get_db_id(self) -> int: return None
    def get_name(self) -> str: return "Inicio"
    def tomar_pago(self): self._transition_to(ContratoReservado)

class ContratoReservado(ContratoBaseState):
    def get_db_id(self) -> int: return ID_CONTRATO_RESERVADO
    def get_name(self) -> str: return "Reservado"
    def tomar_retiro(self): self._transition_to(ContratoEnCurso)
    def cancelar(self): self._transition_to(ContratoCancelado)

class ContratoEnCurso(ContratoBaseState):
    def get_db_id(self) -> int: return ID_CONTRATO_EN_CURSO
    def get_name(self) -> str: return "En Curso"
    def recibir_devolucion(self): self._transition_to(ContratoEntregado)
    def cancelar(self): self._transition_to(ContratoCancelado)
    def renovar(self): print("Contrato renovado (fecha extendida). Estado no cambia.")

class ContratoEntregado(ContratoBaseState):
    def get_db_id(self) -> int: return ID_CONTRATO_ENTREGADO
    def get_name(self) -> str: return "Entregado"

class ContratoCancelado(ContratoBaseState):
    def get_db_id(self) -> int: return ID_CONTRATO_CANCELADO
    def get_name(self) -> str: return "Cancelado"

# --- MAPEO DE LA BASE DE DATOS A CLASES ---

# El tipo de dato para el mapa: {DB_ID: CLASE_DE_ESTADO}
CONTRATO_STATE_MAPPING: Dict[int, Type[ContratoBaseState]] = {
    ID_CONTRATO_RESERVADO: ContratoReservado,
    ID_CONTRATO_EN_CURSO: ContratoEnCurso,
    ID_CONTRATO_CANCELADO: ContratoCancelado,
    ID_CONTRATO_ENTREGADO: ContratoEntregado,
}

# Clase de estado por defecto para IDs no reconocidos o errores
class ContratoUnknownState(ContratoBaseState):
    def get_db_id(self) -> int: return -1
    def get_name(self) -> str: return "Desconocido/Error"
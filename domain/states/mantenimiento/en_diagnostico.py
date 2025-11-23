from domain.states.mantenimiento.en_reparacion import EnReparacion
from domain.states.mantenimiento.state import State


class EnDiagnostico(State):
    def diagnosticar(self) -> None:
        print("El mantenimiento ya está en diagnóstico.")

    def reparar(self) -> None:
        print("El diagnostico se realizo correctamente, el vehiculo pasara a reparacion.")
        self.context.transition_to(EnReparacion())

    def finalizar_reparacion(self) -> None:
        print("El mantenimiento no está en reparación, no se puede finalizar la reparación.")

    def marcar_irreparable(self) -> None:
        print("Un vehiculo en diagnostico no puede ser marcado como irreparable.")
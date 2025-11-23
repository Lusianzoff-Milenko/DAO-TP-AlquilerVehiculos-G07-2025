from domain.states.mantenimiento.reparado import Reparado
from domain.states.mantenimiento.state import State


class EnReparacion(State):
    def diagnosticar(self) -> None:
        print("El vehiculo ya fue diagnosticado. No se puede diagnosticar de nuevo.")

    def reparar(self) -> None:
        print("El vehiculo ya se encuentra en reparacion.")

    def finalizar_reparacion(self) -> None:
        print("El vehiculo fue reparado exitosamente. Cambiando estado a 'Finalizado'.")
        self.context.transition_to(Reparado())

    def marcar_irreparable(self) -> None:
        print("El vehiculo no se pudo reparar. Marcando como irreparable.")
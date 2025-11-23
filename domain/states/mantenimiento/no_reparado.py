from domain.states.mantenimiento.state import State


class NoReparado(State):
    def diagnosticar(self) -> None:
        print("El vehiculo no se puede reparar. Queda fuera de servicio.")

    def reparar(self) -> None:
        print("El vehiculo no se puede reparar. Queda fuera de servicio.")

    def finalizar_reparacion(self) -> None:
        print("El vehiculo no se puede reparar. Queda fuera de servicio.")

    def marcar_irreparable(self) -> None:
        print("El vehiculo ya ha sido marcado como irreparable.")
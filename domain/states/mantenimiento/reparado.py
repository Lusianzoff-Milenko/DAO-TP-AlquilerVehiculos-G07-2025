from domain.states.mantenimiento.state import State


class Reparado(State):
    def diagnosticar(self) -> None:
        print("El vehiculo ya fue reparado no es necesario diagnosticar")

    def reparar(self) -> None:
        print("El vehiculo ya fue reparado")

    def finalizar_reparacion(self) -> None:
        print("El vehiculo ya fue reparado")

    def marcar_irreparable(self) -> None:
        print("El vehiculo ya fue reparado")
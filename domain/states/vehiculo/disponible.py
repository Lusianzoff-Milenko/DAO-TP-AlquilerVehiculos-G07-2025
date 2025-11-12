from domain.states.vehiculo.state import State


class Disponible(State):

    def reservar(self) -> None:
        pass

    def retirar(self) -> None:
        pass

    def entregar(self) -> None:
        pass

    def mover_a_revision(self) -> None:
        pass

    def iniciar_mantenimiento(self) -> None:
        pass

    def reincorporar(self):
        pass

    def marcar_fuera_de_servicio(self) -> None:
        pass

    def marcar_no_devolucion(self) -> None:
        pass
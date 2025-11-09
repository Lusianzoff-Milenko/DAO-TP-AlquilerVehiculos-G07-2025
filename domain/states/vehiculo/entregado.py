from domain.states.vehiculo.state import State


class Entregado(State):
    def handle1(self) -> None:
        print("El vehículo ha sido entregado al cliente.")
        print("No puede ser entregado nuevamente hasta que se devuelva.")

    def handle2(self) -> None:
        print("El vehículo entregado ha sido devuelto y ahora está disponible.")
        # Aquí podrías agregar la transición a otro estado, como Disponible
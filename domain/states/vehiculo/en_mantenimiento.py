from domain.states.vehiculo.state import State


class EnMantenimiento(State):
    def handle1(self) -> None:
        print("El vehículo está en mantenimiento.")
        print("No puede ser alquilado o reservado hasta que se complete el mantenimiento.")

    def handle2(self) -> None:
        print("El mantenimiento del vehículo ha sido completado y ahora está disponible.")
        # Aquí podrías agregar la transición a otro estado, como Disponible
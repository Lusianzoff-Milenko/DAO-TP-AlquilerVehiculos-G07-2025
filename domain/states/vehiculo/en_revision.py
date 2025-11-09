from domain.states.vehiculo.state import State


class EnRevision(State):
    def handle1(self) -> None:
        print("El vehículo está en revisión.")
        print("No puede ser alquilado o reservado hasta que la revisión se complete.")

    def handle2(self) -> None:
        print("La revisión del vehículo ha sido completada y ahora está disponible.")
        # Aquí podrías agregar la transición a otro estado, como Disponible
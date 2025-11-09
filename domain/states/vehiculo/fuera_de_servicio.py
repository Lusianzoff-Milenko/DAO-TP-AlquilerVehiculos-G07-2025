from domain.states.vehiculo.state import State


class FueraDeServicio(State):
    def handle1(self) -> None:
        print("El vehículo está fuera de servicio.")
        print("No puede ser alquilado ni reservado hasta que se repare.")

    def handle2(self) -> None:
        print("El vehículo ha sido reparado y ahora está disponible.")
        # Aquí podrías agregar la transición a otro estado, como Disponible
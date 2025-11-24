from datetime import datetime
from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State


class Disponible(State):
    def reservar(self, contrato: Contrato) -> None:
        if contrato.fecha_desde.date().month == datetime.now().date().month and (contrato.fecha_desde.date().day - datetime.now().date().day) <= 3:
            print(f"El vehiculo ha sido reservado por el empleado {contrato.Empleado.Persona.nombre}, para el cliente {contrato.Cliente.persona.nombre}.")
            # 🚨 IMPORTACIÓN LOCAL
            from domain.states.vehiculo.reservado import Reservado
            self.context.transition_to(Reservado())

    def retirar(self, contrato: Contrato) -> None:
        if contrato.fecha_desde.date() == datetime.now().date() and contrato.fecha_hasta.hour <= datetime.now().hour:
            print("El vehiculo fue retirado de la playa de estacionamiento por el cliente.")
            # 🚨 IMPORTACIÓN LOCAL
            from domain.states.vehiculo.alquilado import Alquilado
            self.context.transition_to(Alquilado())

    def entregar(self) -> None:
        print("Un vehiculo disponible no puede ser entregado.")

    def mover_a_revision(self) -> None:
        print("Un vehiculo disponible no puede ser movido a revision.")

    def iniciar_mantenimiento(self) -> None:
        for mantenimiento in self.context.mantenimientos:
            if mantenimiento.get_last_maintenance() is not None:
                print("El vehiculo ha sido enviado a mantenimiento.")
                # 🚨 IMPORTACIÓN LOCAL
                from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
                self.context.transition_to(EnMantenimiento())

    def reincorporar(self, razon:str):
        print("El vehiculo ya se encuentra disponible.")

    def marcar_fuera_de_servicio(self) -> None:
        if self.context.anio_fabricacion.year > datetime.now().year - 15:
            print("El vehiculo ha sido marcado como fuera de servicio.")
            # 🚨 IMPORTACIÓN LOCAL
            from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
            self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        print("Un vehiculo disponible no puede ser marcado como no devolucion.")
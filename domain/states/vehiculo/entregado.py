from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State


class Entregado(State):
    def reservar(self, contrato: Contrato) -> None:
        print("El vehiculo no se encuentra disponible")

    def retirar(self, contrato: Contrato) -> None:
        print("El vehiculo no se encuentra disponible")

    def entregar(self) -> None:
        print("El vehiculo ya fue entregado.")

    def mover_a_revision(self) -> None:
        print("El vehiculo fue entrago y requiere revision de rutina.")
        # 🚨 IMPORTACIÓN LOCAL
        from domain.states.vehiculo.en_revision import EnRevision
        self.context.transition_to(EnRevision())

    # ... (resto de métodos iguales) ...
    def iniciar_mantenimiento(self) -> None:
        print("El vehiculo requiere ser revisado antes de iniciar mantenimiento.")

    def reincorporar(self, razon: str) -> None:
        print("El vehiculo requeire ser revisado antes de ser reincorporado.")

    def marcar_fuera_de_servicio(self) -> None:
        print("El vehiculo requiere ser revisado antes de ser marcado como fuera de servicio.")

    def marcar_no_devolucion(self) -> None:
        print("El vehiculo no puede ser marcado como no devolucion ya que fue entregado.")
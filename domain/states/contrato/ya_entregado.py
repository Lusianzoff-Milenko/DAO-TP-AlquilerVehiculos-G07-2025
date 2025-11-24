from datetime import datetime
from domain.states.contrato.state import State


class YaEntregado(State):
    """
    Estado terminal: El contrato finalizó con éxito.
    El cliente devolvió el vehículo.
    No permite ninguna transición adicional.
    """

    def tomar_pago(self, monto: float) -> bool:
        """
        No permitido: El contrato ya finalizó.
        """
        print("Error: El contrato ya fue entregado y finalizó. No se pueden registrar pagos.")
        return False

    def cancelar(self, razon: str) -> bool:
        """
        No permitido: El contrato ya finalizó exitosamente.
        """
        print("Error: El contrato ya fue entregado. No se puede cancelar un contrato finalizado.")
        return False

    def recibir_devolucion(self, fecha_devolucion: datetime) -> tuple[bool, float]:
        """
        No permitido: El vehículo ya fue devuelto.
        """
        print("Error: El vehículo ya fue devuelto previamente. Contrato finalizado.")
        return (False, 0.0)

    def puede_modificar_fechas(self) -> bool:
        """
        No permite modificar fechas una vez finalizado.
        """
        return False

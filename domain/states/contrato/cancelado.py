from datetime import datetime
from domain.states.contrato.state import State


class Cancelado(State):
    """
    Estado terminal: El contrato fue cancelado.
    No permite ninguna transición adicional.
    """

    def tomar_pago(self, monto: float) -> bool:
        """
        No permitido: El contrato fue cancelado.
        """
        print("Error: El contrato fue cancelado. No se pueden registrar pagos.")
        return False

    def cancelar(self, razon: str) -> bool:
        """
        No permitido: El contrato ya está cancelado.
        """
        print("Error: El contrato ya está cancelado.")
        return False

    def recibir_devolucion(self, fecha_devolucion: datetime) -> tuple[bool, float]:
        """
        No permitido: El contrato fue cancelado, no hay devolución.
        """
        print("Error: El contrato fue cancelado. No se puede registrar devolución.")
        return (False, 0.0)

    def puede_modificar_fechas(self) -> bool:
        """
        No permite modificar fechas una vez cancelado.
        """
        return False

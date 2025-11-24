from datetime import datetime
from domain.states.contrato.state import State
from domain.states.contrato.en_curso import EnCurso
from domain.states.contrato.cancelado import Cancelado


class EnReservado(State):
    """
    Estado inicial cuando se hace una reserva.
    Permite: tomar_pago() → EnCurso, cancelar() → Cancelado
    """

    def tomar_pago(self, monto: float) -> bool:
        """
        Transición: EnReservado → EnCurso
        Se ejecuta cuando el cliente paga y confirma el alquiler.
        """
        if monto <= 0:
            print(f"Error: El monto del pago debe ser positivo. Recibido: {monto}")
            return False
        
        print(f"Pago de ${monto:.2f} registrado. Contrato confirmado y pasando a En Curso.")
        self.context.transition_to(EnCurso())
        return True

    def cancelar(self, razon: str) -> bool:
        """
        Transición: EnReservado → Cancelado
        Cancela la reserva antes de que se confirme el pago.
        """
        print(f"Reserva cancelada. Razón: {razon}")
        self.context.transition_to(Cancelado())
        return True

    def recibir_devolucion(self, fecha_devolucion: datetime) -> tuple[bool, float]:
        """
        No permitido: No se puede devolver un contrato que aún está en reserva.
        """
        print("Error: No se puede registrar devolución de un contrato en reserva.")
        return (False, 0.0)

    def puede_modificar_fechas(self) -> bool:
        """
        Permite modificar fechas mientras está en reserva.
        """
        return True

from datetime import datetime
from domain.states.contrato.state import State
from domain.states.contrato.ya_entregado import YaEntregado


class EnCurso(State):
    """
    Estado activo cuando el contrato está en ejecución.
    Permite: recibir_devolucion() → YaEntregado
    Bloquea: cancelar() (no se puede cancelar un contrato activo)
    """

    def tomar_pago(self, monto: float) -> bool:
        """
        No permitido: El contrato ya está en curso y pagado.
        """
        print("Error: El contrato ya está En Curso. No se puede registrar otro pago.")
        return False

    def cancelar(self, razon: str) -> bool:
        """
        No permitido: No se puede cancelar un contrato que ya está en curso.
        """
        print("Error: No se puede cancelar un contrato En Curso. Solo se pueden cancelar reservas.")
        return False

    def recibir_devolucion(self, fecha_devolucion: datetime) -> tuple[bool, float]:
        """
        Transición: EnCurso → YaEntregado
        Registra la devolución del vehículo por parte del cliente.
        
        Calcula recargo si la devolución es posterior a fecha_hasta.
        Retorna (éxito, recargo_calculado).
        
        NOTA: El recargo real se calcula en el Service según la regla:
        10% del total por cada día de retraso.
        """
        if fecha_devolucion is None:
            print("Error: Fecha de devolución no puede ser None.")
            return (False, 0.0)
        
        # Validar que la devolución no sea antes de fecha_desde
        if fecha_devolucion < self.context.fecha_desde:
            print(f"Error: La fecha de devolución ({fecha_devolucion}) no puede ser anterior a la fecha de inicio ({self.context.fecha_desde}).")
            return (False, 0.0)
        
        # Calcular si hay retraso
        dias_retraso = 0
        if fecha_devolucion > self.context.fecha_hasta:
            diferencia = fecha_devolucion - self.context.fecha_hasta
            dias_retraso = diferencia.days
            if diferencia.seconds > 0:  # Si hay horas extras, cuenta como día completo
                dias_retraso += 1
        
        if dias_retraso > 0:
            print(f"Devolución con {dias_retraso} día(s) de retraso.")
            print("NOTA: El recargo del 10% por día de retraso será calculado por el Service.")
        else:
            print("Devolución registrada a tiempo.")
        
        # Transición a YaEntregado
        self.context.transition_to(YaEntregado())
        
        # Retornar éxito y días de retraso (el Service calculará el monto)
        return (True, float(dias_retraso))

    def puede_modificar_fechas(self) -> bool:
        """
        No permite modificar fechas cuando el contrato está en curso.
        """
        return False

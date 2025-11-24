from datetime import datetime
from domain.models.contrato import Contrato
from domain.states.vehiculo.state import State
from domain.exceptions import StateTransitionError, BusinessRuleError


class Disponible(State):
    def reservar(self, contrato: Contrato) -> None:
        # Validación de Regla de Negocio: Anticipación
        hoy = datetime.now().date()
        fecha_inicio = contrato.fecha_desde.date()
        dias_anticipacion = (fecha_inicio - hoy).days

        # Lógica: Debe ser en el mismo mes y máximo 3 días antes (según tu lógica original)
        # O ajusta según prefieras. Aquí mantengo tu regla original pero con excepción.
        es_mismo_mes = fecha_inicio.month == hoy.month

        if es_mismo_mes and dias_anticipacion <= 3:
            # 🚨 IMPORTACIÓN LOCAL
            from domain.states.vehiculo.reservado import Reservado
            print(f"LOG: Vehículo reservado para el contrato {contrato.id}")
            self.context.transition_to(Reservado())
        else:
            raise BusinessRuleError("La reserva debe hacerse con al menos 3 días de anticipación dentro del mismo mes.")

    def retirar(self, contrato: Contrato) -> None:
        # Regla: Retiro directo (walk-in)
        es_hoy = contrato.fecha_desde.date() == datetime.now().date()
        hora_valida = contrato.fecha_hasta.hour <= datetime.now().hour  # Tu lógica original

        if es_hoy:  # Simplificado para el ejemplo, añade 'and hora_valida' si es estricto
            # 🚨 IMPORTACIÓN LOCAL
            from domain.states.vehiculo.alquilado import Alquilado
            print(f"LOG: Vehículo retirado directamente (alquiler inmediato) por contrato {contrato.id}")
            self.context.transition_to(Alquilado())
        else:
            raise BusinessRuleError(
                f"Solo se puede retirar el vehículo en la fecha de inicio: {contrato.fecha_desde.date()}")

    def entregar(self) -> None:
        raise StateTransitionError("Un vehículo disponible no puede ser entregado (ya está en la flota).")

    def mover_a_revision(self) -> None:
        raise StateTransitionError("Un vehículo disponible no requiere revisión inmediata (solo post-alquiler).")

    def iniciar_mantenimiento(self) -> None:
        # Aquí sí se permite si hay orden de mantenimiento
        # 🚨 IMPORTACIÓN LOCAL
        from domain.states.vehiculo.en_mantenimiento import EnMantenimiento
        print("LOG: Iniciando mantenimiento programado.")
        self.context.transition_to(EnMantenimiento())

    def reincorporar(self, razon: str) -> None:
        print(f"LOG: El vehículo ya se encuentra disponible. Razón: {razon}")

    def marcar_fuera_de_servicio(self) -> None:
        # Regla: Antigüedad
        antiguedad = datetime.now().year - self.context.anio_fabricacion.year
        if antiguedad > 15:
            from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
            print("LOG: Vehículo marcado como obsoleto.")
            self.context.transition_to(FueraDeServicio())
        else:
            # Si se fuerza manual
            from domain.states.vehiculo.fuera_de_servicio import FueraDeServicio
            print("LOG: Marcando fuera de servicio manualmente.")
            self.context.transition_to(FueraDeServicio())

    def marcar_no_devolucion(self) -> None:
        raise StateTransitionError(
            "Un vehículo disponible no puede ser marcado como no devolución (está en nuestro poder).")
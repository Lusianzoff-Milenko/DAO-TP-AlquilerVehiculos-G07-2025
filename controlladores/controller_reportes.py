from decimal import Decimal
from typing import List, Dict, Any, Tuple, Literal
from services.reporte_service import ReporteService

class ReporteController:
    def __init__(self, reporte_service: ReporteService):
        self._service = reporte_service

    def get_clientes_contacto(self) -> List[Dict[str, Any]]:
        return self._service.get_clientes_contacto()

    def get_disponibilidad_flota(self) -> List[Dict[str, Any]]:
        return self._service.get_disponibilidad_flota()

    def get_utilizacion_flota(self) -> List[Dict[str, Any]]:
        return self._service.get_utilizacion_flota()

    def get_rentabilidad_contratos(self) -> List[Dict[str, Any]]:
        return self._service.get_rentabilidad_contratos()

    def get_facturacion_mensual(self) -> tuple[
        list[dict[str, int | str | Decimal | float]], Decimal | float | Literal[0]]:
        return self._service.get_reporte_facturacion_cerrada()

    def get_detalle_flota(self) -> List[Dict[str, Any]]:
        return self._service.get_detalle_flota_completo()

    def get_empleados_activos(self) -> List[Dict[str, Any]]:
        return self._service.get_empleados_activos()

    def get_demanda_por_modelo(self) -> List[Dict[str, Any]]:
        return self._service.get_demanda_por_modelo()

    def get_historial_mantenimiento(self) -> List[Dict[str, Any]]:
        return self._service.get_historial_mantenimiento()

    # --- NUEVO MÉTODO AGREGADO ---
    def get_alquileres_por_cliente(self, cliente_id: int | None = None,
                                   fecha_inicio=None, fecha_fin=None) -> List[Dict[str, Any]]:
        """
        Busca el historial de alquileres filtrando por cliente y fechas.
        """
        return self._service.get_alquileres_por_cliente(cliente_id, fecha_inicio, fecha_fin)
from decimal import Decimal
from typing import List, Dict, Any, Tuple, Literal
from services.reporte_service import ReporteService

class ReporteController:
    def __init__(self, reporte_service: ReporteService):
        self._service = reporte_service

    def get_clientes_contacto(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de clientes con sus datos de contacto formateados.
        """
        return self._service.get_clientes_contacto()

    def get_disponibilidad_flota(self) -> List[Dict[str, Any]]:
        """
        Retorna los vehículos que están listos para alquilar (Disponibles, EnRevisión, etc).
        """
        return self._service.get_disponibilidad_flota()

    def get_utilizacion_flota(self) -> List[Dict[str, Any]]:
        """
        Retorna métricas de uso por vehículo (cuántas veces se alquiló).
        """
        return self._service.get_utilizacion_flota()

    def get_rentabilidad_contratos(self) -> List[Dict[str, Any]]:
        """
        Retorna el análisis financiero de cada contrato.
        """
        return self._service.get_rentabilidad_contratos()

    def get_facturacion_mensual(self) -> tuple[
        list[dict[str, int | str | Decimal | float]], Decimal | float | Literal[0]]:
        """
        Retorna una tupla: (Lista de registros, Total Facturado Global).
        Útil para llenar una tabla y un KPI Card al mismo tiempo.
        """
        # El servicio retorna (data, total)
        return self._service.get_reporte_facturacion_cerrada()

    def get_detalle_flota(self) -> List[Dict[str, Any]]:
        """
        Retorna el listado completo de vehículos con fotos y detalles técnicos.
        """
        return self._service.get_detalle_flota_completo()

    def get_empleados_activos(self) -> List[Dict[str, Any]]:
        """
        Retorna el listado de empleados con su actividad reciente.
        """
        return self._service.get_empleados_activos()

    def get_demanda_por_modelo(self) -> List[Dict[str, Any]]:
        """
        Retorna el análisis de demanda por modelo de vehículo.
        """
        return self._service.get_demanda_por_modelo()

    def get_historial_mantenimiento(self) -> List[Dict[str, Any]]:
        """
        Retorna el historial de mantenimiento de los vehículos.
        """
        return self._service.get_historial_mantenimiento()
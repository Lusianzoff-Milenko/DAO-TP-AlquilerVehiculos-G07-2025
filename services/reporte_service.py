from decimal import Decimal
from typing import List, Dict, Any, Literal
from data_access.repositories.view_repositories import (
    VistaClientesRepository, VistaRentabilidadRepository,
    VistaDisponibilidadRepository, VistaFacturacionRepository,
    VistaUtilizacionRepository, VistaVehiculosRepository, VistaEmpleadosRepository
)


class ReporteService:
    def __init__(self,
                 vista_clientes_repo: VistaClientesRepository,
                 vista_rentabilidad_repo: VistaRentabilidadRepository,
                 vista_disponibilidad_repo: VistaDisponibilidadRepository,
                 vista_facturacion_repo: VistaFacturacionRepository,
                 vista_utilizacion_repo: VistaUtilizacionRepository,
                 vista_vehiculos_repo: VistaVehiculosRepository,
                 vista_empleados_repo: VistaEmpleadosRepository):
        self._clientes = vista_clientes_repo
        self._rentabilidad = vista_rentabilidad_repo
        self._disponibilidad = vista_disponibilidad_repo
        self._facturacion = vista_facturacion_repo
        self._utilizacion = vista_utilizacion_repo
        self._vehiculos = vista_vehiculos_repo
        self._empleados = vista_empleados_repo

    # --- Reportes de Clientes ---
    def get_clientes_contacto(self) -> List[Dict]:
        data = self._clientes.list_all()
        # Convertimos a dict para fácil consumo en UI (tablas)
        return [
            {
                "Nombre": c.nombre,
                "Apellido": c.apellido,
                "Documento": f"{c.tipo_documento} {c.documento}",
                "Contacto": f"{c.mail} | {c.telefono}"
            }
            for c in data
        ]

    # --- Reportes de Vehículos y Flota ---
    def get_disponibilidad_flota(self) -> List[Dict]:
        """Vehículos listos para alquilar."""
        data = self._disponibilidad.list_all()
        return [
            {
                "Vehículo": f"{v.marca} {v.modelo}",
                "Patente": v.patente,
                "Precio Diario": f"${v.precio_base}",
                "Estado": v.estado_actual
            }
            for v in data
        ]

    def get_utilizacion_flota(self) -> List[Dict]:
        """Métricas de uso por vehículo."""
        data = self._utilizacion.list_all()
        return [
            {
                "Patente": v.patente, "Modelo": v.modelo,
                "Contratos": v.contratos_totales,
                "Días Alquilado": v.dias_alquilados,
                "Estado": v.estado_actual
            }
            for v in data
        ]

    def get_detalle_flota_completo(self) -> List[Dict]:
        """Listado detallado con fotos y características."""
        data = self._vehiculos.list_all()
        return [
            {
                "Foto": v.foto, "Modelo": f"{v.marca} {v.modelo} ({v.anio})",
                "Color": v.color,
                "Config": f"{v.pasajeros} Pasj. / {v.puertas} Ptas.",
                "Precio": v.precio, "Estado": v.estado
            }
            for v in data
        ]

    # --- Reportes de Contratos y Reservas ---
    def get_rentabilidad_contratos(self) -> List[Dict]:
        """Análisis financiero de contratos."""
        data = self._rentabilidad.list_all()
        return [
            {
                "Contrato #": c.id_contrato, "Cliente": c.cliente,
                "Vehículo": c.patente, "Estado": c.estado,
                "Monto": c.monto, "Extras/Multas": c.costo_inconvenientes,
                "Total": (c.monto or 0) + (c.costo_inconvenientes or 0)
            }
            for c in data
        ]

    def get_reporte_facturacion_cerrada(self) -> tuple[
        list[dict[str, int | str | Decimal | float]], Decimal | float | Literal[0]]:
        """Facturación final de contratos cerrados."""
        data = self._facturacion.list_all()
        total_global = sum(r.total_facturado for r in data if r.total_facturado)

        reporte = [
            {
                "Contrato": r.id_contrato, "Cliente": r.cliente,
                "Fecha Fin": r.fecha_fin, "Días": r.dias_alquilados,
                "Facturado": r.total_facturado
            }
            for r in data
        ]
        return reporte, total_global

    def get_empleados_activos(self) -> List[Dict]:
        """Listado de empleados activos con detalles."""
        data = self._empleados.list_all()
        return [
            {
                "Nombre": f"{e.nombre} {e.apellido}",
                "Documento": f"{e.tipo_documento} {e.documento}",
                "Cargo": e.cargo,
                "Contacto": f"{e.mail} | {e.telefono}",
                "Puesto": e.puesto
            }
            for e in data if e.estado == "Activo"
        ]
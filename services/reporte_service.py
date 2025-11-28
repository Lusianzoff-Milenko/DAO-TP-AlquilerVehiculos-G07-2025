from decimal import Decimal
from typing import List, Dict, Any, Literal, Optional
from data_access.repositories.view_repositories import (
    VistaClientesRepository, VistaRentabilidadRepository,
    VistaDisponibilidadRepository, VistaFacturacionRepository,
    VistaUtilizacionRepository, VistaVehiculosRepository, VistaEmpleadosRepository, VistaHistorialMantenimientoRepository, VistaDemandaPorModeloRepository
)

class ReporteService:
    def __init__(self,
                 vista_clientes_repo: VistaClientesRepository,
                 vista_rentabilidad_repo: VistaRentabilidadRepository,
                 vista_disponibilidad_repo: VistaDisponibilidadRepository,
                 vista_facturacion_repo: VistaFacturacionRepository,
                 vista_utilizacion_repo: VistaUtilizacionRepository,
                 vista_vehiculos_repo: VistaVehiculosRepository,
                 vista_empleados_repo: VistaEmpleadosRepository,
                 vista_historial_mantenimiento_repo: VistaHistorialMantenimientoRepository,
                 vista_demanda_por_modelo_repo: VistaDemandaPorModeloRepository,
                 contrato_repo=None,                 # <-- nuevo
                 detalle_contrato_repo=None):        # <-- nuevo
        self._clientes = vista_clientes_repo
        self._rentabilidad = vista_rentabilidad_repo
        self._disponibilidad = vista_disponibilidad_repo
        self._facturacion = vista_facturacion_repo
        self._utilizacion = vista_utilizacion_repo
        self._vehiculos = vista_vehiculos_repo
        self._empleados = vista_empleados_repo
        self._historial_mantenimiento = vista_historial_mantenimiento_repo
        self._demanda_por_modelo = vista_demanda_por_modelo_repo

        # nuevos repositorios para listado detallado
        self._contrato_repo = contrato_repo
        self._detalle_contrato_repo = detalle_contrato_repo
        

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

    def get_demanda_por_modelo(self) -> List[Dict]:
        """Análisis de demanda por modelo de vehículo."""
        data = self._demanda_por_modelo.list_all()
        return [
            {
                "Modelo": m.modelo,
                "Cantidad Alquileres": m.cantidad_alquileres,
                "Ingresos Generados": m.total_dias_reservados_contratados
            }
            for m in data
        ]

    def get_historial_mantenimiento(self) -> List[Dict]:
        """Historial de mantenimiento de vehículos."""
        data = self._historial_mantenimiento.list_all()
        return [
            {
                "Vehículo": f""
                            f"({h.patente})",
                "Fecha Mantenimiento": h.fecha_mantenimiento,
                "Tipo Mantenimiento": h.descripcion,
                "Costo": h.costo,
                "Estado": h.estado_actual,
                "Empleado Responsable": h.empleado_responsable
            }
            for h in data
        ]
    
     # --- Listado detallado: Alquileres por cliente ---
    def get_alquileres_por_cliente(self, cliente_id: Optional[int] = None,
                                   fecha_inicio: Optional[Any] = None,
                                   fecha_fin: Optional[Any] = None) -> List[Dict[str, Any]]:
        """
        Listado detallado de alquileres por cliente.
        Usa contrato_repo.list_all() y detalle_contrato_repo.list_all() como fuente principal.
        Retorna lista de dicts: contrato_id, cliente, fecha_inicio, fecha_fin, total, detalles (lista).
        """
        # 1) Obtener contratos desde el repo
        if not self._contrato_repo:
            print("ReporteService: contrato_repo no configurado.")
            return []

        try:
            if hasattr(self._contrato_repo, "list_all"):
                contratos = self._contrato_repo.list_all()
            elif hasattr(self._contrato_repo, "all"):
                contratos = self._contrato_repo.all()
            else:
                print("ReporteService: contrato_repo no tiene list_all()/all().")
                return []
        except Exception as e:
            print("ReporteService: error listando contratos:", e)
            return []

        # 2) Filtrar por cliente y rango de fechas
        def contrato_en_rango(c):
            try:
                if cliente_id is not None:
                    cid = getattr(c, "cliente_id", None)
                    if cid is None:
                        cli = getattr(c, "cliente", None)
                        cid = getattr(cli, "id", None) if cli is not None else None
                    if cid is None or int(cid) != int(cliente_id):
                        return False
                if fecha_inicio:
                    fi = getattr(c, "fecha_inicio", None)
                    if fi is None or fi < fecha_inicio:
                        return False
                if fecha_fin:
                    ff = getattr(c, "fecha_fin", None)
                    if ff is None or ff > fecha_fin:
                        return False
                return True
            except Exception:
                return False

        contratos = [c for c in contratos if contrato_en_rango(c)]

        # 3) Obtener todos los detalles (si existe el repo) para relacionarlos por contrato_id
        detalles_all = []
        if self._detalle_contrato_repo:
            try:
                if hasattr(self._detalle_contrato_repo, "list_all"):
                    detalles_all = self._detalle_contrato_repo.list_all()
                elif hasattr(self._detalle_contrato_repo, "all"):
                    detalles_all = self._detalle_contrato_repo.all()
            except Exception as e:
                print("ReporteService: error listando detalles de contrato:", e)
                detalles_all = []

        # 4) Construir salida
        salida: List[Dict[str, Any]] = []
        for c in contratos:
            contrato_id = getattr(c, "id", None) or getattr(c, "contrato_id", None)
            # construir nombre cliente
            cliente_display = ""
            cli = getattr(c, "cliente", None)
            if cli:
                nombre = getattr(cli, "nombre", "") or getattr(cli, "first_name", "")
                apellido = getattr(cli, "apellido", "") or getattr(cli, "last_name", "")
                cliente_display = " ".join(filter(None, [str(nombre), str(apellido)])).strip()
            else:
                cliente_display = getattr(c, "cliente_nombre", None) or str(getattr(c, "cliente_id", "") or "")

            fecha_i = getattr(c, "fecha_inicio", None)
            fecha_f = getattr(c, "fecha_fin", None)
            total = getattr(c, "total", None) or getattr(c, "monto", None) or getattr(c, "importe", None)

            # detalles del contrato: preferir c.detalles si existe, sino filtrar detalles_all
            detalles_iter = []
            if hasattr(c, "detalles") and getattr(c, "detalles"):
                detalles_iter = getattr(c, "detalles")
            else:
                detalles_iter = [d for d in detalles_all if getattr(d, "contrato_id", None) == contrato_id]

            detalles_list = []
            for d in detalles_iter:
                vehiculo = getattr(d, "vehiculo_descripcion", None) or getattr(getattr(d, "vehiculo", None), "descripcion", None) or getattr(d, "vehiculo_id", None)
                cantidad = getattr(d, "cantidad", None) or getattr(d, "qty", None)
                precio = getattr(d, "precio", None) or getattr(d, "precio_unitario", None) or getattr(d, "valor", None)
                subtotal = getattr(d, "subtotal", None)
                if subtotal is None:
                    try:
                        if cantidad is not None and precio is not None:
                            subtotal = cantidad * precio
                    except Exception:
                        subtotal = None
                detalles_list.append({
                    "vehiculo_id": getattr(d, "vehiculo_id", None),
                    "vehiculo": vehiculo,
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "subtotal": subtotal
                })

            salida.append({
                "contrato_id": contrato_id,
                "cliente": cliente_display,
                "fecha_inicio": fecha_i,
                "fecha_fin": fecha_f,
                "total": total,
                "detalles": detalles_list
            })

        return salida
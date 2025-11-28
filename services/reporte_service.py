from decimal import Decimal
from typing import List, Dict, Any, Literal, Optional
from data_access.repositories.view_repositories import (
    VistaClientesRepository, VistaRentabilidadRepository,
    VistaDisponibilidadRepository, VistaFacturacionRepository,
    VistaUtilizacionRepository, VistaVehiculosRepository, VistaEmpleadosRepository,
    VistaHistorialMantenimientoRepository, VistaDemandaPorModeloRepository
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
                 contrato_repo=None,
                 detalle_contrato_repo=None,
                 vista_cantidad_flota_repo=None):
        self._clientes = vista_clientes_repo
        self._rentabilidad = vista_rentabilidad_repo
        self._disponibilidad = vista_disponibilidad_repo
        self._facturacion = vista_facturacion_repo
        self._utilizacion = vista_utilizacion_repo
        self._vehiculos = vista_vehiculos_repo
        self._empleados = vista_empleados_repo
        self._historial_mantenimiento = vista_historial_mantenimiento_repo
        self._demanda_por_modelo = vista_demanda_por_modelo_repo
        self._cantidad_flota = vista_cantidad_flota_repo
        self._contrato_repo = contrato_repo
        self._detalle_contrato_repo = detalle_contrato_repo

    # --- Reportes de Clientes ---
    def get_clientes_contacto(self) -> List[Dict]:
        data = self._clientes.list_all()
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


    # --- MÉTODO CORREGIDO ---
    def get_alquileres_por_cliente(self, cliente_id: Optional[int] = None,
                                   fecha_inicio: Optional[Any] = None,
                                   fecha_fin: Optional[Any] = None) -> List[Dict[str, Any]]:
        """
        Retorna historial de alquileres (YaEntregado, EnCurso, EnReservado).
        """
        if not self._contrato_repo:
            return []

        try:
            # Asumimos que el repo usa joinedload para traer todo
            contratos = self._contrato_repo.list_all()
        except Exception as e:
            print("Error leyendo contratos:", e)
            return []

        salida = []

        # Estados visibles
        ESTADOS_VISIBLES = ["YaEntregado", "EnCurso", "EnReservado"]

        for c in contratos:
            try:
                # 1. Filtro de Estado
                estado_nombre = c.Estado.nombre if c.Estado else "Desconocido"
                if estado_nombre not in ESTADOS_VISIBLES:
                    continue

                # 2. Filtro por Cliente
                if cliente_id is not None:
                    if c.id_cliente != int(cliente_id):
                        continue

                # 3. Filtro por Fechas
                if fecha_inicio or fecha_fin:
                    c_inicio = c.fecha_desde.date() if hasattr(c.fecha_desde, "date") else c.fecha_desde
                    c_fin = c.fecha_hasta.date() if hasattr(c.fecha_hasta, "date") else c.fecha_hasta

                    if fecha_inicio and c_inicio < fecha_inicio: continue
                    if fecha_fin and c_fin > fecha_fin: continue

                # --- Armado de Datos ---
                cliente_str = "S/D"
                if c.Cliente and c.Cliente.persona:
                    cliente_str = f"{c.Cliente.persona.nombre} {c.Cliente.persona.apellido}"

                detalles_list = []
                total_contrato = 0.0

                if c.detalles_contrato:
                    for d in c.detalles_contrato:
                        total_contrato += d.monto
                        v_str = "Vehículo"
                        if d.Vehiculo:
                            mod = d.Vehiculo.Modelo.nombre if d.Vehiculo.Modelo else ""
                            v_str = f"{mod} ({d.Vehiculo.patente})"

                        detalles_list.append({
                            "vehiculo": v_str,
                            "cantidad": 1,
                            "subtotal": f"${d.monto:,.2f}"
                        })

                salida.append({
                    "contrato_id": c.id,
                    "cliente": f"[{estado_nombre}] {cliente_str}",
                    "fecha_inicio": c.fecha_desde.strftime("%Y-%m-%d"),
                    "fecha_fin": c.fecha_hasta.strftime("%Y-%m-%d"),
                    "total": f"${total_contrato:,.2f}",
                    "detalles": detalles_list
                })
            except Exception as e:
                print(f"Error procesando contrato {c.id}: {e}")
                continue

        return salida

    def get_conteo_flota_por_modelo(self) -> List[Dict]:
        if not self._cantidad_flota:
            return []

        data = self._cantidad_flota.list_all()
        return [
            {
                "Modelo": f"{row.marca} {row.modelo}",
                "Cantidad": row.cantidad
            }
            for row in data
        ]
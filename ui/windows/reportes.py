import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.services.workers import run_async
from services.containers.container import Container
from typing import List, Dict, Any

_TAG = "view_reportes"
_controller = Container().reporte_controller()


# --- Utilidades de Actualización ---

def _update_table(table_tag, data):
    """Limpia y rellena una tabla con una lista de diccionarios."""
    # 1. Limpiar filas antiguas
    if dpg.does_item_exist(table_tag):
        # Usamos slot 1 para las filas
        children = dpg.get_item_children(table_tag, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    if not data:
        return

    # 2. Llenar nuevas filas
    # Asumimos que el orden de las columnas en el dict coincide con la tabla visual
    for row in data:
        with dpg.table_row(parent=table_tag):
            for value in row.values():
                dpg.add_text(str(value))


# --- Callbacks para Manejo de Datos (incluyendo gráfico) ---

def _aggregate_utilizacion_by_model(data: List[Dict[str, Any]]) -> tuple[List[str], List[float]]:
    """Agrega los días alquilados por Modelo (simplificado)."""
    model_days = {}
    for item in data:
        model = item['Modelo']
        days = float(item['Días Alquilado'])
        model_days[model] = model_days.get(model, 0) + days

    # Convertir a listas para el DPG: labels (x) y values (y)
    labels = list(model_days.keys())
    values = list(model_days.values())

    # Ordenar por valores de mayor a menor (Top N)
    sorted_pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)

    # Tomar los top 5
    top_n = 5
    top_labels = [p[0] for p in sorted_pairs[:top_n]]
    top_values = [p[1] for p in sorted_pairs[:top_n]]

    return top_labels, top_values


def _on_utilizacion_loaded(result):
    """Callback para Utilización: actualiza tabla y gráfico."""
    _update_table("tbl_utilizacion", result)

    # Lógica de Gráfico
    model_labels, days_values = _aggregate_utilizacion_by_model(result)

    # Crear o actualizar series del gráfico
    # Necesitamos convertir los labels a índices numéricos para el gráfico de barras
    x_data = [i for i in range(len(model_labels))]

    if dpg.does_item_exist("utilizacion_bar_series"):  # Debe existir, se crea en register()
        dpg.set_value("utilizacion_bar_series", [x_data, days_values])

        # Actualizar etiquetas del eje X
        dpg.configure_item("utilizacion_x_axis", label="Modelo de Vehículo (Top 5)")

        # Hack para configurar ticks del eje X con texto
        ticks = [(i, label) for i, label in enumerate(model_labels)]
        dpg.set_axis_ticks("utilizacion_x_axis", ticks)

        # Forzar límites para que el gráfico sea visible
        dpg.set_axis_limits("utilizacion_x_axis", -0.5, len(model_labels) - 0.5)
        dpg.set_axis_limits_auto("utilizacion_y_axis")


def _on_facturacion_loaded(result):
    """Callback especial para facturación que recibe (lista, total)."""
    data, total = result
    _update_table("tbl_facturacion", data)
    dpg.set_value("txt_total_facturado", f"Total Facturado: ${total:,.2f}")

def _on_alquileres_loaded(result):
    """Callback para listado de alquileres por cliente (result = lista de dicts)."""
    # limpiar tabla si existe
    if dpg.does_item_exist("tbl_alquileres_cliente"):
        children = dpg.get_item_children("tbl_alquileres_cliente", slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    if not result:
        return

    for row in result:
        with dpg.table_row(parent="tbl_alquileres_cliente"):
            dpg.add_text(str(row.get("contrato_id", "")))
            dpg.add_text(str(row.get("cliente", "")))
            dpg.add_text(str(row.get("fecha_inicio", "")))
            dpg.add_text(str(row.get("fecha_fin", "")))
            dpg.add_text(str(row.get("total", "")))
        # detalles del contrato como filas secundarias
        for det in row.get("detalles", []):
            with dpg.table_row(parent="tbl_alquileres_cliente"):
                dpg.add_text("   → " + str(det.get("vehiculo", "")))
                dpg.add_text("")  # columna vacía para alinear
                dpg.add_text("")
                dpg.add_text(f" Cant: {det.get('cantidad', '')}")
                dpg.add_text(f" Subt: {det.get('subtotal', '')}")

def _load_alquileres_por_cliente(cliente_id=None, inicio=None, fin=None):
    # Ejecuta el método del controlador asincrónicamente y actualiza con el callback
    run_async(lambda: _controller.get_alquileres_por_cliente() if cliente_id is None
              else _controller.get_alquileres_por_cliente(cliente_id, inicio, fin),
              on_success=_on_alquileres_loaded)

# --- Loaders (Disparadores de tareas) ---

def _load_disponibilidad():
    run_async(lambda: _controller.get_disponibilidad_flota(),
              on_success=lambda data: _update_table("tbl_disponibilidad", data))


def _load_rentabilidad():
    run_async(lambda: _controller.get_rentabilidad_contratos(),
              on_success=lambda data: _update_table("tbl_rentabilidad", data))


def _load_utilizacion():
    # Usar el nuevo callback
    run_async(lambda: _controller.get_utilizacion_flota(),
              on_success=_on_utilizacion_loaded)


def _load_facturacion():
    run_async(lambda: _controller.get_facturacion_mensual(),
              on_success=_on_facturacion_loaded)


def _load_clientes():
    run_async(lambda: _controller.get_clientes_contacto(),
              on_success=lambda data: _update_table("tbl_clientes_report", data))


# --- Registro de la Vista ---

def register():
    with dpg.group(tag=_TAG, parent="content_area", show=False):
        dpg.add_spacer(height=10)
        dpg.add_text("Centro de Reportes", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.tab_bar():
            # TAB 1: Disponibilidad de Flota (Remover ID)
            with dpg.tab(label="🚗 Disponibilidad"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_disponibilidad)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_disponibilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    # dpg.add_table_column(label="ID", width_fixed=True)
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Patente")
                    dpg.add_table_column(label="Precio Diario")
                    dpg.add_table_column(label="Estado")

            # TAB: Alquileres por Cliente (pegar en el tab_bar)
            with dpg.tab(label="📋 Alquileres por Cliente"):
                dpg.add_spacer(height=5)
                dpg.add_input_int(label="Cliente ID", tag="r_alq_cliente_id")
                dpg.add_input_text(label="Fecha inicio (YYYY-MM-DD)", tag="r_alq_fecha_inicio")
                dpg.add_input_text(label="Fecha fin (YYYY-MM-DD)", tag="r_alq_fecha_fin")
                dpg.add_button(label="🔎 Buscar", callback=lambda s,a: _load_alquileres_por_cliente(
                    dpg.get_value("r_alq_cliente_id") or None,
                    (lambda t: None if not t else __import__('datetime').date.fromisoformat(t))(dpg.get_value("r_alq_fecha_inicio")),
                    (lambda t: None if not t else __import__('datetime').date.fromisoformat(t))(dpg.get_value("r_alq_fecha_fin"))
                ))
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_alquileres_cliente", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=450,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Contrato #")
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Fecha Inicio")
                    dpg.add_table_column(label="Fecha Fin")
                    dpg.add_table_column(label="Total")


            # TAB 2: Rentabilidad de Contratos (Ajustar ancho de ID)
            with dpg.tab(label="💰 Rentabilidad"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_rentabilidad)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_rentabilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Contrato #", width_fixed=True, init_width_or_weight=0.5)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Estado")
                    dpg.add_table_column(label="Monto Base")
                    dpg.add_table_column(label="Extras/Multas")
                    dpg.add_table_column(label="Total Final")

            # TAB 3: Utilización (Añadir gráfico)
            with dpg.tab(label="📈 Utilización"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_utilizacion)
                dpg.add_spacer(height=5)

                # --- GRÁFICO DE UTILIZACIÓN ---
                with dpg.group(horizontal=True):
                    # Placeholder para el gráfico (50% ancho)
                    with dpg.plot(label="Uso de Flota (Días Alquilados por Modelo)", height=400, width=500,
                                  tag="utilizacion_plot"):
                        dpg.add_plot_legend()

                        # Eje X
                        dpg.add_plot_axis(dpg.mvXAxis, label="Modelo de Vehículo", tag="utilizacion_x_axis")

                        # Eje Y
                        # FIX: No usar 'with' aquí, ya que add_plot_axis retorna un tag (str), no un context manager
                        dpg.add_plot_axis(dpg.mvYAxis, label="Total Días Alquilados", tag="utilizacion_y_axis")

                        # Serie de Barras (inicialmente vacía) - Usamos parent explícito
                        dpg.add_bar_series([], [], label="Días Alquilados", weight=0.5, tag="utilizacion_bar_series",
                                           parent="utilizacion_y_axis")

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text("Detalle por Vehículo:")
                dpg.add_spacer(height=5)

                # Tabla de Utilización (Detalle)
                with dpg.table(tag="tbl_utilizacion", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=300,  # Reducir altura por el gráfico
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Patente")
                    dpg.add_table_column(label="Modelo")
                    dpg.add_table_column(label="Cant. Contratos")
                    dpg.add_table_column(label="Días Alquilado")
                    dpg.add_table_column(label="Estado Actual")

            # TAB 4: Facturación Cerrada (Ajustar ancho de ID)
            with dpg.tab(label="💵 Facturación"):
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="🔄 Actualizar", callback=_load_facturacion)
                    dpg.add_spacer(width=20)
                    dpg.add_text("Total Facturado: $0.00", tag="txt_total_facturado", color=(0, 255, 0))

                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_facturacion", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Contrato #", width_fixed=True, init_width_or_weight=0.5)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Fecha Fin")
                    dpg.add_table_column(label="Días")
                    dpg.add_table_column(label="Facturado")

            # TAB 5: Directorio Clientes (Remover ID)
            with dpg.tab(label="👥 Contactos"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_clientes)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_clientes_report", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    # dpg.add_table_column(label="ID", width_fixed=True)
                    dpg.add_table_column(label="Nombre")
                    dpg.add_table_column(label="Apellido")
                    dpg.add_table_column(label="Documento")
                    dpg.add_table_column(label="Contacto")

    register_view("reportes", _TAG)

    # Carga inicial de datos
    _load_disponibilidad()
    _load_rentabilidad()
    _load_utilizacion()
    _load_clientes()
    _load_facturacion()
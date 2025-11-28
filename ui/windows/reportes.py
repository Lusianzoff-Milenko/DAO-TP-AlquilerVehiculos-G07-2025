import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.services.workers import run_async
from services.containers.container import Container
from typing import List, Dict, Any

_TAG = "view_reportes"

# Instanciamos ambos controladores
_controller = Container().reporte_controller()
_cliente_controller = Container().cliente_controller()

# Estado local para los filtros
_tipos_documento_options = []  # Lista de tuplas (Label, ID)


# --- Utilidades de Actualización ---

def _update_table(table_tag, data):
    """Limpia y rellena una tabla con una lista de diccionarios."""
    if dpg.does_item_exist(table_tag):
        children = dpg.get_item_children(table_tag, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    if not data:
        return

    for row in data:
        with dpg.table_row(parent=table_tag):
            for value in row.values():
                dpg.add_text(str(value))


# --- Callbacks para Manejo de Datos ---

def _on_utilizacion_loaded(result):
    """Callback para Demanda por Modelo: actualiza tabla y gráfico."""
    _update_table("tbl_utilizacion", result)

    if not result: return

    # Gráfico Top 5
    sorted_data = sorted(result, key=lambda x: x['Cantidad Alquileres'], reverse=True)[:5]
    labels = [item['Modelo'] for item in sorted_data]
    values = [item['Cantidad Alquileres'] for item in sorted_data]
    x_data = [i for i in range(len(labels))]

    if dpg.does_item_exist("utilizacion_bar_series"):
        dpg.set_value("utilizacion_bar_series", [x_data, values])
        dpg.configure_item("utilizacion_x_axis", label="Modelo")
        dpg.set_axis_ticks("utilizacion_x_axis", [(label, i) for i, label in enumerate(labels)])
        dpg.set_axis_limits("utilizacion_x_axis", -0.5, len(labels) - 0.5)
        max_val = max(values) if values else 10
        dpg.set_axis_limits("utilizacion_y_axis", 0, max_val * 1.2)


def _on_facturacion_loaded(result):
    data, total = result
    _update_table("tbl_facturacion", data)
    dpg.set_value("txt_total_facturado", f"Total Facturado: ${total:,.2f}")


def _on_alquileres_loaded(result):
    """Callback para listado de alquileres por cliente."""
    if dpg.does_item_exist("tbl_alquileres_cliente"):
        children = dpg.get_item_children("tbl_alquileres_cliente", slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    if dpg.does_item_exist("txt_status_busqueda"):
        dpg.set_value("txt_status_busqueda", f"Se encontraron {len(result)} contratos.")

    if not result:
        return

    for row in result:
        # Fila principal (Contrato)
        with dpg.table_row(parent="tbl_alquileres_cliente"):
            dpg.add_text(f"#{row.get('contrato_id', '')}", color=(100, 255, 100))
            dpg.add_text(str(row.get("cliente", "")))
            dpg.add_text(str(row.get("fecha_inicio", "")))
            dpg.add_text(str(row.get("fecha_fin", "")))
            dpg.add_text(str(row.get("total", "")))

        # Filas detalle (Vehículos) - Indentados visualmente
        for det in row.get("detalles", []):
            with dpg.table_row(parent="tbl_alquileres_cliente"):
                dpg.add_text("")  # Espacio en ID
                dpg.add_text(f"   ↳ {det.get('vehiculo', '')}", color=(200, 200, 200))
                dpg.add_text("")
                dpg.add_text(f"Cant: {det.get('cantidad', '')}")
                dpg.add_text(f"Sub: {det.get('subtotal', '')}")


# --- LÓGICA DE BÚSQUEDA DE CLIENTE ---

def _on_alquileres_loaded(result):
    # Callback específico para la tabla jerárquica de alquileres
    if dpg.does_item_exist("tbl_alquileres_cliente"):
        children = dpg.get_item_children("tbl_alquileres_cliente", slot=1)
        if children:
            for child in children: dpg.delete_item(child)

    dpg.set_value("txt_status_busqueda", f"Se encontraron {len(result)} contratos.")

    for row in result:
        with dpg.table_row(parent="tbl_alquileres_cliente"):
            dpg.add_text(f"#{row.get('contrato_id')}", color=(100, 255, 100))
            dpg.add_text(row.get("cliente"))
            dpg.add_text(row.get("fecha_inicio"))
            dpg.add_text(row.get("fecha_fin"))
            dpg.add_text(row.get("total"))

        for det in row.get("detalles", []):
            with dpg.table_row(parent="tbl_alquileres_cliente"):
                dpg.add_text("")
                dpg.add_text(f"   ↳ {det.get('vehiculo')}", color=(200, 200, 200))
                dpg.add_text("")
                dpg.add_text(f"x{det.get('cantidad')}")
                dpg.add_text(det.get("subtotal"))


def _ejecutar_busqueda_alquileres():
    tipo_doc_label = dpg.get_value("r_alq_tipo_doc")
    nro_doc = dpg.get_value("r_alq_nro_doc").strip()
    f_ini = dpg.get_value("r_alq_fecha_inicio")
    f_fin = dpg.get_value("r_alq_fecha_fin")

    f_ini_obj = None
    f_fin_obj = None
    try:
        if f_ini: f_ini_obj = __import__('datetime').date.fromisoformat(f_ini)
        if f_fin: f_fin_obj = __import__('datetime').date.fromisoformat(f_fin)
    except:
        dpg.set_value("txt_status_busqueda", "Error en fechas (use YYYY-MM-DD)")
        return

    cliente_id = None
    if nro_doc:
        tipo_id = next((uid for label, uid in _tipos_documento_options if label == tipo_doc_label), 1)
        dpg.set_value("txt_status_busqueda", "Buscando cliente...")

        # Buscar ID del cliente
        c_data = _cliente_controller.get_cliente_by_documento_and_tipo(tipo_id, nro_doc)
        if c_data:
            cliente_id = c_data["ID"]
            dpg.set_value("txt_status_busqueda", f"Cliente: {c_data['Nombre']} {c_data['Apellido']}. Buscando...")
        else:
            dpg.set_value("txt_status_busqueda", "❌ Cliente no encontrado.")
            _on_alquileres_loaded([])
            return
    else:
        dpg.set_value("txt_status_busqueda", "Mostrando todo...")

    run_async(
        lambda: _controller.get_alquileres_por_cliente(cliente_id, f_ini_obj, f_fin_obj),
        on_success=_on_alquileres_loaded
    )


def _load_utilizacion():
    # Reutilizamos la lógica de Demanda por Modelo
    def _cb(res):
        _update_table("tbl_utilizacion", res)
        if not res: return
        # Gráfico simple
        vals = [x['Cantidad Alquileres'] for x in res[:5]]
        dpg.set_value("utilizacion_bar_series", [[i for i in range(len(vals))], vals])
        dpg.configure_item("utilizacion_x_axis", label="Modelos Top")

    run_async(lambda: _controller.get_demanda_por_modelo(), on_success=_cb)

# --- Loaders Generales ---

def _load_disponibilidad():
    run_async(lambda: _controller.get_disponibilidad_flota(),
              on_success=lambda data: _update_table("tbl_disponibilidad", data))


def _load_rentabilidad():
    run_async(lambda: _controller.get_rentabilidad_contratos(),
              on_success=lambda data: _update_table("tbl_rentabilidad", data))


def _load_utilizacion():
    run_async(lambda: _controller.get_demanda_por_modelo(),
              on_success=_on_utilizacion_loaded)


def _load_facturacion():
    run_async(lambda: _controller.get_facturacion_mensual(),
              on_success=_on_facturacion_loaded)


def _load_clientes():
    run_async(lambda: _controller.get_clientes_contacto(),
              on_success=lambda data: _update_table("tbl_clientes_report", data))


def _init_options():
    """Carga las opciones de tipos de documento para el combo."""
    global _tipos_documento_options
    try:
        opts = _cliente_controller.get_form_options()
        # Formato esperado de get_form_options: {'tipos_documento': [{'label': 'DNI', 'value': 1}, ...]}
        raw_opts = opts.get("tipos_documento", [])
        _tipos_documento_options = [(o['label'], o['value']) for o in raw_opts]

        # Actualizar el combo si ya existe
        if dpg.does_item_exist("r_alq_tipo_doc"):
            items = [label for label, _ in _tipos_documento_options]
            dpg.configure_item("r_alq_tipo_doc", items=items)
            if items:
                dpg.set_value("r_alq_tipo_doc", items[0])

    except Exception as e:
        print(f"Error cargando opciones en reportes: {e}")


# --- Registro de la Vista ---

def register():
    if dpg.does_item_exist(_TAG):
        dpg.delete_item(_TAG)

    with dpg.group(tag=_TAG, parent="content_area", show=False):
        dpg.add_spacer(height=10)
        dpg.add_text("Centro de Reportes", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.tab_bar():
            # TAB HISTORIAL CLIENTE
            with dpg.tab(label="📋 Historial Cliente"):
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_combo(tag="r_alq_tipo_doc", width=80, items=[])
                    dpg.add_input_text(tag="r_alq_nro_doc", width=120, hint="Documento", on_enter=True,
                                       callback=_ejecutar_busqueda_alquileres)
                    dpg.add_spacer(width=10)
                    dpg.add_input_text(tag="r_alq_fecha_inicio", width=100, hint="Desde")
                    dpg.add_input_text(tag="r_alq_fecha_fin", width=100, hint="Hasta")
                    dpg.add_button(label="Buscar", callback=_ejecutar_busqueda_alquileres)

                dpg.add_text("", tag="txt_status_busqueda", color=(200, 200, 200))
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_alquileres_cliente", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=450, policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Contrato", init_width_or_weight=0.5)
                    dpg.add_table_column(label="Cliente / Detalle", init_width_or_weight=2.5)
                    dpg.add_table_column(label="Inicio", init_width_or_weight=0.8)
                    dpg.add_table_column(label="Fin", init_width_or_weight=0.8)
                    dpg.add_table_column(label="Monto", init_width_or_weight=0.8)

            # TAB 2: Utilización
            with dpg.tab(label="📈 Demanda Modelos"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_utilizacion)
                dpg.add_spacer(height=5)

                with dpg.group(horizontal=True):
                    with dpg.plot(label="Top 5 Modelos más Alquilados", height=350, width=-1, tag="utilizacion_plot"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="Modelo", tag="utilizacion_x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="Cantidad Alquileres", tag="utilizacion_y_axis")
                        dpg.add_bar_series([], [], label="Alquileres", weight=0.5, tag="utilizacion_bar_series",
                                           parent="utilizacion_y_axis")

                dpg.add_spacer(height=10)
                with dpg.table(tag="tbl_utilizacion", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=250,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Modelo")
                    dpg.add_table_column(label="Cant. Alquileres")
                    dpg.add_table_column(label="Días Reservados")

            # TAB 3: Disponibilidad
            with dpg.tab(label="🚗 Flota Disponible"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_disponibilidad)
                dpg.add_spacer(height=5)
                with dpg.table(tag="tbl_disponibilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Patente")
                    dpg.add_table_column(label="Precio Diario")
                    dpg.add_table_column(label="Estado")

            # TAB 4: Rentabilidad
            with dpg.tab(label="💰 Rentabilidad"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_rentabilidad)
                dpg.add_spacer(height=5)
                with dpg.table(tag="tbl_rentabilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="#", width_fixed=True)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Estado")
                    dpg.add_table_column(label="Base")
                    dpg.add_table_column(label="Extras")
                    dpg.add_table_column(label="Total")

            # TAB 5: Facturación
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
                    dpg.add_table_column(label="#", width_fixed=True)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Fecha Fin")
                    dpg.add_table_column(label="Días")
                    dpg.add_table_column(label="Facturado")

            # TAB 6: Contactos
            with dpg.tab(label="👥 Clientes"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_clientes)
                dpg.add_spacer(height=5)
                with dpg.table(tag="tbl_clientes_report", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Nombre")
                    dpg.add_table_column(label="Apellido")
                    dpg.add_table_column(label="Documento")
                    dpg.add_table_column(label="Contacto")

    register_view("reportes", _TAG)

    # Inicializaciones
    _init_options()
    _load_disponibilidad()
    _load_utilizacion()
    _ejecutar_busqueda_alquileres()  # Carga inicial (sin filtros = todos)
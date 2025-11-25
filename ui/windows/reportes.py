import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.services.workers import run_async
from services.containers.container import Container

_TAG = "view_reportes"
_controller = Container().reporte_controller()


# --- Utilidades de Actualización ---

def _update_table(table_tag, data):
    """Limpia y rellena una tabla con una lista de diccionarios."""
    # 1. Limpiar filas antiguas
    if dpg.does_item_exist(table_tag):
        dpg.delete_item(table_tag, children_only=True)

    if not data:
        return

    # 2. Llenar nuevas filas
    # Asumimos que el orden de las columnas en el dict coincide con la tabla visual
    for row in data:
        with dpg.table_row(parent=table_tag):
            for value in row.values():
                dpg.add_text(str(value))


def _on_facturacion_loaded(result):
    """Callback especial para facturación que recibe (lista, total)."""
    data, total = result
    _update_table("tbl_facturacion", data)
    dpg.set_value("txt_total_facturado", f"Total Facturado: ${total:,.2f}")


# --- Loaders (Disparadores de tareas) ---

def _load_disponibilidad():
    run_async(lambda: _controller.get_disponibilidad_flota(),
              on_success=lambda data: _update_table("tbl_disponibilidad", data))


def _load_rentabilidad():
    run_async(lambda: _controller.get_rentabilidad_contratos(),
              on_success=lambda data: _update_table("tbl_rentabilidad", data))


def _load_utilizacion():
    run_async(lambda: _controller.get_utilizacion_flota(),
              on_success=lambda data: _update_table("tbl_utilizacion", data))


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
            # TAB 1: Disponibilidad de Flota
            with dpg.tab(label="🚗 Disponibilidad"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_disponibilidad)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_disponibilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="ID", width_fixed=True)
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Patente")
                    dpg.add_table_column(label="Precio Diario")
                    dpg.add_table_column(label="Estado")

            # TAB 2: Rentabilidad de Contratos
            with dpg.tab(label="💰 Rentabilidad"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_rentabilidad)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_rentabilidad", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Contrato #", width_fixed=True)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Vehículo")
                    dpg.add_table_column(label="Estado")
                    dpg.add_table_column(label="Monto Base")
                    dpg.add_table_column(label="Extras/Multas")
                    dpg.add_table_column(label="Total Final")

            # TAB 3: Utilización
            with dpg.tab(label="📈 Utilización"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_utilizacion)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_utilizacion", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Patente")
                    dpg.add_table_column(label="Modelo")
                    dpg.add_table_column(label="Cant. Contratos")
                    dpg.add_table_column(label="Días Alquilado")
                    dpg.add_table_column(label="Estado Actual")

            # TAB 4: Facturación Cerrada
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
                    dpg.add_table_column(label="Contrato #", width_fixed=True)
                    dpg.add_table_column(label="Cliente")
                    dpg.add_table_column(label="Fecha Fin")
                    dpg.add_table_column(label="Días")
                    dpg.add_table_column(label="Facturado")

            # TAB 5: Directorio Clientes
            with dpg.tab(label="👥 Contactos"):
                dpg.add_spacer(height=5)
                dpg.add_button(label="🔄 Actualizar", callback=_load_clientes)
                dpg.add_spacer(height=5)

                with dpg.table(tag="tbl_clientes_report", header_row=True, borders_innerH=True,
                               row_background=True, scrollY=True, height=500,
                               policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="ID", width_fixed=True)
                    dpg.add_table_column(label="Nombre")
                    dpg.add_table_column(label="Apellido")
                    dpg.add_table_column(label="Documento")
                    dpg.add_table_column(label="Contacto")

    register_view("reportes", _TAG)

    # Carga inicial de datos
    _load_disponibilidad()
    _load_rentabilidad()
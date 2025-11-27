import dearpygui.dearpygui as dpg

_TAG = "view_contratos"
_TABLE_TAG = "contratos_table"

_contrato_controller = None


def _refresh_table():
    if not _contrato_controller:
        return
    contratos = _contrato_controller.get_all_contratos_en_curso()
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)
    for contrato in contratos:
        cliente = contrato.get("Cliente", "")
        fecha_desde = contrato.get("FechaDesde", "")
        fecha_hasta = contrato.get("FechaHasta", "")
        estado = contrato.get("Estado", "")
        vehiculo = contrato.get("Vehiculo", "")
        precio_diario = contrato.get("PrecioDiario", "")
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(cliente)
            dpg.add_text(fecha_desde)
            dpg.add_text(fecha_hasta)
            dpg.add_text(estado)
            dpg.add_text(vehiculo)
            dpg.add_text(str(precio_diario))


def register(contrato_controller):
    from ui.navigation import register_view
    global _contrato_controller
    _contrato_controller = contrato_controller
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Contratos en Curso", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)
        with dpg.table(
            tag=_TABLE_TAG,
            header_row=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            row_background=True,
            resizable=True,
            policy=dpg.mvTable_SizingStretchProp,
            scrollY=True,
            height=500
        ):
            dpg.add_table_column(label="Cliente", init_width_or_weight=2.0)
            dpg.add_table_column(label="Fecha Desde", init_width_or_weight=1.2)
            dpg.add_table_column(label="Fecha Hasta", init_width_or_weight=1.2)
            dpg.add_table_column(label="Estado", init_width_or_weight=1.2)
            dpg.add_table_column(label="Vehículo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Precio Diario", init_width_or_weight=1.2)
    # Llamar a _refresh_table() cuando sea necesario para actualizar los datos
    register_view("alquileres", _TAG)

import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from services.containers.container import Container

# Identificadores únicos para los elementos de la UI
_TAG = "view_mantenimiento"
_TABLE_TAG = "mantenimientos_table"

# Instanciamos el controlador usando el contenedor de inyección de dependencias
_controller = Container().mantenimiento_controller()


def _refresh_table():
    """Obtiene los datos actualizados del controlador y rellena la tabla."""
    if not _controller:
        return

    # Obtener lista de diccionarios desde el controlador
    data = _controller.get_all_mantenimientos()

    # Actualizar etiqueta de total
    if dpg.does_item_exist("total_mantenimientos_txt"):
        dpg.set_value("total_mantenimientos_txt", f"Total Registros: {len(data)}")

    # Limpiar filas antiguas si existen
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    # Llenar nuevas filas
    for row in data:
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(row.get("ID", "")))
            dpg.add_text(row.get("Vehículo", ""))
            dpg.add_text(row.get("Descripción", ""))
            dpg.add_text(row.get("Costo", ""))
            dpg.add_text(row.get("Fecha", ""))
            dpg.add_text(row.get("Estado", ""))
            dpg.add_text(row.get("Empleado", ""))


def register():
    """Registra la ventana en el sistema de navegación."""
    if dpg.does_item_exist(_TAG):
        dpg.delete_item(_TAG)

    # Grupo principal de la vista (oculto por defecto)
    with dpg.group(tag=_TAG, parent="content_area", show=False):
        dpg.add_spacer(height=10)
        dpg.add_text("Historial de Mantenimientos", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        # Barra de herramientas
        with dpg.group(horizontal=True):
            dpg.add_button(label="Refrescar", callback=_refresh_table)
            dpg.add_spacer(width=20)
            dpg.add_text("Total Registros: 0", tag="total_mantenimientos_txt")

        dpg.add_spacer(height=10)

        # Tabla de datos
        with dpg.table(tag=_TABLE_TAG, header_row=True, borders_innerH=True,
                       row_background=True, scrollY=True, height=500,
                       policy=dpg.mvTable_SizingStretchProp):
            # Definición de columnas
            dpg.add_table_column(label="ID", init_width_or_weight=0.3)
            dpg.add_table_column(label="Vehículo", init_width_or_weight=0.8)
            dpg.add_table_column(label="Descripción", init_width_or_weight=2.5)
            dpg.add_table_column(label="Costo", init_width_or_weight=0.6)
            dpg.add_table_column(label="Fecha", init_width_or_weight=0.8)
            dpg.add_table_column(label="Estado", init_width_or_weight=0.8)
            dpg.add_table_column(label="Mecánico/Empleado", init_width_or_weight=1.2)

    # Registrar la vista con el nombre clave que usa el menú ('mantenimiento')
    register_view("mantenimiento", _TAG)

    # Cargar datos iniciales
    _refresh_table()
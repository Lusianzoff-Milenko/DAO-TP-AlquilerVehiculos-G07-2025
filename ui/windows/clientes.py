import dearpygui.dearpygui as dpg
from ui.navigation import register_view

_TAG = "view_clientes"


def register():
    # Usamos GROUP, igual que en vehículos
    with dpg.group(tag=_TAG, parent="content_area", show=False):
        dpg.add_spacer(height=10)
        dpg.add_text("Gestión de Clientes", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_button(label="+ Nuevo Cliente")
        dpg.add_spacer(height=10)

        # Tabla mock de prueba
        with dpg.table(header_row=True, borders_innerH=True, row_background=True,
                       policy=dpg.mvTable_SizingStretchProp, scrollY=True, height=-1):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Nombre")
            dpg.add_table_column(label="DNI")

            # Datos de prueba
            with dpg.table_row():
                dpg.add_text("1")
                dpg.add_text("Juan Perez")
                dpg.add_text("12345678")
            with dpg.table_row():
                dpg.add_text("2")
                dpg.add_text("Maria Gomez")
                dpg.add_text("87654321")

    register_view("clientes", _TAG)
import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.form_dialog import FormDialog
from ui.services.workers import run_async
from services.containers.container import Container

_TAG = "view_vehiculos"
_TABLE_TAG = "vehiculos_table_real"

_container = Container()
_controller = _container.vehiculo_controller()
_form_dialog = None
_options_cache = {}


def _load_data():
    run_async(lambda: _controller.get_all_vehiculos(), on_success=_refresh_table)


def _load_options():
    run_async(lambda: _controller.get_form_options(), on_success=lambda opts: _options_cache.update(opts))


def _refresh_table(data):
    # Borrar filas anteriores
    if dpg.does_item_exist(_TABLE_TAG):
        dpg.delete_item(_TABLE_TAG, children_only=True)

    # Agregar filas nuevas
    for row in data:
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(row.get("ID", "")))
            dpg.add_text(row.get("Patente", ""))
            dpg.add_text(row.get("Marca", ""))
            dpg.add_text(row.get("Modelo", ""))
            dpg.add_text(row.get("Color", ""))
            dpg.add_text(str(row.get("Año", "")))
            dpg.add_text(f"${row.get('Precio', 0)}")
            dpg.add_text(row.get("Estado", ""))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Edit", callback=lambda s, a, r=row: _form_dialog.show(r))
                dpg.add_button(label="Del", callback=lambda s, a, r=row: _on_eliminar(r))


def _on_guardar(data):
    # Mapeo inverso simplificado
    mod_name = data.get("Modelo")
    col_name = data.get("Color")
    data['id_modelo'] = next((m['value'] for m in _options_cache.get('modelos', []) if m['label'] == mod_name), None)
    data['id_color'] = next((c['value'] for c in _options_cache.get('colores', []) if c['label'] == col_name), None)

    run_async(lambda: _controller.update_vehiculo(data) if data.get("ID") else _controller.create_vehiculo(data),
              on_success=lambda x: _load_data())


def _on_eliminar(row):
    run_async(lambda: _controller.delete_vehiculo(row["ID"]), on_success=lambda x: _load_data())


def register():
    global _form_dialog

    # USAMOS GROUP (No child_window) para la vista, así se ajusta al content_area
    with dpg.group(tag=_TAG, parent="content_area", show=False):
        dpg.add_spacer(height=10)
        dpg.add_text("Gestión de Flota", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Nuevo Vehículo", callback=lambda: _form_dialog.show())
            dpg.add_button(label="Recargar", callback=_load_data)

        dpg.add_spacer(height=10)

        # Tabla directa
        with dpg.table(tag=_TABLE_TAG, header_row=True, borders_innerH=True, row_background=True,
                       policy=dpg.mvTable_SizingStretchProp, scrollY=True, height=-1):
            # Columnas Fijas (IDs, Fechas cortas, Botones)
            dpg.add_table_column(label="ID", width_fixed=True, init_width_or_weight=40)
            dpg.add_table_column(label="Patente", width_fixed=True, init_width_or_weight=80)

            # Columnas Flexibles (Se estiran para llenar el espacio y mostrar todo el texto)
            # Al quitar width_fixed=True, se vuelven elásticas
            dpg.add_table_column(label="Marca", width_stretch=True, init_width_or_weight=1.0)
            dpg.add_table_column(label="Modelo", width_stretch=True,
                                 init_width_or_weight=1.5)  # Le damos más peso al modelo
            dpg.add_table_column(label="Color", width_stretch=True, init_width_or_weight=0.8)

            dpg.add_table_column(label="Año", width_fixed=True, init_width_or_weight=60)
            dpg.add_table_column(label="Precio", width_fixed=True, init_width_or_weight=80)

            # Estado flexible
            dpg.add_table_column(label="Estado", width_stretch=True, init_width_or_weight=1.0)

            # Acciones fija al final
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=110)

    # Formulario
    _form_dialog = FormDialog(
        tag="vehiculo_form",
        title="Vehículo",
        fields=[
            {'key': 'ID', 'label': 'ID', 'type': 'number', 'required': False},
            {'key': 'Patente', 'label': 'Patente', 'type': 'text', 'required': True},
            {'key': 'Chasis', 'label': 'Chasis', 'type': 'text', 'required': True},
            {'key': 'Modelo', 'label': 'Modelo', 'type': 'combo', 'options': [], 'required': True},
            {'key': 'Color', 'label': 'Color', 'type': 'combo', 'options': [], 'required': True},
            {'key': 'Año', 'label': 'Año', 'type': 'number', 'default': 2024, 'required': True},
            {'key': 'Precio', 'label': 'Precio', 'type': 'float', 'required': True},
        ],
        on_submit=_on_guardar
    )

    register_view("vehiculos", _TAG)
    _load_data()
    _load_options()
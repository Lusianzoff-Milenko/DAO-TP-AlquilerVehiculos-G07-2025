# ui/windows/vehiculos.py
import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.table_view import TableView
from ui.components.form_dialog import FormDialog
from ui.services.workers import run_async
from services.containers.container import Container

_TAG = "view_vehiculos"
_container = Container()  # Instancia del contenedor (o usa una global si tienes una instancia única en app.py)
_controller = _container.vehiculo_controller()  # Instanciamos el controller con sus dependencias

_form_dialog = None
_options_cache = {}  # Para guardar modelos y colores para los combos

def _on_error(e):
    print(f"❌ ERROR cargando vehículos: {e}")

def _load_data():
    """Llama al controller en un hilo separado."""
    print("🔄 Iniciando carga de datos...") # Debug visual
    def task():
        try:
            datos = _controller.get_all_vehiculos()
            print(f"✅ Datos recibidos en hilo ({len(datos)} registros)")
            return datos
        except Exception as e:
            print(f"❌ Error en controller: {e}")
            return []

    # Importante: Pasamos una función lambda para asegurar que _update_table reciba los datos
    run_async(task, on_success=lambda data: _update_table(data))


def _update_table(data):
    """Callback que corre en el hilo principal al terminar la carga."""
    if _table_view:
        print("🔄 Actualizando tabla en hilo principal")
        print(_table_view)
        _table_view.refresh(data)


def _load_options():
    """Carga opciones para los combos (Modelos, Colores)."""

    def task():
        return _controller.get_form_options()

    def on_success(opts):
        global _options_cache
        _options_cache = opts
        # Aquí podríamos actualizar el diálogo si ya estuviera creado

    run_async(task, on_success=on_success)


# --- Acciones de Botones ---

def _on_nuevo_click():
    if _form_dialog:
        # Preparamos las opciones para el combo
        model_names = [m['label'] for m in _options_cache.get('modelos', [])]
        color_names = [c['label'] for c in _options_cache.get('colores', [])]

        # Actualizamos las opciones del dialogo dinámicamente (esto requiere soporte en tu FormDialog o reconstruirlo)
        # Por simplicidad, asumimos que FormDialog puede recibir actualización o se reconstruye.
        _form_dialog.show()


def _on_guardar(data):
    """Data viene del FormDialog."""

    # Mapeo inverso de Nombre -> ID para el controller
    # (Esto es necesario porque el Combo de DearPyGui devuelve strings, no objetos)
    modelo_nombre = data.get("Modelo")
    color_nombre = data.get("Color")

    id_modelo = next((m['value'] for m in _options_cache['modelos'] if m['label'] == modelo_nombre), None)
    id_color = next((c['value'] for c in _options_cache['colores'] if c['label'] == color_nombre), None)

    data['id_modelo'] = id_modelo
    data['id_color'] = id_color

    def task():
        if data.get("ID"):
            return _controller.update_vehiculo(data)
        else:
            return _controller.create_vehiculo(data)

    def on_done(result):
        print(f"Operación resultado: {result}")
        _load_data()  # Recargar tabla

    run_async(task, on_success=on_done)


def _on_eliminar(row):
    def task():
        return _controller.delete_vehiculo(row["ID"])

    run_async(task, on_success=lambda x: _load_data())


def register():
    global _table_view, _form_dialog

    # Registramos la vista primero para asegurar que el tag _TAG exista
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1):
        dpg.add_spacer(height=16)
        dpg.add_text("Gestión de Flota", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)

        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Nuevo Vehículo", callback=_on_nuevo_click)
            dpg.add_spacer(width=10)
            # Botón de auxilio por si la carga automática falla
            dpg.add_button(label="🔄 Recargar Tabla", callback=_load_data)

        dpg.add_spacer(height=12)

        # 1. CREAMOS LA TABLA VISUALMENTE
        _table_view = TableView(
            tag="vehiculos_table_view",
            columns=["ID", "Patente", "Marca", "Modelo", "Color", "Año", "Precio", "Estado"],
            on_edit=lambda row: _form_dialog.show(row),
            on_delete=_on_eliminar
        )
        _table_view.render(_TAG)

        # 2. CREAMOS EL FORMULARIO
        _form_dialog = FormDialog(
            tag="vehiculo_form",
            title="Datos del Vehículo",
            fields=[
                {'key': 'ID', 'label': 'ID', 'type': 'number', 'required': False},
                {'key': 'Patente', 'label': 'Patente', 'type': 'text', 'required': True},
                {'key': 'Chasis', 'label': 'Nro Chasis', 'type': 'text', 'required': True},
                {'key': 'Modelo', 'label': 'Modelo', 'type': 'combo', 'options': [], 'required': True},
                {'key': 'Color', 'label': 'Color', 'type': 'combo', 'options': [], 'required': True},
                {'key': 'Año', 'label': 'Año Fab.', 'type': 'number', 'default': 2024, 'required': True},
                {'key': 'Precio', 'label': 'Precio Diario', 'type': 'float', 'required': True},
            ],
            on_submit=_on_guardar,
            width=500,
            height=500
        )

    # 3. REGISTRO EN SISTEMA DE NAVEGACIÓN
    register_view("vehiculos", _TAG)

    # 4. CARGA DE DATOS (Al final de todo)
    # Esto sigue ocurriendo al inicio del programa, pero ahora la tabla YA existe visualmente
    _load_data()
    _load_options()
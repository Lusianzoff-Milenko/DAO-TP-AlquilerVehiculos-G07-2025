import dearpygui.dearpygui as dpg
from ui.navigation import register_view

_TAG = "view_vehiculos"
_TABLE_TAG = "vehiculos_table"
_SEARCH_TAG = "vehiculos_search"

# Global state
_vehiculo_controller = None
_editing_vehiculo_id = None
_modelos_options = []
_colores_options = []
_estados_options = []
_marcas_options = []


# --- UTILIDADES ---

def _get_center_pos(width, height):
    """Calcula la posición central [x, y] basada en el viewport actual."""
    # Obtener tamaño de la ventana principal
    vp_w = dpg.get_viewport_client_width()
    vp_h = dpg.get_viewport_client_height()
    # Calcular centro
    pos_x = (vp_w - width) // 2
    pos_y = (vp_h - height) // 2
    # Asegurar que no sea negativo
    return [max(0, pos_x), max(0, pos_y)]


def _force_focus(tag):
    """Fuerza el foco en la ventana."""
    if dpg.does_item_exist(tag):
        dpg.focus_item(tag)


# --- GESTIÓN DE DATOS ---
def _get_filtered_data():
    if not _vehiculo_controller: return []
    try:
        vehiculos = _vehiculo_controller.get_all_vehiculos()
        search_text = dpg.get_value(_SEARCH_TAG) if dpg.does_item_exist(_SEARCH_TAG) else ""
        if search_text:
            search_lower = search_text.lower()
            vehiculos = [
                v for v in vehiculos
                if search_lower in v.get("Patente", "").lower()
                   or search_lower in v.get("Marca/Modelo", "").lower()
                   or search_lower in v.get("Color", "").lower()
            ]
        return vehiculos
    except Exception as e:
        print(f"Error obteniendo datos: {e}")
        return []


def _refresh_table():
    vehiculos = _get_filtered_data()

    if dpg.does_item_exist("total_vehiculos"):
        dpg.set_value("total_vehiculos", f"Total: {len(vehiculos)} vehículos")

    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    for vehiculo in vehiculos:
        vehiculo_data = dict(vehiculo)
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(vehiculo.get("Patente", ""))
            dpg.add_text(vehiculo.get("Marca/Modelo", ""))
            dpg.add_text(vehiculo.get("Color", ""))
            dpg.add_text(str(vehiculo.get("Año", "")))
            dpg.add_text(vehiculo.get("Estado", ""))
            dpg.add_text(vehiculo.get("Precio Diario", ""))

            with dpg.group(horizontal=True):
                dpg.add_button(label="Editar", callback=lambda s, a, u=vehiculo_data: _on_editar_vehiculo(u), width=60,
                               user_data=vehiculo_data)
                dpg.add_button(label="Eliminar", callback=lambda s, a, u=vehiculo_data: _on_eliminar_vehiculo(u),
                               width=60, user_data=vehiculo_data)


def _show_error_message(message):
    if dpg.does_item_exist("error_window"): dpg.delete_item("error_window")
    w, h = 400, 150
    # Usamos _get_center_pos para posicionar
    with dpg.window(label="Error", tag="error_window", modal=True, width=w, height=h, pos=_get_center_pos(w, h),
                    no_collapse=True):
        dpg.add_text(message, color=(255, 100, 100), wrap=380)
        dpg.add_spacer(height=20)
        dpg.add_button(label="Aceptar", callback=lambda: dpg.delete_item("error_window"), width=100)
    _force_focus("error_window")


def _refresh_options():
    """Recarga las opciones de los combos."""
    global _modelos_options, _colores_options, _estados_options, _marcas_options
    if not _vehiculo_controller: return

    try:
        options = _vehiculo_controller.get_form_options()
        _modelos_options = options.get("modelos", [])
        _colores_options = options.get("colores", [])
        _estados_options = options.get("estados", [])

        if hasattr(_vehiculo_controller, "get_all_marcas"):
            _marcas_options = _vehiculo_controller.get_all_marcas()
    except Exception as e:
        print(f"Error refrescando opciones: {e}")


def _update_combos_in_ui():
    """Actualiza los items de los combos si las ventanas están abiertas."""
    if dpg.does_item_exist("form_vehiculo_modelo"):
        dpg.configure_item("form_vehiculo_modelo", items=[m["label"] for m in _modelos_options])
    if dpg.does_item_exist("form_vehiculo_color"):
        dpg.configure_item("form_vehiculo_color", items=[c["label"] for c in _colores_options])
    if dpg.does_item_exist("form_modelo_marca"):
        dpg.configure_item("form_modelo_marca", items=[m["label"] for m in _marcas_options])


# --- MODAL: NUEVA MARCA ---
def _on_guardar_nueva_marca(sender, app_data, user_data):
    nombre = dpg.get_value("new_marca_nombre")
    desc = dpg.get_value("new_marca_desc")
    if not nombre:
        _show_error_message("El nombre es obligatorio.")
        return

    if _vehiculo_controller.create_marca(nombre, desc):
        dpg.delete_item("modal_new_marca")
        _refresh_options()
        _update_combos_in_ui()
    else:
        _show_error_message("Error al crear la marca. ¿Ya existe?")


def _show_modal_marca(sender=None, app_data=None, user_data=None):
    if dpg.does_item_exist("modal_new_marca"): dpg.delete_item("modal_new_marca")
    w, h = 320, 200

    with dpg.window(label="Nueva Marca", tag="modal_new_marca", modal=True, width=w, height=h,
                    pos=_get_center_pos(w, h), no_collapse=True):
        dpg.add_text("Nombre de la Marca:")
        dpg.add_input_text(tag="new_marca_nombre", width=-1)
        dpg.add_text("Descripción:")
        dpg.add_input_text(tag="new_marca_desc", width=-1)
        dpg.add_spacer(height=15)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Guardar", callback=_on_guardar_nueva_marca, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("modal_new_marca"), width=100)
    _force_focus("modal_new_marca")


# --- MODAL: NUEVO MODELO ---
def _on_guardar_nuevo_modelo(sender, app_data, user_data):
    nombre = dpg.get_value("new_modelo_nombre")
    marca_nombre = dpg.get_value("form_modelo_marca")

    if not nombre or not marca_nombre:
        _show_error_message("Nombre y Marca son obligatorios.")
        return

    id_marca = next((m["value"] for m in _marcas_options if m["label"] == marca_nombre), None)
    if not id_marca:
        _show_error_message("Marca no válida.")
        return

    # Recopilar datos incluyendo Pasajeros y Puertas
    data = {
        "nombre": nombre,
        "id_marca": id_marca,
        "pasajeros": dpg.get_value("new_modelo_pasajeros"),
        "puertas": dpg.get_value("new_modelo_puertas"),
        "motor": dpg.get_value("new_modelo_motor"),
        "anio": dpg.get_value("new_modelo_anio")
    }

    if _vehiculo_controller.create_modelo(data):
        dpg.delete_item("modal_new_modelo")
        _refresh_options()
        _update_combos_in_ui()
    else:
        _show_error_message("Error al crear modelo.")


def _show_modal_modelo(sender=None, app_data=None, user_data=None):
    if dpg.does_item_exist("modal_new_modelo"): dpg.delete_item("modal_new_modelo")
    _refresh_options()
    w, h = 350, 420  # Altura ajustada para más campos

    with dpg.window(label="Nuevo Modelo", tag="modal_new_modelo", modal=True, width=w, height=h,
                    pos=_get_center_pos(w, h), no_collapse=True):
        dpg.add_text("Marca:")
        dpg.add_combo(items=[m["label"] for m in _marcas_options], tag="form_modelo_marca", width=-1)

        dpg.add_text("Nombre Modelo:")
        dpg.add_input_text(tag="new_modelo_nombre", width=-1)

        dpg.add_spacer(height=5)

        # Fila para Pasajeros y Puertas
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("Pasajeros:")
                dpg.add_input_int(tag="new_modelo_pasajeros", default_value=5, width=150, min_value=1, min_clamped=True)

            dpg.add_spacer(width=10)

            with dpg.group():
                dpg.add_text("Puertas:")
                dpg.add_input_int(tag="new_modelo_puertas", default_value=4, width=150, min_value=1, min_clamped=True)

        dpg.add_spacer(height=5)
        dpg.add_text("Motor:")
        dpg.add_input_text(tag="new_modelo_motor", default_value="1.6L", width=-1)

        dpg.add_text("Año Lanzamiento:")
        dpg.add_input_int(tag="new_modelo_anio", default_value=2024, width=-1)

        dpg.add_spacer(height=15)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Guardar", callback=_on_guardar_nuevo_modelo, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("modal_new_modelo"), width=100)
    _force_focus("modal_new_modelo")


# --- MODAL: NUEVO COLOR ---
def _on_guardar_nuevo_color(sender, app_data, user_data):
    nombre = dpg.get_value("new_color_nombre")
    if not nombre:
        _show_error_message("El nombre es obligatorio.")
        return

    if _vehiculo_controller.create_color(nombre):
        dpg.delete_item("modal_new_color")
        _refresh_options()
        _update_combos_in_ui()
    else:
        _show_error_message("Error al crear color. ¿Ya existe?")


def _show_modal_color(sender=None, app_data=None, user_data=None):
    if dpg.does_item_exist("modal_new_color"): dpg.delete_item("modal_new_color")
    w, h = 320, 150

    with dpg.window(label="Nuevo Color", tag="modal_new_color", modal=True, width=w, height=h,
                    pos=_get_center_pos(w, h), no_collapse=True):
        dpg.add_text("Nombre del Color:")
        dpg.add_input_text(tag="new_color_nombre", width=-1)
        dpg.add_spacer(height=15)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Guardar", callback=_on_guardar_nuevo_color, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("modal_new_color"), width=100)
    _force_focus("modal_new_color")


# --- FORMULARIO VEHÍCULO ---
def _on_nuevo_vehiculo(sender=None, app_data=None, user_data=None):
    global _editing_vehiculo_id
    _editing_vehiculo_id = None
    _show_formulario()


def _on_editar_vehiculo(vehiculo):
    global _editing_vehiculo_id
    _editing_vehiculo_id = vehiculo["ID"]

    form_data = {
        "Patente": vehiculo.get("Patente", ""),
        "Chasis": vehiculo.get("Chasis", ""),
        "Año": vehiculo.get("Año", 2024),
        "Precio": vehiculo.get("Precio", 0.0),
    }

    id_modelo = vehiculo.get("id_modelo")
    id_color = vehiculo.get("id_color")

    _refresh_options()

    for m in _modelos_options:
        if m["value"] == id_modelo:
            form_data["Modelo"] = m["label"]
            break
    for c in _colores_options:
        if c["value"] == id_color:
            form_data["Color"] = c["label"]
            break

    _show_formulario(form_data)


def _on_guardar_vehiculo(sender, app_data, user_data):
    patente = dpg.get_value("form_vehiculo_patente")
    chasis = dpg.get_value("form_vehiculo_chasis")
    precio = dpg.get_value("form_vehiculo_precio")
    modelo_nombre = dpg.get_value("form_vehiculo_modelo")
    color_nombre = dpg.get_value("form_vehiculo_color")

    if not (patente and chasis and modelo_nombre and color_nombre):
        _show_error_message("Todos los campos son obligatorios.")
        return

    data = {
        "Patente": patente,
        "Chasis": chasis,
        "Año": int(dpg.get_value("form_vehiculo_anio")),
        "Precio": float(precio),
        "id_estado": 1 if not _editing_vehiculo_id else None
    }

    for m in _modelos_options:
        if m["label"] == modelo_nombre:
            data["id_modelo"] = m["value"]
            break
    for c in _colores_options:
        if c["label"] == color_nombre:
            data["id_color"] = c["value"]
            break

    try:
        if _editing_vehiculo_id:
            if _vehiculo_controller.update_vehiculo(_editing_vehiculo_id, data):
                dpg.delete_item("ventana_form_vehiculo")
                _refresh_table()
            else:
                _show_error_message("Error al actualizar.")
        else:
            if _vehiculo_controller.create_vehiculo(data):
                dpg.delete_item("ventana_form_vehiculo")
                _refresh_table()
            else:
                _show_error_message("Error al crear (verifique duplicados).")
    except Exception as e:
        _show_error_message(f"Excepción: {str(e)}")


def _on_eliminar_vehiculo(vehiculo):
    if _vehiculo_controller.delete_vehiculo(vehiculo["ID"]):
        _refresh_table()
    else:
        _show_error_message("No se puede eliminar (tiene historial).")


def _show_formulario(data=None):
    if dpg.does_item_exist("ventana_form_vehiculo"): dpg.delete_item("ventana_form_vehiculo")
    _refresh_options()
    w, h = 450, 450

    with dpg.window(label="Gestión Vehículo", tag="ventana_form_vehiculo", modal=True, width=w, height=h,
                    pos=_get_center_pos(w, h), no_collapse=True):
        dpg.add_input_text(label="Patente", tag="form_vehiculo_patente",
                           default_value=data.get("Patente", "") if data else "", width=200)
        dpg.add_input_text(label="Chasis", tag="form_vehiculo_chasis",
                           default_value=data.get("Chasis", "") if data else "", width=200)

        dpg.add_combo(label="Modelo", tag="form_vehiculo_modelo", items=[m["label"] for m in _modelos_options],
                      default_value=data.get("Modelo", "") if data else "", width=200)
        dpg.add_combo(label="Color", tag="form_vehiculo_color", items=[c["label"] for c in _colores_options],
                      default_value=data.get("Color", "") if data else "", width=200)

        dpg.add_input_int(label="Año", tag="form_vehiculo_anio", default_value=data.get("Año", 2024) if data else 2024,
                          width=200)
        dpg.add_input_float(label="Precio Diario", tag="form_vehiculo_precio",
                            default_value=float(data.get("Precio", 0.0)) if data else 0.0, width=200, format="%.2f")

        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Guardar", callback=_on_guardar_vehiculo, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("ventana_form_vehiculo"), width=100)

    _force_focus("ventana_form_vehiculo")


def register(vehiculo_controller):
    global _vehiculo_controller
    _vehiculo_controller = vehiculo_controller

    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Gestión de Flota", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)

        # BARRA DE HERRAMIENTAS
        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Vehículo", width=100, callback=_on_nuevo_vehiculo)
            dpg.add_spacer(width=15)
            dpg.add_button(label="+ Marca", width=90, callback=_show_modal_marca)
            dpg.add_button(label="+ Modelo", width=90, callback=_show_modal_modelo)
            dpg.add_button(label="+ Color", width=90, callback=_show_modal_color)

            dpg.add_spacer(width=20)
            dpg.add_text("Total: 0", tag="total_vehiculos")

            dpg.add_spacer(width=20)
            dpg.add_input_text(hint="Buscar...", tag=_SEARCH_TAG, callback=_refresh_table, width=180)

        dpg.add_spacer(height=12)
        with dpg.table(tag=_TABLE_TAG, header_row=True, row_background=True, resizable=True,
                       policy=dpg.mvTable_SizingStretchProp, scrollY=True, height=500):
            dpg.add_table_column(label="Patente")
            dpg.add_table_column(label="Marca/Modelo")
            dpg.add_table_column(label="Color")
            dpg.add_table_column(label="Año")
            dpg.add_table_column(label="Estado")
            dpg.add_table_column(label="Precio")
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=160)

            try:
                _refresh_table()
            except Exception as e:
                print(f"Error carga inicial vehiculos: {e}")

    register_view("vehiculos", _TAG)
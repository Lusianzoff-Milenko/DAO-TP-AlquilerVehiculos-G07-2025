import dearpygui.dearpygui as dpg
from ui.navigation import register_view

_TAG = "view_empleados"
_TABLE_TAG = "empleados_table"

_empleado_controller = None
_editing_empleado_id = None
_puestos_options = []

def _get_filtered_data():
    if not _empleado_controller:
        return []
    return _empleado_controller.get_all_empleados()

def _refresh_table():
    empleados = _get_filtered_data()
    if dpg.does_item_exist("total_empleados"):
        dpg.set_value("total_empleados", f"Total: {len(empleados)} empleados")
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)
    for empleado in empleados:
        e_id = empleado.get("ID")
        e_nombre_completo = f"{empleado.get('Nombre', '')} {empleado.get('Apellido', '')}"
        e_puesto = empleado.get("Puesto", "")
        e_email = empleado.get("Email", "")
        e_telefono = empleado.get("Teléfono", "")
        e_ingreso = empleado.get("Ingreso", "")
        empleado_data = dict(empleado)
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(e_nombre_completo)
            dpg.add_text(e_puesto)
            dpg.add_text(e_email)
            dpg.add_text(e_telefono)
            dpg.add_text(e_ingreso)
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Editar",
                    callback=lambda s, a, u=empleado_data: _on_editar_empleado(u),
                    width=70,
                    user_data=empleado_data
                )

def _show_error_message(message):
    if dpg.does_item_exist("error_window"):
        dpg.delete_item("error_window")
    with dpg.window(
        label="Error",
        tag="error_window",
        modal=True,
        width=400,
        height=150,
        no_resize=True,
        pos=[440, 300]
    ):
        dpg.add_text(message, color=(255, 100, 100))
        dpg.add_spacer(height=20)
        dpg.add_button(
            label="Aceptar",
            callback=lambda: dpg.delete_item("error_window"),
            width=-1
        )

def _on_nuevo_empleado():
    global _editing_empleado_id
    _editing_empleado_id = None
    _show_formulario()

def _on_editar_empleado(empleado):
    if not empleado:
        return
    global _editing_empleado_id
    _editing_empleado_id = empleado["ID"]
    # Buscar datos completos del empleado para el formulario
    empleado_id = empleado.get("ID")
    form_data = None
    if _empleado_controller:
        if hasattr(_empleado_controller, "get_empleado_full_data"):
            form_data = _empleado_controller.get_empleado_full_data(empleado_id)
            if form_data:
                for puesto in _puestos_options:
                    if puesto["value"] == form_data.get("id_tipo_puesto"):
                        form_data["Puesto"] = puesto["label"]
                        break
                _show_formulario(form_data)
                return
        else:
            _show_error_message("Error: El controlador de empleados no tiene el método get_empleado_full_data. Reinicie la aplicación.")
            return
    # Fallback si no se pudo obtener datos completos
    nombre = empleado.get("Nombre", "")
    apellido = empleado.get("Apellido", "")
    if not apellido and nombre and " " in nombre:
        partes = nombre.split()
        nombre = partes[0]
        apellido = " ".join(partes[1:])
    form_data = {
        "Nombre": nombre,
        "Apellido": apellido,
        "Email": empleado.get("Email", ""),
        "Teléfono": empleado.get("Teléfono", ""),
        "Dirección": empleado.get("Dirección", ""),
        "Fecha Nacimiento": empleado.get("Fecha Nacimiento", "2000-01-01"),
    }
    id_puesto = empleado.get("id_tipo_puesto")
    for puesto in _puestos_options:
        if puesto["value"] == id_puesto:
            form_data["Puesto"] = puesto["label"]
            break
    _show_formulario(form_data)

def _on_guardar_empleado(sender, app_data, user_data):
    global _editing_empleado_id
    nombre = dpg.get_value("form_empleado_nombre")
    apellido = dpg.get_value("form_empleado_apellido")
    email = dpg.get_value("form_empleado_email")
    if not nombre or not apellido or not email:
        _show_error_message("Error: Nombre, Apellido y Email son obligatorios")
        return
    from datetime import datetime
    fecha_nac_str = dpg.get_value("form_empleado_fecha_nac")
    try:
        fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
        hoy = datetime.now()
        edad = (hoy - fecha_nac).days / 365.25
        if edad < 18:
            _show_error_message("Error: El empleado debe ser mayor de 18 años")
            return
    except ValueError:
        _show_error_message("Error: Formato de fecha inválido. Use YYYY-MM-DD")
        return
    data = {
        "Nombre": nombre,
        "Apellido": apellido,
        "Email": email,
        "Teléfono": dpg.get_value("form_empleado_telefono"),
        "Dirección": dpg.get_value("form_empleado_direccion"),
        "Fecha Nacimiento": fecha_nac_str,
    }
    puesto_nombre = dpg.get_value("form_empleado_puesto")
    if not puesto_nombre:
        _show_error_message("Error: Debe seleccionar un Puesto")
        return
    for puesto in _puestos_options:
        if puesto["label"] == puesto_nombre:
            data["id_tipo_puesto"] = puesto["value"]
            break
    try:
        if _editing_empleado_id:
            success = _empleado_controller.update_empleado(_editing_empleado_id, data)
            if success:
                _editing_empleado_id = None
                if dpg.does_item_exist("ventana_form_empleado"):
                    dpg.delete_item("ventana_form_empleado")
                _refresh_table()
            else:
                _show_error_message("Error al actualizar empleado.")
        else:
            new_id = _empleado_controller.create_empleado(data)
            if new_id:
                if dpg.does_item_exist("ventana_form_empleado"):
                    dpg.delete_item("ventana_form_empleado")
                _refresh_table()
            else:
                _show_error_message("Error al crear empleado.")
    except Exception as e:
        _show_error_message(f"Error inesperado: {str(e)}")

def _show_formulario(data=None):
    if dpg.does_item_exist("ventana_form_empleado"):
        dpg.delete_item("ventana_form_empleado")
    is_edit = data is not None
    with dpg.window(
        label="Editar Empleado" if is_edit else "Nuevo Empleado",
        tag="ventana_form_empleado",
        modal=False,
        width=450,
        height=520,
        no_resize=True,
        pos=[450, 100],
        on_close=lambda: dpg.delete_item("ventana_form_empleado")
    ):
        dpg.add_input_text(
            label="Nombre",
            tag="form_empleado_nombre",
            default_value=data.get("Nombre", "") if data else "",
            width=200
        )
        dpg.add_input_text(
            label="Apellido",
            tag="form_empleado_apellido",
            default_value=data.get("Apellido", "") if data else "",
            width=200
        )
        dpg.add_input_text(
            label="Email",
            tag="form_empleado_email",
            default_value=data.get("Email", "") if data else "",
            width=200
        )
        dpg.add_input_text(
            label="Teléfono",
            tag="form_empleado_telefono",
            default_value=data.get("Teléfono", "") if data else "",
            width=200
        )
        dpg.add_input_text(
            label="Dirección",
            tag="form_empleado_direccion",
            default_value=data.get("Dirección", "") if data else "",
            width=200
        )
        dpg.add_combo(
            label="Puesto",
            tag="form_empleado_puesto",
            items=[p["label"] for p in _puestos_options],
            default_value=data.get("Puesto", "") if data else "",
            width=200
        )
        dpg.add_input_text(
            label="Fecha Nacimiento (YYYY-MM-DD)",
            tag="form_empleado_fecha_nac",
            default_value=data.get("Fecha Nacimiento", "2000-01-01") if data else "2000-01-01",
            width=200
        )
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Guardar",
                callback=_on_guardar_empleado,
                width=100
            )
            dpg.add_button(
                label="Cancelar",
                callback=lambda: dpg.delete_item("ventana_form_empleado"),
                width=100
            )

def register(empleado_controller):
    global _empleado_controller, _puestos_options
    _empleado_controller = empleado_controller
    options = _empleado_controller.get_form_options()
    _puestos_options = options.get("puestos", [])
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Gestión de Empleados", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=12)
            dpg.add_text("Total: 0 empleados", tag="total_empleados")
            dpg.add_spacer(width=20)
            dpg.add_button(label="Nuevo Empleado", callback=_on_nuevo_empleado, width=140)
        dpg.add_spacer(height=12)
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
            dpg.add_table_column(label="Nombre Completo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Puesto", init_width_or_weight=1.5)
            dpg.add_table_column(label="Email", init_width_or_weight=2.0)
            dpg.add_table_column(label="Teléfono", init_width_or_weight=1.2)
            dpg.add_table_column(label="Fecha Ingreso", init_width_or_weight=1.0)
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=150)
            try:
                empleados = _empleado_controller.get_all_empleados()
                if dpg.does_item_exist("total_empleados"):
                    dpg.set_value("total_empleados", f"Total: {len(empleados)} empleados")
                for empleado in empleados:
                    e_id = empleado.get("ID")
                    e_nombre_completo = f"{empleado.get('Nombre', '')} {empleado.get('Apellido', '')}"
                    e_puesto = empleado.get("Puesto", "")
                    e_email = empleado.get("Email", "")
                    e_telefono = empleado.get("Teléfono", "")
                    e_ingreso = empleado.get("Ingreso", "")
                    empleado_data = dict(empleado)
                    with dpg.table_row():
                        dpg.add_text(e_nombre_completo)
                        dpg.add_text(e_puesto)
                        dpg.add_text(e_email)
                        dpg.add_text(e_telefono)
                        dpg.add_text(e_ingreso)
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label="Editar",
                                callback=lambda s, a, u=empleado_data: _on_editar_empleado(u),
                                width=70,
                                user_data=empleado_data
                            )
            except Exception as e:
                print(f"[Empleados] Error cargando datos iniciales: {e}")
    register_view("empleados", _TAG)

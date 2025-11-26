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


def _get_filtered_data():
    """Obtiene datos de la base de datos y aplica filtros."""
    vehiculos = _vehiculo_controller.get_all_vehiculos()
    
    # Aplicar filtro de búsqueda
    search_text = dpg.get_value(_SEARCH_TAG) if dpg.does_item_exist(_SEARCH_TAG) else ""
    if search_text:
        search_lower = search_text.lower()
        vehiculos = [
            v for v in vehiculos
            if search_lower in v.get("Patente", "").lower()
            or search_lower in v.get("Marca/Modelo", "").lower()
            or search_lower in v.get("Color", "").lower()
            or search_lower in str(v.get("Año", "")).lower()
            or search_lower in v.get("Estado", "").lower()
        ]
    
    return vehiculos


def _refresh_table():
    """Recarga la tabla desde la base de datos."""
    if dpg.does_item_exist(_TABLE_TAG):
        dpg.delete_item(_TABLE_TAG, children_only=True)
    
    vehiculos = _get_filtered_data()
    print(f"[Vehiculos] Recargando {len(vehiculos)} vehículos en la tabla")
    
    # Actualizar contador
    if dpg.does_item_exist("total_vehiculos"):
        dpg.set_value("total_vehiculos", f"Total: {len(vehiculos)} vehículos")
    
    for vehiculo in vehiculos:
        vehiculo_data = dict(vehiculo)
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(vehiculo_data.get("ID", "")))
            dpg.add_text(vehiculo_data.get("Patente", ""))
            dpg.add_text(vehiculo_data.get("Marca/Modelo", ""))
            dpg.add_text(vehiculo_data.get("Color", ""))
            dpg.add_text(str(vehiculo_data.get("Año", "")))
            dpg.add_text(vehiculo_data.get("Estado", ""))
            dpg.add_text(vehiculo_data.get("Precio Diario", ""))
            
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Editar",
                    callback=lambda s, a, v=vehiculo_data: _on_editar_vehiculo(v),
                    width=70
                )
                dpg.add_button(
                    label="Eliminar",
                    callback=lambda s, a, v=vehiculo_data: _on_eliminar_vehiculo(v),
                    width=70
                )


def _on_nuevo_vehiculo():
    """Abre el formulario para crear un nuevo vehículo."""
    global _editing_vehiculo_id
    _editing_vehiculo_id = None
    _show_formulario()


def _on_editar_vehiculo(vehiculo):
    """Abre el formulario para editar un vehículo existente."""
    global _editing_vehiculo_id
    _editing_vehiculo_id = vehiculo["ID"]
    
    print(f"[Vehiculos] Editando vehículo ID: {_editing_vehiculo_id}")
    print(f"[Vehiculos] Datos: {vehiculo}")
    
    # Preparar datos para el formulario
    form_data = {
        "Patente": vehiculo.get("Patente", ""),
        "Chasis": vehiculo.get("Chasis", ""),
        "Año": vehiculo.get("Año", 2024),
        "Precio": vehiculo.get("Precio", 0.0),
    }
    
    # Mapear IDs a nombres para los combos
    id_modelo = vehiculo.get("id_modelo")
    id_color = vehiculo.get("id_color")
    id_estado = vehiculo.get("id_estado")
    
    for modelo in _modelos_options:
        if modelo["value"] == id_modelo:
            form_data["Modelo"] = modelo["label"]
            break
    
    for color in _colores_options:
        if color["value"] == id_color:
            form_data["Color"] = color["label"]
            break
    
    for estado in _estados_options:
        if estado["value"] == id_estado:
            form_data["Estado"] = estado["label"]
            break
    
    _show_formulario(form_data)


def _on_guardar_vehiculo(sender, app_data, user_data):
    """Guarda un vehículo (crear o actualizar)."""
    global _editing_vehiculo_id
    
    # Recopilar datos del formulario
    data = {
        "Patente": dpg.get_value("form_vehiculo_patente"),
        "Chasis": dpg.get_value("form_vehiculo_chasis"),
        "Año": int(dpg.get_value("form_vehiculo_anio")),
        "Precio": float(dpg.get_value("form_vehiculo_precio")),
    }
    
    # Mapear nombres de combo a IDs
    modelo_nombre = dpg.get_value("form_vehiculo_modelo")
    color_nombre = dpg.get_value("form_vehiculo_color")
    estado_nombre = dpg.get_value("form_vehiculo_estado")
    
    for modelo in _modelos_options:
        if modelo["label"] == modelo_nombre:
            data["id_modelo"] = modelo["value"]
            break
    
    for color in _colores_options:
        if color["label"] == color_nombre:
            data["id_color"] = color["value"]
            break
    
    for estado in _estados_options:
        if estado["label"] == estado_nombre:
            data["id_estado"] = estado["value"]
            break
    
    try:
        if _editing_vehiculo_id:
            # Actualizar vehículo existente
            success = _vehiculo_controller.update_vehiculo(_editing_vehiculo_id, data)
            if success:
                print(f"Vehículo {_editing_vehiculo_id} actualizado exitosamente")
            else:
                print(f"Error al actualizar vehículo {_editing_vehiculo_id}")
        else:
            # Crear nuevo vehículo
            vehiculo_id = _vehiculo_controller.create_vehiculo(data)
            if vehiculo_id:
                print(f"Vehículo creado con ID: {vehiculo_id}")
            else:
                print("Error al crear vehículo")
        
        # Cerrar formulario y refrescar tabla
        dpg.delete_item("ventana_form_vehiculo")
        _refresh_table()
        _editing_vehiculo_id = None
        
    except Exception as e:
        print(f"Error al guardar vehículo: {e}")


def _on_eliminar_vehiculo(vehiculo):
    """Elimina un vehículo."""
    try:
        success = _vehiculo_controller.delete_vehiculo(vehiculo["ID"])
        if success:
            print(f"Vehículo {vehiculo['ID']} eliminado exitosamente")
            _refresh_table()
        else:
            print(f"Error al eliminar vehículo {vehiculo['ID']}")
    except Exception as e:
        print(f"Error al eliminar vehículo: {e}")


def _show_formulario(data=None):
    """Muestra el formulario de vehículo."""
    if dpg.does_item_exist("ventana_form_vehiculo"):
        dpg.delete_item("ventana_form_vehiculo")
    
    with dpg.window(
        label="Nuevo Vehículo" if not data else "Editar Vehículo",
        tag="ventana_form_vehiculo",
        modal=True,
        width=400,
        height=500,
        no_resize=True,
        pos=[400, 150]
    ):
        dpg.add_input_text(
            label="Patente",
            tag="form_vehiculo_patente",
            default_value=data.get("Patente", "") if data else "",
            width=200
        )
        
        dpg.add_input_text(
            label="Chasis",
            tag="form_vehiculo_chasis",
            default_value=data.get("Chasis", "") if data else "",
            width=200
        )
        
        dpg.add_combo(
            label="Modelo",
            tag="form_vehiculo_modelo",
            items=[m["label"] for m in _modelos_options],
            default_value=data.get("Modelo", "") if data else "",
            width=200
        )
        
        dpg.add_combo(
            label="Color",
            tag="form_vehiculo_color",
            items=[c["label"] for c in _colores_options],
            default_value=data.get("Color", "") if data else "",
            width=200
        )
        
        dpg.add_combo(
            label="Estado",
            tag="form_vehiculo_estado",
            items=[e["label"] for e in _estados_options],
            default_value=data.get("Estado", "") if data else "",
            width=200
        )
        
        dpg.add_input_int(
            label="Año",
            tag="form_vehiculo_anio",
            default_value=data.get("Año", 2024) if data else 2024,
            width=200
        )
        
        dpg.add_input_float(
            label="Precio Diario",
            tag="form_vehiculo_precio",
            default_value=float(data.get("Precio", 0.0)) if data else 0.0,
            width=200,
            format="%.2f"
        )
        
        dpg.add_spacer(height=10)
        
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Guardar",
                callback=_on_guardar_vehiculo,
                width=100
            )
            dpg.add_button(
                label="Cancelar",
                callback=lambda: dpg.delete_item("ventana_form_vehiculo"),
                width=100
            )


def register(vehiculo_controller):
    """Registra la vista de vehículos."""
    global _vehiculo_controller, _modelos_options, _colores_options, _estados_options
    
    _vehiculo_controller = vehiculo_controller
    
    # Cargar opciones para los combos
    options = _vehiculo_controller.get_form_options()
    _modelos_options = options.get("modelos", [])
    _colores_options = options.get("colores", [])
    _estados_options = options.get("estados", [])
    
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1):
        dpg.add_spacer(height=16)
        
        dpg.add_text("Gestión de Flota", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)
        
        # Barra de herramientas
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="+ Nuevo Vehículo",
                width=150,
                callback=lambda: _on_nuevo_vehiculo()
            )
            dpg.add_button(
                label="Actualizar",
                width=100,
                callback=lambda: _refresh_table()
            )
            dpg.add_spacer(width=12)
            vehiculos_count = len(_get_filtered_data())
            dpg.add_text(f"Total: {vehiculos_count} vehículos", tag="total_vehiculos")
        
        dpg.add_spacer(height=12)
        
        # Tabla de vehículos
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
            dpg.add_table_column(label="ID", init_width_or_weight=0.5)
            dpg.add_table_column(label="Patente", init_width_or_weight=1.0)
            dpg.add_table_column(label="Marca/Modelo", init_width_or_weight=2.5)
            dpg.add_table_column(label="Color", init_width_or_weight=1.0)
            dpg.add_table_column(label="Año", init_width_or_weight=0.8)
            dpg.add_table_column(label="Estado", init_width_or_weight=1.2)
            dpg.add_table_column(label="Precio Diario", init_width_or_weight=1.2)
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=150)
            
            # Cargar datos directamente
            vehiculos = _get_filtered_data()
            print(f"[Vehiculos] Cargando {len(vehiculos)} vehículos en la tabla")
            for vehiculo in vehiculos:
                vehiculo_data = dict(vehiculo)
                with dpg.table_row():
                    dpg.add_text(str(vehiculo_data.get("ID", "")))
                    dpg.add_text(vehiculo_data.get("Patente", ""))
                    dpg.add_text(vehiculo_data.get("Marca/Modelo", ""))
                    dpg.add_text(vehiculo_data.get("Color", ""))
                    dpg.add_text(str(vehiculo_data.get("Año", "")))
                    dpg.add_text(vehiculo_data.get("Estado", ""))
                    dpg.add_text(vehiculo_data.get("Precio Diario", ""))
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Editar",
                            callback=lambda s, a, v=vehiculo_data: _on_editar_vehiculo(v),
                            width=70
                        )
                        dpg.add_button(
                            label="Eliminar",
                            callback=lambda s, a, v=vehiculo_data: _on_eliminar_vehiculo(v),
                            width=70
                        )
    
    register_view("vehiculos", _TAG)
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
    vehiculos = _get_filtered_data()
    print(f"[Vehiculos] Recargando {len(vehiculos)} vehículos en la tabla")
    
    # Actualizar contador
    if dpg.does_item_exist("total_vehiculos"):
        dpg.set_value("total_vehiculos", f"Total: {len(vehiculos)} vehículos")
    
    # Eliminar filas existentes (slot 1 contiene las filas)
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)
    
    # Agregar las filas actualizadas
    for vehiculo in vehiculos:
        # Crear una copia inmutable para el callback
        v_id = vehiculo.get("ID")
        v_patente = vehiculo.get("Patente", "")
        v_marca_modelo = vehiculo.get("Marca/Modelo", "")
        v_color = vehiculo.get("Color", "")
        v_anio = vehiculo.get("Año", "")
        v_estado = vehiculo.get("Estado", "")
        v_precio = vehiculo.get("Precio Diario", "")
        v_chasis = vehiculo.get("Chasis", "")
        v_precio_num = vehiculo.get("Precio", 0.0)
        v_id_modelo = vehiculo.get("id_modelo")
        v_id_color = vehiculo.get("id_color")
        v_id_estado = vehiculo.get("id_estado")
        
        # Crear diccionario completo para callbacks
        vehiculo_data = {
            "ID": v_id,
            "Patente": v_patente,
            "Marca/Modelo": v_marca_modelo,
            "Color": v_color,
            "Año": v_anio,
            "Estado": v_estado,
            "Precio Diario": v_precio,
            "Chasis": v_chasis,
            "Precio": v_precio_num,
            "id_modelo": v_id_modelo,
            "id_color": v_id_color,
            "id_estado": v_id_estado
        }
        
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(v_patente)
            dpg.add_text(v_marca_modelo)
            dpg.add_text(v_color)
            dpg.add_text(str(v_anio))
            dpg.add_text(v_estado)
            dpg.add_text(v_precio)
            
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Editar",
                    callback=lambda s, a, u=vehiculo_data: _on_editar_vehiculo(u),
                    width=70,
                    user_data=vehiculo_data
                )
                dpg.add_button(
                    label="Eliminar",
                    callback=lambda s, a, u=vehiculo_data: _on_eliminar_vehiculo(u),
                    width=70,
                    user_data=vehiculo_data
                )


def _show_error_message(message):
    """Muestra un mensaje de error en una ventana modal."""
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


def _on_nuevo_vehiculo():
    """Abre el formulario para crear un nuevo vehículo."""
    global _editing_vehiculo_id
    _editing_vehiculo_id = None
    print("[Vehiculos] Abriendo formulario para nuevo vehículo")
    _show_formulario()


def _on_editar_vehiculo(vehiculo):
    """Abre el formulario para editar un vehículo existente."""
    if not vehiculo:
        print("[Vehiculos] Error: vehiculo es None")
        return
    
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
    
    # Validar campos requeridos
    patente = dpg.get_value("form_vehiculo_patente")
    chasis = dpg.get_value("form_vehiculo_chasis")
    precio = float(dpg.get_value("form_vehiculo_precio"))
    
    if not patente or not chasis:
        _show_error_message("Error: Patente y Chasis son obligatorios")
        return
    
    if precio < 0:
        _show_error_message("Error: El precio diario no puede ser negativo")
        return
    
    # Recopilar datos del formulario
    data = {
        "Patente": patente,
        "Chasis": chasis,
        "Año": int(dpg.get_value("form_vehiculo_anio")),
        "Precio": precio,
    }
    
    # Mapear nombres de combo a IDs
    modelo_nombre = dpg.get_value("form_vehiculo_modelo")
    color_nombre = dpg.get_value("form_vehiculo_color")
    
    if not modelo_nombre or not color_nombre:
        _show_error_message("Error: Debe seleccionar Modelo y Color")
        return
    
    for modelo in _modelos_options:
        if modelo["label"] == modelo_nombre:
            data["id_modelo"] = modelo["value"]
            break
    
    for color in _colores_options:
        if color["label"] == color_nombre:
            data["id_color"] = color["value"]
            break
    
    # Al crear, siempre usar estado "Disponible" (ID 1)
    # Al actualizar, no incluir id_estado para mantener el estado actual
    if not _editing_vehiculo_id:
        data["id_estado"] = 1
    
    try:
        if _editing_vehiculo_id:
            # Actualizar vehículo existente
            success = _vehiculo_controller.update_vehiculo(_editing_vehiculo_id, data)
            if success:
                print(f"Vehículo {_editing_vehiculo_id} actualizado exitosamente")
                _editing_vehiculo_id = None
                # Cerrar formulario
                if dpg.does_item_exist("ventana_form_vehiculo"):
                    dpg.delete_item("ventana_form_vehiculo")
                # Refrescar tabla después de cerrar
                _refresh_table()
            else:
                _show_error_message("Error al actualizar vehículo. Verifique que Patente/Chasis no estén duplicados.")
        else:
            # Crear nuevo vehículo
            vehiculo_id = _vehiculo_controller.create_vehiculo(data)
            if vehiculo_id:
                print(f"Vehículo creado con ID: {vehiculo_id}")
                _editing_vehiculo_id = None
                # Cerrar formulario
                if dpg.does_item_exist("ventana_form_vehiculo"):
                    dpg.delete_item("ventana_form_vehiculo")
                # Refrescar tabla después de cerrar
                _refresh_table()
            else:
                _show_error_message("Error al crear vehículo. La Patente o el Chasis ya existen en la base de datos.")
        
    except Exception as e:
        print(f"Error al guardar vehículo: {e}")
        _show_error_message(f"Error inesperado: {str(e)}")


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
    
    is_edit = data is not None
    
    with dpg.window(
        label="Nuevo Vehículo" if not is_edit else "Editar Vehículo",
        tag="ventana_form_vehiculo",
        modal=False,
        width=450,
        height=500,
        no_resize=True,
        pos=[450, 100],
        on_close=lambda: dpg.delete_item("ventana_form_vehiculo")
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
            format="%.2f",
            min_value=0.0,
            min_clamped=True
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
    
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
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
            dpg.add_spacer(width=12)
            dpg.add_text("Total: 0 vehículos", tag="total_vehiculos")
        
        dpg.add_spacer(height=12)
        
        # Tabla de vehículos (crear vacía)
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
            dpg.add_table_column(label="Patente", init_width_or_weight=1.0)
            dpg.add_table_column(label="Marca/Modelo", init_width_or_weight=2.5)
            dpg.add_table_column(label="Color", init_width_or_weight=1.0)
            dpg.add_table_column(label="Año", init_width_or_weight=0.8)
            dpg.add_table_column(label="Estado", init_width_or_weight=1.2)
            dpg.add_table_column(label="Precio Diario", init_width_or_weight=1.2)
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=150)
            
            # Cargar datos iniciales directamente en la tabla
            try:
                vehiculos = _vehiculo_controller.get_all_vehiculos()
                print(f"[Vehiculos] Cargando {len(vehiculos)} vehículos en la tabla")
                
                # Actualizar contador
                if dpg.does_item_exist("total_vehiculos"):
                    dpg.set_value("total_vehiculos", f"Total: {len(vehiculos)} vehículos")
                
                for vehiculo in vehiculos:
                    # Crear una copia inmutable para el callback
                    v_id = vehiculo.get("ID")
                    v_patente = vehiculo.get("Patente", "")
                    v_marca_modelo = vehiculo.get("Marca/Modelo", "")
                    v_color = vehiculo.get("Color", "")
                    v_anio = vehiculo.get("Año", "")
                    v_estado = vehiculo.get("Estado", "")
                    v_precio = vehiculo.get("Precio Diario", "")
                    v_chasis = vehiculo.get("Chasis", "")
                    v_precio_num = vehiculo.get("Precio", 0.0)
                    v_id_modelo = vehiculo.get("id_modelo")
                    v_id_color = vehiculo.get("id_color")
                    v_id_estado = vehiculo.get("id_estado")
                    
                    # Crear diccionario completo para callbacks
                    vehiculo_data = {
                        "ID": v_id,
                        "Patente": v_patente,
                        "Marca/Modelo": v_marca_modelo,
                        "Color": v_color,
                        "Año": v_anio,
                        "Estado": v_estado,
                        "Precio Diario": v_precio,
                        "Chasis": v_chasis,
                        "Precio": v_precio_num,
                        "id_modelo": v_id_modelo,
                        "id_color": v_id_color,
                        "id_estado": v_id_estado
                    }
                    
                    with dpg.table_row():
                        dpg.add_text(v_patente)
                        dpg.add_text(v_marca_modelo)
                        dpg.add_text(v_color)
                        dpg.add_text(str(v_anio))
                        dpg.add_text(v_estado)
                        dpg.add_text(v_precio)
                        
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label="Editar",
                                callback=lambda s, a, u=vehiculo_data: _on_editar_vehiculo(u),
                                width=70,
                                user_data=vehiculo_data
                            )
                            dpg.add_button(
                                label="Eliminar",
                                callback=lambda s, a, u=vehiculo_data: _on_eliminar_vehiculo(u),
                                width=70,
                                user_data=vehiculo_data
                            )
            except Exception as e:
                print(f"[Vehiculos] Error cargando datos iniciales: {e}")
    
    register_view("vehiculos", _TAG)
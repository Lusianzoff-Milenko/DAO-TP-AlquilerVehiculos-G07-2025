import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.form_dialog import FormDialog
from typing import Optional

_TAG = "view_clientes"

_cliente_controller = None
_form_dialog = None
_current_filter = {"query": ""}
_tipos_documento_options = []
_editing_cliente_id = None  # ID del cliente siendo editado

def _get_filtered_data():
    """Obtiene y filtra los datos desde la base de datos."""
    if not _cliente_controller:
        return []
    
    try:
        # Obtener todos los clientes desde la BD
        clientes = _cliente_controller.get_all_clientes()
        
        # Concatenar Nombre + Apellido para mostrar nombre completo
        for c in clientes:
            c["Nombre Completo"] = f"{c['Nombre']} {c['Apellido']}"
        
        query = _current_filter["query"].lower()
        
        # Filtrar por búsqueda
        if query:
            clientes = [
                c for c in clientes
                if query in c["Nombre"].lower() 
                or query in c["Apellido"].lower()
                or query in c["Documento"].lower() 
                or query in c["Email"].lower()
            ]
        
        return clientes
    except Exception as e:
        print(f"Error obteniendo clientes: {e}")
        return []

def _on_search(query: str):
    """Maneja la búsqueda."""
    _current_filter["query"] = query
    _refresh_table()

def _on_nuevo_cliente():
    """Abre el diálogo para crear un nuevo cliente."""
    global _editing_cliente_id
    _editing_cliente_id = None
    if _form_dialog:
        _form_dialog.show()

def _on_editar_cliente(cliente: dict):
    """Abre el diálogo para editar un cliente existente."""
    global _editing_cliente_id
    
    if not _form_dialog:
        return
    
    try:
        # Guardar el ID del cliente que se está editando
        _editing_cliente_id = cliente.get("ID", 0)
        
        # Mapear los datos del cliente al formato del formulario (sin ID)
        form_data = {
            "Nombre": cliente.get("Nombre", ""),
            "Apellido": cliente.get("Apellido", ""),
            "Documento": cliente.get("Documento", ""),
            "id_tipo_documento": cliente.get("Tipo Doc", "DNI"),  # Nombre del tipo
            "Email": cliente.get("Email", ""),
            "Teléfono": cliente.get("Teléfono", ""),
            "Dirección": cliente.get("Dirección", ""),
            "Fecha Nacimiento": "2000-01-01"  # Placeholder - no tenemos fecha en el get_all
        }
        _form_dialog.show(data=form_data)
    except Exception as e:
        print(f"ERROR en _on_editar_cliente: {e}")
        _show_notification(f"Error al abrir edición: {str(e)}", error=True)

def _on_eliminar_cliente(cliente: dict):
    """Elimina un cliente con confirmación."""
    # Crear ventana de confirmación
    with dpg.window(label="Confirmar eliminación", modal=True, width=400, height=150, tag="confirm_delete"):
        dpg.add_spacer(height=12)
        dpg.add_text(f"¿Está seguro que desea eliminar al cliente '{cliente['Nombre Completo']}'?")
        dpg.add_spacer(height=12)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=80)
            dpg.add_button(
                label="Sí, eliminar",
                width=100,
                callback=lambda: _confirmar_eliminacion(cliente)
            )
            dpg.add_button(
                label="Cancelar",
                width=100,
                callback=lambda: dpg.delete_item("confirm_delete")
            )
    
    # Centrar ventana
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    dpg.set_item_pos("confirm_delete", [(viewport_width - 400) // 2, (viewport_height - 150) // 2])

def _confirmar_eliminacion(cliente: dict):
    """Elimina el cliente de la base de datos."""
    try:
        success = _cliente_controller.delete_cliente(cliente["ID"])
        
        if success:
            _show_notification(f"Cliente '{cliente['Nombre Completo']}' eliminado correctamente")
            _refresh_table()
        else:
            _show_notification(f"Error: No se pudo eliminar el cliente. Puede tener contratos asociados.", error=True)
    except Exception as e:
        _show_notification(f"Error al eliminar: {str(e)}", error=True)
    
    dpg.delete_item("confirm_delete")

def _on_guardar_cliente(data: dict):
    """Guarda un cliente nuevo o editado en la base de datos."""
    global _editing_cliente_id
    
    try:
        # Mapear el índice del combo al ID real del tipo de documento
        tipo_doc_value = data.get('id_tipo_documento', '')
        if isinstance(tipo_doc_value, str):
            # Si viene como string (nombre del tipo), buscar el ID
            tipo_doc_labels = [label for label, _ in _tipos_documento_options]
            if tipo_doc_value in tipo_doc_labels:
                tipo_doc_index = tipo_doc_labels.index(tipo_doc_value)
                data['id_tipo_documento'] = _tipos_documento_options[tipo_doc_index][1]
            else:
                data['id_tipo_documento'] = _tipos_documento_options[0][1] if _tipos_documento_options else 1
        
        nombre_completo = f"{data['Nombre']} {data['Apellido']}"
        
        if _editing_cliente_id and _editing_cliente_id > 0:
            # Es edición
            success = _cliente_controller.update_cliente(_editing_cliente_id, data)
            
            if success:
                _show_notification(f"Cliente '{nombre_completo}' actualizado correctamente")
                _refresh_table()
            else:
                _show_notification(f"Error al actualizar el cliente. Verifique los datos.", error=True)
            
            _editing_cliente_id = None
        else:
            # Es creación
            nuevo_id = _cliente_controller.create_cliente(data)
            
            if nuevo_id:
                _show_notification(f"Cliente '{nombre_completo}' creado correctamente")
                _refresh_table()
            else:
                _show_notification(f"Error al crear el cliente. Verifique los datos.", error=True)
    except Exception as e:
        _show_notification(f"Error: {str(e)}", error=True)

def _refresh_table():
    """Recarga los datos de la tabla desde la base de datos."""
    if not dpg.does_item_exist("clientes_table"):
        return
    
    # Eliminar todas las filas existentes
    children = dpg.get_item_children("clientes_table", slot=1)  # slot 1 = rows
    if children:
        for child in children:
            dpg.delete_item(child)
    
    # Agregar nuevas filas con datos actualizados
    clientes = _get_filtered_data()
    for cliente in clientes:
        # Crear una copia del cliente para evitar problemas con la lambda
        cliente_data = dict(cliente)
        with dpg.table_row(parent="clientes_table"):
            dpg.add_text(str(cliente_data["ID"]))
            dpg.add_text(cliente_data["Nombre Completo"])
            dpg.add_text(cliente_data["Documento"])
            dpg.add_text(cliente_data["Email"])
            dpg.add_text(cliente_data["Teléfono"])
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Editar",
                    callback=lambda s, a, u=cliente_data: _on_editar_cliente(u),
                    width=60,
                    user_data=cliente_data
                )
    
    # Actualizar contador
    if dpg.does_item_exist("total_clientes"):
        dpg.set_value("total_clientes", f"Total: {len(clientes)} clientes")

def _show_notification(message: str, error: bool = False):
    """Muestra una notificación temporal."""
    color = (255, 100, 100) if error else (100, 255, 100)
    
    if dpg.does_item_exist("notification_text"):
        dpg.set_value("notification_text", message)
        dpg.configure_item("notification_text", color=color)
    else:
        dpg.add_text(message, tag="notification_text", color=color, parent=_TAG, before="search_container")
    
    # Auto-ocultar después de 3 segundos
    import threading
    def hide_notification():
        import time
        time.sleep(3)
        if dpg.does_item_exist("notification_text"):
            dpg.delete_item("notification_text")
    
    threading.Thread(target=hide_notification, daemon=True).start()

def register(cliente_controller):
    """Registra la vista de clientes."""
    global _form_dialog, _cliente_controller, _tipos_documento_options
    
    _cliente_controller = cliente_controller
    
    # Cargar opciones de tipos de documento
    try:
        form_options = _cliente_controller.get_form_options()
        _tipos_documento_options = [(opt["label"], opt["value"]) for opt in form_options["tipos_documento"]]
    except Exception as e:
        print(f"Error cargando tipos de documento: {e}")
        _tipos_documento_options = [("DNI", 1)]
    
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1):
        dpg.add_spacer(height=16)
        
        # Título
        dpg.add_text("Gestión de Clientes", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)
        
        # Botón nuevo cliente
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="+ Nuevo Cliente",
                width=150,
                callback=_on_nuevo_cliente
            )
            dpg.add_spacer(width=12)
            clientes_count = len(_get_filtered_data())
            dpg.add_text(f"Total: {clientes_count} clientes", tag="total_clientes")
        
        dpg.add_spacer(height=12)
        
        # Tabla simple de clientes
        with dpg.table(
            tag="clientes_table",
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
            # Headers con anchos proporcionales
            dpg.add_table_column(label="ID", init_width_or_weight=0.5)
            dpg.add_table_column(label="Nombre Completo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Documento", init_width_or_weight=1.0)
            dpg.add_table_column(label="Email", init_width_or_weight=2.5)
            dpg.add_table_column(label="Teléfono", init_width_or_weight=1.5)
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=70)
            
            # Datos desde la base de datos
            clientes = _get_filtered_data()
            for cliente in clientes:
                # Crear una copia del cliente para evitar problemas con la lambda
                cliente_data = dict(cliente)
                with dpg.table_row():
                    dpg.add_text(str(cliente_data["ID"]))
                    dpg.add_text(cliente_data["Nombre Completo"])
                    dpg.add_text(cliente_data["Documento"])
                    dpg.add_text(cliente_data["Email"])
                    dpg.add_text(cliente_data["Teléfono"])
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Editar",
                            callback=lambda s, a, u=cliente_data: _on_editar_cliente(u),
                            width=60,
                            user_data=cliente_data
                        )
        
        # Formulario de cliente (modal)
        tipo_doc_labels = [label for label, _ in _tipos_documento_options]
        _form_dialog = FormDialog(
            tag="cliente_form",
            title="Cliente",
            fields=[
                {'key': 'Nombre', 'label': 'Nombre', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Apellido', 'label': 'Apellido', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Documento', 'label': 'Documento', 'type': 'text', 'default': '', 'required': True},
                {'key': 'id_tipo_documento', 'label': 'Tipo Documento', 'type': 'combo', 'default': _tipos_documento_options[0][0] if _tipos_documento_options else "DNI", 'required': True, 'options': tipo_doc_labels},
                {'key': 'Email', 'label': 'Email', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Teléfono', 'label': 'Teléfono', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Dirección', 'label': 'Dirección', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Fecha Nacimiento', 'label': 'Fecha Nacimiento (YYYY-MM-DD)', 'type': 'text', 'default': '2000-01-01', 'required': True}
            ],
            on_submit=_on_guardar_cliente,
            width=600,
            height=500
        )
    
    register_view("clientes", _TAG)

import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.table_view import TableView
from ui.components.search_box import SearchBox
from ui.components.form_dialog import FormDialog

_TAG = "view_clientes"

# Mock de datos de clientes
_clientes_data = [
    {"ID": 1, "Nombre": "Juan Pérez", "DNI": "12345678", "Email": "juan.perez@email.com", "Teléfono": "1123456789", "Estado": "Activo"},
    {"ID": 2, "Nombre": "María García", "DNI": "23456789", "Email": "maria.garcia@email.com", "Teléfono": "1134567890", "Estado": "Activo"},
    {"ID": 3, "Nombre": "Carlos López", "DNI": "34567890", "Email": "carlos.lopez@email.com", "Teléfono": "1145678901", "Estado": "Activo"},
    {"ID": 4, "Nombre": "Ana Martínez", "DNI": "45678901", "Email": "ana.martinez@email.com", "Teléfono": "1156789012", "Estado": "Inactivo"},
    {"ID": 5, "Nombre": "Luis Rodríguez", "DNI": "56789012", "Email": "luis.rodriguez@email.com", "Teléfono": "1167890123", "Estado": "Activo"},
    {"ID": 6, "Nombre": "Laura Fernández", "DNI": "67890123", "Email": "laura.fernandez@email.com", "Teléfono": "1178901234", "Estado": "Activo"},
    {"ID": 7, "Nombre": "Diego Sánchez", "DNI": "78901234", "Email": "diego.sanchez@email.com", "Teléfono": "1189012345", "Estado": "Activo"},
    {"ID": 8, "Nombre": "Sofía González", "DNI": "89012345", "Email": "sofia.gonzalez@email.com", "Teléfono": "1190123456", "Estado": "Inactivo"},
]

_next_id = 9
_table_view = None
_form_dialog = None
_current_filter = {"query": "", "estado": "Todos"}

def _get_filtered_data():
    """Filtra los datos según búsqueda y filtros activos."""
    query = _current_filter["query"].lower()
    estado_filter = _current_filter["estado"]
    
    filtered = _clientes_data
    
    # Filtrar por estado
    if estado_filter != "Todos":
        filtered = [c for c in filtered if c["Estado"] == estado_filter]
    
    # Filtrar por búsqueda
    if query:
        filtered = [
            c for c in filtered
            if query in c["Nombre"].lower() or query in c["DNI"] or query in c["Email"].lower()
        ]
    
    return filtered

def _on_search(query: str, filters: dict):
    """Maneja la búsqueda y filtros."""
    _current_filter["query"] = query
    _current_filter["estado"] = filters.get("estado", "Todos")
    
    if _table_view:
        _table_view.refresh(_get_filtered_data())

def _on_nuevo_cliente():
    """Abre el diálogo para crear un nuevo cliente."""
    if _form_dialog:
        _form_dialog.show()

def _on_editar_cliente(cliente: dict):
    """Abre el diálogo para editar un cliente existente."""
    if _form_dialog:
        _form_dialog.show(data=cliente)

def _on_eliminar_cliente(cliente: dict):
    """Elimina un cliente con confirmación."""
    # Crear ventana de confirmación
    with dpg.window(label="Confirmar eliminación", modal=True, width=400, height=150, tag="confirm_delete"):
        dpg.add_spacer(height=12)
        dpg.add_text(f"¿Está seguro que desea eliminar al cliente '{cliente['Nombre']}'?")
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
    """Elimina el cliente de la lista."""
    global _clientes_data
    _clientes_data = [c for c in _clientes_data if c["ID"] != cliente["ID"]]
    
    if _table_view:
        _table_view.refresh(_get_filtered_data())
    
    dpg.delete_item("confirm_delete")
    _show_notification(f"Cliente '{cliente['Nombre']}' eliminado correctamente")

def _on_guardar_cliente(data: dict):
    """Guarda un cliente nuevo o editado."""
    global _next_id, _clientes_data
    
    # Validar DNI único
    dni = data["DNI"]
    cliente_id = data.get("ID")
    
    # Verificar si el DNI ya existe (excepto el actual en caso de edición)
    dni_existente = any(c["DNI"] == dni and c["ID"] != cliente_id for c in _clientes_data)
    if dni_existente:
        _show_notification(f"Error: Ya existe un cliente con DNI {dni}", error=True)
        return
    
    if cliente_id:
        # Editar existente
        for i, c in enumerate(_clientes_data):
            if c["ID"] == cliente_id:
                _clientes_data[i] = {
                    "ID": cliente_id,
                    "Nombre": data["Nombre"],
                    "DNI": dni,
                    "Email": data["Email"],
                    "Teléfono": data["Teléfono"],
                    "Estado": data["Estado"]
                }
                _show_notification(f"Cliente '{data['Nombre']}' actualizado correctamente")
                break
    else:
        # Crear nuevo
        nuevo_cliente = {
            "ID": _next_id,
            "Nombre": data["Nombre"],
            "DNI": dni,
            "Email": data["Email"],
            "Teléfono": data["Teléfono"],
            "Estado": data["Estado"]
        }
        _clientes_data.append(nuevo_cliente)
        _next_id += 1
        _show_notification(f"Cliente '{data['Nombre']}' creado correctamente")
    
    if _table_view:
        _table_view.refresh(_get_filtered_data())

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

def register():
    """Registra la vista de clientes."""
    global _table_view, _form_dialog
    
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
            dpg.add_text(f"Total: {len(_clientes_data)} clientes", tag="total_clientes")
        
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
            # Headers
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Nombre")
            dpg.add_table_column(label="DNI")
            dpg.add_table_column(label="Email")
            dpg.add_table_column(label="Teléfono")
            dpg.add_table_column(label="Estado")
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=150)
            
            # Datos
            for cliente in _clientes_data:
                with dpg.table_row():
                    dpg.add_text(str(cliente["ID"]))
                    dpg.add_text(cliente["Nombre"])
                    dpg.add_text(cliente["DNI"])
                    dpg.add_text(cliente["Email"])
                    dpg.add_text(cliente["Teléfono"])
                    dpg.add_text(cliente["Estado"])
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Editar",
                            callback=lambda s, a, c=cliente: _on_editar_cliente(c),
                            width=60
                        )
                        dpg.add_button(
                            label="Eliminar",
                            callback=lambda s, a, c=cliente: _on_eliminar_cliente(c),
                            width=70
                        )
        
        # Formulario de cliente (modal)
        _form_dialog = FormDialog(
            tag="cliente_form",
            title="Cliente",
            fields=[
                {'key': 'ID', 'label': 'ID', 'type': 'number', 'default': 0, 'required': False},
                {'key': 'Nombre', 'label': 'Nombre Completo', 'type': 'text', 'default': '', 'required': True},
                {'key': 'DNI', 'label': 'DNI', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Email', 'label': 'Email', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Teléfono', 'label': 'Teléfono', 'type': 'text', 'default': '', 'required': True},
                {'key': 'Estado', 'label': 'Estado', 'type': 'combo', 'default': 'Activo', 'required': True, 'options': ['Activo', 'Inactivo']}
            ],
            on_submit=_on_guardar_cliente,
            width=600,
            height=450
        )
    
    register_view("clientes", _TAG)

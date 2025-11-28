import dearpygui.dearpygui as dpg
from ui.components.form_dialog import FormDialog
from ui.navigation import register_view

_TAG = "view_reservas"
_TABLE_TAG = "reservas_table"

_contrato_controller = None
_form_dialog = None
_form_options = None
_selected_reserva_id = None
_selected_reserva_monto = 0.0


def _show_notification(message: str, error: bool = False):
    color = (255, 100, 100) if error else (100, 255, 100)
    tag_notif = "reservas_notification"
    if dpg.does_item_exist(tag_notif):
        dpg.set_value(tag_notif, message)
        dpg.configure_item(tag_notif, color=color)
    else:
        dpg.add_text(message, tag=tag_notif, color=color, parent=_TAG, before=_TABLE_TAG)

    import threading
    import time
    def hide():
        time.sleep(3)
        if dpg.does_item_exist(tag_notif): dpg.delete_item(tag_notif)

    threading.Thread(target=hide, daemon=True).start()


def _refresh_table():
    if not _contrato_controller: return

    # Obtener todos y filtrar
    todos = _contrato_controller.get_all_contratos()
    reservas = [c for c in todos if c.get("Estado") == "EnReservado"]

    if dpg.does_item_exist("total_reservas_txt"):
        dpg.set_value("total_reservas_txt", f"Total Reservas: {len(reservas)}")

    # Limpiar tabla
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children: dpg.delete_item(child)

    # Llenar tabla
    for r in reservas:
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(r.get("ID")))
            dpg.add_text(r.get("Cliente"))
            dpg.add_text(r.get("Vehículo"))
            dpg.add_text(r.get("Desde"))
            dpg.add_text(r.get("Hasta"))
            dpg.add_text(r.get("Total"))

            # Botón de acción
            dpg.add_button(
                label="Entregar Vehículo",
                callback=lambda s, a, u=r: _abrir_confirmacion_pago(u),
                user_data=r
            )


def _abrir_confirmacion_pago(reserva_data):
    global _selected_reserva_id, _selected_reserva_monto
    _selected_reserva_id = reserva_data.get("ID")

    # Intentar parsear el monto total desde el string "$123.00" o usar raw si existe
    try:
        if "raw_total" in reserva_data:
            _selected_reserva_monto = float(reserva_data["raw_total"])
        else:
            txt = reserva_data.get("Total", "0").replace("$", "").strip()
            _selected_reserva_monto = float(txt)
    except:
        _selected_reserva_monto = 0.0

    # Crear ventana modal
    if dpg.does_item_exist("modal_pago_reserva"):
        dpg.delete_item("modal_pago_reserva")

    with dpg.window(label="Confirmar Entrega", tag="modal_pago_reserva", modal=True, width=350, height=200,
                    pos=[400, 200], no_resize=True):
        dpg.add_text(f"Contrato #{_selected_reserva_id}")
        dpg.add_text("Para entregar el vehículo, el cliente debe abonar.")
        dpg.add_spacer(height=5)
        dpg.add_input_float(label="Monto Abonado ($)", tag="input_monto_pago", default_value=_selected_reserva_monto)
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Confirmar y Entregar", callback=_on_confirmar_entrega, width=150)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("modal_pago_reserva"), width=100)


# ... código anterior ...

# CAMBIO: Agregar sender, app_data, user_data
def _on_confirmar_entrega(sender, app_data, user_data):
    global _selected_reserva_id
    monto = dpg.get_value("input_monto_pago")

    # (Opcional) Validación básica
    if not monto:
        monto = 0.0

    if _contrato_controller.iniciar_alquiler(_selected_reserva_id, monto):
        _show_notification("Vehículo entregado. Contrato pasó a 'En Curso'.")
        dpg.delete_item("modal_pago_reserva")
        _refresh_table()
    else:
        _show_notification("Error al iniciar alquiler.", error=True)

# ... resto del código ...

# ... (El resto de _on_nueva_reserva y _on_guardar_reserva se mantiene igual al paso anterior) ...
def _on_nueva_reserva():
    if _form_dialog: _form_dialog.show()


def _on_guardar_reserva(data: dict):
    # Lógica de mapeo de IDs igual que antes
    try:
        # Recuperar IDs reales de los combos
        cli_lbl = data.get('id_cliente')
        veh_lbl = data.get('id_vehiculo')
        pag_lbl = data.get('id_metodo_pago')

        # Buscar en opciones
        cli_id = next((x['value'] for x in _form_options['clientes'] if x['label'] == cli_lbl), None)
        veh_id = next((x['value'] for x in _form_options['vehiculos'] if x['label'] == veh_lbl), None)
        pag_id = next((x['value'] for x in _form_options['pagos'] if x['label'] == pag_lbl), None)

        if not (cli_id and veh_id and pag_id):
            _show_notification("Error: Seleccione opciones válidas.", error=True)
            return

        data['id_cliente'] = cli_id
        data['id_vehiculo'] = veh_id
        data['id_metodo_pago'] = pag_id
        data['Seguro'] = bool(data.get('Seguro', False))

        if _contrato_controller.crear_reserva(data):
            _show_notification("Reserva creada.")
            _refresh_table()
        else:
            _show_notification("Error al crear reserva.", error=True)
    except Exception as e:
        _show_notification(f"Excepción: {e}", error=True)


def register(contrato_controller):
    global _contrato_controller, _form_dialog, _form_options
    _contrato_controller = contrato_controller

    # Cargar opciones
    _form_options = _contrato_controller.get_form_options() if _contrato_controller else {'clientes': [],
                                                                                          'vehiculos': [], 'pagos': []}

    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Reservas Pendientes", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)

        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Nueva Reserva", callback=_on_nueva_reserva, width=150)
            dpg.add_spacer(width=20)
            dpg.add_text("Total: 0", tag="total_reservas_txt")
            dpg.add_spacer(width=20)
            dpg.add_button(label="Refrescar", callback=_refresh_table)

        dpg.add_spacer(height=10)
        dpg.add_text("", tag="reservas_notification")

        with dpg.table(tag=_TABLE_TAG, header_row=True, row_background=True, resizable=True, scrollY=True, height=500,
                       policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(label="ID", init_width_or_weight=0.5)
            dpg.add_table_column(label="Cliente", init_width_or_weight=2.0)
            dpg.add_table_column(label="Vehículo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Desde", init_width_or_weight=1.0)
            dpg.add_table_column(label="Hasta", init_width_or_weight=1.0)
            dpg.add_table_column(label="Total", init_width_or_weight=1.0)
            dpg.add_table_column(label="Acciones", init_width_or_weight=1.5)

        # Configurar formulario
        _form_dialog = FormDialog(
            tag="modal_nueva_reserva",
            title="Nueva Reserva",
            fields=[
                {'key': 'id_cliente', 'label': 'Cliente', 'type': 'combo',
                 'options': [x['label'] for x in _form_options['clientes']], 'required': True},
                {'key': 'id_vehiculo', 'label': 'Vehículo', 'type': 'combo',
                 'options': [x['label'] for x in _form_options['vehiculos']], 'required': True},
                {'key': 'id_metodo_pago', 'label': 'Pago', 'type': 'combo',
                 'options': [x['label'] for x in _form_options['pagos']], 'required': True},
                {'key': 'Fecha Desde', 'label': 'Desde (YYYY-MM-DD)', 'type': 'date', 'required': True},
                {'key': 'Fecha Hasta', 'label': 'Hasta (YYYY-MM-DD)', 'type': 'date', 'required': True},
                {'key': 'Seguro', 'label': 'Con Seguro', 'type': 'checkbox', 'default': False}
            ],
            on_submit=_on_guardar_reserva
        )

    register_view("reservas", _TAG)
    if _contrato_controller: _refresh_table()
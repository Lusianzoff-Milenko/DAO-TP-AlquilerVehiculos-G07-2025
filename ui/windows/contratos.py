import dearpygui.dearpygui as dpg
from ui.components.form_dialog import FormDialog
from functools import partial

_TAG = "view_contratos"
_TABLE_TAG = "contratos_table"

_contrato_controller = None

_form_dialog = None
_form_options = None
_estado_filtro = "EnCurso"  # Por defecto mostramos los alquileres activos
_estados_combo = ["EnCurso", "EnReservado", "Cancelado", "YaEntregado", "Todos"]


def _show_notification(message: str, error: bool = False):
    color = (255, 100, 100) if error else (100, 255, 100)
    tag_notif = "contrato_notification"

    if dpg.does_item_exist(tag_notif):
        dpg.set_value(tag_notif, message)
        dpg.configure_item(tag_notif, color=color)
    else:
        dpg.add_text(message, tag=tag_notif, color=color, parent=_TAG, before=_TABLE_TAG)

    import threading
    import time
    def hide_notification():
        time.sleep(3)
        if dpg.does_item_exist(tag_notif):
            dpg.delete_item(tag_notif)

    threading.Thread(target=hide_notification, daemon=True).start()


def _confirmar_finalizacion(contrato_data):
    """Muestra un modal para confirmar la devolución del vehículo."""
    modal_tag = "modal_fin_contrato"

    if dpg.does_item_exist(modal_tag):
        dpg.delete_item(modal_tag)

    def _on_yes(sender, app_data, user_data):
        c_id = user_data["ID"]
        # Llamamos al controlador para finalizar
        if _contrato_controller.finalizar_alquiler(c_id):
            _show_notification(f"Vehículo devuelto. Contrato #{c_id} finalizado.")
            dpg.delete_item(modal_tag)
            _refresh_table()
        else:
            _show_notification("Error al finalizar el contrato.", error=True)

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    w, h = 320, 150

    with dpg.window(label="Finalizar Alquiler", tag=modal_tag, modal=True, width=w, height=h, no_resize=True,
                    pos=[(viewport_width - w) // 2, (viewport_height - h) // 2]):
        dpg.add_text(f"¿Confirmar devolución del vehículo\ndel contrato #{contrato_data.get('ID')}?")
        dpg.add_spacer(height=15)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_button(label="Sí, Finalizar", callback=_on_yes, user_data=contrato_data, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item(modal_tag), width=100)


def _refresh_table():
    if not _contrato_controller:
        return

    global _estado_filtro

    # Obtenemos todos los contratos del controlador
    todos_contratos = _contrato_controller.get_all_contratos()

    # Filtramos según el combo seleccionado
    if _estado_filtro == "Todos":
        contratos = todos_contratos
    else:
        contratos = [c for c in todos_contratos if c.get("Estado", "") == _estado_filtro]

    # Limpiamos la tabla
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    # Rellenamos la tabla
    for contrato in contratos:
        nro = contrato.get("ID", "")
        cliente = contrato.get("Cliente", "")
        fecha_desde = contrato.get("Desde", "")  # Clave actualizada según tu controller
        fecha_hasta = contrato.get("Hasta", "")
        estado = contrato.get("Estado", "")
        vehiculo = contrato.get("Vehículo", "")
        total = contrato.get("Total", "")

        # Copia para callbacks
        contrato_copia = dict(contrato)

        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(nro))
            dpg.add_text(cliente)
            dpg.add_text(fecha_desde)
            dpg.add_text(fecha_hasta)
            dpg.add_text(estado)
            dpg.add_text(vehiculo)
            dpg.add_text(str(total))

            # Columna de Acciones
            with dpg.group(horizontal=True):
                if estado == "EnCurso":
                    dpg.add_button(
                        label="Finalizar",
                        callback=lambda s, a, u=contrato_copia: _confirmar_finalizacion(u),
                        width=70
                    )
                elif estado == "EnReservado":
                    dpg.add_text("(Ver Reservas)", color=(150, 150, 150))
                elif estado == "YaEntregado":
                    dpg.add_text("Cerrado", color=(100, 255, 100))


def _on_estado_filtro(sender, app_data):
    global _estado_filtro
    _estado_filtro = app_data
    _refresh_table()


def _on_nuevo_contrato():
    global _form_dialog
    if _form_dialog:
        _form_dialog.show()
    else:
        _show_notification("Error cargando formulario", error=True)


def _on_guardar_contrato(data: dict):
    global _contrato_controller, _form_options
    try:
        # Mapear etiquetas a IDs (igual que en reservas.py)
        cliente_label = data.get('id_cliente', '')
        cliente_opts = [opt['label'] for opt in _form_options['clientes']]
        if cliente_label in cliente_opts:
            idx = cliente_opts.index(cliente_label)
            data['id_cliente'] = _form_options['clientes'][idx]['value']
        else:
            data['id_cliente'] = _form_options['clientes'][0]['value'] if _form_options['clientes'] else 1

        vehiculo_label = data.get('id_vehiculo', '')
        vehiculo_opts = [opt['label'] for opt in _form_options['vehiculos']]
        if vehiculo_label in vehiculo_opts:
            idx = vehiculo_opts.index(vehiculo_label)
            data['id_vehiculo'] = _form_options['vehiculos'][idx]['value']
        else:
            data['id_vehiculo'] = _form_options['vehiculos'][0]['value'] if _form_options['vehiculos'] else 1

        pago_label = data.get('id_metodo_pago', '')
        pago_opts = [opt['label'] for opt in _form_options['pagos']]
        if pago_label in pago_opts:
            idx = pago_opts.index(pago_label)
            data['id_metodo_pago'] = _form_options['pagos'][idx]['value']
        else:
            data['id_metodo_pago'] = _form_options['pagos'][0]['value'] if _form_options['pagos'] else 1

        data['Seguro'] = bool(data.get('Seguro', False))

        # Validar fechas (simple)
        from datetime import datetime
        try:
            f_desde = datetime.strptime(data['Fecha Desde'], "%Y-%m-%d")
            f_hasta = datetime.strptime(data['Fecha Hasta'], "%Y-%m-%d")
            if f_hasta < f_desde:
                _show_notification("La fecha hasta debe ser posterior a la fecha desde.", error=True)
                return
        except:
            _show_notification("Formato de fecha inválido. Use YYYY-MM-DD.", error=True)
            return

        exito = _contrato_controller.crear_reserva(data)
        if exito:
            _show_notification("Contrato/Reserva creado correctamente.")
            _refresh_table()
        else:
            _show_notification("No se pudo crear. Verifique disponibilidad.", error=True)

    except Exception as e:
        _show_notification(f"Error: {str(e)}", error=True)


def register(contrato_controller):
    from ui.navigation import register_view
    global _contrato_controller, _form_dialog, _form_options
    _contrato_controller = contrato_controller

    # Cargar opciones para el formulario de creación
    _form_options = _contrato_controller.get_form_options() if _contrato_controller else {"clientes": [],
                                                                                          "vehiculos": [], "pagos": []}

    cliente_labels = [opt['label'] for opt in _form_options['clientes']]
    vehiculo_labels = [opt['label'] for opt in _form_options['vehiculos']]
    pago_labels = [opt['label'] for opt in _form_options['pagos']]

    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Gestión de Alquileres", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)

        # Botones de acción y filtro
        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Nuevo Contrato", width=150, callback=_on_nuevo_contrato)
            dpg.add_spacer(width=12)
            dpg.add_combo(
                items=_estados_combo,
                default_value=_estado_filtro,
                width=200,
                callback=_on_estado_filtro,
                tag="contrato_estado_combo"
            )
            dpg.add_spacer(width=12)
            dpg.add_button(label="Refrescar", callback=_refresh_table)

        dpg.add_spacer(height=10)
        dpg.add_text("", tag="contrato_notification")
        dpg.add_spacer(height=5)

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
            dpg.add_table_column(label="Cliente", init_width_or_weight=2.0)
            dpg.add_table_column(label="Desde", init_width_or_weight=1.2)
            dpg.add_table_column(label="Hasta", init_width_or_weight=1.2)
            dpg.add_table_column(label="Estado", init_width_or_weight=1.2)
            dpg.add_table_column(label="Vehículo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Total", init_width_or_weight=1.2)
            dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=90)

        # Formulario (reutilizado)
        _form_dialog = FormDialog(
            tag="contrato_form",
            title="Nuevo Contrato",
            fields=[
                {'key': 'id_cliente', 'label': 'Cliente', 'type': 'combo', 'default': '', 'required': True,
                 'options': cliente_labels},
                {'key': 'id_vehiculo', 'label': 'Vehículo', 'type': 'combo', 'default': '', 'required': True,
                 'options': vehiculo_labels},
                {'key': 'id_metodo_pago', 'label': 'Método de Pago', 'type': 'combo', 'default': '', 'required': True,
                 'options': pago_labels},
                {'key': 'Fecha Desde', 'label': 'Fecha Desde', 'type': 'date', 'default': '', 'required': True},
                {'key': 'Fecha Hasta', 'label': 'Fecha Hasta', 'type': 'date', 'default': '', 'required': True},
                {'key': 'Seguro', 'label': 'Seguro', 'type': 'checkbox', 'default': False, 'required': False},
            ],
            on_submit=_on_guardar_contrato,
            width=600,
            height=450
        )

    register_view("alquileres", _TAG)
    if _contrato_controller:
        _refresh_table()
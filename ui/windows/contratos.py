
import dearpygui.dearpygui as dpg
from ui.components.form_dialog import FormDialog
from functools import partial

_TAG = "view_contratos"
_TABLE_TAG = "contratos_table"

_contrato_controller = None

_form_dialog = None
_form_options = None
_estado_filtro = "EnCurso"
_estados_combo = ["EnCurso", "EnReservado", "Cancelado", "YaEntregado", "Todos"]

def _show_notification(message: str, error: bool = False):
    color = (255, 100, 100) if error else (100, 255, 100)
    if dpg.does_item_exist("contrato_notification"):
        dpg.set_value("contrato_notification", message)
        dpg.configure_item("contrato_notification", color=color)
    else:
        dpg.add_text(message, tag="contrato_notification", color=color, parent=_TAG, before=_TABLE_TAG)
    import threading
    def hide_notification():
        import time
        time.sleep(3)
        if dpg.does_item_exist("contrato_notification"):
            dpg.delete_item("contrato_notification")
    threading.Thread(target=hide_notification, daemon=True).start()

def _show_contrato_detalle(contrato):
    # Chequeo defensivo
    if not contrato or not isinstance(contrato, dict):
        return
    popup_tag = f"popup_contrato_{contrato.get('ID', '0')}"
    if dpg.does_item_exist(popup_tag):
        dpg.delete_item(popup_tag)
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    win_width = min(520, int(viewport_width * 0.9))
    win_height = min(420, int(viewport_height * 0.9))
    with dpg.window(label=f"Detalle Contrato #{contrato.get('ID', '')}", modal=True, tag=popup_tag, width=win_width, height=win_height, no_resize=True, no_move=False, on_close=lambda: dpg.delete_item(popup_tag)):
        dpg.set_item_pos(popup_tag, [max(0, (viewport_width - win_width)//2), max(0, (viewport_height - win_height)//2)])
        dpg.add_spacer(height=8)
        for k, v in contrato.items():
            dpg.add_text(f"{k}: {v}")
        dpg.add_spacer(height=10)
        dpg.add_button(label="Cerrar", width=100, callback=lambda: dpg.delete_item(popup_tag))

def _refresh_table():
    if not _contrato_controller:
        return
    global _estado_filtro
    if _estado_filtro == "EnCurso":
        contratos = [c for c in _contrato_controller.get_all_contratos() if c.get("Estado", "") == "EnCurso"]
    elif _estado_filtro == "Todos":
        contratos = _contrato_controller.get_all_contratos()
    else:
        contratos = [c for c in _contrato_controller.get_all_contratos() if c.get("Estado", "") == _estado_filtro]
    if dpg.does_item_exist(_TABLE_TAG):
        children = dpg.get_item_children(_TABLE_TAG, slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)
    for contrato in contratos:
        nro = contrato.get("ID", "")
        cliente = contrato.get("Cliente", "")
        fecha_desde = contrato.get("FechaDesde", contrato.get("Desde", ""))
        fecha_hasta = contrato.get("FechaHasta", contrato.get("Hasta", ""))
        estado = contrato.get("Estado", "")
        vehiculo = contrato.get("Vehiculo", contrato.get("Vehículo", ""))
        precio_diario = contrato.get("PrecioDiario", contrato.get("Total", ""))
        if contrato is not None:
            contrato_copia = dict(contrato)
        else:
            contrato_copia = {}
        with dpg.table_row(parent=_TABLE_TAG):
            dpg.add_text(str(nro))
            dpg.add_text(cliente)
            dpg.add_text(fecha_desde)
            dpg.add_text(fecha_hasta)
            dpg.add_text(estado)
            dpg.add_text(vehiculo)
            dpg.add_text(str(precio_diario))

def _on_estado_filtro(sender, app_data):
    global _estado_filtro
    _estado_filtro = app_data
    _refresh_table()

def _on_toggle_filtro():
    global _mostrar_todos
    _mostrar_todos = not _mostrar_todos
    if dpg.does_item_exist("contrato_filtro_btn"):
        dpg.set_value("contrato_filtro_btn", "Ver solo en curso" if _mostrar_todos else "Ver todos los contratos")
    _refresh_table()

def _on_nuevo_contrato():
    global _form_dialog, _form_options
    if not _form_dialog or not _form_options:
        _show_notification("No se pudo cargar el formulario. Intente recargar la vista.", error=True)
        return
    _form_dialog.show()

def _on_guardar_contrato(data: dict):
    global _contrato_controller, _form_options
    try:
        # Mapear los valores del combo al ID real
        # Cliente
        cliente_label = data.get('id_cliente', '')
        cliente_opts = [opt['label'] for opt in _form_options['clientes']]
        if cliente_label in cliente_opts:
            idx = cliente_opts.index(cliente_label)
            data['id_cliente'] = _form_options['clientes'][idx]['value']
        else:
            data['id_cliente'] = _form_options['clientes'][0]['value'] if _form_options['clientes'] else 1
        # Vehículo
        vehiculo_label = data.get('id_vehiculo', '')
        vehiculo_opts = [opt['label'] for opt in _form_options['vehiculos']]
        if vehiculo_label in vehiculo_opts:
            idx = vehiculo_opts.index(vehiculo_label)
            data['id_vehiculo'] = _form_options['vehiculos'][idx]['value']
        else:
            data['id_vehiculo'] = _form_options['vehiculos'][0]['value'] if _form_options['vehiculos'] else 1
        # Método de pago
        pago_label = data.get('id_metodo_pago', '')
        pago_opts = [opt['label'] for opt in _form_options['pagos']]
        if pago_label in pago_opts:
            idx = pago_opts.index(pago_label)
            data['id_metodo_pago'] = _form_options['pagos'][idx]['value']
        else:
            data['id_metodo_pago'] = _form_options['pagos'][0]['value'] if _form_options['pagos'] else 1

        data['Seguro'] = bool(data.get('Seguro', False))

        # Validar fechas
        from datetime import datetime
        try:
            f_desde = datetime.strptime(data['Fecha Desde'], "%Y-%m-%d")
            f_hasta = datetime.strptime(data['Fecha Hasta'], "%Y-%m-%d")
            if f_hasta < f_desde:
                _show_notification("La fecha hasta debe ser posterior a la fecha desde.", error=True)
                return
        except Exception:
            _show_notification("Formato de fecha inválido. Use YYYY-MM-DD.", error=True)
            return

        exito = _contrato_controller.crear_reserva(data)
        if exito:
            _show_notification("Contrato creado correctamente.")
            _refresh_table()
        else:
            _show_notification("No se pudo crear el contrato. Verifique los datos o disponibilidad.", error=True)
    except Exception as e:
        _show_notification(f"Error: {str(e)}", error=True)

def register(contrato_controller):
    from ui.navigation import register_view
    global _contrato_controller, _form_dialog, _form_options
    _contrato_controller = contrato_controller
    _form_options = _contrato_controller.get_form_options() if _contrato_controller else None

    # Opciones para combos
    cliente_labels = [opt['label'] for opt in _form_options['clientes']] if _form_options else []
    vehiculo_labels = [opt['label'] for opt in _form_options['vehiculos']] if _form_options else []
    pago_labels = [opt['label'] for opt in _form_options['pagos']] if _form_options else []

    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=16)
        dpg.add_text("Contratos", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)

        # Botones de acción y filtro
        with dpg.group(horizontal=True):
            dpg.add_button(label="+ Nuevo Contrato", width=180, callback=_on_nuevo_contrato)
            dpg.add_spacer(width=12)
            dpg.add_combo(
                items=_estados_combo,
                default_value=_estado_filtro,
                width=220,
                callback=_on_estado_filtro,
                tag="contrato_estado_combo"
            )
            dpg.add_spacer(width=12)
            dpg.add_text("", tag="contrato_notification")

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
            dpg.add_table_column(label="Número", init_width_or_weight=0.8)
            dpg.add_table_column(label="Cliente", init_width_or_weight=2.0)
            dpg.add_table_column(label="Fecha Desde", init_width_or_weight=1.2)
            dpg.add_table_column(label="Fecha Hasta", init_width_or_weight=1.2)
            dpg.add_table_column(label="Estado", init_width_or_weight=1.2)
            dpg.add_table_column(label="Vehículo", init_width_or_weight=2.0)
            dpg.add_table_column(label="Precio Diario", init_width_or_weight=1.2)

        # Formulario de contrato
        _form_dialog = FormDialog(
            tag="contrato_form",
            title="Nuevo Contrato",
            fields=[
                {'key': 'id_cliente', 'label': 'Cliente', 'type': 'combo', 'default': cliente_labels[0] if cliente_labels else '', 'required': True, 'options': cliente_labels},
                {'key': 'id_vehiculo', 'label': 'Vehículo', 'type': 'combo', 'default': vehiculo_labels[0] if vehiculo_labels else '', 'required': True, 'options': vehiculo_labels},
                {'key': 'id_metodo_pago', 'label': 'Método de Pago', 'type': 'combo', 'default': pago_labels[0] if pago_labels else '', 'required': True, 'options': pago_labels},
                {'key': 'Fecha Desde', 'label': 'Fecha Desde', 'type': 'date', 'default': '', 'required': True},
                {'key': 'Fecha Hasta', 'label': 'Fecha Hasta', 'type': 'date', 'default': '', 'required': True},
                {'key': 'Seguro', 'label': 'Seguro', 'type': 'checkbox', 'default': False, 'required': False},
            ],
            on_submit=_on_guardar_contrato,
            width=600,
            height=420
        )

    register_view("alquileres", _TAG)
    _refresh_table()

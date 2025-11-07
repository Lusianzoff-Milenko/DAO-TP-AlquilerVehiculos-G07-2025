import dearpygui.dearpygui as dpg
from ui.navigation import register_view, go_to
from ui.services.workers import run_async
from ui.state.store import STATE

_TAG = "view_login"

def _api_login(usuario: str, password: str) -> dict:
    import time; time.sleep(0.6)
    if usuario == "admin" and password == "1234":
        return {"nombre": "Administrador", "rol": "admin", "token": "fake"}
    raise Exception("Credenciales inválidas")

def _set_loading(is_loading: bool):
    dpg.configure_item("btn_login", enabled=not is_loading)
    dpg.configure_item("login_spinner", show=is_loading)
    dpg.configure_item("login_status", default_value="Iniciando sesión…" if is_loading else "")

def _on_success(data: dict):
    STATE.user = data.get("nombre", "Usuario")
    STATE.role = data.get("rol", "user")
    dpg.configure_item("login_status", default_value="Inicio de sesión exitoso")
    _set_loading(False)
    dpg.split_frame()
    go_to("home")

def _on_error(err: Exception):
    _set_loading(False)
    dpg.configure_item("login_status", default_value=f"{err}")

def _do_login():
    usuario  = dpg.get_value("input_user")
    password = dpg.get_value("input_pass")
    if not usuario or not password:
        dpg.configure_item("login_status", default_value="Ingresá usuario y contraseña")
        return
    _set_loading(True)
    run_async(lambda: _api_login(usuario, password), on_success=_on_success, on_error=_on_error)

def _toggle_password():
    # invierte el modo oculto
    current = dpg.get_item_configuration("input_pass").get("password", True)
    dpg.configure_item("input_pass", password=not current)

def _on_enter(sender, app_data):
    if app_data == "\r" or app_data == "\n":
        _do_login()

def register():
    # contenedor a pantalla completa dentro de root
    with dpg.child_window(tag=_TAG, parent="root", show=True, width=-1, height=-1):
        dpg.add_spacer(height=12)
        # panel centrado
        with dpg.group(horizontal=False):
            dpg.add_text("Inicio de sesión", bullet=True)
            dpg.add_spacer(height=6)

            # layout en dos columnas: labels a la izquierda, inputs a la derecha
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp, borders_innerV=True):
                dpg.add_table_column(init_width_or_weight=0.3)
                dpg.add_table_column(init_width_or_weight=0.7)

                with dpg.table_row():
                    dpg.add_text("Nombre de usuario")
                    dpg.add_input_text(tag="input_user", hint="usuario", on_enter=True, callback=_on_enter)

                with dpg.table_row():
                    dpg.add_text("Contraseña")
                    dpg.add_input_text(tag="input_pass", password=True, hint="••••••", on_enter=True, callback=_on_enter)

            dpg.add_spacer(height=6)

            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="Recordar sesión", tag="chk_remember")
                dpg.add_button(label="Mostrar contraseña", callback=_toggle_password)
                dpg.add_loading_indicator(tag="login_spinner", style=1, radius=6.0, thickness=3.0, show=False)

            dpg.add_spacer(height=6)
            dpg.add_button(label="Ingresar", tag="btn_login", width=120, callback=_do_login)

            dpg.add_spacer(height=4)
            dpg.add_text("", tag="login_status")

    register_view("login", _TAG)

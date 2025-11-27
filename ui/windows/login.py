import dearpygui.dearpygui as dpg
from ui.navigation import register_view, go_to
from ui.services.workers import run_async
from ui.state.store import STATE

_TAG = "view_login"
_CARD_WIDTH = 400
_CARD_HEIGHT = 460  # Aumentado para que quepa todo sin scroll


def _api_login(usuario: str, password: str) -> dict:
    # Simulación de API
    import time;
    time.sleep(0.8)
    if usuario == "admin" and password == "1234":
        return {"nombre": "Administrador", "rol": "admin", "token": "fake"}
    raise Exception("Credenciales inválidas")


def _set_loading(is_loading: bool):
    if dpg.does_item_exist("btn_login"):
        dpg.configure_item("btn_login", label="Cargando..." if is_loading else "Ingresar", enabled=not is_loading)
    if dpg.does_item_exist("login_spinner"):
        dpg.configure_item("login_spinner", show=is_loading)
    if dpg.does_item_exist("login_status"):
        if is_loading:
            dpg.set_value("login_status", "")


def _on_success(data: dict):
    STATE.user = data.get("nombre", "Usuario")
    STATE.role = data.get("rol", "user")
    _set_loading(False)
    go_to("home")


def _on_error(err: Exception):
    _set_loading(False)
    dpg.set_value("login_status", f"⚠ {err}")
    dpg.configure_item("login_status", color=(255, 100, 100))


def _do_login():
    usuario = dpg.get_value("input_user")
    password = dpg.get_value("input_pass")

    if not usuario or not password:
        dpg.set_value("login_status", "⚠ Ingresa usuario y contraseña")
        dpg.configure_item("login_status", color=(255, 200, 100))
        return

    _set_loading(True)
    run_async(lambda: _api_login(usuario, password), on_success=_on_success, on_error=_on_error)


def _on_enter(sender, app_data):
    _do_login()


def _center_card(sender=None, app_data=None):
    if not dpg.does_item_exist("login_card"):
        return

    # Solo centramos si la vista de login está activa
    if not dpg.get_item_configuration(_TAG)["show"]:
        return

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    pos_x = (viewport_width - _CARD_WIDTH) // 2
    pos_y = (viewport_height - _CARD_HEIGHT) // 2

    dpg.set_item_pos("login_card", [max(0, pos_x), max(0, pos_y)])


def register():
    if dpg.does_item_exist(_TAG):
        dpg.delete_item(_TAG)

    with dpg.group(tag=_TAG, parent="content_area", show=True):

        # --- TARJETA DE LOGIN ---
        # Mantenemos bloqueado el scroll, pero aseguramos que el tamaño sea suficiente
        with dpg.child_window(tag="login_card", width=_CARD_WIDTH, height=_CARD_HEIGHT,
                              border=False, no_scrollbar=True, no_scroll_with_mouse=True):
            # Espacio superior (reducido para ganar espacio)
            dpg.add_spacer(height=25)

            # 2. TÍTULO (INICIAR SESIÓN)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=(_CARD_WIDTH - 140) // 2)
                dpg.add_text("INICIAR SESIÓN", color=(200, 200, 200))

            dpg.add_spacer(height=25)  # Reducido de 35 a 25

            # 3. FORMULARIO
            margin_x = 50
            field_width = _CARD_WIDTH - (margin_x * 2)

            with dpg.group(indent=margin_x):
                # Usuario
                dpg.add_text("Usuario / Email", color=(120, 120, 120))
                dpg.add_input_text(tag="input_user", width=field_width, hint="admin", on_enter=True, callback=_on_enter)
                dpg.add_spacer(height=12)  # Reducido de 15 a 12

                # Password
                with dpg.group(horizontal=True):
                    dpg.add_text("Contraseña", color=(120, 120, 120))
                    spacer_gap = field_width - 160
                    if spacer_gap > 0:
                        dpg.add_spacer(width=spacer_gap)

                dpg.add_input_text(tag="input_pass", width=field_width, password=True, hint="****", on_enter=True,
                                   callback=_on_enter)

                dpg.add_spacer(height=12)  # Reducido de 15 a 12

                # Checkbox
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(tag="chk_remember", default_value=True)
                    dpg.add_text("Recordar sesión", color=(150, 150, 150))

                dpg.add_spacer(height=25)  # Reducido de 30 a 25

                # Botón
                with dpg.theme(tag="login_btn_theme"):
                    with dpg.theme_component(dpg.mvButton):
                        dpg.add_theme_color(dpg.mvThemeCol_Button, (56, 117, 215, 255))
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 130, 230, 255))
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (40, 90, 180, 255))
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 8)

                btn = dpg.add_button(label="Ingresar", tag="btn_login", width=field_width, callback=_do_login)
                dpg.bind_item_theme(btn, "login_btn_theme")

                dpg.add_spacer(height=15)

                # Spinner centrado
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=(field_width - 25) // 2)
                    dpg.add_loading_indicator(tag="login_spinner", style=1, radius=2.5, thickness=2.0, show=False,
                                              color=(56, 117, 215))

                dpg.add_text("", tag="login_status", wrap=field_width, color=(255, 100, 100))

    register_view("login", _TAG)

    # Callbacks de centrado
    dpg.set_viewport_resize_callback(_center_card)
    dpg.set_frame_callback(1, _center_card)
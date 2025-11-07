import dearpygui.dearpygui as dpg
from ui.theme import install_theme
from ui.navigation import go_to

from ui.windows.home import register as register_home
from ui.windows.login import register as register_login

def _build_menu_bar():
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Inicio"):
            dpg.add_menu_item(label="Dashboard", callback=lambda: go_to("home"))

def _build_root():
    # ventana principal “root” SIN docking
    with dpg.window(tag="root", label="Alquiler de Vehículos", width=1280, height=800):
        dpg.add_text("Inicializando UI…")  # texto de prueba
    dpg.set_primary_window("root", True)

def run_app():
    dpg.create_context()
    dpg.create_viewport(title="DAO - Alquiler de Vehículos", width=1280, height=800)
    install_theme()
    _build_root()
    _build_menu_bar()

    # registrar vistas (login primero)
    register_login()
    register_home()

    go_to("login")  # debe mostrar el login
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

# ui/app.py
import dearpygui.dearpygui as dpg
from ui.theme import install_theme
from ui.navigation import go_to

from ui.windows.home import register as register_home
from ui.windows.login import register as register_login
from ui.windows.clientes import register as register_clientes
from ui.windows.vehiculos import register as register_vehiculos

SIDEBAR_WIDTH = 220


def _build_layout():
    with dpg.window(tag="root", label="Drive&Go Fleet Manager"):
        # HEADER (Barra superior)
        with dpg.group(horizontal=True):
            with dpg.group(width=SIDEBAR_WIDTH):
                dpg.add_spacer(height=5)
                # Texto grande y centrado simulado con padding
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=15)
                    dpg.add_text("DRIVE & GO", color=(56, 140, 255, 255))

            # Línea vertical separadora
            dpg.add_spacer(width=10)
            dpg.add_text("|", color=(80, 80, 80))
            dpg.add_spacer(width=10)
            dpg.add_text("Panel de Administración", color=(150, 150, 150))

        dpg.add_separator()

        # CUERPO PRINCIPAL (Sidebar + Contenido)
        with dpg.group(tag="main_layout", horizontal=True):
            # 1. Sidebar (Menú)
            with dpg.child_window(tag="sidebar", width=SIDEBAR_WIDTH, height=-1, border=False):
                dpg.add_spacer(height=15)

                # Sección PRINCIPAL
                dpg.add_text("   NAVEGACION", color=(100, 100, 100))
                dpg.add_spacer(height=5)
                _add_menu_btn("Dashboard", "home")
                _add_menu_btn("Clientes", "clientes")
                _add_menu_btn("Vehiculos", "vehiculos")
                _add_menu_btn("Empleados", "empleados")

                dpg.add_spacer(height=20)

                # Sección OPERATIVA
                dpg.add_text("   OPERACIONES", color=(100, 100, 100))
                dpg.add_spacer(height=5)
                _add_menu_btn("Alquileres", "alquileres")
                _add_menu_btn("Reservas", "reservas")
                _add_menu_btn("Mantenimiento", "mantenimiento")

                dpg.add_spacer(height=40)
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Botón Salir
                _add_menu_btn("Cerrar Sesion", "login", is_logout=True)

            # 2. Separador Vertical Fino
            with dpg.theme() as theme_border:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (60, 65, 75, 255))

            # 3. Area de Contenido
            with dpg.group(width=-1, height=-1):
                # Pequeño margen a la izquierda del contenido
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=10)
                    # El child_window que contendrá las vistas
                    with dpg.child_window(tag="content_area", width=-1, height=-1, border=False):
                        pass

    dpg.set_primary_window("root", True)


def _add_menu_btn(label, view_name, is_logout=False):
    """Crea botones de menú limpios y anchos."""

    def _cb(s, a):
        go_to(view_name)

    # Tema especial para el botón de salir
    btn_theme = None
    if is_logout:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 40, 40, 255))
        btn_theme = theme

    # Usamos un grupo horizontal para dar un pequeño margen izquierdo al botón
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=10)  # Margen izquierdo
        btn = dpg.add_button(label=label, width=-15, height=32, callback=_cb)

        if btn_theme:
            dpg.bind_item_theme(btn, btn_theme)

    dpg.add_spacer(height=3)


def run_app():
    dpg.create_context()
    # Tamaño HD estándar
    dpg.create_viewport(title="Drive&Go System", width=1280, height=768)

    install_theme()  # Cargará la fuente del sistema
    _build_layout()

    register_login()
    register_home()
    register_clientes()
    register_vehiculos()

    dpg.configure_item("sidebar", show=False)
    go_to("login")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
import dearpygui.dearpygui as dpg
from ui.theme import install_theme
from ui.navigation import go_to
from ui.icons import *  # Importar iconos
from services.containers.container import Container

# Importamos las vistas
from ui.windows.home import register as register_home
from ui.windows.login import register as register_login

from ui.windows.clientes import register as register_clientes
from ui.windows.vehiculos import register as register_vehiculos
from ui.windows.reportes import register as register_reportes
from ui.windows.empleados import register as register_empleados

SIDEBAR_WIDTH = 250


def _build_layout():
    with dpg.window(tag="root", label="Drive&Go System"):
        # HEADER
        with dpg.group(horizontal=True):
            with dpg.group(width=SIDEBAR_WIDTH):
                dpg.add_spacer(height=5)
                # Logo con icono de auto
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=10)
                    dpg.add_text(f"{ICON_CAR}  DRIVE & GO", color=(56, 170, 255, 255))

            dpg.add_spacer(width=10)
            dpg.add_text("|")
            dpg.add_spacer(width=10)
            dpg.add_text(f"Panel de Control", color=(150, 150, 150))

        dpg.add_separator()

        # MAIN LAYOUT
        with dpg.group(tag="main_layout", horizontal=True):
            # --- SIDEBAR ---
            with dpg.child_window(tag="sidebar", width=SIDEBAR_WIDTH, height=-1, border=False):
                dpg.add_spacer(height=8)

                # Grupo de Navegación
                dpg.add_text("   PRINCIPAL", color=(100, 100, 100))
                dpg.add_spacer(height=3)

                _add_menu_btn(f"{ICON_DASHBOARD}  Dashboard", "home")
                _add_menu_btn(f"{ICON_USERS}  Clientes", "clientes")
                _add_menu_btn(f"{ICON_CAR}  Vehículos", "vehiculos")
                _add_menu_btn(f"{ICON_USER}  Empleados", "empleados")
                _add_menu_btn(f"{ICON_CHART}  Reportes", "reportes")

                dpg.add_spacer(height=10)
                dpg.add_text("   GESTIÓN", color=(100, 100, 100))
                dpg.add_spacer(height=3)

                _add_menu_btn(f"{ICON_LIST}  Alquileres", "alquileres")
                _add_menu_btn(f"{ICON_CALENDAR}  Reservas", "reservas")
                _add_menu_btn(f"{ICON_WRENCH}  Mantenimiento", "mantenimiento")

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_spacer(height=8)

                _add_menu_btn(f"{ICON_LOGOUT}  Salir", "login", is_logout=True)

            # --- CONTENT AREA ---
            # width=-1 hace que ocupe TODO el espacio restante automáticamente
            with dpg.group(width=-1, height=-1):
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=5)
                    with dpg.child_window(tag="content_area", width=-1, height=-1, border=False):
                        pass

    dpg.set_primary_window("root", True)


def _add_menu_btn(label, view_name, is_logout=False):
    """Crea un botón de menú que se auto-ajusta al ancho."""

    def _cb(s, a):
        go_to(view_name)

    btn_theme = None
    if is_logout:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (130, 40, 40, 255))
        btn_theme = theme

    # width=-1 hace que el botón se estire horizontalmente
    # alignment=0.0 alinea el texto a la izquierda (típico de menús)
    btn = dpg.add_button(label=f"  {label}", width=-1, height=32, callback=_cb)

    # Ajustar alineación del texto a la izquierda (hack de tema)
    with dpg.theme() as align_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)  # X=0 (Izquierda), Y=0.5 (Centro)
            if is_logout:  # Reaplicar colores si es logout
                dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (130, 40, 40, 255))

    dpg.bind_item_theme(btn, align_theme)
    dpg.add_spacer(height=1)


def run_app():
    dpg.create_context()
    dpg.create_viewport(title="Drive&Go System", width=1280, height=800)

    # Instalar tema (esto descargará la fuente automáticamente)
    install_theme()

    _build_layout()

    # Crear container e inyectar dependencias

    container = Container()
    cliente_controller = container.cliente_controller()
    vehiculo_controller = container.vehiculo_controller()
    empleado_controller = container.empleado_controller()


    from ui.windows.contratos import register as register_contratos

    contrato_controller = container.contrato_controller()

    register_login()
    register_home()
    register_clientes(cliente_controller)
    register_vehiculos(vehiculo_controller)
    register_empleados(empleado_controller)
    register_reportes()
    register_contratos(contrato_controller)

    dpg.configure_item("sidebar", show=False)
    go_to("login")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
import dearpygui.dearpygui as dpg
from ui.theme import install_theme
from ui.navigation import go_to
from ui.icons import *
from services.containers.container import Container

# vistas
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
            # SIDEBAR
            with dpg.child_window(tag="sidebar", width=SIDEBAR_WIDTH, height=-1, border=False):
                dpg.add_spacer(height=8)
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

            # CONTENT AREA
            with dpg.group(width=-1, height=-1):
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=5)
                    with dpg.child_window(tag="content_area", width=-1, height=-1, border=False):
                        pass

    dpg.set_primary_window("root", True)


def _add_menu_btn(label, view_name, is_logout=False):
    def _cb(s, a):
        go_to(view_name)

    btn = dpg.add_button(label=f"  {label}", width=-1, height=32, callback=_cb)

    with dpg.theme() as align_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
            if is_logout:
                dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (130, 40, 40, 255))

    dpg.bind_item_theme(btn, align_theme)
    dpg.add_spacer(height=1)


def run_app():
    dpg.create_context()
    dpg.create_viewport(title="Drive&Go System", width=1280, height=800)

    install_theme()
    _build_layout()

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

    dpg.maximize_viewport()

    dpg.start_dearpygui()
    dpg.destroy_context()
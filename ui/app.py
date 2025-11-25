import dearpygui.dearpygui as dpg
from ui.theme import install_theme
from ui.navigation import go_to

from ui.windows.home import register as register_home
from ui.windows.login import register as register_login
from ui.windows.clientes import register as register_clientes
from ui.windows.vehiculos import register as register_vehiculos

# Configuración del sidebar
SIDEBAR_WIDTH = 200
SIDEBAR_COLLAPSED_WIDTH = 50

_sidebar_collapsed = {"value": False}

def _build_sidebar():
    """Construye el sidebar lateral con navegación."""
    with dpg.child_window(
        tag="sidebar",
        parent="root",
        width=SIDEBAR_WIDTH,
        height=-1,
        border=True
    ):
        dpg.add_spacer(height=12)
        
        # Logo/Título
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=8)
            dpg.add_text("Alquileres", color=(56, 117, 215))
        
        dpg.add_separator()
        dpg.add_spacer(height=12)
        
        # Menú de navegación
        _add_nav_button("Dashboard", "home")
        _add_nav_button("Clientes", "clientes")
        _add_nav_button("Vehículos", "vehiculos")
        _add_nav_button("Empleados", "empleados")
        _add_nav_button("Alquileres", "alquileres")
        _add_nav_button("Reservas", "reservas")
        _add_nav_button("Mantenimiento", "mantenimiento")
        _add_nav_button("Reportes", "reportes")
        
        dpg.add_spacer(height=12)
        dpg.add_separator()
        dpg.add_spacer(height=8)
        
        # Botón de cerrar sesión
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="Salir",
                width=-16,
                callback=lambda: go_to("login")
            )

def _add_nav_button(label: str, view_name: str):
    """Agrega un botón de navegación al sidebar."""
    def _navigate():
        go_to(view_name)
    
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=8)
        dpg.add_button(
            label=label,
            width=-16,
            callback=_navigate
        )
    dpg.add_spacer(height=4)

def _build_content_area():
    """Construye el área de contenido principal."""
    with dpg.child_window(
        tag="content_area",
        parent="root",
        width=-1,
        height=-1,
        border=False
    ):
        dpg.add_text("Cargando contenido...")

def _build_root():
    """Ventana principal con layout sidebar + contenido."""
    with dpg.window(tag="root", label="Sistema de Alquiler de Vehículos"):
        with dpg.group(horizontal=True):
            # El sidebar y content_area se crean después
            pass
    
    dpg.set_primary_window("root", True)

def run_app():
    dpg.create_context()
    dpg.create_viewport(title="DAO - Alquiler de Vehículos", width=1280, height=800)
    install_theme()
    _build_root()
    
    # Construir sidebar y área de contenido PRIMERO
    _build_sidebar()
    _build_content_area()
    
    # LUEGO registrar vistas (ahora content_area ya existe)
    register_login()
    register_home()
    register_clientes()
    register_vehiculos()
    
    # Ocultar sidebar al inicio (solo visible después del login)
    dpg.configure_item("sidebar", show=False)

    go_to("login")  # debe mostrar el login
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

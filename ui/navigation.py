import dearpygui.dearpygui as dpg
_VIEWS = {}

def register_view(name: str, tag: str):
    _VIEWS[name] = tag

def go_to(name: str):
    """Navega a una vista. Muestra/oculta sidebar según la vista."""
    # Mostrar sidebar solo si NO es login
    show_sidebar = (name != "login")
    if dpg.does_item_exist("sidebar"):
        dpg.configure_item("sidebar", show=show_sidebar)
    
    # Cambiar vista activa
    for n, tag in _VIEWS.items():
        if dpg.does_item_exist(tag):
            dpg.configure_item(tag, show=(n == name))

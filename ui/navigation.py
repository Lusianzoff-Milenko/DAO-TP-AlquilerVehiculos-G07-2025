import dearpygui.dearpygui as dpg
_VIEWS = {}

def register_view(name: str, tag: str):
    _VIEWS[name] = tag

def go_to(name: str):
    for n, tag in _VIEWS.items():
        dpg.configure_item(tag, show=(n == name))

import dearpygui.dearpygui as dpg
from ui.navigation import register_view

_TAG = "view_home"

def register():
    with dpg.child_window(tag=_TAG, parent="root", show=False, width=-1, height=-1):
        dpg.add_text("Dashboard")
        dpg.add_text("KPIs y accesos rápidos…")
    register_view("home", _TAG)

# ui/theme.py
import os
import dearpygui.dearpygui as dpg

def _try_load_font():
    fonts_dir = os.path.join(os.path.dirname(__file__), "assets")
    font_path = os.path.join(fonts_dir, "Inter-Regular.ttf")  # cambiá si usás otra
    if os.path.exists(font_path):
        with dpg.font_registry():
            font = dpg.add_font(font_path, 16)
            dpg.bind_font(font)

def _install_base_theme():
    with dpg.theme() as base_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 10)
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 6, 4)
    dpg.bind_theme(base_theme)

def _apply_dark_palette():
    with dpg.theme() as dark_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 27, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (235, 235, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (150, 150, 150, 255))
            # Inputs / frames
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (45, 48, 52, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (65, 68, 72, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (75, 78, 82, 255))
            # Botones
            dpg.add_theme_color(dpg.mvThemeCol_Button, (56, 117, 215, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (66, 137, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (52, 105, 200, 255))
            # Tablas / headers
            dpg.add_theme_color(dpg.mvThemeCol_Header, (52, 60, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (70, 80, 92, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (80, 92, 104, 255))
            # Bordes
            dpg.add_theme_color(dpg.mvThemeCol_Border, (70, 70, 70, 255))
    dpg.bind_theme(dark_theme)

def _apply_light_palette():
    with dpg.theme() as light_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (245, 246, 248, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 27, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (120, 120, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (240, 242, 245, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (230, 232, 236, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (56, 117, 215, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (66, 137, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (52, 105, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (230, 232, 236, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (210, 214, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200, 205, 212, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (210, 210, 210, 255))
    dpg.bind_theme(light_theme)

# --- API pública ---
_current_mode = {"dark": True}

def install_theme(dark: bool = True):
    """Llamala desde app.run_app()."""
    _try_load_font()
    _install_base_theme()
    if dark:
        _apply_dark_palette()
    else:
        _apply_light_palette()
    _current_mode["dark"] = dark

def toggle_theme():
    """Podés colgar esto a un botón de menú para alternar claro/oscuro."""
    new_mode = not _current_mode["dark"]
    install_theme(dark=new_mode)

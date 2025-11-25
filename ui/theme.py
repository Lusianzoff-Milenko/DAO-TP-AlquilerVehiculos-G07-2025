import os
import dearpygui.dearpygui as dpg


def _load_fonts():
    """Carga la fuente del sistema para texto de alta calidad."""
    with dpg.font_registry():
        # Ruta a fuente de Windows (Alta Calidad)
        main_font_path = "C:/Windows/Fonts/segoeui.ttf"

        # Si no existe (ej. Linux/Mac), usamos Arial
        if not os.path.exists(main_font_path):
            main_font_path = "C:/Windows/Fonts/arial.ttf"

        try:
            # Cargamos solo la fuente principal, tamaño 20 para claridad
            with dpg.font(main_font_path, 20) as default_font:
                # Agregamos caracteres extendidos para evitar '??' en acentos
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

            dpg.bind_font(default_font)
            print(f"✅ Fuente HD cargada: {main_font_path}")

        except Exception as e:
            print(f"⚠️ No se pudo cargar fuente del sistema: {e}. Usando default.")


def _install_theme_styles():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # --- GEOMETRÍA MODERNA ---
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)  # Botones más grandes

            # --- PALETA "MIDNIGHT PRO" ---
            bg_color = (20, 22, 25, 255)  # Fondo muy oscuro
            panel_color = (32, 34, 40, 255)  # Paneles gris acero
            primary = (0, 110, 200, 255)  # Azul Corporativo
            primary_hover = (30, 130, 220, 255)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, bg_color)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, panel_color)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (50, 55, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, panel_color)

            # Botones y Headers
            dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 47, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, primary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 90, 160, 255))

            # Texto e Inputs
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (25, 27, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (225, 225, 225, 255))

            # Tablas
            dpg.add_theme_color(dpg.mvThemeCol_Header, (45, 47, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, primary_hover)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, primary)

    dpg.bind_theme(global_theme)


def install_theme():
    _load_fonts()
    _install_theme_styles()
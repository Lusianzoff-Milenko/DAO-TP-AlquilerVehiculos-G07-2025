# ui/theme.py
import dearpygui.dearpygui as dpg
import os
import platform


def _load_system_font():
    """Intenta cargar una fuente del sistema para mejor calidad."""
    # Registro de fuente
    with dpg.font_registry():
        # Intentamos buscar rutas comunes de fuentes en Windows/Linux
        possible_paths = [
            "C:/Windows/Fonts/segoeui.ttf",  # Windows moderna
            "C:/Windows/Fonts/arial.ttf",  # Windows clásica
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/System/Library/Fonts/Helvetica.ttc"  # Mac
        ]

        font_loaded = False
        for path in possible_paths:
            if os.path.exists(path):
                # Tamaño 18 para que se vea nítido y legible
                try:
                    # Agregamos soporte para caracteres latinos y símbolos básicos
                    with dpg.font(path, 20) as font_id:
                        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

                    dpg.bind_font(font_id)
                    print(f"✅ Fuente cargada: {path}")
                    font_loaded = True
                    break
                except Exception as e:
                    print(f"⚠️ No se pudo cargar la fuente {path}: {e}")

        if not font_loaded:
            print("⚠️ Usando fuente por defecto (puede verse pixelada).")


def _install_base_theme():
    with dpg.theme() as base_theme:
        with dpg.theme_component(dpg.mvAll):
            # Estilo geométrico moderno
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)

            # Colores Generales (Gris Azulado Profundo)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 33, 38, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (36, 40, 46, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 65, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (40, 45, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (56, 117, 215, 255))

            # Textos
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 235, 240, 255))

            # Botones
            dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 55, 65, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (60, 120, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (50, 100, 180, 255))

            # Headers de tablas
            dpg.add_theme_color(dpg.mvThemeCol_Header, (50, 55, 65, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (70, 75, 85, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (90, 95, 105, 255))

    dpg.bind_theme(base_theme)


def install_theme():
    _load_system_font()
    _install_base_theme()
import dearpygui.dearpygui as dpg
from datetime import datetime
from collections import defaultdict
from ui.navigation import register_view
from ui.services.workers import run_async
from services.containers.container import Container

_TAG = "view_home"

# --- TAGS ---
_TAG_KPI_DISPONIBLES = "val_kpi_disponibles"
_TAG_KPI_ACTIVOS = "val_kpi_activos"
_TAG_KPI_TALLER = "val_kpi_taller"
_TAG_KPI_FACTURACION = "val_kpi_facturacion"

_TAG_CHART_PIE_ESTADO = "chart_pie_estado"
_TAG_CHART_BAR_MONEY = "chart_bar_money"
_TAG_CHART_BAR_MODELS = "chart_bar_models"
_TAG_CHART_PIE_MANT = "chart_pie_mant"

_TAG_AXIS_X_MONEY = "axis_x_money"
_TAG_AXIS_Y_MONEY = "axis_y_money"
_TAG_AXIS_Y_MODELS = "axis_y_models"
_TAG_AXIS_X_MODELS = "axis_x_models"

# --- COLORES TEMA ---
COL_BG_CARD = (32, 32, 32, 255)
COL_BORDER = (60, 60, 60, 255)
COL_TEXT_TITLE = (180, 180, 180, 255)
COL_TEXT_VAL = (255, 255, 255, 255)

COL_ACCENT_VERDE = (100, 220, 120, 255)
COL_ACCENT_AZUL = (56, 170, 255, 255)
COL_ACCENT_ROJO = (255, 100, 100, 255)
COL_ACCENT_AMARILLO = (255, 200, 80, 255)


def _apply_card_theme(item_tag):
    with dpg.theme() as card_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COL_BG_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_Border, COL_BORDER)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 15)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
    dpg.bind_item_theme(item_tag, card_theme)


def _fetch_dashboard_data():
    """Recolección de datos para el dashboard."""
    local_container = Container()

    try:
        # 1. Obtener controladores y repositorios
        local_controller = local_container.reporte_controller()
        vehiculo_repo = local_container.vehiculo_repo()
        mant_repo = local_container.mantenimiento_repo()

        # 2. Cargar datos básicos (KPIs)
        vehiculos_all = vehiculo_repo.list_all()
        mantenimientos = mant_repo.list_all()

        # KPIs
        disponibles = [v for v in vehiculos_all if v.Estado.nombre == "Disponible"]
        kpi_disp = len(disponibles)
        kpi_rent = len([v for v in vehiculos_all if v.Estado.nombre == "Alquilado"])
        en_taller = [v for v in vehiculos_all if v.Estado.ambito == "Mantenimiento"]
        kpi_mant = len(en_taller)

        # Facturación (Manejo de error si no hay datos)
        try:
            _, total_facturado = local_controller.get_facturacion_mensual()
        except:
            total_facturado = 0.0

        # --- GRÁFICO 1: Estado Flota (Pie) ---
        estado_counts = defaultdict(int)
        for v in vehiculos_all:
            estado_counts[v.Estado.nombre] += 1
        pie_est_lbl = list(estado_counts.keys())
        pie_est_val = list(estado_counts.values())
        if not pie_est_val: pie_est_val, pie_est_lbl = [1], ["Sin Datos"]

        # --- GRÁFICO 2: Ingresos (Barras) ---
        bar_money_lbl, bar_money_val = ["-"], [0]
        try:
            fact_data, _ = local_controller.get_facturacion_mensual()
            if fact_data:
                bar_money_lbl = [str(x['Fecha Fin']) for x in fact_data[:5]]
                bar_money_val = [float(x['Facturado']) for x in fact_data[:5]]
        except:
            pass

        # ==================================================================
        # GRÁFICO 3: FLOTA POR MODELO
        # ==================================================================
        try:
            # 1. Obtenemos los datos
            flota_data = local_controller._service.get_conteo_flota_por_modelo()

            if flota_data:
                # 2. Ordenamos por cantidad (mayor a menor) y tomamos los top 5
                top_mods = sorted(flota_data, key=lambda x: x['Cantidad'], reverse=True)[:5]

                # 3. Separamos en dos listas
                bar_mod_lbl = [item['Modelo'] for item in top_mods]
                # Aseguramos que sea float para DPG
                bar_mod_val = [float(item['Cantidad']) for item in top_mods]
            else:
                bar_mod_lbl = ["Sin Vehículos"]
                bar_mod_val = [0.0]

        except Exception as e:
            print(f"[Dashboard] Error procesando G3: {e}")
            bar_mod_lbl, bar_mod_val = ["Error"], [0.0]

        # --- GRÁFICO 4: Mantenimientos (Pie) ---
        pie_mant_lbl, pie_mant_val = ["Sin Datos"], [1]
        if mantenimientos:
            mant_counts = defaultdict(int)
            for m in mantenimientos:
                # Agrupa por desc (primeros 15 chars)
                label = m.descripcion[:15] + "..." if len(m.descripcion) > 15 else m.descripcion
                mant_counts[label] += 1
            pie_mant_lbl = list(mant_counts.keys())
            pie_mant_val = list(mant_counts.values())

        # Retorno de datos
        return {
            'kpi_disp': kpi_disp,
            'kpi_rent': kpi_rent,
            'kpi_mant': kpi_mant,
            'kpi_total': total_facturado,
            'g1': (pie_est_lbl, pie_est_val),
            'g2': (bar_money_lbl, bar_money_val),
            'g3': (bar_mod_lbl, bar_mod_val),
            'g4': (pie_mant_lbl, pie_mant_val)
        }

    except Exception as e:
        print(f"[Dashboard Fatal Error]: {e}")
        return None
    finally:
        local_container.shutdown_resources()


def _update_ui(data):
    if not data: return

    # Actualizar KPIs
    dpg.set_value(_TAG_KPI_DISPONIBLES, str(data['kpi_disp']))
    dpg.set_value(_TAG_KPI_ACTIVOS, str(data['kpi_rent']))
    dpg.set_value(_TAG_KPI_TALLER, str(data['kpi_mant']))
    dpg.set_value(_TAG_KPI_FACTURACION, f"${data['kpi_total']:,.0f}")

    def update_bar_chart(tag_series, tag_axis_x, tag_axis_y, labels, values):
        if not dpg.does_item_exist(tag_series): return

        # Generar eje X numérico (0, 1, 2...)
        x = list(range(len(values)))

        # Asegurar que values sean floats (CRÍTICO PARA DPG)
        y = [float(v) for v in values]

        # Actualizar datos del gráfico [x, y]
        dpg.set_value(tag_series, [x, y])

        # Actualizar etiquetas del eje X (Tuplas de (label, posición))
        # DPG espera una lista/tupla de tuplas ((label, pos), ...)
        ticks = tuple((label, i) for i, label in enumerate(labels))
        dpg.set_axis_ticks(tag_axis_x, ticks)

        # Ajustar límites para que se vea centrado
        if x:
            dpg.set_axis_limits(tag_axis_x, -0.5, len(x) - 0.5)

            max_val = max(y) if y else 0
            ymax = max_val if max_val > 0 else 5
            dpg.set_axis_limits(tag_axis_y, 0, ymax * 1.2)

    # Actualizar Pie Chart Estado
    if dpg.does_item_exist(_TAG_CHART_PIE_ESTADO):
        l, v = data['g1']
        dpg.configure_item(_TAG_CHART_PIE_ESTADO, labels=l, values=v)

    # Actualizar Gráficos de Barras
    update_bar_chart(_TAG_CHART_BAR_MONEY, _TAG_AXIS_X_MONEY, _TAG_AXIS_Y_MONEY, data['g2'][0], data['g2'][1])
    update_bar_chart(_TAG_CHART_BAR_MODELS, _TAG_AXIS_X_MODELS, _TAG_AXIS_Y_MODELS, data['g3'][0], data['g3'][1])

    # Actualizar Pie Chart Mantenimiento
    if dpg.does_item_exist(_TAG_CHART_PIE_MANT):
        l, v = data['g4']
        dpg.configure_item(_TAG_CHART_PIE_MANT, labels=l, values=v)


def _refresh_data():
    dpg.set_value(_TAG_KPI_DISPONIBLES, "...")
    run_async(_fetch_dashboard_data, _update_ui)


def _draw_kpi_card(tag_val, label, icon, color):
    with dpg.child_window(border=True, width=-1, height=140, no_scrollbar=True, no_scroll_with_mouse=True):
        _apply_card_theme(dpg.last_item())
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_text(icon, color=color)
                dpg.add_text(label, color=COL_TEXT_TITLE)
            dpg.add_spacer(height=10)
            dpg.add_text("0", tag=tag_val, color=COL_TEXT_VAL)
            dpg.add_spacer(height=15)
            with dpg.drawlist(width=100, height=6):
                dpg.draw_rectangle((0, 0), (50, 6), color=color, fill=color, rounding=3)


def _draw_chart_container(title, height=500):
    container = dpg.add_child_window(border=True, width=-1, height=height, no_scrollbar=True, no_scroll_with_mouse=True)
    _apply_card_theme(container)
    with dpg.group(parent=container):
        dpg.add_text(title, color=COL_TEXT_TITLE)
        dpg.add_separator()
        dpg.add_spacer(height=10)
    return container


def register():
    if dpg.does_item_exist(_TAG):
        dpg.delete_item(_TAG)

    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, border=False):
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            dpg.add_text("Dashboard Operativo", color=(56, 117, 215))
            dpg.add_spacer(width=20)
            dpg.add_button(label="Refrescar Datos", callback=_refresh_data, small=True)

        dpg.add_spacer(height=20)

        # ROW 1: KPI CARDS
        with dpg.table(header_row=False, width=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerV=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=1.0)

            with dpg.table_row():
                _draw_kpi_card(_TAG_KPI_DISPONIBLES, "DISPONIBLES", "##", COL_ACCENT_VERDE)
                _draw_kpi_card(_TAG_KPI_ACTIVOS, "ALQUILADOS", ">>", COL_ACCENT_AZUL)
                _draw_kpi_card(_TAG_KPI_TALLER, "EN TALLER", "!!", COL_ACCENT_ROJO)
                _draw_kpi_card(_TAG_KPI_FACTURACION, "FACTURACIÓN", "$$", COL_ACCENT_AMARILLO)

        dpg.add_spacer(height=20)

        CHART_HEIGHT = 450

        # ROW 2: GRÁFICOS SUPERIORES
        with dpg.table(header_row=False, width=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerH=False, borders_innerV=False):
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=1.0)

            with dpg.table_row():
                # G2: Ingresos
                c1 = _draw_chart_container("Ingresos Semestrales", height=CHART_HEIGHT)
                with dpg.plot(parent=c1, no_title=True, width=-1, height=-1, no_mouse_pos=True):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="", tag=_TAG_AXIS_X_MONEY, no_gridlines=True)
                    with dpg.plot_axis(dpg.mvYAxis, label="Monto ($)", tag=_TAG_AXIS_Y_MONEY):
                        dpg.add_bar_series([], [], label="Ingresos", tag=_TAG_CHART_BAR_MONEY, weight=0.5)

                # G1: Estado (Pie)
                c2 = _draw_chart_container("Estado de Flota", height=CHART_HEIGHT)
                with dpg.plot(parent=c2, no_title=True, width=-1, height=-1,
                              no_mouse_pos=True, equal_aspects=True):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                        dpg.add_pie_series(0.5, 0.5, 0.35, [], [], tag=_TAG_CHART_PIE_ESTADO, normalize=True)

        dpg.add_spacer(height=20)

        # ROW 3: GRÁFICOS INFERIORES
        with dpg.table(header_row=False, width=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerH=False, borders_innerV=False):
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=1.0)

            with dpg.table_row():
                # G3: Modelos (Barras Verticales) - CORREGIDO
                c3 = _draw_chart_container("Flota por Modelo (Top 5)", height=CHART_HEIGHT)
                with dpg.plot(parent=c3, no_title=True, width=-1, height=-1, no_mouse_pos=True):
                    dpg.add_plot_axis(dpg.mvXAxis, label="", tag=_TAG_AXIS_X_MODELS, no_gridlines=True)
                    with dpg.plot_axis(dpg.mvYAxis, label="Unidades", tag=_TAG_AXIS_Y_MODELS):
                        dpg.add_bar_series([], [], label="Vehículos", tag=_TAG_CHART_BAR_MODELS, weight=0.5)

                # G4: Mantenimiento (Pie)
                c4 = _draw_chart_container("Tipos de Mantenimiento", height=CHART_HEIGHT)
                with dpg.plot(parent=c4, no_title=True, width=-1, height=-1,
                              no_mouse_pos=True, equal_aspects=True):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                        dpg.add_pie_series(0.5, 0.5, 0.35, [], [], tag=_TAG_CHART_PIE_MANT, normalize=True)

        dpg.add_spacer(height=20)

    register_view("home", _TAG)
    _refresh_data()
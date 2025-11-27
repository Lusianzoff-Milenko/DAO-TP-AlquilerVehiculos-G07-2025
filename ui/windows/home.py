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
    """Recolección de datos robusta (calculando en Python si las vistas fallan)."""
    local_container = Container()

    # Servicios y Repositorios directos
    local_controller = local_container.reporte_controller()
    mant_repo = local_container.mantenimiento_repo()
    vehiculo_repo = local_container.vehiculo_repo()
    contrato_repo = local_container.contrato_repo()  # Para fallback

    try:
        # --- 1. OBTENCIÓN DE DATOS ---

        # Vehículos (Directo de tabla para asegurar datos)
        vehiculos_all = vehiculo_repo.list_all()
        print(f"[DEBUG] Total Vehículos encontrados: {len(vehiculos_all)}")

        # Mantenimientos (Directo de tabla)
        mantenimientos = mant_repo.list_all()
        print(f"[DEBUG] Total Mantenimientos encontrados: {len(mantenimientos)}")

        # Contratos
        contratos_all = contrato_repo.list_all()

        # Intentar usar vistas para facturación (si fallan, usaremos 0)
        try:
            facturacion, total_facturado = local_controller.get_facturacion_mensual()
        except:
            facturacion, total_facturado = [], 0.0

        # --- 2. PROCESAMIENTO ---

        # KPI: Disponibilidad
        disponibles = [v for v in vehiculos_all if v.Estado.nombre == "Disponible"]
        kpi_disp = len(disponibles)

        # KPI: Activos (Alquilados)
        kpi_rent = len([v for v in vehiculos_all if v.Estado.nombre == "Alquilado"])

        # KPI: En Taller (Cualquier estado de mantenimiento)
        en_taller = [v for v in vehiculos_all if
                     v.Estado.ambito == "Mantenimiento" or v.Estado.nombre in ["EnMantenimiento", "EnReparacion",
                                                                               "EnDiagnostico"]]
        kpi_mant = len(en_taller)

        # --- GRÁFICOS ---

        # G1: Estado Flota (Pie)
        estado_counts = defaultdict(int)
        for v in vehiculos_all:
            est_nombre = v.Estado.nombre
            # Agrupar para limpiar el gráfico
            if est_nombre in ["EnMantenimiento", "EnReparacion", "EnDiagnostico", "EnRevision"]:
                label = "Mantenimiento"
            elif est_nombre in ["Disponible", "Alquilado", "Reservado"]:
                label = est_nombre
            else:
                label = "Otros"
            estado_counts[label] += 1

        pie_est_lbl = list(estado_counts.keys())
        pie_est_val = list(estado_counts.values())
        if not pie_est_val: pie_est_val, pie_est_lbl = [1], ["Sin Datos"]

        # G2: Ingresos (Barras)
        # Si la vista falló, usamos datos dummy o 0 para no romper el gráfico
        if not facturacion:
            bar_money_lbl = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
            bar_money_val = [0, 0, 0, 0, 0, 0]
        else:
            ingresos_mes = defaultdict(float)
            for item in facturacion:
                try:
                    f_str = str(item.get('Fecha Fin', ''))[:10]
                    dt = datetime.strptime(f_str, "%Y-%m-%d")
                    ingresos_mes[dt.strftime("%m/%y")] += float(item.get('Facturado', 0))
                except:
                    continue
            sorted_m = sorted(ingresos_mes.items(), key=lambda x: datetime.strptime(x[0], "%m/%y"))[-6:]
            bar_money_lbl = [x[0] for x in sorted_m]
            bar_money_val = [x[1] for x in sorted_m]

        # G3: Top Modelos (Barras) - CALCULO MANUAL (Sin depender de vista)
        # Contamos cuántas veces aparece cada modelo en los contratos
        modelo_counter = defaultdict(int)
        # Si tienes acceso a los contratos y sus detalles:
        # (Simplificado: usamos el vehículo actual, idealmente sería histórico de contratos)
        # Como aproximación, contamos cuántos vehículos tenemos de cada modelo en la flota
        for v in vehiculos_all:
            modelo_name = v.Modelo.nombre if v.Modelo else "Desconocido"
            modelo_counter[modelo_name] += 1

        # Ordenar top 5
        top_mods = sorted(modelo_counter.items(), key=lambda x: x[1], reverse=True)[:5]
        bar_mod_lbl = [x[0] for x in top_mods]
        bar_mod_val = [x[1] for x in top_mods]

        if not bar_mod_val:  # Fallback si no hay vehículos
            bar_mod_lbl, bar_mod_val = ["Sin Datos"], [0]

        # G4: Tipos Mantenimiento (Pie)
        mant_counts = {"Preventivo": 0, "Correctivo": 0}
        for m in mantenimientos:
            # Lógica simple: si cuesta más de $50.000 es correctivo (arreglo), sino preventivo (service)
            tipo = "Correctivo" if m.costo > 50000 else "Preventivo"
            mant_counts[tipo] += 1

        pie_mant_lbl = [k for k, v in mant_counts.items() if v > 0]
        pie_mant_val = [v for v in mant_counts.values() if v > 0]

        # Fallback para que el gráfico no quede negro
        if not pie_mant_val:
            pie_mant_val, pie_mant_lbl = [1], ["Sin Mantenimientos"]

        return {
            'kpi_disp': kpi_disp, 'kpi_rent': kpi_rent, 'kpi_mant': kpi_mant, 'kpi_total': total_facturado,
            'g1': (pie_est_lbl, pie_est_val),
            'g2': (bar_money_lbl, bar_money_val),
            'g3': (bar_mod_lbl, bar_mod_val),
            'g4': (pie_mant_lbl, pie_mant_val)
        }

    except Exception as e:
        print(f"[Dashboard Error Crítico]: {e}")
        import traceback
        traceback.print_exc()
        return None


def _update_ui(data):
    if not data: return

    dpg.set_value(_TAG_KPI_DISPONIBLES, str(data['kpi_disp']))
    dpg.set_value(_TAG_KPI_ACTIVOS, str(data['kpi_rent']))
    dpg.set_value(_TAG_KPI_TALLER, str(data['kpi_mant']))
    dpg.set_value(_TAG_KPI_FACTURACION, f"${data['kpi_total']:,.0f}")

    def update_bar_chart(tag_series, tag_axis_x, tag_axis_y, labels, values):
        if not dpg.does_item_exist(tag_series): return

        # Eje X numérico
        x = list(range(len(values)))
        if not values: x, values, labels = [0], [0], ["-"]

        dpg.set_value(tag_series, [x, values])
        # Etiquetas personalizadas en eje X
        dpg.set_axis_ticks(tag_axis_x, [(label, i) for i, label in enumerate(labels)])

        # Ajustar límites para estética
        dpg.set_axis_limits(tag_axis_x, -0.6, len(x) - 0.4)
        ymax = max(values) if values else 10
        dpg.set_axis_limits(tag_axis_y, 0, ymax * 1.2)

    # Actualizar Pie Chart Estado
    if dpg.does_item_exist(_TAG_CHART_PIE_ESTADO):
        l, v = data['g1']
        dpg.configure_item(_TAG_CHART_PIE_ESTADO, labels=l, values=v)

    # Actualizar Barras
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
    # Aumentamos height para formato cuadrado
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

        # Header
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            dpg.add_text("Dashboard Operativo", color=(56, 117, 215))
            dpg.add_spacer(width=20)
            dpg.add_button(label="Refrescar Datos", callback=_refresh_data, small=True)

        dpg.add_spacer(height=20)

        # ROW 1: KPI CARDS (Tabla para distribución uniforme)
        with dpg.table(header_row=False, width=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerV=False, borders_innerH=False):
            # Columnas con peso 1.0 aseguran distribución equitativa
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

        # Configuración de altura para gráficos cuadrados
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
                # G3: Modelos (Barras Verticales)
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
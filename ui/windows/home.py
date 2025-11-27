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
COL_BG_CARD = (35, 37, 45, 255)
COL_TEXT_TITLE = (150, 160, 170, 255)
COL_ACCENT_1 = (86, 200, 255, 255)  # Azul
COL_ACCENT_2 = (255, 100, 100, 255)  # Rojo
COL_ACCENT_3 = (255, 200, 80, 255)  # Amarillo
COL_ACCENT_4 = (100, 220, 120, 255)  # Verde


def _apply_card_theme(item_tag):
    """Estilo de tarjeta con bordes redondeados."""
    with dpg.theme() as card_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COL_BG_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 65, 75, 255))
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
    dpg.bind_item_theme(item_tag, card_theme)


def _apply_table_spacing(item_tag, h_spacing=15, v_spacing=0):
    """Aplica espaciado interno a las celdas de la tabla correctamente."""
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvTable):
            # CellPadding añade espacio dentro de cada celda
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding, h_spacing, v_spacing)
    dpg.bind_item_theme(item_tag, t)


def _fetch_dashboard_data():
    """Lógica segura de recolección de datos."""
    local_container = Container()
    local_controller = local_container.reporte_controller()
    mant_service = local_container.mantenimiento_service()

    try:
        # 1. Datos Crudos
        disponibles = local_controller.get_disponibilidad_flota() or []
        utilizacion = local_controller.get_utilizacion_flota() or []
        contratos = local_controller.get_rentabilidad_contratos() or []
        facturacion, total_facturado = local_controller.get_facturacion_mensual()
        mantenimientos = mant_service._repo.list_all() or []

        # 2. KPIs
        kpi_disp = len(disponibles)
        kpi_rent = sum(1 for c in contratos if c.get('Estado') == 'EnCurso')
        kpi_mant = sum(
            1 for u in utilizacion if u.get('Estado') in ['EnMantenimiento', 'EnReparacion', 'EnDiagnostico'])

        # 3. Datos Gráficos

        # G1: Estado Flota
        estado_counts = defaultdict(int)
        for u in utilizacion:
            est = u.get('Estado', 'Otro')
            if est in ['EnMantenimiento', 'EnReparacion', 'EnDiagnostico']:
                est = 'Mantenimiento'
            elif est not in ['Disponible', 'Alquilado']:
                est = 'Otros'
            estado_counts[est] += 1

        pie_est_lbl, pie_est_val = [], []
        for k, v in estado_counts.items():
            if v > 0:
                pie_est_lbl.append(f"{k} ({v})")
                pie_est_val.append(v)
        if not pie_est_val: pie_est_val, pie_est_lbl = [1], ["Sin Datos"]

        # G2: Ingresos
        ingresos_mes = defaultdict(float)
        for item in facturacion:
            try:
                f_str = str(item.get('Fecha Fin', ''))[:10]
                if len(f_str) < 10: continue
                dt = datetime.strptime(f_str, "%Y-%m-%d")
                key = dt.strftime("%m/%y")
                ingresos_mes[key] += float(item.get('Facturado', 0))
            except:
                continue

        sorted_m = sorted(ingresos_mes.items(), key=lambda x: datetime.strptime(x[0], "%m/%y"))[-6:]
        bar_money_lbl = [x[0] for x in sorted_m]
        bar_money_val = [x[1] for x in sorted_m]

        # G3: Top Modelos
        mod_counts = defaultdict(int)
        for u in utilizacion:
            mod_counts[u['Modelo']] += u.get('Contratos', 0)
        top_mods = sorted(mod_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        bar_mod_lbl = [x[0] for x in top_mods]
        bar_mod_val = [x[1] for x in top_mods]

        # G4: Mantenimiento
        mant_counts = {"Preventivo": 0, "Correctivo": 0}
        for m in mantenimientos:
            tipo = "Correctivo" if m.costo > 50000 else "Preventivo"
            mant_counts[tipo] += 1
        pie_mant_lbl = [f"{k} ({v})" for k, v in mant_counts.items() if v > 0]
        pie_mant_val = [v for v in mant_counts.values() if v > 0]
        if not pie_mant_val: pie_mant_val, pie_mant_lbl = [1], ["Sin Datos"]

        return {
            'kpi_disp': kpi_disp, 'kpi_rent': kpi_rent,
            'kpi_mant': kpi_mant, 'kpi_total': total_facturado,
            'g1': (pie_est_lbl, pie_est_val),
            'g2': (bar_money_lbl, bar_money_val),
            'g3': (bar_mod_lbl, bar_mod_val),
            'g4': (pie_mant_lbl, pie_mant_val)
        }

    except Exception as e:
        print(f"[Dashboard Error Crítico]: {e}")
        return None


def _update_ui(data):
    if not data: return

    dpg.set_value(_TAG_KPI_DISPONIBLES, str(data['kpi_disp']))
    dpg.set_value(_TAG_KPI_ACTIVOS, str(data['kpi_rent']))
    dpg.set_value(_TAG_KPI_TALLER, str(data['kpi_mant']))
    dpg.set_value(_TAG_KPI_FACTURACION, f"${data['kpi_total']:,.0f}")

    def update_bar_chart(tag_series, tag_axis_x, tag_axis_y, labels, values, y_margin=1.2):
        if not dpg.does_item_exist(tag_series): return
        x = list(range(len(values)))
        if not values: x, values, labels = [0], [0], ["Sin Datos"]
        dpg.set_value(tag_series, [x, values])
        dpg.set_axis_ticks(tag_axis_x, [(l, i) for i, l in enumerate(labels)])
        width_x = max(len(x), 5)
        dpg.set_axis_limits(tag_axis_x, -0.5, width_x - 0.5)
        max_val = max(values) if values else 100
        dpg.set_axis_limits(tag_axis_y, 0, max_val * y_margin)

    if dpg.does_item_exist(_TAG_CHART_PIE_ESTADO):
        l, v = data['g1']
        dpg.configure_item(_TAG_CHART_PIE_ESTADO, labels=l, values=v)

    update_bar_chart(_TAG_CHART_BAR_MONEY, _TAG_AXIS_X_MONEY, _TAG_AXIS_Y_MONEY, data['g2'][0], data['g2'][1])
    update_bar_chart(_TAG_CHART_BAR_MODELS, _TAG_AXIS_X_MODELS, _TAG_AXIS_Y_MODELS, data['g3'][0], data['g3'][1])

    if dpg.does_item_exist(_TAG_CHART_PIE_MANT):
        l, v = data['g4']
        dpg.configure_item(_TAG_CHART_PIE_MANT, labels=l, values=v)


def _refresh_data():
    dpg.set_value(_TAG_KPI_DISPONIBLES, "...")
    run_async(_fetch_dashboard_data, _update_ui)


def _draw_kpi_card(tag_val, label, icon, color):
    # Altura aumentada para evitar cortes
    with dpg.child_window(border=True, width=-1, height=120, no_scrollbar=True):
        _apply_card_theme(dpg.last_item())
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_text(icon, color=color)
                dpg.add_text(label, color=COL_TEXT_TITLE)
            dpg.add_spacer(height=5)
            dpg.add_text("0", tag=tag_val, color=(255, 255, 255))
            dpg.add_spacer(height=5)
            with dpg.drawlist(width=100, height=5):
                dpg.draw_rectangle((0, 0), (40, 4), color=color, fill=color, rounding=2)


def _draw_chart_container(title):
    # Altura aumentada para evitar aplastamiento
    container = dpg.add_child_window(border=True, width=-1, height=320, no_scrollbar=True)
    _apply_card_theme(container)
    with dpg.group(parent=container):
        dpg.add_text(title, color=COL_TEXT_TITLE)
        dpg.add_spacer(height=5)
    return container


def register():
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1,
                          border=False, no_scrollbar=True):
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            dpg.add_text("Panel de Control", color=(56, 117, 215))
            dpg.add_spacer(width=20)
            dpg.add_button(label="Actualizar", callback=_refresh_data, small=True)

        dpg.add_spacer(height=15)

        # ROW 1: KPIs
        # AQUÍ ESTÁ LA CORRECCIÓN: Creamos la tabla y luego aplicamos el tema de espaciado
        with dpg.table(header_row=False, width=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerV=False, borders_innerH=False) as table_kpis:
            for _ in range(4): dpg.add_table_column()

            with dpg.table_row():
                _draw_kpi_card(_TAG_KPI_DISPONIBLES, "DISPONIBLES", "[AUTO]", COL_ACCENT_4)
                _draw_kpi_card(_TAG_KPI_ACTIVOS, "ALQUILADOS", "[KEY]", COL_ACCENT_1)
                _draw_kpi_card(_TAG_KPI_TALLER, "TALLER", "[TOOL]", COL_ACCENT_2)
                _draw_kpi_card(_TAG_KPI_FACTURACION, "INGRESOS", "[$]", COL_ACCENT_3)

        # Aplicamos el espaciado a la tabla usando su tag (o variable)
        _apply_table_spacing(table_kpis, h_spacing=15)

        dpg.add_spacer(height=15)

        # ROW 2: GRÁFICOS SUPERIORES
        with dpg.table(header_row=False, width=-1, height=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerH=False, borders_innerV=False) as table_g1:
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():
                # G1
                parent = _draw_chart_container("Ingresos ($)")
                with dpg.plot(parent=parent, no_title=True, width=-1, height=-1, no_mouse_pos=True):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Mes", tag=_TAG_AXIS_X_MONEY, no_gridlines=True)
                    with dpg.plot_axis(dpg.mvYAxis, label="Monto", tag=_TAG_AXIS_Y_MONEY):
                        dpg.add_bar_series([], [], label="Ingresos", tag=_TAG_CHART_BAR_MONEY, weight=0.5)

                # G2
                parent = _draw_chart_container("Estado Flota")
                with dpg.group(horizontal=True, parent=parent):
                    dpg.add_spacer(width=50)
                    with dpg.plot(no_title=True, width=220, height=220, no_mouse_pos=True, equal_aspects=True):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                        with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                            dpg.set_axis_limits(dpg.last_item(), 0, 1)
                            dpg.add_pie_series(0.5, 0.5, 0.4, [], [], tag=_TAG_CHART_PIE_ESTADO, normalize=True)

        _apply_table_spacing(table_g1, h_spacing=15)
        dpg.add_spacer(height=15)

        # ROW 3: GRÁFICOS INFERIORES
        with dpg.table(header_row=False, width=-1, height=-1, policy=dpg.mvTable_SizingStretchProp,
                       borders_innerH=False, borders_innerV=False) as table_g2:
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():
                # G3
                parent = _draw_chart_container("Top Modelos")
                with dpg.plot(parent=parent, no_title=True, width=-1, height=-1, no_mouse_pos=True):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Modelo", tag=_TAG_AXIS_X_MODELS, no_gridlines=True)
                    with dpg.plot_axis(dpg.mvYAxis, label="Cant", tag=_TAG_AXIS_Y_MODELS):
                        dpg.add_bar_series([], [], label="Alquileres", tag=_TAG_CHART_BAR_MODELS, weight=0.5)

                # G4
                parent = _draw_chart_container("Mantenimiento")
                with dpg.group(horizontal=True, parent=parent):
                    dpg.add_spacer(width=50)
                    with dpg.plot(no_title=True, width=220, height=220, no_mouse_pos=True, equal_aspects=True):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                        with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                            dpg.set_axis_limits(dpg.last_item(), 0, 1)
                            dpg.add_pie_series(0.5, 0.5, 0.4, [], [], tag=_TAG_CHART_PIE_MANT, normalize=True)

        _apply_table_spacing(table_g2, h_spacing=15)
        dpg.add_spacer(height=10)

    register_view("home", _TAG)
    _refresh_data()
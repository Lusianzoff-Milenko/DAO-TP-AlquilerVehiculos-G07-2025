import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.kpi_card import KPICard
from ui.services.workers import run_async
from services.containers.container import Container

_TAG = "view_home"
_controller = Container().reporte_controller()

# --- Tags para actualizar elementos dinámicamente ---
_TAG_CHART_SERIES = "home_chart_series"
_TAG_CHART_X_AXIS = "home_chart_x_axis"

# --- Instancias de Tarjetas KPI (para usar sus métodos update) ---
card_disponibles = KPICard("kpi_avail", "Vehículos Disponibles", icon="🚗", color=(46, 204, 113, 255))
card_alquileres = KPICard("kpi_active", "Alquileres En Curso", icon="🔑", color=(52, 152, 219, 255))
card_facturacion = KPICard("kpi_money", "Facturación Histórica", icon="💰", color=(155, 89, 182, 255))
card_mantenimiento = KPICard("kpi_mant", "En Mantenimiento", icon="🔧", color=(231, 76, 60, 255))


def _fetch_dashboard_data():
    """
    Tarea en segundo plano: Recolecta datos de varios servicios.
    """
    # 1. Disponibilidad
    disponibles_list = _controller.get_disponibilidad_flota()
    count_disponibles = len(disponibles_list)

    # 2. Alquileres Activos (Buscamos en rentabilidad contratos con estado EnCurso)
    # Nota: Como get_rentabilidad trae todo, filtramos aquí.
    # Idealmente el controller tendría un método específico, pero esto funciona.
    contratos = _controller.get_rentabilidad_contratos()
    count_activos = sum(1 for c in contratos if c['Estado'] == 'EnCurso')

    # 3. Facturación (Tupla: [lista], total)
    _, total_facturado = _controller.get_facturacion_mensual()

    # 4. Utilización y Mantenimiento
    utilizacion = _controller.get_utilizacion_flota()
    count_mantenimiento = sum(
        1 for u in utilizacion if u['Estado'] == 'EnMantenimiento' or u['Estado'] == 'EnReparacion')

    # 5. Datos para el gráfico (Top 5 Modelos por Días Alquilados)
    # Agrupar por modelo
    model_stats = {}
    for u in utilizacion:
        modelo = u['Modelo']
        dias = u['Días Alquilado'] if u['Días Alquilado'] else 0
        model_stats[modelo] = model_stats.get(modelo, 0) + dias

    # Ordenar y tomar top 5
    top_models = sorted(model_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    chart_labels = [m[0] for m in top_models]
    chart_values = [m[1] for m in top_models]

    return {
        'disponibles': count_disponibles,
        'activos': count_activos,
        'facturado': total_facturado,
        'mantenimiento': count_mantenimiento,
        'chart_labels': chart_labels,
        'chart_values': chart_values
    }


def _update_ui(data):
    """
    Callback: Se ejecuta en el hilo principal para actualizar la GUI.
    """
    # Actualizar Tarjetas
    card_disponibles.update(str(data['disponibles']), "Listos para salir")
    card_alquileres.update(str(data['activos']), "Contratos activos")
    card_facturacion.update(f"${data['facturado']:,.2f}", "Total acumulado")
    card_mantenimiento.update(str(data['mantenimiento']), "En taller")

    # Actualizar Gráfico
    if dpg.does_item_exist(_TAG_CHART_SERIES):
        # DPG requiere coordenadas numéricas X para gráficos de barras
        x_coords = list(range(len(data['chart_values'])))

        dpg.set_value(_TAG_CHART_SERIES, [x_coords, data['chart_values']])

        # Actualizar etiquetas del eje X (Hack para mostrar texto en eje X)
        # DPG no soporta strings nativos en eje X fácilmente, usamos Ticks custom
        ticks = []
        for i, label in enumerate(data['chart_labels']):
            ticks.append((label, i))

        dpg.set_axis_ticks(_TAG_CHART_X_AXIS, ticks)


def _refresh_data():
    """Dispara la actualización asíncrona."""
    # Poner indicadores de carga visual si se desea
    card_disponibles.update("...")
    run_async(_fetch_dashboard_data, _update_ui)


def register():
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, no_scrollbar=False):
        dpg.add_spacer(height=16)

        # Cabecera con botón de actualizar
        with dpg.group(horizontal=True):
            dpg.add_text("Dashboard Operativo", color=(56, 117, 215))
            dpg.add_spacer(width=10)
            dpg.add_button(label="🔄", callback=_refresh_data)

        dpg.add_separator()
        dpg.add_spacer(height=20)

        # --- FILA 1: TARJETAS KPI ---
        # Usamos un grupo horizontal centrado (simulado con espaciadores)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            card_disponibles.render(dpg.last_container(), width=250)
            dpg.add_spacer(width=20)
            card_alquileres.render(dpg.last_container(), width=250)
            dpg.add_spacer(width=20)
            card_mantenimiento.render(dpg.last_container(), width=250)
            dpg.add_spacer(width=20)
            card_facturacion.render(dpg.last_container(), width=250)

        dpg.add_spacer(height=30)

        # --- FILA 2: GRÁFICO Y ACCESOS ---
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)

            # Panel Izquierdo: Gráfico
            with dpg.child_window(width=700, height=400, border=True):
                dpg.add_spacer(height=10)
                dpg.add_text("  📈 Top Modelos por Demanda (Días Alquilados)", color=(200, 200, 200))

                with dpg.plot(tag="plot_utilizacion", height=-1, width=-1, no_mouse_pos=True):
                    dpg.add_plot_legend()

                    # Ejes
                    dpg.add_plot_axis(dpg.mvXAxis, label="Modelo", tag=_TAG_CHART_X_AXIS, no_gridlines=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Días Totales", tag="y_axis")

                    # Serie de barras (inicialmente vacía)
                    dpg.add_bar_series([], [], label="Días Alquilado", parent=y_axis, tag=_TAG_CHART_SERIES, weight=0.5)

            dpg.add_spacer(width=20)

            # Panel Derecho: Accesos Rápidos / Resumen
            with dpg.child_window(width=-1, height=400, border=True):  # -1 llena el resto
                dpg.add_spacer(height=10)
                dpg.add_text("  ⚡ Accesos Rápidos", color=(200, 200, 200))
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Botones grandes
                dpg.add_button(label="📝 Nueva Reserva", width=-1, height=40,
                               callback=lambda: print("Ir a reservas"))  # Puedes conectar con navegación
                dpg.add_spacer(height=10)
                dpg.add_button(label="👥 Registrar Cliente", width=-1, height=40,
                               callback=lambda: print("Ir a clientes"))
                dpg.add_spacer(height=10)
                dpg.add_button(label="🚗 Flota Completa", width=-1, height=40, callback=lambda: print("Ir a vehículos"))

                dpg.add_spacer(height=30)
                dpg.add_text("  📢 Estado del Sistema", color=(200, 200, 200))
                dpg.add_separator()
                dpg.add_text("Base de datos: Conectada (SQLite)", color=(100, 255, 100), bullet=True)
                dpg.add_text("Sistema: Online", color=(100, 255, 100), bullet=True)

        dpg.add_spacer(height=20)

    register_view("home", _TAG)

    # Cargar datos al iniciar
    _refresh_data()
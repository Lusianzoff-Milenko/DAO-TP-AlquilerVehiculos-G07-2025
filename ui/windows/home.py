import dearpygui.dearpygui as dpg
from ui.navigation import register_view
from ui.components.kpi_card import KPICard

_TAG = "view_home"

def _mock_get_kpis():
    """Mock de datos para KPIs."""
    return {
        'vehiculos_disponibles': 12,
        'vehiculos_total': 25,
        'alquileres_activos': 8,
        'reservas_pendientes': 5,
        'facturacion_mes': 45000.50,
        'clientes_activos': 34
    }

def register():
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1):
        dpg.add_spacer(height=16)
        
        # Título
        dpg.add_text("Dashboard - Sistema de Alquiler de Vehículos", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=16)
        
        # Obtener datos mock
        kpis = _mock_get_kpis()
        
        # Primera fila de KPIs
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=12)
            
            kpi1 = KPICard(
                tag="kpi_vehiculos",
                title="Vehículos Disponibles",
                value=f"{kpis['vehiculos_disponibles']}/{kpis['vehiculos_total']}",
                subtitle="Para alquilar",
                color=(46, 204, 113, 255),
                icon="[V]"
            )
            kpi1.render("view_home", width=240, height=130)
            
            dpg.add_spacer(width=12)
            
            kpi2 = KPICard(
                tag="kpi_alquileres",
                title="Alquileres Activos",
                value=str(kpis['alquileres_activos']),
                subtitle="En curso",
                color=(52, 152, 219, 255),
                icon="[A]"
            )
            kpi2.render("view_home", width=240, height=130)
            
            dpg.add_spacer(width=12)
            
            kpi3 = KPICard(
                tag="kpi_reservas",
                title="Reservas Pendientes",
                value=str(kpis['reservas_pendientes']),
                subtitle="Por confirmar",
                color=(241, 196, 15, 255),
                icon="[R]"
            )
            kpi3.render("view_home", width=240, height=130)
            
            dpg.add_spacer(width=12)
            
            kpi4 = KPICard(
                tag="kpi_facturacion",
                title="Facturación Mensual",
                value=f"${kpis['facturacion_mes']:,.2f}",
                subtitle="Noviembre 2025",
                color=(155, 89, 182, 255),
                icon="[$]"
            )
            kpi4.render("view_home", width=240, height=130)
        
        dpg.add_spacer(height=24)
        
        # Segunda fila - Resumen
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=12)
            
            # Panel de accesos rápidos
            with dpg.child_window(width=480, height=200, border=True):
                dpg.add_spacer(height=8)
                dpg.add_text("Accesos Rápidos", color=(200, 200, 200))
                dpg.add_separator()
                dpg.add_spacer(height=12)
                
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    with dpg.group():
                        dpg.add_button(label="Nuevo Alquiler", width=200, callback=lambda: print("Nuevo alquiler"))
                        dpg.add_spacer(height=8)
                        dpg.add_button(label="Buscar Cliente", width=200, callback=lambda: print("Buscar cliente"))
                        dpg.add_spacer(height=8)
                        dpg.add_button(label="Ver Reportes", width=200, callback=lambda: print("Ver reportes"))
                        dpg.add_spacer(height=8)
                        dpg.add_button(label="Registrar Mantenimiento", width=200, callback=lambda: print("Mantenimiento"))
            
            dpg.add_spacer(width=12)
            
            # Panel de actividad reciente
            with dpg.child_window(width=500, height=200, border=True):
                dpg.add_spacer(height=8)
                dpg.add_text("Actividad Reciente", color=(200, 200, 200))
                dpg.add_separator()
                dpg.add_spacer(height=12)
                
                dpg.add_text("  • Nuevo alquiler: Juan Pérez - Toyota Corolla")
                dpg.add_text("  • Devolución: María García - Honda Civic")
                dpg.add_text("  • Mantenimiento programado: Ford Focus (Mañana)")
                dpg.add_text("  • Nueva reserva: Carlos López - Volkswagen Golf")
                dpg.add_text("  • Cliente registrado: Ana Martínez")
        
        dpg.add_spacer(height=16)
    
    register_view("home", _TAG)

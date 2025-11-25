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
    with dpg.child_window(tag=_TAG, parent="content_area", show=False, width=-1, height=-1, no_scrollbar=True):
        dpg.add_spacer(height=16)
        
        # Título
        dpg.add_text("Dashboard - Sistema de Alquiler de Vehículos", color=(56, 117, 215))
        dpg.add_separator()
        dpg.add_spacer(height=20)
        
        # Obtener datos mock
        kpis = _mock_get_kpis()
        
        # Contenedor horizontal para primera fila con centrado
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)  # Espaciado izquierdo para centrar
            
            # Primera tarjeta
            with dpg.child_window(width=350, height=130, border=True, no_scrollbar=True):
                dpg.add_spacer(height=12)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Vehículos Disponibles", color=(200, 200, 200))
                dpg.add_spacer(height=4)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text(f"{kpis['vehiculos_disponibles']}/{kpis['vehiculos_total']}", color=(46, 204, 113, 255))
                dpg.add_spacer(height=6)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Para alquilar", color=(150, 150, 150))
            
            dpg.add_spacer(width=20)
            
            # Segunda tarjeta
            with dpg.child_window(width=350, height=130, border=True, no_scrollbar=True):
                dpg.add_spacer(height=12)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Alquileres Activos", color=(200, 200, 200))
                dpg.add_spacer(height=4)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text(str(kpis['alquileres_activos']), color=(52, 152, 219, 255))
                dpg.add_spacer(height=6)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("En curso", color=(150, 150, 150))
        
        dpg.add_spacer(height=20)
        
        # Contenedor horizontal para segunda fila con centrado
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)  # Espaciado izquierdo para centrar
            
            # Tercera tarjeta
            with dpg.child_window(width=350, height=130, border=True, no_scrollbar=True):
                dpg.add_spacer(height=12)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Reservas Pendientes", color=(200, 200, 200))
                dpg.add_spacer(height=4)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text(str(kpis['reservas_pendientes']), color=(241, 196, 15, 255))
                dpg.add_spacer(height=6)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Por confirmar", color=(150, 150, 150))
            
            dpg.add_spacer(width=20)
            
            # Cuarta tarjeta
            with dpg.child_window(width=350, height=130, border=True, no_scrollbar=True):
                dpg.add_spacer(height=12)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Facturación Mensual", color=(200, 200, 200))
                dpg.add_spacer(height=4)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text(f"${kpis['facturacion_mes']:,.2f}", color=(155, 89, 182, 255))
                dpg.add_spacer(height=6)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Noviembre 2025", color=(150, 150, 150))
        
        dpg.add_spacer(height=30)
        
        # Segunda fila - Resumen con centrado
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)
            
            # Panel de accesos rápidos
            with dpg.child_window(width=350, height=200, border=True, no_scrollbar=True):
                dpg.add_spacer(height=8)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
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
            
            dpg.add_spacer(width=20)
            
            # Panel de actividad reciente
            with dpg.child_window(width=350, height=200, border=True, no_scrollbar=True):
                dpg.add_spacer(height=8)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    dpg.add_text("Actividad Reciente", color=(200, 200, 200))
                dpg.add_separator()
                dpg.add_spacer(height=12)
                
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=12)
                    with dpg.group():
                        dpg.add_text("Nuevo alquiler: Juan Pérez - Toyota Corolla")
                        dpg.add_text("Devolución: María García - Honda Civic")
                        dpg.add_text("Mantenimiento programado: Ford Focus (Mañana)")
                        dpg.add_text("Nueva reserva: Carlos López - Volkswagen Golf")
                        dpg.add_text("Cliente registrado: Ana Martínez")
        
        dpg.add_spacer(height=16)
    
    register_view("home", _TAG)

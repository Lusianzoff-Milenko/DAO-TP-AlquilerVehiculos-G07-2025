import dearpygui.dearpygui as dpg

# Diccionario global para guardar las vistas
_VIEWS = {}


def register_view(name: str, tag: str):
    """Registra una vista en el sistema de navegación."""
    print(f"[Navigation] Registrando vista: '{name}' -> Tag: '{tag}'")
    _VIEWS[name] = tag


def go_to(name: str):
    """Navega a una vista. Muestra/oculta sidebar según la vista."""
    print(f"[Navigation] Intentando ir a: '{name}'")
    print(f"   - Vistas registradas actualmente: {list(_VIEWS.keys())}")

    # Mostrar sidebar solo si NO es login
    show_sidebar = (name != "login")
    if dpg.does_item_exist("sidebar"):
        dpg.configure_item("sidebar", show=show_sidebar)

    found_target = False

    # Recorrer TODAS las vistas registradas
    for n, tag in _VIEWS.items():
        if dpg.does_item_exist(tag):
            if n == name:
                # ES la vista destino: Mostrarla
                print(f"   - MOSTRANDO: {n} ({tag})")
                dpg.configure_item(tag, show=True)
                found_target = True

                # Forzar que se vaya al frente por si acaso (opcional)
                # dpg.focus_item(tag)
            else:
                # NO es la vista destino: Ocultarla
                # Solo imprimimos si estaba visible para no llenar la consola
                is_visible = dpg.get_item_configuration(tag)["show"]
                if is_visible:
                    print(f"   - 🙈 OCULTANDO: {n} ({tag})")
                dpg.configure_item(tag, show=False)
        else:
            print(f"   - ADVERTENCIA: El tag '{tag}' registrado para '{n}' NO EXISTE en DearPyGui.")

    if not found_target:
        print(f"[Navigation] ERROR: No se encontró la vista destino '{name}' o su tag no existe.")

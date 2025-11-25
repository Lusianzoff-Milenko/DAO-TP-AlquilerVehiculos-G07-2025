# ui/icons.py

# Definimos iconos como etiquetas de texto.
# Son seguros, no requieren fuentes externas y se ven profesionales (estilo terminal/dev).

ICON_DASHBOARD = "[ DASH ]"
ICON_CAR       = "[ AUTO ]"
ICON_USERS     = "[ CLIE ]"
ICON_USER      = "[ EMPL ]"
ICON_LIST      = "[ LIST ]"
ICON_CALENDAR  = "[ RESV ]"
ICON_WRENCH    = "[ SERV ]"
ICON_CHART     = "[ REPT ]"
ICON_LOGOUT    = "[ SALIR ]"

# Símbolos simples estándar (ASCII/Unicode básico seguro)
ICON_SEARCH    = "[ ? ]"
ICON_EDIT      = "[ / ]"
ICON_TRASH     = "[ X ]"
ICON_CHECK     = "[ OK ]"
ICON_PLUS      = "[ + ]"
ICON_REFRESH   = "[ R ]"

# Función dummy para compatibilidad
def ensure_font_exists():
    return True

def get_font_path():
    return ""
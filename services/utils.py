import datetime
from typing import Optional, Any

DB_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f" # Formato ISO estándar para SQLite

def datetime_to_iso(dt: Optional[datetime.datetime]) -> Optional[str]:
    """
    Convierte un objeto datetime a formato ISO (string) para almacenamiento en DB.
    Maneja valores None.
    """
    if dt is None:
        return None
    try:
        return dt.isoformat()
    except AttributeError:
        # En caso de que se pase un objeto incorrecto que no sea datetime
        return None

def iso_to_datetime(iso_str: Optional[str]) -> Optional[datetime.datetime]:
    """
    Convierte una string ISO (desde la DB) a un objeto datetime.
    Maneja valores None.
    """
    if iso_str is None:
        return None
    try:
        # A veces la precisión de milisegundos se pierde o varía,
        # 'fromisoformat' es robusto, pero el manejo de excepciones ayuda.
        return datetime.datetime.fromisoformat(iso_str)
    except ValueError:
        # En caso de un formato de fecha no estándar
        print(f"Warning: Could not parse date string: {iso_str}")
        return None

def validate_string(value: Any, name: str, max_length: Optional[int] = None) -> Optional[str]:
    """Valida que un valor sea una string no vacía."""
    if not isinstance(value, str) or not value.strip():
        return f"Invalid '{name}' — must be a non-empty string."
    if max_length is not None and len(value) > max_length:
        return f"Invalid '{name}' — maximum length is {max_length} characters."
    return None

def validate_positive_int(value: Any, name: str) -> Optional[str]:
    """Valida que un valor sea un entero positivo (mayor a 0)."""
    # También permite números convertibles a entero, pero en el contexto de IDs,
    # se suele exigir el tipo exacto. Usaremos solo int.
    if not isinstance(value, int) or value <= 0:
        return f"Invalid '{name}' — must be a positive integer."
    return None

def validate_non_negative_number(value: Any, name: str) -> Optional[str]:
    """Valida que un valor sea un float o int no negativo."""
    if not isinstance(value, (float, int)):
        return f"Invalid '{name}' — must be a number."
    if value < 0:
        return f"Invalid '{name}' — must be a non-negative number."
    return None

def validate_boolean(value: Any, name: str) -> Optional[str]:
    """Valida que un valor sea un booleano."""
    if not isinstance(value, bool):
        return f"Invalid '{name}' — must be a boolean."
    return None

def validate_fecha_rango(fecha_desde: Optional[datetime.datetime], 
                         fecha_hasta: Optional[datetime.datetime]) -> Optional[str]:
    """
    Valida que fecha_hasta sea posterior a fecha_desde.
    Retorna un mensaje de error si la validación falla, None si es válido.
    """
    if fecha_desde is None:
        return "Invalid 'fecha_desde' — must not be None."
    if fecha_hasta is None:
        return "Invalid 'fecha_hasta' — must not be None."
    if not isinstance(fecha_desde, datetime.datetime):
        return "Invalid 'fecha_desde' — must be a datetime object."
    if not isinstance(fecha_hasta, datetime.datetime):
        return "Invalid 'fecha_hasta' — must be a datetime object."
    if fecha_hasta <= fecha_desde:
        return "Invalid date range — 'fecha_hasta' must be after 'fecha_desde'."
    return None
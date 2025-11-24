import datetime
from typing import Optional, Any
def validate_string(value: Any, name: str, max_length: Optional[int] = None) -> bool:
    """Retorna True si es válido, False si no."""
    if not isinstance(value, str) or not value.strip():
        print(f"Error: '{name}' debe ser un texto no vacío.")
        return False
    if max_length is not None and len(value) > max_length:
        print(f"Error: '{name}' excede {max_length} caracteres.")
        return False
    return True


def validate_positive_int(value: Any, name: str) -> bool:
    if not isinstance(value, int) or value <= 0:
        print(f"Error: '{name}' debe ser un entero positivo.")
        return False
    return True


def validate_fecha_rango(fecha_desde: Optional[datetime.datetime],
                         fecha_hasta: Optional[datetime.datetime]) -> Optional[str]:
    """
    Valida rango de fechas. Retorna string de error o None si está OK.
    """
    if not fecha_desde or not fecha_hasta:
        return "Las fechas son obligatorias."

    if not isinstance(fecha_desde, datetime.datetime) or not isinstance(fecha_hasta, datetime.datetime):
        return "Formato de fecha inválido (se espera datetime)."

    if fecha_hasta <= fecha_desde:
        return "La fecha de fin debe ser posterior a la de inicio."

    return None
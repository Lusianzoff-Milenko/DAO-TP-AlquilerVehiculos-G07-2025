class DomainError(Exception):
    """Clase base para errores de lógica de negocio."""
    pass

class StateTransitionError(DomainError):
    """Se lanza cuando una acción no es válida en el estado actual."""
    pass

class BusinessRuleError(DomainError):
    """Se lanza cuando una regla de negocio (fechas, montos) no se cumple."""
    pass
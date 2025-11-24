from dataclasses import dataclass
@dataclass
class VistaInconvenientesContratoDTO:
    id_contrato: int
    nombre_tipo_inconveniente: str
    nombre_inconveniente: str
    descripcion_inconveniente: str
    costo: float
    estado_inconveniente: str

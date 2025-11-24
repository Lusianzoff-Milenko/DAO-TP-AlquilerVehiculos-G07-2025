from dataclasses import dataclass
@dataclass
class VistaUtilizacionFlotaDTO:
    id_vehiculo: int
    patente: str
    nombre_marca: str
    nombre_modelo: str
    año_fabricacion: str
    estado_actual: str

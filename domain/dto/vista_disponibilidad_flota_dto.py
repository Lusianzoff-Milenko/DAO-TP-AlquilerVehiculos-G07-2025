from dataclasses import dataclass
@dataclass
class VistaDisponibilidadFlotaDTO:
    id_vehiculo: int
    patente: str
    nombre_marca: str
    nombre_modelo: str
    año_fabricacion: str
    estado: str
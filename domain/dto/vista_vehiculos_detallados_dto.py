from dataclasses import dataclass
@dataclass
class VistaVehiculosDetalladosDTO:
    nombre_marca: str
    nombre_modelo: str
    motor: str
    año_lanzamiento: str
    año_fabricacion: str
    patente: str
    color: str
    estado: str

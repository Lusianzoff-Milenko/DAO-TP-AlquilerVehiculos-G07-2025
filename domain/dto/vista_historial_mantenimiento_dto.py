from dataclasses import dataclass
@dataclass
class VistaHistorialMantenimientoDTO:
    patente: str
    nombre_marca: str
    nombre_modelo: str
    año_fabricacion: str
    costo: float
    descripcion: str
    estado: str
    nombre_empleado: str
    apellido_empleado: str
    fecha_hora: str
    id_mantenimiento: int

from dataclasses import dataclass
@dataclass
class VistaEmpleadosPuestosDTO:
    id_empleado: int
    nombre_empleado: str
    apellido_empleado: str
    nombre_puesto: str

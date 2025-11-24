from dataclasses import dataclass
@dataclass
class VistaReporteFacturacionDTO:
    id_contrato: int
    nombre_cliente: str
    apellido_cliente: str
    fecha_desde: str
    fecha_hasta: str
    fecha_entrega: str
    monto: float
    nombre_empleado: str

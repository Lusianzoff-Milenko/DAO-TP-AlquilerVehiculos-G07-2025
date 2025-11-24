from dataclasses import dataclass
@dataclass
class VistaContratosRentabilidadDTO:
    id_contrato: int
    nombre_cliente: str
    apellido_cliente: str
    fecha_desde: str
    fecha_hasta: str
    fecha_entrega: str
    metodo_pago: str
    estado_contrato: str
    monto: float
    tiene_seguro: int

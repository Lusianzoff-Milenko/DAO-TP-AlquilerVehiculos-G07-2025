from dataclasses import dataclass

@dataclass
class VistaDemandaPorModeloDTO:
    nombre_marca: str
    nombre_modelo: str
    año_fabricacion: str
    total_dias_reservados_contratados: int

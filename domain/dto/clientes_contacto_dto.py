from dataclasses import dataclass
@dataclass
class VistaClientesContactoDTO:
    id_cliente: int
    nombre: str
    apellido: str
    telefono: str
    mail: str
    direccion: str
    tipo_documento: str
    documento: str

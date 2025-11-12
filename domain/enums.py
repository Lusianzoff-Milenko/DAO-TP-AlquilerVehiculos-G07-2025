from enum import Enum

class EstadosPoblador(Enum):
    Disponible = "Vehiculo"
    Reservado = "Vehiculo"
    Alquilado = "Vehiculo"
    EnMantenimiento = "Vehiculo"
    Entregado = "Vehiculo"
    FueraDeServicio = "Vehiculo"
    EnRevision = "Vehiculo"
    EnCurso = "Contrato"
    EnReservado = "Contrato"
    YaEntregado = "Contrato"
    Cancelado = "Contrato"
    EnDiagnostico = "Mantenimiento"
    EnReparacion = "Mantenimiento"
    Reparado = "Mantenimiento"
    NoReparado = "Mantenimiento"
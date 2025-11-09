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
    Reservado = "Contrato"
    Entregado = "Contrato"
    Cancelado = "Contrato"
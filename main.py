from datetime import datetime

from domain.models.estado import Estado
from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.disponible import Disponible
from services import VehiculoService
from services.containers.container import Container
from domain.enums import EstadosPoblador


def main():
    container: Container = Container()
    '''
    vehiculo_service: VehiculoService = container.vehiculo_service()
    vehicle = Vehiculo(id_modelo=1, patente="ABC123", nro_chasis="XYZ789", id_color=1, anio_fabricacion=datetime(2005, 3, 15), precio_base=15000.00, state=Disponible())
    vehiculo_service.create_vehiculo(vehicle)
    vehiculos = vehiculo_service.get_all_vehiculos()
    for v in vehiculos:
        print(v)
    '''
    estado_service = container.estado_service()
    estados = [Estado(nombre=name, ambito=ambito.value) for name, ambito in EstadosPoblador.__members__.items()]
    for e in estados:
        print(f"Creando estado: {e.nombre} - {e.ambito}")
    #estado_service.create_estados(estados)

if __name__ == '__main__':
    main()
from services.containers.container import Container



def main():
    container: Container = Container()
    vehiculo_service = container.vehiculo_service()

    vehiculo = vehiculo_service.get_vehiculo_by_id(1)
    print(vehiculo)
    print(vehiculo.get_state() + "soy el estado actual")

if __name__ == "__main__":

    main()


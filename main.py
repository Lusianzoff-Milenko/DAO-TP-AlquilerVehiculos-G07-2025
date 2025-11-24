from services.containers.container import Container



def main():
    container: Container = Container()
    vehiculo_service = container.vehiculo_service()
    contrato_service = container.contrato_service()
    contrato = contrato_service.get_contrato_by_id(1)
    vehiculo = vehiculo_service.get_vehiculo_by_id(1)
    print(contrato)
    print(vehiculo)
    vehiculo.get_state().reservar(contrato)
    print(f"{vehiculo.get_state().__class__.__name__} soy el estado actual")

if __name__ == "__main__":

    main()


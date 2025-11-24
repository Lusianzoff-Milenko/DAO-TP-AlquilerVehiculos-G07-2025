from datetime import timedelta, datetime

from services.containers.container import Container



def main():
    container: Container = Container()
    vehiculo_service = container.vehiculo_service()
    contrato_service = container.contrato_service()
    cliente = container.cliente_service().get_cliente_by_id(1)
    empleado = container.empleado_service().get_empleado_by_id(1)
    metodo_pago = container.metodo_pago_service().get_metodo_pago_by_id(1)
    contrato = contrato_service.get_contrato_by_id(1)
    vehiculo = vehiculo_service.get_vehiculo_by_id(1)
    print(contrato)
    print(vehiculo)
    contrato_service.tomar_reserva(vehiculo, cliente, empleado, metodo_pago, True, datetime.now() + timedelta(days=15), datetime.now() + timedelta(days=50))
    print(f"{vehiculo.get_state().__class__.__name__} soy el estado actual")

if __name__ == "__main__":

    main()


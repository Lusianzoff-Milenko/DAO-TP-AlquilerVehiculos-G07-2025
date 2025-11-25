from controlladores.controller_contrato import ContratoController
from services.containers.container import Container
from ui.app import run_app

def main():
    containter = Container()
    controller = containter.reporte_controller()
    print(controller.get_detalle_flota())
    print(controller.get_facturacion_mensual())
    print(controller.get_clientes_contacto())
    print(controller.get_utilizacion_flota())
    print(controller.get_disponibilidad_flota())
    print(controller.get_rentabilidad_contratos())


if __name__ == "__main__":
    main()
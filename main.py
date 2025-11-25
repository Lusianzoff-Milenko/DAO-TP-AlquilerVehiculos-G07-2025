from services.containers.container import Container

def main():
    container = Container()
    contrato_controller = container.contrato_controller()
    print(contrato_controller.get_all_contratos())


if __name__ == "__main__":
    main()
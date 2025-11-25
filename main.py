from services.containers.container import Container

def main():
    container = Container()
    mantebimiento_controller = container.mantenimiento_controller()
    print(mantebimiento_controller.get_all_mantenimientos())


if __name__ == "__main__":
    main()
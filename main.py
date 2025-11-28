# ...existing code...
from ui.app import run_app
from services.containers.container import Container

def main():
    container = Container()
    cliente_controller = container.cliente_controller()
    print(cliente_controller.get_cliente_by_documento_and_tipo(45404967,1))

if __name__ == "__main__":
    main()
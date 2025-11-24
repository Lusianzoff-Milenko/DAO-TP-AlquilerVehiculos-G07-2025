from datetime import datetime
from typing import List

from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from services.containers.container import Container



def main():
    container: Container = Container()
    contrato_service = container.contrato_service()
    vehiculo_service = container.vehiculo_service()
    contrato = Contrato(
                id_cliente=1,
                fecha_desde=datetime(2026, 1, 1),
                fecha_hasta=datetime(2026, 2, 10),
                id_metodo_de_pago=1,
                id_empleado=1,
                tiene_seguro=True
            )
    detalles_ejemplo: List[DetalleContrato] = [
        DetalleContrato(
            # id_contrato= El servicio lo asignará (debe ser None al inicio)
            id_vehiculo=1,  # Alquila el Vehículo con ID 1
            monto=5000.0,
            fecha_retiro=datetime(2026, 1, 1),
            fecha_entrega=datetime(2026, 2, 10),
        ),
        DetalleContrato(
            # id_contrato= El servicio lo asignará
            id_vehiculo=2,  # Alquila el Vehículo con ID 2
            monto=7500.0,
            fecha_retiro=datetime(2026, 1, 1),
            fecha_entrega=datetime(2026, 2, 10),
        )
    ]
    contrato_service.crear_contrato_reserva(contrato, detalles_ejemplo)
    print("Contrato de reserva creado con éxito.")
    print(vehiculo_service.get_vehiculo_by_id(1))


if __name__ == "__main__":
    main()


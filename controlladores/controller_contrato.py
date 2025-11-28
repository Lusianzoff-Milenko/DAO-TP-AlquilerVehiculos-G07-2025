from typing import List, Dict, Any, Optional
from datetime import datetime

# Importamos los modelos necesarios para crear los objetos manualmente
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato

from services.contrato_service import ContratoService
from services.vehiculo_service import VehiculoService
from services.cliente_service import ClienteService
from services.empleado_service import EmpleadoService
from services.metododepago_service import MetodoDePagoService
from services.estado_service import EstadoService  # Necesitamos buscar el estado


class ContratoController:
    def __init__(self,
                 contrato_service: ContratoService,
                 vehiculo_service: VehiculoService,
                 cliente_service: ClienteService,
                 empleado_service: EmpleadoService,
                 pago_service: MetodoDePagoService,
                 estado_service: EstadoService = None):  # Inyección opcional o recuperarla del container
        self._service = contrato_service
        self._vehiculo_service = vehiculo_service
        self._cliente_service = cliente_service
        self._empleado_service = empleado_service
        self._pago_service = pago_service
        # Si no se inyecta, usamos el del servicio de contratos (hack temporal si no actualizas container)
        self._estado_service = estado_service if estado_service else contrato_service._estado_service

    def get_all_contratos(self) -> List[Dict[str, Any]]:
        # ... (Mantener este método igual que en la respuesta anterior) ...
        contratos = self._service._repo.list_all()
        data = []
        for c in contratos:
            patente = "N/A"
            if c.detalles_contrato and len(c.detalles_contrato) > 0:
                v = c.detalles_contrato[0].Vehiculo
                if v: patente = v.patente

            total = sum(d.monto for d in c.detalles_contrato) if c.detalles_contrato else 0.0

            data.append({
                "ID": c.id,
                "Cliente": f"{c.Cliente.persona.nombre} {c.Cliente.persona.apellido}" if c.Cliente and c.Cliente.persona else "S/D",
                "Vehículo": patente,
                "Desde": c.fecha_desde.strftime("%Y-%m-%d"),
                "Hasta": c.fecha_hasta.strftime("%Y-%m-%d"),
                "Estado": c.Estado.nombre if c.Estado else "N/A",
                "Total": f"${total:.2f}",
                "raw_total": total
            })
        return data

    def crear_reserva(self, data: Dict[str, Any]) -> bool:
        """
        Crea una reserva instanciando manualmente el Contrato y el Detalle,
        y utilizando el método crear_contrato_reserva del servicio.
        """
        try:
            # 1. Preparar Fechas
            f_desde = datetime.strptime(data["Fecha Desde"], "%Y-%m-%d")
            f_hasta = datetime.strptime(data["Fecha Hasta"], "%Y-%m-%d")

            # Calcular días para el costo
            dias = (f_hasta - f_desde).days
            if dias < 1: dias = 1

            # 2. Obtener Entidades
            vehiculo = self._vehiculo_service.get_vehiculo_by_id(data["id_vehiculo"])
            cliente = self._cliente_service.get_cliente_by_id(data["id_cliente"])
            # Empleado hardcodeado o del contexto de sesión
            empleado = self._empleado_service.get_empleado_by_id(1)
            metodo = self._pago_service.get_metodo_pago_by_id(data["id_metodo_pago"])

            if not all([vehiculo, cliente, empleado, metodo]):
                print("Error: Datos incompletos para la reserva.")
                return False

            # 3. Buscar el estado 'EnReservado' para asignarlo explícitamente
            estado_reserva = self._estado_service.get_estado_by_name_and_ambito("EnReservado", "Contrato")
            if not estado_reserva:
                print("Error: Estado 'EnReservado' no existe en BD.")
                return False

            # 4. Crear Objeto Contrato (Sin guardar aún)
            nuevo_contrato = Contrato(
                id_cliente=cliente.id,
                id_empleado=empleado.id,
                id_metodo_de_pago=metodo.id,
                fecha_desde=f_desde,
                fecha_hasta=f_hasta,
                tiene_seguro=data.get("Seguro", False),
                id_estado=estado_reserva.id  # Forzamos estado RESERVA
            )

            # 5. Crear Objeto Detalle (Calculando monto)
            monto_total = vehiculo.precio_base * dias

            nuevo_detalle = DetalleContrato(
                id_vehiculo=vehiculo.id,
                monto=monto_total,
                fecha_retiro=f_desde,
                fecha_entrega=f_hasta  # Fecha esperada
            )

            # 6. Llamar al servicio con los objetos ya armados
            print(f"Creando reserva manual para {vehiculo.patente}, monto: {monto_total}")

            resultado_id = self._service.crear_contrato_reserva(nuevo_contrato, [nuevo_detalle])

            return resultado_id is not None

        except Exception as e:
            print(f"Error crítico en controller crear_reserva: {e}")
            return False

    # ... (resto de métodos iniciar_alquiler, finalizar_alquiler, get_form_options iguales) ...
    def iniciar_alquiler(self, contrato_id: int, pago_inicial: float) -> bool:
        try:
            return self._service.confirmar_pago(contrato_id, pago_inicial)
        except Exception as e:
            print(f"Error iniciando alquiler: {e}")
            return False

    def finalizar_alquiler(self, contrato_id: int) -> bool:
        try:
            return self._service.finalizar_alquiler(contrato_id, datetime.now())
        except Exception as e:
            print(f"Error finalizando: {e}")
            return False

    def get_form_options(self) -> Dict:
        vehiculos = [v for v in self._vehiculo_service.list_all_vehiculos()
                     if v.Estado.nombre == "Disponible"]
        clientes = self._cliente_service.list_all_clientes()
        pagos = self._pago_service.list_all_metodos_pago()

        return {
            "vehiculos": [{"label": f"{v.Modelo.nombre} - {v.patente}", "value": v.id} for v in vehiculos],
            "clientes": [{"label": f"{c.documento} - {c.persona.nombre}", "value": c.id} for c in clientes],
            "pagos": [{"label": p.nombre, "value": p.id} for p in pagos]
        }
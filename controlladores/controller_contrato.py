from typing import List, Dict, Any, Optional
from datetime import datetime
from services.contrato_service import ContratoService
from services.vehiculo_service import VehiculoService
from services.cliente_service import ClienteService
from services.empleado_service import EmpleadoService
from services.metododepago_service import MetodoDePagoService


class ContratoController:
    def __init__(self,
                 contrato_service: ContratoService,
                 vehiculo_service: VehiculoService,
                 cliente_service: ClienteService,
                 empleado_service: EmpleadoService,
                 pago_service: MetodoDePagoService):
        self._service = contrato_service
        self._vehiculo_service = vehiculo_service
        self._cliente_service = cliente_service
        self._empleado_service = empleado_service
        self._pago_service = pago_service

    def get_all_contratos(self) -> List[Dict[str, Any]]:
        # Como no tienes un list_all en contrato_service que retorne todos directamente (solo por ID),
        # deberás usar el repo directamente o agregar el método en el service.
        # Asumiremos que agregas un list_all_contratos() en ContratoService o usamos el repo interno.
        contratos = self._service._repo.list_all()  # Acceso directo temporal
        data = []
        for c in contratos:
            # Obtener patente del primer vehículo (simplificado para tabla)
            patente = "N/A"
            if c.detalles_contrato and len(c.detalles_contrato) > 0:
                # Lazy loading debe estar activo o usar joinedload en repo
                v = c.detalles_contrato[0].Vehiculo
                if v: patente = v.patente

            data.append({
                "ID": c.id,
                "Cliente": f"{c.Cliente.persona.nombre} {c.Cliente.persona.apellido}" if c.Cliente and c.Cliente.persona else "S/D",
                "Vehículo": patente,
                "Desde": c.fecha_desde.strftime("%d/%m/%Y"),
                "Hasta": c.fecha_hasta.strftime("%d/%m/%Y"),
                "Estado": c.Estado.nombre if c.Estado else "N/A",
                "Total": f"${sum(d.monto for d in c.detalles_contrato):.2f}"
            })
        return data

    def crear_reserva(self, data: Dict[str, Any]) -> bool:
        """
        Maneja la lógica de 'Tomar Reserva' desde la UI.
        """
        try:
            # Convertir fechas
            f_desde = datetime.strptime(data["Fecha Desde"], "%Y-%m-%d")
            f_hasta = datetime.strptime(data["Fecha Hasta"], "%Y-%m-%d")

            # Obtener objetos de dominio necesarios
            vehiculo = self._vehiculo_service.get_vehiculo_by_id(data["id_vehiculo"])
            cliente = self._cliente_service.get_cliente_by_id(data["id_cliente"])
            # Empleado logueado (hardcodeado ID 1 por ahora o sacar de AppState)
            empleado = self._empleado_service.get_empleado_by_id(1)
            metodo = self._pago_service.get_metodo_pago_by_id(data["id_metodo_pago"])

            if not all([vehiculo, cliente, empleado, metodo]):
                print("Error: Datos inválidos (ID no encontrado)")
                return False

            # Llamar al facade del servicio
            nuevo_id = self._service.tomar_reserva(
                vehiculo=vehiculo,
                cliente=cliente,
                empleado=empleado,
                metodo_pago=metodo,
                tiene_seguro=data.get("Seguro", False),
                fecha_desde=f_desde,
                fecha_hasta=f_hasta
            )
            return nuevo_id is not None

        except Exception as e:
            print(f"Error en controller reserva: {e}")
            return False

    def get_form_options(self) -> Dict:
        # Para llenar los combos de la pantalla de Nueva Reserva
        vehiculos = [v for v in self._vehiculo_service.list_all_vehiculos()
                     if v.Estado.nombre == "Disponible"]  # Solo disponibles

        clientes = self._cliente_service.list_all_clientes()
        pagos = self._pago_service.list_all_metodos_pago()

        return {
            "vehiculos": [{"label": f"{v.Modelo.nombre} - {v.patente}", "value": v.id} for v in vehiculos],
            "clientes": [{"label": c.documento, "value": c.id} for c in clientes],
            "pagos": [{"label": p.nombre, "value": p.id} for p in pagos]
        }
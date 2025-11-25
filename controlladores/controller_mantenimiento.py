from typing import List, Dict, Any, Optional
from datetime import datetime
from services.mantenimiento_service import MantenimientoService
from services.vehiculo_service import VehiculoService
from services.empleado_service import EmpleadoService


class MantenimientoController:
    def __init__(self,
                 mantenimiento_service: MantenimientoService,
                 vehiculo_service: VehiculoService,
                 empleado_service: EmpleadoService):
        self._service = mantenimiento_service
        self._vehiculo_service = vehiculo_service
        self._empleado_service = empleado_service

    def get_all_mantenimientos(self) -> List[Dict[str, Any]]:
        # Asumimos que el repo tiene list_all
        mantenimientos = self._service._repo.list_all()
        data = []
        for m in mantenimientos:
            data.append({
                "ID": m.id,
                "Vehículo": m.Vehiculo.patente if m.Vehiculo else "S/D",
                "Descripción": m.descripcion,
                "Costo": f"${m.costo:.2f}",
                "Fecha": m.fecha_hora.strftime("%d/%m/%Y"),
                "Estado": m.Estado.nombre if m.Estado else "S/D",
                "Empleado": f"{m.Empleado.Persona.nombre} {m.Empleado.Persona.apellido}" if m.Empleado and m.Empleado.Persona else "S/D"
            })
        return data

    def iniciar_mantenimiento(self, data: Dict[str, Any]) -> bool:
        """Envía un vehículo a taller."""
        try:
            vehiculo_id = data.get("id_vehiculo")
            empleado_id = 1  # Hardcodeado o obtener del usuario logueado

            # Validar estado del vehículo
            vehiculo = self._vehiculo_service.get_vehiculo_by_id(vehiculo_id)
            if not vehiculo: return False

            # Usamos el servicio de vehículo que orquesta el cambio de estado + creación de mantenimiento
            return self._vehiculo_service.enviar_a_mantenimiento(
                vehiculo_id=vehiculo_id,
                costo=float(data.get("Costo", 0)),
                descripcion=data.get("Descripción", "Mantenimiento General"),
                id_empleado=empleado_id
            )
        except Exception as e:
            print(f"Error iniciando mantenimiento: {e}")
            return False

    def finalizar_mantenimiento(self, data: Dict[str, Any]) -> bool:
        """Marca un mantenimiento como finalizado y libera el vehículo."""
        try:
            # Asumimos que data trae el ID del mantenimiento o del vehículo
            vehiculo_id = data.get("id_vehiculo")  # O buscamos por mantenimiento ID
            return self._vehiculo_service.finalizar_mantenimiento(vehiculo_id)
        except Exception as e:
            print(f"Error finalizando: {e}")
            return False

    def get_form_options(self) -> Dict:
        # Solo vehículos disponibles o en revisión pueden ir a mantenimiento
        vehiculos = self._vehiculo_service.list_all_vehiculos()
        # Filtramos (opcional, según lógica de negocio)
        v_aptos = [v for v in vehiculos if v.Estado.nombre in ["Disponible", "EnRevision", "Entregado"]]

        return {
            "vehiculos": [{"label": f"{v.patente} - {v.Modelo.nombre}", "value": v.id} for v in v_aptos]
        }
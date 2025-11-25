from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models.empleado import Empleado
from domain.models.persona import Persona
from services.empleado_service import EmpleadoService
from services.persona_service import PersonaService
from services.tipopuesto_service import TipoPuestoService

class EmpleadoController:
    def __init__(self,
                 empleado_service: EmpleadoService,
                 persona_service: PersonaService,
                 tipo_puesto_service: TipoPuestoService):
        self._service = empleado_service
        self._persona_service = persona_service
        self._tipo_puesto_service = tipo_puesto_service

    def get_all_empleados(self) -> List[Dict[str, Any]]:
        empleados = self._service.list_all_empleados()
        data = []
        for e in empleados:
            p = e.Persona
            if p:
                data.append({
                    "ID": e.id,
                    "Nombre": f"{p.nombre} {p.apellido}",
                    "Puesto": e.TipoPuesto.nombre if e.TipoPuesto else "S/D",
                    "Ingreso": e.fecha_ingreso.strftime("%Y-%m-%d"),
                    "Email": p.mail,
                    "Teléfono": p.telefono
                })
        return data

    def create_empleado(self, data: Dict[str, Any]) -> Optional[int]:
        try:
            # 1. Crear Persona
            persona = Persona(
                nombre=data.get("Nombre"),
                apellido=data.get("Apellido"),
                telefono=data.get("Teléfono"),
                mail=data.get("Email"),
                direccion=data.get("Dirección", ""),
                fecha_nacimiento=datetime.strptime(data.get("Fecha Nacimiento"), "%Y-%m-%d")
            )
            p_id = self._persona_service.create_persona(persona)
            if not p_id: return None

            # 2. Crear Empleado
            empleado = Empleado(
                id_persona=p_id,
                id_tipo_puesto=data.get("id_tipo_puesto"),
                fecha_ingreso=datetime.now()
            )
            return self._service.create_empleado(empleado)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_form_options(self) -> Dict[str, List]:
        puestos = self._tipo_puesto_service.list_all_tipos_puesto()
        return {
            "puestos": [{"label": p.nombre, "value": p.id} for p in puestos]
        }
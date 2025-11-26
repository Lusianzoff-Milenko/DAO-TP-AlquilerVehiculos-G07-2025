from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models.cliente import Cliente
from domain.models.persona import Persona
from services.cliente_service import ClienteService
from services.persona_service import PersonaService
from services.tipodocumento_service import TipoDocumentoService


class ClienteController:
    def __init__(self,
                 cliente_service: ClienteService,
                 persona_service: PersonaService,
                 tipo_doc_service: TipoDocumentoService):
        self._service = cliente_service
        self._persona_service = persona_service
        self._tipo_doc_service = tipo_doc_service

    def get_all_clientes(self) -> List[Dict[str, Any]]:
        clientes = self._service.list_all_clientes()
        data = []
        for c in clientes:
            # Aplanamos Persona + Cliente
            p = c.persona  # Relación ORM
            if p:
                data.append({
                    "ID": c.id,
                    "Nombre": p.nombre,
                    "Apellido": p.apellido,
                    "Documento": c.documento,
                    "Tipo Doc": c.TipoDocumento.nombre if c.TipoDocumento else "S/D",
                    "Email": p.mail,
                    "Teléfono": p.telefono,
                    "Dirección": p.direccion,
                    "Fecha Nacimiento": p.fecha_nacimiento.strftime("%Y-%m-%d") if p.fecha_nacimiento else "2000-01-01"
                })
        return data

    def create_cliente(self, data: Dict[str, Any]) -> Optional[int]:
        try:
            # 1. Primero creamos/buscamos la Persona
            persona = Persona(
                nombre=data.get("Nombre"),
                apellido=data.get("Apellido"),
                telefono=data.get("Teléfono"),
                mail=data.get("Email"),
                direccion=data.get("Dirección"),
                # Asumiendo formato ISO YYYY-MM-DD del datepicker
                fecha_nacimiento=datetime.strptime(data.get("Fecha Nacimiento"), "%Y-%m-%d")
            )

            # Guardamos persona primero
            persona_id = self._persona_service.create_persona(persona)
            if not persona_id: raise Exception("Error al crear persona")

            # 2. Creamos el Cliente asociado
            cliente = Cliente(
                documento=data.get("Documento"),
                id_tipo_documento=data.get("id_tipo_documento"),
                id_persona=persona_id
            )
            return self._service.create_cliente(cliente)

        except Exception as e:
            print(f"Error creando cliente: {e}")
            return None

    def update_cliente(self, cliente_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza un cliente existente."""
        try:
            # Obtener el cliente actual
            cliente = self._service.get_cliente_by_id(cliente_id)
            if not cliente:
                print(f"Cliente con ID {cliente_id} no encontrado")
                return False
            
            # Actualizar la persona asociada
            persona = cliente.persona
            if persona:
                persona.nombre = data.get("Nombre", persona.nombre)
                persona.apellido = data.get("Apellido", persona.apellido)
                persona.telefono = data.get("Teléfono", persona.telefono)
                persona.mail = data.get("Email", persona.mail)
                persona.direccion = data.get("Dirección", persona.direccion)
                
                # Actualizar fecha si viene en el formato correcto
                if data.get("Fecha Nacimiento"):
                    try:
                        persona.fecha_nacimiento = datetime.strptime(data.get("Fecha Nacimiento"), "%Y-%m-%d")
                    except:
                        pass  # Mantener fecha actual si hay error
                
                self._persona_service.update_persona(persona)
            
            # Actualizar datos del cliente
            cliente.documento = data.get("Documento", cliente.documento)
            cliente.id_tipo_documento = data.get("id_tipo_documento", cliente.id_tipo_documento)
            
            return self._service.update_cliente(cliente)
        except Exception as e:
            print(f"Error actualizando cliente: {e}")
            return False

    def delete_cliente(self, cliente_id: int) -> bool:
        return self._service.delete_cliente(cliente_id)

    def get_form_options(self) -> Dict[str, List]:
        tipos = self._tipo_doc_service.list_all_tipos_documento()
        return {
            "tipos_documento": [{"label": t.nombre, "value": t.id} for t in tipos]
        }